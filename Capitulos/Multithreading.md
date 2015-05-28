\chapter{Soporte para multithreading}
Como contribución a la herramienta original de línea de comandos, $pmctrack$, hemos añadido soporte para monitorización de programas *multithreading*, es decir con más de un hilo.

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
