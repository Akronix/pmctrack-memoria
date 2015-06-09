\chapter{Soporte para multithreading}
Como contribución a la herramienta original de línea de comandos PMCTrack, hemos añadido soporte para monitorización de programas *multithreading* o multihilo.

# Antecedentes

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
