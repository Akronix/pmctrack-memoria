\chapter{Conclusiones y trabajo futuro}

<!-- En castellano y en inglés -->

# Conclusiones

Después de la realización de este proyecto, PMCTrack cuenta con tres nuevas características: (1) soporte de monitorización para aplicaciones multihilo, (2) la librería libpmctrack --que permite la monitorización de fragmentos de código con los contadores hardware--, y (3) la aplicación PMCTrack-GUI -- un _frontend_ gráfico para PMCTrack que facilita su uso y permite obtener gráficas en tiempo real de métricas de alto nivel definidas por el usuario--. En los capítulos 2, 3 y 4, hemos explicado en detalle el funcionamiento y el proceso de diseño e implementación de cada una de estas características. En el capítulo 5, hemos puesto a prueba su funcionamiento y mostrado su gran utilidad mediante tres casos de estudio. Para finalizar, analizaremos ahora a fondo el impacto holístico de cada una de estas nuevas características.

\begin{figure}%
\selectlanguage{english}
    \centering
    \subfloat[Antes del comienzo del TFG]{{ \input{Imagenes/Fuentes/architecture} }}%
    \qquad
    \subfloat[Después de la finalización del TFG]{{ \input{Imagenes/Fuentes/architecture-new} }}%
\selectlanguage{spanish}
\caption{Arquitectura de PMCTrack}%
\label{fig:antesydespues}%
\end{figure}

En la figura \ref{fig:antesydespues} podemos ver dos diagramas. El primero es el que ya presentamos en el capítulo de Introducción en este mismo documento y corresponde a la arquitectura de PMCTrack antes de comenzar este TFG. El segundo muestra la nueva arquitectura de PMCTrack al finalizar nuestro proyecto. Podemos observar cómo los cambios han afectado a todos los niveles de PMCTrack: desde el nivel del kernel al modificar y rediseñar el módulo para que permita recabar muestras de los contadores hardware de varios hilos de una misma aplicación, pasando por el nivel del espacio de usuario con libpmctrack, hasta finalmente llegar al nivel más alto de aplicaciones que permiten al usuario final interactuar con la herramienta, como es el caso de PMCTrack-GUI.

En primer lugar, el soporte multihilo o *multithreading* permite extender considerablemente la funcionalidad de PMCTrack. Podemos usar esta nueva característica para monitorizar el rendimiento de aplicaciones con más de un hilo de ejecución; o, también, podemos usarla para comparar la efectividad de varias implementaciones alternativas (secuenciales o paralelas) para un mismo problema. Esta capacidad era definitivamente necesaria para una herramienta de monitorización tan potente como PMCTrack. Ahora, por fin podemos afirmar que la herramienta es capaz de monitorizar cualquier tipo de programa que se ejecute en un microprocesador moderno con arquitectura ARM o x86. Además, incorporar el soporte para aplicaciones multihilo, también constituyó una gran oportunidad para que modificarámos profundamiente la aproximación utilizada el almacenamiento temporal de los datos de las muestras de los contadores hardware para las aplicaciones monitorizadas. Tras la modificación, el diseño interno del módulo del kernel de PMCTrack ha mejorado sustancialmente en cuanto a claridad y robustez.

En segundo lugar, la nueva librería libpmctrack provee a los programadores de todas las capacidades de la monitorización mediante contadores hardware que ofrece PMCTrack. Con libpmctrack, un desarrollador puede evaluar y comparar las implementaciones de sus programas a partir de datos muy específicos del hardware, como puede ser los accesos a memoria caché o los fallos de predicción de saltos. Asímismo, libpmctrack permite una monitorización de grano más fino que la que permite la herramienta de línea de comandos `pmctrack`: libpmctrack permite la monitorización individualizada de fragmentos de código seleccionados por el programador. Esto es especialmente útil para aislar partes del código cuyo análisis sea relevante por alguna razón como, por ejemplo, tratarse de un cuello de botella del programa. Además, de nuevo la implementación de una nueva característica en el proyecto permitió la mejora del código existente en PMCTrack. Concretamente, el este proyecto empleamos libpmctrack sirvió para realizar una refactorización completa del programa `pmctrack`, dando lugar a un código mucho más sencillo y completamente desacoplado de la interfaz exportada por el módulo del kernel de PMCTrack.

En tercer lugar, la interfaz gráfica PMCTrack-GUI facilita en gran medida el uso de PMCTrack y, además, incorpora el soporte de gráficas que pueden resultar de gran interés para el usuario final.\newline
El comando `pmctrack` requiere de la especificación de muchos detalles tremendamente tediosos y específicos de cada modelo de procesador como, por ejemplo, la identificación de la máquina, su número de contadores y tipo, el código hexadecimal de cada evento y su configuración, la creación de una métrica personalizada, como el *CPI* o el *cache rate*. En definitiva, el usuario es responsable de especificar todos los parámetros correctos y de bajo nivel para la monitorización mediante `pmctrack`. Aún siendo la temática de la monitorización por hardware ciertamente no apta para todo tipo de usuario, con PMCTrack-GUI esperamos haber resuelto, o, al menos, rebajado ese obstáculo y conseguir que un usuario, con ciertas nociones mínimas del funcionamiento del hardware en una computadora, se centre en su objetivo principal: obtener datos de monitorización del rendimiento de las aplicaciones.\newline
Con mucha frecuencia, se precisa la construcción de gráficas a partir de los datos obtenidos de la monitorización por hardware. PMCTrack-GUI también ha facilitado enormemente esta tarea, permitiendo la creación de gráficas para  la monitorización en tiempo real, sino también permitiendo la visualización de múltiples gráficas simultáneamente. Además esta herramienta ofrece la posibilidad de guardar los resultados obtenidos durante la monitorización y está equipada con opciones avanzadas para la personalización de las gráficas generadas (colores utilizados, anchura de línea, \ldots). \newline
Finalmente, la herramienta además provee de soporte de monitorización remóta de máquinas accesibles por \ac{SSH}. Esta característica no fue planteada inicialmente, pero ha resultado de gran utilidad para nosotros durante el desarrollo del proyecto y creemos que, sin duda, lo será para una gran cantidad de usuarios de PMCTrack-GUI.

# Valoración del TFG

Para la realización de este TFG hemos tenido que trabajar en tres niveles muy distintos. Programando unas veces en C, al nivel del kernel del sistema operativo; otras veces en C, a nivel de usuario cuando estuvimos desarrollando libpmctrack; y otras en Python al más alto nivel de interfaz gráfica.

La particularidad de haber sido un proyecto muy transversal, con esta gran variedad de niveles de abstracción, creemos que ha aumentado sensiblemente su dificultad. De hecho, durante el transcurso del proyecto, hemos tenido que documentarnos profundamente para poder comprender la interacción entre cada uno de estos niveles.

A continuación, listamos los aspectos que nos han resultado más relevantes:

* El funcionamiento y la documentación de los contadores hardware de cada fabricante, arquitectura y modelo.
* El funcionamiento interno del kernel Linux.
* La arquitectura interna de la herramienta PMCTrack, tanto en su parte en el espacio de usuario con `pmctrack` como en sus parte relacionada con la modificación del kernel y de los módulos para cada arquitectura.
* El lenguaje de programación Python.
* Los lenguajes de marcado XML y DTD, cómo realizar la lectura ficheros con este formato y cómo generarlos a partir de otros ficheros CSV.
* Diversas librerías externas de Python usadas en el desarrollo de la interfaz gráfica: wx, matplotlib,\ldots

Para conseguir que todo esto funcionase, este proyecto nos ha supuesto la inversión de una gran parte de nuestro tiempo y esfuerzo**, fines de semana sin salir de la biblioteca, noches sin dormir, dejar algún trabajo o examen de lado,**\ldots No obstante, al fin podemos estar satisfechos por haber logrado los objetivos marcados por el proyecto.

Para concluir, creemos que hemos hecho una importante aportación a la herramienta PMCTrack y esperamos que resulte de gran utilidad tanto dentro como fuera de nuestra universidad.

# Trabajo futuro
Seguidamente, presentamos una lista de posibles ampliaciones de PMCTrack que se podrían añadir al trabajo realizado en este TFG en el futuro:

* Soporte de PMCTrack en Android.
* Diseño de nuevos algoritmos de planificación en el kernel Linux que realicen optimizaciones en tiempo de ejecución en base en las medidas de los contadores que ofrece PMCTrack.
* Inclusión de una nueva opción en el comando `pmctrack` para permitir la monitorización de varias CPU al mismo tiempo y separar su salida
* Soporte para otras arquitecturas hardware (más allá de x86 y ARM)
* Soporte para uso de contadores virtuales en PMCTrack-GUI.
* Capacidad para salvar configuraciones de contadores en ficheros para su carga posterior en PMCTrack-GUI.
* Soporte para almacenar no sólo la salida de `pmctrack` en un fichero sino también incorporar en éste los valores de las métricas de rendimiento que el usuario de PMCTrack-GUI ha solicitado mostrar gráficamente.
* Soporte de arquitecturas asimétricas o heterogéneas en PMCTrack-GUI.
