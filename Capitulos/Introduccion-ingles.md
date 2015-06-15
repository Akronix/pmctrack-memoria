\chapter{Introducción}

<!-- En castellano y en inglés -->

# PMCTrack: gestión de los contadores hardware de monitorización del rendimiento

La mayor parte de los procesadores actuales cuentan con una serie de contadores hardware para monitorización o **PMCs** (*Performance Monitoring Counters*). Estos contadores permiten a los usuarios obtener métricas de rendimiento de sus aplicaciones, tales como el número de instrucciones por ciclo (IPC) o la tasa de fallos del último nivel de la cache (*last-level-cache (LLC) miss rate*). Estas métricas ayudan a identificar posibles cuellos de botella en desarrollos software, proporcionando pistas que pueden resultar muy valiosas para programadores y diseñadores de microprocesadores. Sin embargo, el acceso a estos PMCs está normalmente restringido a código que se esté ejecutando en el nivel privilegiado reservado al sistema operativo. Para permitir el acceso a estos contadores desde el espacio del usuario es preciso implementar una herramienta a nivel de kernel, un código integrado en el propio sistema operativo o un driver, que ofrezca una interfaz de alto nivel para el usuario final \cite{perfevents,perfmon2,oprofile}.

Trabajos previos han demostrado que el planificador del sistema operativo (SO) puede beneficiarse de los datos proporcionados por los PMCs, haciendo posible la realización de sofisticadas y efectivas optimizaciones en tiempo de ejecución en sistemas multicore \cite{observations,cache-aware-asplos,merkel-eurosys10,akula,intel-amp,camp,petrucci-tecs15,acfs}. Las herramientas de dominio público que hacen uso de los PMCs permiten monitorizar el rendimiento de aplicaciones desde el espacio del usuario, pero no proporcionan una API independiente de la arquitectura para que el propio sistema operativo pueda utilizar la información de los PMCs para llevar a cabo decisiones de planificación. Ante tal situación, algunos investigadores han recurrido al desarrollo de código *ad-hoc* específico de la arquitectura para acceder a los PMCs, usándolos para realizar implementaciones de distintas estrategias de planificación \cite{observations,intel-amp,camp,acfs}. Sin embargo, esta aproximación deja "atada" la implementación del planificador a una cierta arquitectura o modelo del procesador, y adicionalmente, obliga a los desarrolladores a tratar con las rutinas de bajo nivel que acceden a los PMCs en cada arquitectura soportada por el planificador. Para evitar enfrentarse a estos graves problemas, otros investigadores han recurrido al desarrollo de sencillos prototipos ejecutados en el espacio de usuario \cite{cache-aware-asplos,akula,petrucci-tecs15}. Estos prototipos dependen de herramientas de *PMCs* existentes orientadas a ser utilizadas en el espacio de usuario.

<!--
# Antecedentes: La herramienta PMCTrack

Para superar las limitaciones comentadas en el punto anterior se propuso el desarrollo de PMCTrack, una herramienta de uso de *PMCs* para el kernel Linux orientada a ser usada por el sistema operativo.
-->


Para superar estas limitaciones se propuso el desarrollo de PMCTrack, una herramienta de gestión de contadores hardware para el kernel Linux, pero diseñada principalmente para que el SO usara los contadores para llevar a cabo tareas internas, como la planificación de procesos. Esta herramienta fue desarrollada inicialmente en un proyecto de Sistemas Informáticos por estudiantes de esta misma facultad, en el año 2012 \cite{MSDTFG12}. Actualmente, distintos miembros del Grupo de investigación en Arquitectura y Tecnología de Sistemas de Computación (ArTeCS) de esta universidad, se ocupan del desarrollo y mantenimiento de PMCTrack. De hecho, de forma simultánea a la realización de nuestro Trabajo de Fin de Grado se han añadido nuevas funcionalidades a esta herramienta más allá de las extensiones propuestas en nuestro TFG.

La novedad de la herramienta PMCTrack está ligada a la abstracción del *módulo de monitorización*, una extensión específica de la arquitectura responsable de proporcionar a cualquier algoritmo de planificación del SO que aprovecha los datos de los PMCs, aquellas  métricas de rendimiento necesarias para poder realizar su función. Esta abstracción permite la implementación de algoritmos de planificación del SO independientes de la arquitectura. En concreto, para hacer funcionar el planificador en una nueva arquitectura o modelo de procesador basta con desarrollar el módulo de monitorización correspondiente para esa nueva arquitectura o modelo de procesador en un módulo cargable del kernel. Además, PMCTrack ofrece una interfaz independiente de la arquitectura para configurar fácilmente los eventos y recopilar datos de los PMCs. Gracias a esto, el desarrollador del módulo de monitorización no tiene que lidiar con el código de bajo nivel específico de la arquitectura para acceder a los PMCs, lo que simplifica enormemente la implementación.

A pesar de ser una herramienta diseñada específicamente para ayudar al planificador del SO, PMCTrack también cuenta con un conjunto de herramientas de línea de comandos y componentes en el espacio de usuario. Estas herramientas ayudan a los diseñadores de algoritmos de planificación para el SO durante todo el ciclo de vida del desarrollo, complementando así a las herramientas existentes de depuración a nivel de kernel con información extraída de los PMCs. Por otra parte, dada la flexibilidad de los módulos de monitorización de PMCTrack, cualquier tipo de información de monitorización proporcionada por los procesadores modernos pero que no está modelada directamente a través de contadores hardware, como el consumo de energía o el nivel de ocupcación de una cache compartida, se puede exponer facilmente al usuario mediante la abstracción de _contadores virtuales_ que ofrece PMCTrack.

# Alternativas a PMCTrack

Se han creado varias herramientas para el kernel Linux en los últimos años \cite{oprofile,perfmon2,perf,papi,likwid,schedmon}, ocultando la gran diversidad existente de interfaces hardware a los usuarios finales y proporcionando a estos un acceso cómodo a los PMCs en el espacio de usuario. En general, estas herramientas se pueden dividir en dos grandes grupos. El primer grupo incluye herramientas como Oprofile \cite{oprofile}, perfmon2 \cite{perfmon2}, o perf \cite{perf}, los cuales exponen al usuario los contadores de monitorización a través de un conjunto reducido de herramientas de línea de comandos. Estas herramientas no requieren modificar el código fuente de la aplicación que se desea monitorizar, sino que actúan como procesos externos con la capacidad de recibir datos de los PMCs de otra aplicación. El segundo grupo de herramientas provee al usuario librerías para acceder a los contadores desde el código fuente de la aplicación, lo que constituye una potente interfaz de acceso a los PMCs. Las librerías libpfm \cite{perfmon2} y PAPI \cite{papi} siguen este enfoque.

La herramienta perf \cite{perf}, que se basa en el subsistema de *Eventos Perf* \cite{perfevents} del kernel Linux, es posiblemente la herramienta más completa del primer grupo comentado en la actualidad. Aunque perf comenzó como una herramienta de uso de PMCs que soportaba un amplio abanico de arquitecturas, ahora dota a los usuarios de potentes capacidades de monitorización permitiéndoles hacer un seguimiento de las llamadas al sistema de un proceso o de las actividades relacionadas con el planificador. Además, al igual que PMCTrack, perf también tiene la capacidad de exponer al usuario otra información de monitorización hardware presente en procesadores modernos (pero no proporcionada por los PMCs), como por ejemplo la tasa de ocupación de la memoria caché.

A pesar del potencial de perf y de las otras herramientas relacionadas, ninguna de ellas implementa un mecanismo que proporcione a nivel del kernel una interfaz independiente de la arquitectura que permita al planificador del SO aprovechar la información de los PMCs para sus decisiones internas. Este es el principal propósito de PMCTrack.

<!--Adicionalmente, creemos que el subsistema de *Eventos Perf* \cite{perfevents} de Linux, en el cual se basa perf,  es demasiado complejo, siendo difícil añadir el soporte necesario. Al contrario, los módulos de monitorización de PMCTrack constituyen una forma más directa de exponer este tipo de métricas a los usuarios y al planificador del sistema operativo.-->

Al igual que PMCTrack, algunas herramientas de PMCs requieren la realización de modificaciones en el kernel Linux para que puedan funcionar correctamente \cite{perfmon2,kermon}. KerMon \cite{kermon} se basa en una clase de planificación separada en el kernel para llevar a cabo el acceso a bajo nivel a los PMCs. Para extraer los datos de los PMCs de una aplicación a través de KerMon, la aplicación debe ser planificada con la nueva clase de planificación. Esta clase de planificación realmente no es más que un clon de la clase por defecto de Linux (CFS - _Completely Fair Scheduler_), por lo que no explota la información de los PMCs para tomar decisiones. PMCTrack, por el contrario, hace posible que prácticamente cualquier clase de planificación creada en el kernel pueda obtener métricas de rendimiento a través de un mecanismo independiente de la arquitectura. Para ello, es necesario realizar solo pequeñas modificaciones en el kernel, ya que como se muestra en la siguiente sección, la mayor parte de la funcionalidad de PMCTrack se encapsula en un módulo del kernel.

# Diseño de PMCTrack

Esta sección describe la arquitectura interna de PMCTrack tal y como era antes de iniciarse nuestro TFG, así como los distintos modos de uso que soportaba.

\begin{figure}[tbp]
\centering
\selectlanguage{english}
\input{Imagenes/Fuentes/architecture}
\selectlanguage{spanish}
\caption{Arquitectura de PMCTrack}
\label{fig:arch}
\end{figure}

## Arquitectura

La figura \ref{fig:arch} representa la arquitectura interna de PMCTrack antes de comenzar nuestro desarrollo del TFG. La herramienta consta de un conjunto de componentes en el espacio de usuario y del kernel. Esencialmente, el usuario final interactúa con PMCTrack a través de las herramientas de línea de comandos disponibles. Estos componentes se comunican con el módulo del kernel de PMCTrack por medio de un conjunto de entradas del sistema de ficheros `/proc` exportadas por el módulo.

El módulo del kernel implementa la mayor parte de la funcionalidad de PMCTrack. Para recopilar los datos de los contadores de rendimiento de cada hilo es necesario que el módulo sea plenamente consciente de los eventos de planificación que suceden en todo momento, como por ejemplo los cambios de contexto. Además de exponer los datos de los PMCs de las aplicaciones a las herramientas de modo usuario, el módulo implementa una API sencilla para proporcionar datos de los PMCs a cualquier clase de planificación que requiera esa información para su correcto funcionamiento. Debido a que tanto el núcleo del planificador de Linux como las clases de planificación se implementan en su totalidad en el kernel, para que el módulo de PMCTrack del kernel pueda ser consciente de estos eventos y solicitudes es imprescindible la realización de pequeñas modificaciones en el propio kernel Linux. Estas modificaciones del kernel, representadas en la figura \ref{fig:arch} con el nombre de "PMCTrack kernel API", se encargan de enviar un conjunto de notificaciones al módulo desde el núcleo del planificador. Para poder recibir estas notificaciones, el módulo PMCTrack del kernel implementa la siguiente interfaz:

\begin{lstlisting}[backgroundcolor=,basicstyle=\tt\footnotesize]
typedef struct pmc_ops{
  /* invoked when a new thread is created */
  void* (*pmcs_alloc_per_thread_data)(unsigned long,struct task_struct*);
  /* invoked when thread leaves the CPU */
  void (*pmcs_save_callback)(void*, int);
  /* invoked when thread enters the CPU */
  void (*pmcs_restore_callback)(void*, int);
  /* invoked every clock tick on a per-thread basis */
  void (*pmcs_tbs_tick)(void*, int);
  /* invoked when a process invokes exec() */
  void (*pmcs_exec_thread)(struct task_struct*);
  /* invoked when a thread exists the system */
  void (*pmcs_exit_thread)(struct task_struct*);
  /* invoked when a thread's descriptor is freed up */
  void(*pmcs_free_per_thread_data)(struct task_struct*);
  /* invoked when the scheduler requests per-thread
        monitoring information  */
  int  (*pmcs_get_current_metric_value)(struct task_struct* task, int key, uint64_t* value);
} pmc_ops_t;
\end{lstlisting}

La mayoría de estas notificaciones son enviadas únicamente cuando el módulo PMCTrack del kernel está cargado y el usuario (o el propio planificador) está usando la herramienta para monitorizar el rendimiento de una determinada aplicación.

Tal y como se ilustra en la figura \ref{fig:arch}, el módulo PMCTrack del kernel consta de varios componentes. La capa del núcleo de PMCTrack independiente de la arquitectura implementa un interfaz llamado \texttt{pmc\_ops\_t} e interactúa con la herramienta PMCTrack de línea de comandos a través del sistema de ficheros */proc* de Linux. El componente independiente de la arquitectura se basa en un _backend_ (BE) compatible con la Unidad de Monitorización de Rendimiento (conocida como PMU por sus siglas en inglés) para llevar a cabo el acceso de bajo nivel a los PMCs y para realizar la traducción de los _strings_ de configuración proporcionados por el usuario a estructuras de datos internas para la plataforma en cuestión. Actualmente existen _backends_ compatibles con la mayoría de los procesadores modernos de Intel y AMD. Además, de forma simultánea al desarrollo de nuestro TFG, se llevó a cabo el desarrollo de dos _backends_ extra, uno compatible con procesadores Cortex de ARM de 32 y 64 bits, y otro para el coprocesador Xeon Phi de Intel. El módulo del kernel de PMCTrack también incluye un conjunto de *módulos de monitorización* específicos de la plataforma. El objetivo principal de un módulo de monitorización es proporcionar a un algoritmo de planificación implementado en el kernel aquellas métricas de rendimiento de los hilos necesarias para que éste pueda funcionar.

Dotar al kernel Linux de soporte para PMCTrack implica incluir dos nuevos ficheros en el propio kernel y añadir menos de 20 líneas de código a las fuentes del núcleo. Estos cambios pueden ser aplicados fácilmente a diferentes versiones del kernel a partir de la versión 2.6.38.

## Modos de uso de PMCTrack

Antes de iniciar el desarrollo de este TFG, PMCTrack soportaba tres modos de uso: modo planificador, muestreo por tiempo y muestreo basado en eventos.

\begin{figure}[tbp!]
\centering
\selectlanguage{english}
\input{Imagenes/Fuentes/mmon}
\caption{Módulos de monitorización de PMCTrack}
\label{fig:mmon}
\end{figure}

### Modo planificador

Este modo permite que cualquier algoritmo de planificación en el kernel (es decir, clase de planificación) pueda obtener datos de monitorización de cada hilo, haciendo posible la toma de decisiones en función de estos datos. La activación de este modo en un determinado hilo desde el código del planificador se reduce a la activación del flag \texttt{prof\_enabled}\footnote{Este flag se añade a la estructura \texttt{task\_struct} de Linux al aplicar el parche del kernel para PMCTrack.} en el descriptor del hilo.

Para garantizar que la implementación del algoritmo de planificación que explota este modo de uso se mantiene independiente de la arquitectura, el propio planificador (implementado en el kernel) no configura los PMCs ni se ocupa de ellos directamente. En lugar de eso, uno de los *módulos de monitorización* se encarga de proporcionar a la clase de planificación las métricas de monitorización de alto nivel necesarias para  el algoritmo, como por ejemplo el número de instrucciones retiradas por ciclo (IPC) o la tasa de fallos de cache.

Como puede verse en la figura \ref{fig:mmon}, PMCTrack puede incluir varios *módulos de monitorización* compatibles con una plataforma dada. Sin embargo, sólo uno de ellos puede estar habilitado al mismo tiempo: el que proporciona al planificador la información de los PMCs para que pueda llevar a cabo su función. En el caso de que haya disponibles varios módulos de monitorización, el administrador del sistema puede indicar al sistema cual de ellos usar, escribiéndolo en el fichero \texttt{/proc/pmc/mmon\_manager}. De manera similar, el período de muestreo de datos de los PMCs utilizado en el módulo de monitorización se puede configurar a través del sistema de ficheros */proc*.

El planificador puede comunicarse con el módulo de monitorización activo para obtener datos de monitorización de un hilo a través de la siguiente función de la API de PMCTrack del kernel:
\begin{lstlisting}[backgroundcolor=,basicstyle=\tt\footnotesize]
int pmcs_get_current_metric_value(struct task_struct*
   task, int metric_id, uint64_t* value);
\end{lstlisting}

Por simplicidad, a cada métrica se le asigna un ID numérico, conocido por el planificador y el módulo de monitorización. Para poder obtener datos de métricas actualizados, la función mencionada podrá ser invocada desde la función de tratamiento de señal del planificador.

Los módulos de monitorización hacen posible que una política de planificación que está basada en el uso de contadores de rendimiento pueda ser usada en nuevas arquitecturas o modelos de procesador que aparezcan en un futuro. Todo lo que hay que hacer es construir un módulo de monitorización o adaptar uno existente a la plataforma en cuestión. Desde el punto de vista del programador, la creación de un módulo de monitorización implica la implementación de una interfaz muy similar a \texttt{pmc\_ops\_t}. En concreto, se compone de varias llamadas a funciones que permiten notificar al módulo sobre activaciones y desactivaciones solicitadas por el administrador del sistema, cambios de contexto de hilos, salidas y entradas de un hilo del sistema (_sleep/resume_), solicitudes de valores de métricas de PMCs por parte del planificador, etcétera. Sin embargo, el programador normalmente solo implementa el subconjunto de llamadas a funciones requeridas para llevar a cabo el proceso interno necesario.

La creación de nuevos módulos de monitorización es una tarea bastante sencilla por varias razones. En primer lugar, el programador no necesita acceder directamente a los registros de los PMCs. En lugar de ello, el módulo PMCTrack del kernel ofrece una API independiente de la arquitectura que permite al módulo de monitorización especificar la configuración del contador a través de _strings_, para recibir muestras de PMCs periódicamente y controlar la multiplexación de eventos. En segundo lugar, debido a que el módulo recibe notificaciones cuando se crea un nuevo hilo o cuando éste termina, el módulo de monitorización puede asignar datos referentes a un hilo concreto para simplificar cualquier tipo de procesamiento específico de hilo. Finalmente, como el código de un módulo de monitorización reside en el módulo del kernel de PMCTrack, subsanar un error de programación no precisa reiniciar el sistema en la mayoría de los casos. El módulo del kernel puede recompilarse, descargarse y volverse a cargar una vez se hayan arreglado los errores.

### Muestreo por tiempo (TBS - _Time-Based Sampling_)

Esta característica permite al usuario recopilar datos de rendimiento de una aplicación secuencial desde espacio de usuario a intervalos de tiempo regulares. La herramienta \texttt{pmctrack} de línea de comandos, cuya interfaz de usuario está inspirada en el programa \texttt{cputrack} de Solaris, hace posible esta función. Para ilustrar el funcionamiento de la herramienta consideremos el siguiente ejemplo:

\begin{lstlisting}[language=bash,basicstyle=\tt\scriptsize]
$ pmctrack -T 1 -c pmc0,pmc3=0x2e,umask3=0x41 ./mcf06
nsample  event          pmc0          pmc3
      1   tick    1961001132        110634
      2   tick    1247853112          8323
      3   tick    1230836405          3859
      4   tick    1358134323        409386
      5   tick    1280630906       1199270
      6   tick    1231578609      15488307
...
\end{lstlisting}

En un sistema con un procesador moderno de Intel, este comando proporcionará al usuario el número de instrucciones retiradas (columna pmc0) y los fallos de cache (columna pmc3) en cada segundo. Cada muestra está representada por una fila diferente. El período de muestreo se puede especificar en segundos a través de la opción -T, siendo posible especificar también fracciones de segundo (por ejemplo 0.3 para 300ms). Al final de la línea se especifica el comando para ejecutar la aplicación asociada que se desea monitorizar (por ejemplo ./mcf06).

La opción -c acepta como argumento un _string_ de configuración que sigue el formato de configuración de eventos internos reconocido por el módulo PMCTrack del kernel. El formato de esta línea da flexibilidad a usuarios experimentados permitiéndoles decidir los eventos que contarán cada uno de los contadores, especificando el código hexadecimal que será escrito en los registros de bajo nivel de los PMCs expuestos por el módulo del kernel. Como hemos visto, el string \texttt{pmc0,pmc3=0x2e,umask3=0x41} permite obtener el recuento de eventos mencionados en la mayoría de los procesadores modernos de Intel. En procesadores de la familia ARM Cortex Ax este conjunto de eventos puede representarse mediante el _string_ \texttt{pmc1=0x8,pmc2=0x17}. Si el usuario desconoce los códigos hexadecimales que permiten asociar un evento a un contador es necesario consultar esos códigos en el manual de la arquitectura en cuestión.

Una característica muy destacable del programa `pmctrack` es su capacidad de obtener también los valores de los contadores virtuales que exporta el módulo de monitorización activo. De este modo, es posible contabilizar eventos con los contadores hardware al mismo tiempo que se extrae otro tipo de información de monitorización relevante, como el consumo de potencia media o energía consumida en un intervalo de tiempo prefijado. Para obtener los valores de los contadores virtuales es preciso usar la opción -V seguida de la cadena de caracteres que indica qué contadores virtuales (numerados a partir del 0) se desean consultar. Por ejemplo, la cadena `virt0,virt2` constituiría una cadena válida para consultar el valor de dos contadores virtuales siempre y cuando el módulo de monitorización activo exportase dichos contadores. Para consultar la semántica de los contadores virtuales actualmente exportados es preciso consultar una entrada */proc* gestionada por PMCTrack.

En caso de que un modelo específico del procesador no integre suficientes PMCs como para monitorizar a la vez un conjunto determinado de eventos, el usuario puede activar la función de multiplexación de eventos de PMCTrack. Esto se reduce a especificar varios conjuntos de eventos mediante la inclusión de varias instancias de la opción -c en la línea de comandos. En este caso, en la salida aparecerá un nuevo campo \textit{expid} que indicará al usuario a qué experimento corresponde cada una de las muestras que se imprimen por pantalla.

Cabe destacar que en el caso de que el módulo de monitorización esté utilizando actualmente los PMCs en nombre de un algoritmo de planificación, al usuario no se le permite especificar un _string_ de configuración a través de la opción -c de PMCTrack. Sin embargo, para propósitos de depuración el comando `pmctrack` puede seguir utilizándose (sin la opción -c) para obtener los recuentos de los eventos asociados con la configuración impuesta por el módulo de monitorización.

Para soportar la característica del muestreo por tiempo, el módulo del kernel de PMCTrack almacena las muestras de los contadores en un buffer circular. La herramienta de línea de comandos obtiene las muestras del buffer circular del kernel mediante la lectura de un fichero */proc* que bloquea el proceso de monitorización hasta que se generan nuevas muestras o hasta que termina la aplicación.

### Muestreo basado en eventos  (EBS - _Event-Based Sampling_)

El muestreo basado en eventos constituye una variante del muestreo basado en tiempo en el que los valores de los PMCs se recogen cuando el número de ocurrencias de un cierto evento alcanza un cierto umbral $U$. Para soportar EBS, el módulo PMCTrack del kernel explota la característica de interrupción por desbordamiento presente en la mayoría de las Unidades de Monitorización del Rendimiento (PMU) de los procesadores actuales. Esencialmente, cuando se activa EBS, el módulo del kernel de PMCTrack inicializa el contador a $-U$; cuando este contador se desborda la PMU genera una interrupción, y entonces el módulo del kernel lee todos los *PMCs*.

Para usar EBS desde el espacio de usuario se debe especificar el flag \textit{ebs}, junto al número de contador asociado, al final del _string_ de configuración de eventos pasado al comando \texttt{pmctrack}. Al hacer esto, también es posible especificar un valor del umbral como en el ejemplo siguiente:

\begin{lstlisting}[language=bash,basicstyle=\tt\scriptsize]
$ pmctrack -c pmc0,pmc3=0x2e,umask3=0x41,ebs0=500000000 ./mcf06
nsample  event          pmc0          pmc3
      1    ebs     500000087         10677
      2    ebs     500000002         22336
      3    ebs     500000004         17131
      4    ebs     500000007         12995
      5    ebs     500000014          9348
      6    ebs     500000010          5804
...
\end{lstlisting}

La columna \textit{pmc3} muestra el número de fallos de cache por cada 500 millones de instrucciones retiradas. Hay que tener en cuenta, sin embargo, que los valores de la columna \textit{pmc0} no reflejan con exactitud el número especificado en el flag \textit{ebs}. Esto tiene que ver con el hecho de que, en los procesadores modernos, la interrupción del PMU no se sirve inmediatamente después del desbordamiento del contador. Por el contrario, debido a la ejecución especulativa y fuera de orden, el procesador podría llegar a ejecutar cientos de instrucciones antes de procesar la interrupción. Estas imprecisiones no suponen un gran problema, siempre y cuando se establezcan tamaños de umbral suficientemente altos.


<!--
  Se ha descubierto que la característica del EBS resulta extremadamente útil cuando se trata de caracterizar el rendimiento de las aplicaciones en los distintos cores de un sistema asimétrico. -->

# Objetivos del proyecto

La herramienta PMCTrack ofrece grandes funcionalidades y permite que el planificador del SO pueda explotar los contadores hardware para realizar optimizaciones en tiempo de ejecución. Sin embargo, PMCTrack aún cuenta con importantes limitaciones que ensombrecen su gran potencial, sobre todo en lo que respecta a la monitorización de aplicaciones desde modo usuario.

En primer lugar, su uso resulta un tanto complicado para un usuario poco experimentado, ya que éste tiene que consultar manuales técnicos de distintas arquitecturas para poder especificar los códigos hexadecimales de los eventos que desea contabilizar en cada uno de los PMCs.

En segundo lugar, la obtención del recuento de eventos específicos en los PMCs cada cierto tiempo no proporciona al usuario una visión global acerca de la evolución temporal del valor de esos contadores, y mucho menos de métricas de alto nivel compuestas por la combinación de valores de dos o más PMCs. Esta valiosa información para el usuario puede conseguirse mediante la construcción de gráficas. No obstante, esto requiere (1) procesar los datos proporcionados por el comando \texttt{pmctrack} para obtener los valores de las métricas de alto nivel a lo largo del tiempo y (2) emplear alguna utilidad como *Gnuplot* para la generación de las gráficas finales. Finalmente, otra limitación significativa de la herramienta es el hecho de que el comando \texttt{pmctrack} (y el propio módulo del kernel en el que se basa) no permite la monitorización de aplicaciones multihilo desde el espacio de usuario.

Para proporcionar una solución a estas y otras limitaciones de PMCTrack, este Trabajo de Fin de Grado persigue los siguientes objetivos:

  1. Proporcionar soporte para la monitorización de aplicaciones multihilo desde el espacio de usuario con PMCTrack.

  2. Diseñar e implementar un _frontend_ gráfico para PMCTrack (llamado PMCTrack-GUI) que permita visualizar en tiempo real el valor de distintas métricas de rendimiento definidas por el usuario.

  3. Crear _libpmctrack_, una librería que permita la monitorización de fragmentos de código de aplicaciones en el espacio de usuario mediante PMCs.

<!--
 En primer lugar,  Para ello, se procederdiseñaremos un interfaz gráfico permitiendo visualizar gráficas de rendimiento en tiempo real de cualquier aplicación, y daremos soporte a PMCTrack para la monitorización de aplicaciones multihilo desde el espacio de usuario. En segundo lugar, extenderemos la herramienta PMCTrack con una librería en el espacio de usuario llamada *libpmctrack*, que permitirá la monitorización de fragmentos de código de aplicaciones en el espacio de usuario usando *PMCs*.


Adicionalmente, se llevarán a cabo tres casos de estudio sobre el comportamiento de distintos benchmarks en diversas arquitecturas de distinta potencia computacional. Para la realización de estos casos de estudio se utilizarán las herramientas PMCTrack desarrolladas durante este proyecto: PMCTrack-GUI y libpmctrack.
-->


# Plan de trabajo

Para alcanzar los objetivos del proyecto, presentados en la sección anterior, el desarrollo del proyecto constó de las siguientes etapas:

1. Planificación del trabajo a realizar por cada uno de los dos integrantes del proyecto.
2. Lectura de documentación acerca de los lenguajes de programación y demás tecnologías utilizadas para llevar a cabo los desarrollos (Python, librería WX, matplotlib\ldots). Esta etapa también conlleva familiarizarse con la arquitectura interna de PMCTrack.
3. Realización de bocetos o *mockups* de PMCTrack-GUI para estudiar distintas alternativas de diseño y ayudar a llegar a un consenso sobre el diseño definitivo.
4. Implementación del soporte para la monitorización de aplicaciones multihilo en el espacio de usuario con PMCTrack.
5. Implementación de PMCTrack-GUI.
6. Diseño e implementación de _libpmctrack_ y refactorización del código del programa de línea de comandos `pmctrack`.
7. Realización de casos de estudio poniendo a prueba las herramientas desarrolladas.

Cabe destacar que el orden de estas etapas es meramente orientativo, ya que dichas etapas no se realizaron de forma estrictamente secuencial. En particular, fue necesario realizar planificaciones particulares en cada una de las etapas y distintos componentes de las aplicación PMCTrack-GUI se realizaron de forma simultánea. Adicionalmente, se dio soporte en nuestros desarrollos a funcionalidades de PMCTrack añadidas mientras llevábamos a cabo nuestro proyecto (PMCTrack es una herramienta en continuo desarrollo), y se añadieron nuevas funcionalidades a nuestros desarrollos que no estaban inicialmente previstas (como la inclusión de un modo SSH para PMCTrack-GUI).

# Estructura de la memoria

El resto del contenido de esta memoria se organiza de la siguiente forma:

* **El capítulo 2** explica el desarrollo del soporte a la herramienta PMCTrack para la monitorización de aplicaciones multihilo desde el espacio de usuario.
* **El capítulo 3** presenta la librería libpmctrack. En este capítulo no solo se describen los detalles de la librería sino también se presenta la motivación existente tras la misma.
* **El capítulo 4** presenta la motivación, el diseño e implementación de PMCTrack-GUI, el _frontend_ gráfico de PMCTrack.
<!--
* **El capítulo 5** muestra los resultados de los casos de estudio realizados con las herramientas desarrolladas en este proyecto.
-->
* **El capítulo 5** pone a prueba las extensiones de PMCTrack desarrolladas en este proyecto mediante tres casos de estudio.
<!--
* **El capítulo 6** enumera las principales aportaciones al proyecto efectuadas por cada miembro del equipo.
-->
* **El capítulo 6** expone las conclusiones finales de este Trabajo de Fin de Grado y presenta el trabajo futuro.
* Finalmente, se proporcionan dos apéndices. El primero incluye una serie de diagramas UML para proporcionar al lector detalles concretos del diseño de PMCTrack-GUI. El segundo apéndice, enumera las contribuciones al proyecto de los integrantes del equipo de trabajo de este TFG.
