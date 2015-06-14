\chapter[Soporte para monitorización de aplicaciones multihilo]{Soporte para monitorización de aplicaciones multihilo}

El programa de línea de comandos `pmctrack` carece soporte de monitorización de aplicaciones multihilo desde espacio de usuario. Lamentablemente, esta limitación no se puede subsanar modificando únicamente dicho programa de usuario. Por el contrario, es el módulo del kernel PMCTrack el que no brinda la posibilidad de exportar datos de los contadores a las herramientas de modo usuario cuando la aplicación consta de varios hilos. Por lo tanto, para dotar a PMCTrack de este soporte es necesario realizar un rediseño profundo del módulo del kernel.

Este capítulo se estructura como sigue. La sección \ref{sec:antecedentes} presenta las limitaciones inherentes en el diseño original del módulo del kernel de PMCTrack que impedían el soporte para aplicaciones multihilo.  La sección \ref{sec:solucion} describe el diseño alternativo y la implementación realizada para lograr dotar a PMCTrack del soporte deseado. 

# Diseño previo
\label{sec:antecedentes}

En el kernel Linux, cada hilo del sistema está descrito internamente mediante una estructura `task_struct`. Esta estructura almacena campos críticos del hilo como su PID o el PID de su padre, los ficheros abiertos, un descriptor a las regiones de memoria usadas por el proceso al que pertenece, etcétera. Para ofrecer el soporte necesario, el módulo del kernel de PMCTrack tambien necesita mantener información privada de cada hilo que está siendo monitorizado, como por ejemplo la configuración de eventos hardware establecida por el usuario o el valor temporal de los contadores hardware cuando el hilo no está actualmente en ejecución. Para almancenar esta información, el parche del kernel para PMCtrack añade el campo `pmc`, un puntero a una estructura de tipo `pmon_prof_t` que almacena los datos privados del hilo usados por PMCTrack.



Como se indicó en el capítulo previo, cuando una aplicación está siendo monitorizada con el programa `pmctrack`, el módulo del kernel de PMCTrack almacena los datos recabados con los contadores en un buffer circular acotado. El programa `pmctrack` consume los datos de los contadores leyendo de la entrada `/proc/pmc/monitor` que tiene semántica bloqueante. Al efectuar una lectura\footnote{Antes de poder leer datos de la entrada /proc, el programa pmctrack y la aplicación que está siendo monitorizada tienen que comunicar cierta información al módulo del kernel siguiendo el protocolo descrito en \cite{MSDTFG12}.} de dicha entrada, el programa se queda bloqueado hasta que haya datos para consumir o la aplicación finalice. 

\begin{figure}[tbp]
\begin{center}
\selectlanguage{english}
\input{Imagenes/Fuentes/pmon-prof-single}
\selectlanguage{spanish}
\end{center}
\caption{Relación entre las estructuras \texttt{pmon\_prof\_t} del proceso monitor y monitorizado en la implementación original del módulo de PMCTrack. Los campos sin usar en cada estructura se representan en gris.\label{img:pmon-prof-single}}
\end{figure}

Este escenario constituye claramente un caso particular del problema _Productor/Consumidor_, con un productor --la aplicación secuencial que está siendo monitorizada-- y un consumidor --el programa monitor `pmctrack`--. Notesé que para el kernel Linux el proceso monitor es padre del proceso monitorizado, ya que `pmctrack` emplea las llamadas `fork()` y `exec()` para ejecutar el comando pasado en la línea de comando. Ambos procesos requieren acceder al buffer circular de muestras de los contadores y el acceso puede ser potencialmente concurrente. Nada impide que el kernel, en nombre de la aplicación monitorizada, desee insertar nuevas muestras en el buffer en el modo EBS o TBS, y esto ocurra al mismo tiempo que el programa pmctrack lee de la entrada /proc para extraer elementos del buffer circular. Para garantizar exclusión mutua en el acceso al buffer circular, se empleaba un _spin lock_ almacenado en la estructura `pmon_prof_t` del hilo que está siendo monitorizado. Adicionalmente, para dotar del caracter bloqueante necesario a la entrada /proc, se empleaba un semáforo del kernel y un flag `monitor_waiting` que indica si el programa `pmctrack` está actualmente bloqueado a la espera de nuevas muestras. Ambos campos están también almacenados en la estructura `pmon_prof_t` del hilo monitorizado.


La figura \ref{img:pmon-prof-single} ilustra la relación entre las estructuras `pmon_prof_t` del proceso monitor `pmctrack` y del hilo de la aplicación secuencial que está siendo monitorizada.  Como puede observarse en la figura, además de los campos mencionados previamente, la estructura `pmon_prof_t` poseía originalmente dos campos tipo puntero adicionales: `child` y `parent`. El campo `child` se empleaba para que el descriptor del proceso monitor, que ejecuta el programa `pmctrack`, almacene la referencia al `pmon_prof_t` del hilo de la aplicación secuencial que está siendo monitorizada. Gracias a este puntero el proceso monitor, al entrar en el kernel invocando la _read callback_ de la entrada `/proc/pmc/monitor`, puede acceder tanto al buffer circular de muestras del hijo, como a los recursos de sincronización necesarios para acceder de forma segura al buffer. Por el contrario, el campo `parent` se emplea dentro del módulo de PMCTrack para que la aplicación secuencial sea consciente de que que está siendo monitorizada; en tal caso el puntero será distinto de NULL. Cuando la aplicación monitorizada sale del sistema, el módulo del kernel de PMCTrack debe encargarse de poner a NULL los punteros `child` y `parent` en la estructura `pmon_prof_t` del proceso monitor y del monitorizado, respectivamente. Esto no sería posible sin el puntero `parent` almacenado en el descriptor de la aplicación monitorizada. 

El diseño anteriormente descrito presenta varias limitaciones importantes. La primera y más relevante es el hecho de que como tal este modelo no ofrece soporte para la monitorización de aplicaciones multihilo desde modo usuario. Esencialmente, como se ilustra en la figura \ref{img:pmon-prof-single}, se establece una relación _uno a uno_ entre el proceso monitor y el hilo monitorizado mediante los punteros `child` y `parent`, y no una relación _uno a varios_ como requeriría el escenario con una aplicación multihilo. En este caso, todos los hilos de la aplicación monitorizada deberían compartir tanto el buffer de muestras como los recursos de sincronización para garantizar exclusión mutua y sincronizarse con el hilo monitor. El segundo aspecto negativo de este diseño es la presencia de numerosos campos no utilizados en las estructuras de `pmon_prof_t` de ambos procesos (campos que aparecen en gris). Finalmente, el proceso de actualización de punteros y liberación de la memoria reservada para el buffer de muestras resulta innecesariamente complejo, ya que en la implementación hay que actuar de forma diferente dependiendo del orden de finalización del proceso monitorizado y el monitor. 

<!--
 Asimismo, es en ese momento, cuando se libera la memoria reservada para el almacenamiento temporal de las muestras en el buffer circular.
-->


<!--

de una aplicación que está siendo 
 el programa `pmctrack` lee los datos de los contadores 


El diseño de la herramienta original no se pensó en ningún momento para que la herramienta soportara la monitorización de benchmarks con más de un hilo de ejecución, es por ello por lo que se optó por un diseño que ha resultado ser tremendamente ineficaz.

El proceso de monitorización poseía una estructura \texttt{pmon_prof_t} la cual contenía un puntero al \texttt{task_struct} del benchmark que se deseaba monitorizar. Esta estructura del benchmark contenía un buffer circular de resultados de muestras de monitorización.

El proceso asociado al benchmark escribía los datos de monitorización del benchmark en el buffer circular mencionado, dejando posteriormente una marca en una entrada */proc* para avisar de la existencia de nuevos datos en el buffer. El proceso de monitorización, que estaba dormido a la espera de recibir esa marca en la entrada */proc*, se despertaba consumiendo los nuevos datos del buffer, y mostrándolos al usuario en la salida configurada.

Este diseño ha generado problemas desde que se puso en funcionamiento. Sin embargo, los problemas se agravaron cuando llegó el momento de dar soporte a programas multihilo.

La solución inicialmente propuesta fue almacenar el buffer circular en el \texttt{task\_struct} del hilo principal del programa, de tal manera que el resto de hilos del programa, al igual que el proceso de monitorización, poseyeran en su estructura un puntero a dicho buffer. Sin embargo surgieron cuestiones cuyas soluciones eran tremendamente complicadas e ineficaces: ¿Cómo gestionamos la concurrencia en el caso de que hubiera más de un hilo queriendo escribir muestras en el buffer? ¿Qué ocurre si el hilo principal es interrumpido o finaliza prematuramente? El resto de hilos tendrían un puntero a un buffer circular de muestras que ya habría sido destruido (fenómeno conocido como *puntero salvaje*).



# Solución al problema


Para resolver el problema y dar soporte a PMCTrack para la monitorización de programas con más de un hilo de ejecución, hemos optado por un cambio en el diseño inicial de la herramienta.

Actualmente existe una estructura \texttt{pmc\_samples\_buffer\_t} que contiene el buffer circular que antes contenía el proceso asociado al hilo principal del benchmark, de tal manera que ahora, tanto el proceso de monitorización como los procesos asociados a cada hilo del benchmark, cuentan con un puntero a dicha estructura \texttt{pmc\_samples\_buffer\_t}. Los procesos de los hilos del benchmark se encargarán de escribir las muestras en la estructura, mientras que el proceso de monitorización se encargará de leerlas. Este esquema de funcionamiento sigue el esquema *Productor-Consumidor*.

La estructura \texttt{pmc\_samples\_buffer\_t}, a parte de contener el buffer circular de muestras, cuenta con un semáforo usado para bloquear al proceso de monitorización cuando no hay nuevas muestras que consumir, con un spinlock que garantiza la exclusión mutua para la escritura de nuevas muestras en el buffer, y un contador atómico de referencias usado para destruir la estructura de forma segura, esto es, cuando no haya ningún proceso que lo esté referenciando.

Este cambio en el diseño de la herramienta ha dado lugar a un funcionamiento más estable de la herramienta, y a un código más limpio y fácil de entender. Además, gracias a él hemos logrado que sea posible la monitorización de programas multihilo, lo cual ha sido un avance muy importante en cuanto a potencia y versatibilidad de la herramienta de línea de comandos PMCTrack.

-->

# Nuevo diseño interno de PMCTrack
\label{sec:solucion}

Para superar las limitaciones arriba mencionadas y dar soporte a PMCTrack para la monitorización de programas con más de un hilo de ejecución desde modo usuario, hemos optado por un cambio en el diseño inicial de la herramienta. Los cambios más significativos se realizaron en el módulo del kernel de PMCTrack. 

Cuando se desea monitorizar una aplicación multihilo, el buffer de muestras debe estar compartido por todos los hilos de la aplicación monitorizada y por el proceso monitor. Como el acceso al buffer es de naturaleza concurrente, en este caso se manifiesta el problema _Productor/Consumidor_ con $n$ productores --hilos de la aplicación _multithread_-- y un consumidor --proceso que ejecuta el programa `pmctrack`--. Existen múltiples diseños alternativos, para que todos los hilos del sistema concurrente compartan tanto el buffer como los recursos de sincronización. No obstante, se ha intentado apostar por un diseño que reduzca al máximo el número de campos no utilizados dentro de la estructura `pmon_prof_t`.    

Uno de los principales desafíos que surgió en el proceso de diseño es la gestión de la memoria dinámica asociada al buffer circular de muestras y a los recursos de sincronización. Si bien compartir un buffer entre dos procesos ya complicaba la implementación en la monitorización de aplicaciones secuenciales debido a la casuística en el orden de terminación de los procesos, la compartición con $n$ procesos introduce complicaciones adicionales. En una aplicación multihilo, cada hilo puede finalizar en un orden distinto, y solo el hilo que termine en último lugar debería ocuparse de liberar la memoria del buffer. Adicionalmente, en este escenario se debe tener en cuenta que no se debe liberar la memoria del buffer hasta que el proceso monitor termine, ya que éste debe recoger del buffer todas las muestras de los contadores hardware hasta que cada hilo de la aplicación haya finalizado.

El diseño que ofrece la solución a este problema se basa en la estructura \texttt{pmc\_samples\_buffer\_t} que se muestra a continuación:

\begin{lstlisting}[backgroundcolor=,basicstyle=\tt\footnotesize]
typedef struct {
	cbuffer_t* pmc_samples; 	
	spinlock_t lock;	
	struct semaphore sem_queue;		
	volatile int monitor_waiting;	
	atomic_t ref_counter;	
}pmc_samples_buffer_t;
\end{lstlisting}


Esta estructura alberga múltiples campos que se encontraban dentro de la estructura `pmon_prof_t` en el diseño previo, como es el caso del buffer circular de muestras (`pmc_samples`) y los recursos de sincronización (`lock`, `sem_queue`, `monitor_waiting`). Adicionalmente, la nueva estructura consta de un contador de referencia para solucionar el problema de la gestión de memoria dinámica de forma más robusta, como se describe a continuación.

\begin{figure}[tbp]
\begin{center}
\selectlanguage{english}
\input{Imagenes/Fuentes/pmon-prof-multi}
\selectlanguage{spanish}
\end{center}
\caption{Relación entre la estructura \texttt{pmc\_samples\_buffer\_t} y las estructuras \texttt{pmon\_prof\_t} del proceso monitor y de los hilos de una aplicación monitorizada (cuatro hilos) en la nueva implementación del módulo de PMCTrack. \label{img:pmon-prof-multi}}
\end{figure}

Como ilustra la figura \ref{img:pmon-prof-multi} en el nuevo diseño la estructura `pmon_prof_t` almacena un puntero `sbuf` a una estructura de tipo `pmc_samples_buffer_t`. Esta modificación del diseño permite que múltiples procesos o hilos puedan compartir la estructura simplemente almacenando el mismo puntero en su campo de `sbuf` dentro de `pmon_prof_t`. El contador de referencias `ref_counter` de la estructura `pmc_samples_buffer_t`, permite llevar la cuenta del número de hilos que comparten la misma instancia de dicha estructura. Así por ejemplo, cuando se cree un nuevo hilo en una aplicación que esté siendo monitorizada desde modo usuario con PMCTrack, el campo `sbuf` dentro de la estructura `pmon_prof_t` del nuevo hilo apuntará a la misma dirección de memoria que el resto de hilos de la aplicación. Asimismo, al crear un nuevo hilo, el módulo del kernel incrementa en una unidad el contador de referencias para dejar constancia que que un hilo extra comparte la estructura `pmc_samples_buffer_t`. Análogamente, cuando un hilo finalice, el contador de referencias se decrementa y el puntero `sbuf` se pone a `NULL`. Cuando el contador de referencias de la estructura alcance el valor cero (el último hilo que usa la estructura termina), el módulo del kernel de PMCTrack liberará la memoria de la estructura para que esté disponible de nuevo para el SO.

Para que el programa de usuario `pmctrack` pueda identificar las muestras que provienen de distintos hilos de ejecución de la aplicación, se incluyó un nuevo campo `pid` en la estructura que describe a cada muestra de los contadores (`pmc_sample_t`). Como en el kernel Linux, cada hilo tiene su propio identificador interno (campo `pid` de su `task_struct`) cada muestra que se inserta en el buffer está identificada por dicho campo identificativo. El código del programa `pmctrack` fue también modificado para garantizar que dicho identificador se muestra por pantalla junto con el valor recabado de los contadores hardware. Para ilustrar está característica, el siguiente comando muestra distintos valores en la columna pid al monitorizar una aplicación paralela con cuatro hilos desde modo usuario empleando muestreo por tiempo:

\begin{lstlisting}[backgroundcolor=,language=bash,basicstyle=\tt\scriptsize]

$ pmctrack -T 1 -c pmc0,pmc1,pmc3=0x2e,umask3=0x41./rnaseq 4
nsample    pid      event          pmc0          pmc1          pmc3
      1  30120       tick    7194570808    3804503293        659126 
      2  30127       tick    5414863136    2418082409        170203 
      3  30128       tick    6519550211    3365103167        704584 
      4  30126       tick    5797691183    2668461950        190487 
      5  30120       tick    7417726822    3266118982        100831 
      6  30127       tick    6391099361    2859571911         73155 
      7  30128       tick    6202063856    2804748224         64599 
      8  30126       tick    6747513672    2966250007        123480 
      9  30120       tick    7186768494    3215750336        101673 
     10  30127       tick    5952872137    2755767164         74605 
     11  30128       tick    5704938508    2595268292        188362 
     12  30126       tick    6461952578    2958763944        102871 
     13  30120       tick    6466461413    3018968913        208613 
     ...
\end{lstlisting}


Para concluir, es preciso destacar que el nuevo diseño del módulo del kernel de PMCTrack no solo permite la monitorización de aplicaciones paralelas con `pmctrack` sino que brinda la posibilidad de visualizar en tiempo real distintas métricas de rendimiento de distintos hilos con PMCTrack-GUI, _frontend_ gráfico creado en este Trabajo de Fin De Grado y descrito en el capítulo 4. En el capítulo 5 se muestran ejemplos de monitorización de aplicaciones paralelas con PMCTrack-GUI. Por otra parte, la nueva implementación del módulo del kernel supuso el punto de partida para construir la librería _libpmctrack_ que se describe en el siguiente capítulo. Al instrumentar el código de una aplicación paralela con funciones de esta librería, el módulo del kernel mantiene un buffer de muestras independiente por cada hilo de la aplicación. En este escenario de uso no hay proceso monitor externo, sino que cada hilo puede consumir las muestras de los contadores que ha generado. 


