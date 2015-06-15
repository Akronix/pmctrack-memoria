\chapter{Conclusiones y trabajo futuro}

<!-- En castellano y en inglés -->

# Conclusiones

Después de la realización de este proyecto, PMCTrack cuenta con tres nuevas características: Soporte de monitorización para aplicaciones multihilo; Una librería, libpmctrack, que permite la monitorización de fragmentos de código directamente insertando llamadas a la librería dentro de código fuente; y finalmente, una interfaz gráfica, PMCTrack-GUI, que facilita su uso y permite obtener gráficas en tiempo real de métricas de alto nivel configuradas por el usuario. En los capítulos 2, 3 y 4, hemos pretendido explicar con detalle cómo hemos realizado y cómo funcionan cada una de estas características; y, en el capítulo 5, hemos querido poner a prueba su funcionamiento y mostrar su utilidad con algunos casos de estudio. Para finalizar, en este capítulo queremos a analizar a fondo el impacto holístico de cada una de estas nuevas características.

\begin{figure}%
\selectlanguage{english}
    \centering
    \subfloat[Antes del TFG]{{ \input{Imagenes/Fuentes/architecture} }}%
    \qquad
    \subfloat[Después del TFG]{{ \input{Imagenes/Fuentes/architecture-new} }}%
\selectlanguage{spanish}
\caption{Diagramas arquitectura PMCTrack}%
\label{fig:antesydespues}%
\end{figure}

En la figura \ref{fig:antesydespues} podemos ver dos diagramas. El primero es el que ya presentamos en el capítulo de Introducción en este mismo documento y corresponde al estado de PMCTrack antes de este TFG, el segundo corresponde al estado de PMCTrack al finalizar este proyecto. Podemos observar como los cambios han afectado a todos los niveles de PMCTrack: desde el nivel del kernel al modificar y rediseñar el módulo para que permita obtener valores desde varios procesos, pasando por el nivel del espacio de usuario con libpmctrack, hasta finalmente llegar al nivel más alto de aplicaciones que se comunican directamente con el usuario como PMCTrack-GUI.

En primer lugar, el soporte multihilo o *multithreading* permite aumentar considerablemente la potencialidad de PMCTrack. Podemos usarla para ver el rendimiento de aplicaciones que tienen más de un hilo de ejecución; o, también, podemos usarla para comparar dos resoluciones para un mismo problema, uno haciendo uso de la programación puramente secuencial y otro haciendo uso del paradigma de la programación concurrente. Esta capacidad era definitivamente necesaria para una herramienta de monitorización tan potente como PMCTrack, ahora, por fin podríamos decir que la herramienta es capaz de monitorizar cualquier tipo de programa que se ejecute en un microprocesador. Además, con esta incorporación, aprovechamos para cambiar el diseño que se usaba para guardar los datos de las muestras, mejorándolo sustancialmente en cuanto a claridad y elegancia.

En segundo lugar, la nueva librería libpmctrack provee a los programadores de todas las potencialidades de la monitorización mediante contadores hardware que ofrece PMCTrack. Con libpmctrack, un desarrollador puede evaluar y comparar las implementaciones de sus programas a partir de datos muy específicos del hardware, como puede ser los accesos a memoria caché o los fallos de predicción de saltos. Asímismo, libpmctrack permite una monitorización aún más fina que `pmctrack`, puesto que permite la monitorización individualizada de fragmentos de código marcados por el propio programador. Esto es especialmente útil para aislar partes del código cuyo análisis sea relevante por alguna razón como, por ejemplo, al tratarse de un cuello de botella del programa. Además, de nuevo la implementación de una nueva característica en el proyecto permitió la mejora del código preexistente en PMCTrack. En este caso, libpmctrack sirvió para hacer toda una refactorización del código del programa por línea de comandos `pmctrack`, quedando el código mucho más desacoplado y sencillo.

En tercer lugar, la interfaz gráfica PMCTrack-GUI facilita en gran medida el uso de PMCTrack y, además, incorpora el soporte de gráficas que pueden resultar de gran interés para el usuario.\newline
El comando `pmctrack` requiere de la especificación de muchos detalles tremendamente tediosos y poco portables a diversas máquinas. En particular, la identificación de la máquina, su número de contadores y tipo; la búsqueda y configuración de cada evento, la creación de una métrica personalizada, como el *CPI* o el *cache rate*; y, en definitiva, la selección de todos los parámetros correctos para la monitorización mediante `pmctrack`. Aún siendo la temática de la monitorización por hardware ciertamente no apta para todo tipo de usuario, con PMCTrack-GUI esperamos haber resuelto, o, al menos, rebajado ese obstáculo y conseguir que un usuario, con ciertas nociones mínimas del funcionamiento del hardware en una computadora, se centre en su objetivo principal: monitorizar el hardware.\newline
Con mucha frecuencia, se requerían tener gráficas a partir de los datos obtenidos de la monitorización por hardware. PMCTrack-GUI también ha facilitado enormemente esta tarea. Creando no solamente gráficas de la monitorización en tiempo real, si no también permitiendo la visualización de múltiples gráficas al mismo tiempo, posterior guardado de los resultados y hasta la personalización de los colores y el tamaño de línea de cada gráfica.\newline
Finalmente, la herramienta además provee de soporte de monitorización de máquinas a través de acceso \ac{SSH}. Esta característica no fue planteada inicialmente, pero que fue de gran utilidad para nosotros mismo durante el desarrollo del proyecto y que, sin duda, lo será para una gran cantidad de usuarios de PMCTrack-GUI.

# Valoración del TFG

Para la realización de este TFG hemos tenido que trabajar en tres niveles muy distintos. Programando unas veces en C, al nivel del kernel del sistema operativo; otras veces en C, a nivel de usuario cuando estuvimos desarrollando libpmctrack; y otras en Python al más alto nivel de interfaz gráfica.

La particularidad de haber sido un proyecto muy transversal, con esta gran variedad de niveles de abstraccion, creemos que ha aumentado sensiblemente su dificultad. De hecho, durante el transcurso del proyecto, hemos tenido que aprender y entender diversos temas para cada uno de estos niveles.

A continuación, listamos los que nos han resultado más relevantes:

* El funcionamiento y la documentación de los contadores hardware de cada fabricante, arquitectura y modelo.
* El funcionamiento interno del kernel Linux.
* El funcionamiento de la herramienta PMCTrack, tanto en su parte en el espacio de usuario con `pmctrack` como en sus parte relacionada con la modificación del kernel y de los módulos para cada arquitectura.
* El lenguaje de programación Python.
* Los lenguajes de marcado XML y DTD, cómo realizar la lectura ficheros con este formato y cómo generarlos a partir de otros ficheros CSV.
* Diversas librerías externas en Python para aplicar en la interfaz gráfica: wx, matplotlib,\ldots

Para conseguir que todo esto funcionase, este proyecto nos ha supuesto la inversión de una gran parte de nuestro tiempo y esfuerzo, fines de semana sin salir de la biblioteca, noches sin dormir, dejar algún trabajo o examen de lado,\ldots No obstante, al fin podemos estar satisfechos por haber logrado los objetivos marcados por el proyecto.

Para concluir, creemos que hemos hecho una importante aportación a la herramienta PMCTrack y esperamos que resulte de gran utilidad tanto dentro como fuera de nuestra universidad.

# Trabajo futuro
Seguidamente, presentamos una lista de posibles ampliaciones que se podrían añadir al trabajo realizado en este TFG en el futuro:

* PMCTrack: Soporte para el kernel de Android.
* PMCTrack: Mejorar los algoritmos de planificación del *scheduler* o planificador del kernel Linux en función de los datos que obtenga con PMCTrack de los procesos actualmente corriendo en la CPU.
* PMCTrack: Nueva opción al comando `pmctrack` para que pueda monitorizar varias CPU al mismo tiempo y separar su salida.
* PMCTrack: Soporte para más arquitecturas hardware.
* PMCTrack-GUI: Soporte para uso de contadores virtuales.
* PMCTrack-GUI: Capacidad para salvar configuraciones de contadores en ficheros para su carga posterior.
* PMCTrack-GUI: Soporte para almacenar no sólo la salida de `pmctrack` en un fichero sino también incorporar en éste los valores de las métricas de rendimiento que el usuario ha pedido mostrar en gráficas.
* PMCTrack-GUI: Soporte de arquitecturas asimétricas o heterogéneas.
