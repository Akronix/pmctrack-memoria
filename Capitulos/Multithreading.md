\chapter[Soporte para monitorización de aplicaciones multihilo]{Soporte para monitorización de aplicaciones multihilo desde modo usuario}

El programa de línea de comandos `pmctrack` carece soporte de monitorización de aplicaciones multihilo desde espacio de usuario. Lamentablemente, esta limitación no se puede subsanar modificando únicamente dicho programa de usuario. Por el contrario, es el módulo del kernel PMCTrack el que no brinda la posibilidad de exportar datos de los contadores a las herramientas de modo usuario cuando la aplicación consta de varios hilos. Por lo tanto, para dotar a PMCTrack de este soporte es necesario realizar un rediseño profundo del módulo del kernel.

Este capítulo se estructura como sigue. La sección \ref{sec:antecedentes} presenta las limitaciones inherentes en el diseño original del módulo del kernel de PMCTrack que impedían el soporte para aplicaciones multihilo.  La sección \ref{sec:solucion} describe el diseño alternativo y la implementación realizada para lograr dotar a PMCTrack del soporte deseado. 

# Antecedentes
\label{sec:antecedentes}

En el kernel Linux, cada hilo del sistema está descrito internamente mediante una estructura `task_struct`. Esta estructura almacena campos críticos del hilo como su PID o el PID de su padre, los ficheros abiertos, un descriptor a las regiones de memoria usadas por el proceso al que pertenece, etcétera. Para ofrecer el soporte necesario, el módulo del kernel de PMCTrack tambien necesita mantener información privada de cada hilo que está siendo monitorizado, como por ejemplo la configuración de eventos hardware establecida por el usuario o el valor temporal de los contadores hardware cuando el hilo no está actualmente en ejecución. Para almancenar esta información, el parche del kernel para PMCtrack añade el campo `pmc`, un puntero a una estructura de tipo `pmon_prof_t` que almacena los datos privados del hilo usados por PMCTrack.



Como se indicó en el capítulo previo, cuando una aplicación está siendo monitorizada con el programa `pmctrack`, el módulo del kernel de PMCTrack almacena los datos recabados con los contadores en un buffer circular acotado. El programa `pmctrack` consume los datos de los contadores leyendo de la entrada `/proc/pmc/monitor` que tiene semántica bloqueante. Al efectuar una lectura\footnote{Antes de poder leer datos de la entrada /proc, el programa pmctrack y la aplicación que está siendo monitorizada tienen que comunicar cierta información al módulo del kernel siguiendo el protocolo descrito en \cite{MSDTFG12}.} de dicha entrada, el programa se queda bloqueado hasta que haya datos por consumir o la aplicación finalice. 

\begin{figure}[tbp]
\begin{center}
\selectlanguage{english}
\input{Imagenes/Fuentes/pmon-prof-single}
\selectlanguage{spanish}
\end{center}
\caption{Relación entre las estructuras \texttt{pmon\_prof\_t} del proceso monitor y monitorizado en la implementación original del módulo de PMCTrack. Los campos sin usar en cada estructura se representan en gris.\label{img:pmon-prof-single}}
\end{figure}

Este escenario constituye claramente un caso particular del problema _Productor/Consumidor_, con un productor --la aplicación secuencial que está siendo monitorizada-- y un consumidor --el programa monitor `pmctrack`--. Notesé que para el kernel Linux el proceso monitor es padre del proceso monitorizado, ya que `pmctrack` emplea las llamadas `fork()` y `exec()` para ejecutar el comando pasado en la línea de comando. Ambos procesos requieren acceder al buffer circular de muestras de los contadores y el acceso puede ser potencialmente concurrente. Nada impide que el kernel, en nombre de la aplicación monitorizada, desee insertar nuevas muestras en el buffer cuando se usa el modo EBS o TBS, y esto ocurra al mismo tiempo que el programa pmctrack lea de la entrada /proc para extraer elementos del buffer circular. Para garantizar exclusión mutua en el acceso al buffer circular, se empleaba un _spin lock_ almacenado en la estructura `pmon_prof_t` del hilo que está siendo monitorizado. Adicionalmente, para dotar del caracter bloqueante necesario a la entrada /proc, se empleaba un semáforo del kernel y un flag `monitor_sleeping` que indica si el programa `pmctrack` está actualmente bloqueado a la espera de nuevas muestras. Ambos campos están también almacenados en la estructura `pmon_prof_t` del hilo monitorizado.


La figura \ref{img:pmon-prof-single} ilustra la relación entre las estructuras `pmon_prof_t` del proceso monitor `pmctrack` y del hilo de la aplicación secuencial que está siendo monitorizada.  Como puede observarse en la figura, además de los campos mencionados previamente, la estructura `pmon_prof_t` poseía originalmente dos campos tipo puntero adicionales: `child` y `parent`. El campo `child` se empleaba para que el descriptor del proceso monitor, que ejecuta el programa `pmctrack`, almacene la referencia al `pmon_prof_t` del hilo de la aplicación secuencial que está siendo monitorizada. Gracias a este puntero el proceso monitor, al entrar en el kernel invocando la _read callback_ de la entrada `/proc/pmc/monitor`, puede acceder tanto al buffer circular de muestras del hijo, como a los recursos de sincronización necesarios para acceder de forma segura al buffer. Por el contrario, el campo `parent` se emplea dentro del módulo de PMCTrack para que la aplicación secuencial sea consciente de que que está siendo monitorizada; en tal caso el puntero será distinto de NULL. Cuando la aplicación monitorizada sale del sistema, el módulo del kernel de PMCTrack debe encargarse de poner a NULL los punteros `child` y `parent` en la estructura `pmon_prof_t` del proceso monitor y del monitorizado. Esto no sería posible sin el puntero `parent` almacenado en el descriptor de la aplicación monitorizada. 

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

-->

# Solución al problema
\label{sec:solucion}

Para resolver el problema y dar soporte a PMCTrack para la monitorización de programas con más de un hilo de ejecución, hemos optado por un cambio en el diseño inicial de la herramienta.

Actualmente existe una estructura \texttt{pmc\_samples\_buffer\_t} que contiene el buffer circular que antes contenía el proceso asociado al hilo principal del benchmark, de tal manera que ahora, tanto el proceso de monitorización como los procesos asociados a cada hilo del benchmark, cuentan con un puntero a dicha estructura \texttt{pmc\_samples\_buffer\_t}. Los procesos de los hilos del benchmark se encargarán de escribir las muestras en la estructura, mientras que el proceso de monitorización se encargará de leerlas. Este esquema de funcionamiento sigue el esquema *Productor-Consumidor*.

La estructura \texttt{pmc\_samples\_buffer\_t}, a parte de contener el buffer circular de muestras, cuenta con un semáforo usado para bloquear al proceso de monitorización cuando no hay nuevas muestras que consumir, con un spinlock que garantiza la exclusión mutua para la escritura de nuevas muestras en el buffer, y un contador atómico de referencias usado para destruir la estructura de forma segura, esto es, cuando no haya ningún proceso que lo esté referenciando.

Este cambio en el diseño de la herramienta ha dado lugar a un funcionamiento más estable de la herramienta, y a un código más limpio y fácil de entender. Además, gracias a él hemos logrado que sea posible la monitorización de programas multihilo, lo cual ha sido un avance muy importante en cuanto a potencia y versatibilidad de la herramienta de línea de comandos PMCTrack.

# Antes
Enlace 1-1 entre dos procesos. Enlace muy persistente.
Modificaciones al campo en el struct task en sched.h:
* void* pmc = monitorizar
* bool prof_enable = empieza a usar los contadores

## Funcionamiento
1. Se "casan" los dos hilos.
2. El hijo escribe nuevos datos en su memoria interna (dentro del task struct) y deja una marca en una entrada /proc para que el padre sepa que tiene que leer. (El padre está bloqueado en la lectura de esa entrada /proc)
3. Cuando el hijo termina...
4. si hay una finalización prematura del hijo..

## Problemas
* No permitía multithreading
* Código complejo y propenso a errores
* Problemas cuando los procesos son interrumpidos o finalizados prematuramente.

# Ahora
Procesos menos acoplados. Se envían datos a través de un buffer compartido circular.
Este buffer se aloja en el heap del kernel (memoria dinámica). Tiene un límite. Es importante no dejar que se llene demasiado el
buffer hasta empezar a leer datos o se sobreescribirán datos en el buffer y se perderá información.
Buffer tiene que estar compartido por varios hilos y garantizar concurrencia.
El buffer tiene contadores de referencia como java. Cuando deja de tener procesos asociados, borra el buffer.
Él mismo controla la sincronización.
Sigue esquema productor-consumidor.
El padre lee datos (consumidor)
El hijo escribe datos de sus samples (productor)
Con esta nueva implementación, ahora puede permitir más de un productor escribiendo en el buffer. De este modo se pueden tener varios hilos escribiendo datos en el buffer y, por tanto, siendo monitorizadas.


## Funcionamiento



## Código
código está en mc_experiments.h llamado pmc_samples_buffer_t pmc_samples_buffer


## Ventajas
* Desacoplamiento entre productores y consumidores.
* Gestión del buffer de forma aislada.
* Contadores de referencia para controlar la existencia del buffer.


# Ejemplos de uso
Para probar esta nueva característica de pmctrack, tenemos que utilizar un conjunto de programas diferentes que hagan uso de programación concurrente.

\todo{Añadir shot de pmctrack por línea de comandos multithreading}

\todo{Añadir shot de pmctrackgui con programa multithreading}
