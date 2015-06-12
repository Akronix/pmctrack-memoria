\chapter{Introducción}
<!-- En castellano y en inglés --->

# Los contadores hardware para monitorización

La gran mayoría de los computadores modernos cuentan con una serie de contadores hardware para monitorización, comunmente conocidos como *PMCs* por sus siglas en inglés (Performance Monitoring Counters). Estos contadores permiten a los usuarios obtener métricas de rendimiento de sus aplicaciones, tales como el número de instrucciones por ciclo (IPC) o la tasa de fallos del último nivel de la cache (LLC miss rate).

Estas métricas ayudan a identificar posibles cuellos de botella en desarrollos software, proporcionando pistas que pueden resultar muy valiosas a programadores y arquitectos informáticos.

Sin embargo, el acceso a estos *PMCs* está normalmente restringido a código que se esté ejecutando en un nivel privilegiado del sistema operativo. Para permitir el acceso a estos contadores desde el espacio del usuario es preciso implementar una herramienta a nivel de kernel, un código integrado en el propio sistema operativo o un driver, que ofrezcan un interfaz que pueda usar una herramienta en el espacio del usuario que a su vez ofrezca un interfaz de alto nivel. AÑADIR REFERENCIAS.

Trabajos previos han demostrado que el planificador del sistema operativo puede beneficiarse de los datos provistos por los *PMCs*, haciendo posible la realización de sofisticadas y efectivas optimizaciones en tiempo de ejecución en sistemas multicore. AÑADIR REFERENCIAS.

Las herramientas de dominio público que hacen uso de los *PMCs* permiten monitorizar el rendimiento de aplicaciones desde el espacio del usuario, pero no proporcionan una API independiente de la arquitectura para que el propio sistema operativo pueda utilizar la información de los *PMCs* para llevar a cabo decisiones de planificación.

Ante tal situación, algunos investigadores han recurrido al desarrollo de código *ad-hoc* específico de la arquitectura para acceder a los *PMCs*, usándolos para realizar implementaciones de distintas estrategias de planificación. AÑADIR REFERENCIAS.

Sin embargo, esta aproximación deja "atada" la implementación del planificador a una cierta arquitectura o modelo del procesador, y adicionalmente, obliga a los desarrolladores a tratar con las rutinas de bajo nivel que acceden a los PMCs en cada arquitectura soportada por el planificador.

Para evitar enfrentarse a estos graves problemas, otros investigadores han recurrido al desarrollo de prototipos simples ejecutados en el espacio de usuario. AÑADIR REFERENCIAS. Estos prototipos dependen de herramientas de PMCs existentes orientadas a ser utilizadas en el espacio de usuario. 

# Antecedentes: La herramienta PMCTrack

Para superar las limitaciones comentadas en el punto anterior se propuso el desarrollo de PMCTrack, una herramienta de uso de *PMCs* para el kernel Linux orientada a ser usada por el sistema operativo.

Esta herramienta fue desarrollada inicialmente en un proyecto de sistemas informáticos por estudiantes de esta misma facultad, en el año 2012 \cite{MSDTFG12}. Su uso y desarrollo se ha mantenido por el Grupo de Arquitectura y Tecnología de Computadores de esta universidad, añadiéndose nuevas funcionalidades incluso de forma simultánea a nuestro desarrollo del Trabajo de Fin de Grado.

La novedad de la herramienta PMCTrack reside en la abstracción del *módulo de monitorización*, una extensión específica de la arquitectura responsable de proporcionar cualquier algoritmo de planificación del sistema operativo que aprovecha los datos de los PMCs para generar las métricas de rendimiento necesarias para realizar su función. Esta abstracción permite la implementación de algoritmos de planificación del sistema operativo independientes de la arquitectura. En concreto, para hacer funcionar el planificador en una nueva arquitectura o modelo de procesador basta con desarrollar el módulo de monitorización correspondiente a esa nueva arquitectura o modelo de procesador en un módulo cargable del kernel.

Además, PMCTrack ofrece una interfaz independiente de la arquitectura para configurar fácilmente los eventos y recopilar datos de los PMCs, gracias a esto el desarrollador del módulo de monitorización no tiene que lidiar con el código de bajo nivel específico de la arquitectura para acceder a los PMCs, lo que simplifica enormemente el proceso de diseño.

A pesar de ser una herramienta diseñada específicamente para ayudar al planificador del sistema operativo, PMCTrack también cuenta con un conjunto de herramientas de línea de comandos y componentes en el espacio de usuario. Estas herramientas ayudan a los diseñadores del planificador del sistema operativo durante todo el ciclo de vida del desarrollo, al complementar las herramientas existentes de depuración a nivel de kernel con el análisis de la información extraída de los PMCs.

# Alternativas a PMCTrack

Se han creado varias herramientas para el kernel Linux en los últimos años AÑADIR REFERENCIAS, ocultando la gran diversidad existente de interfaces hardware a los usuarios finales y proporcionando a estos un acceso cómodo a los PMCs en el espacio de usuario. En general, estas herramientas se pueden dividir en dos grandes grupos.

El primer grupo incluye herramientas como Oprofile AÑADIR REFERENCIA, perfmon2 AÑADIR REFERENCIA, o perf AÑADIR REFERENCIA, los cuales exponen al usuario los contadores de monitorización a través de un conjunto reducido de herramientas de línea de comandos. Estas herramientas no requieren modificar el código fuente de la aplicación que se desea monitorizar, actúan como procesos externos con la capacidad de recibir datos de los PMCs de otra aplicación.

El segundo grupo de herramientas provee al usuario librerías para acceder a los contadores desde el código fuente de la aplicación, lo que constituye una potente interfaz de acceso a los *PMCs*. Las librerías libpfm AÑADIR REFERENCIA y PAPI AÑADIR REFERENCIA siguen este enfoque.

La herramienta perf AÑADIR REFERENCIA, que se basa en el subsistema de *Eventos Perf* del kernel Linux, es posiblemente la herramienta más completa del primer grupo comentado, en el momento en el que se publicó esta memoria. Aunque perf comenzó como una herramienta de uso de *PMCs* que soportaba un amplio abanico de arquitecturas, ahora dota a los usuarios de potentes capacidades de monitorización permitiéndoles hacer un seguimiento de las llamadas al sistema de un proceso o de las actividades relacionadas con el planificador. Además, al igual que PMCTrack, perf también tiene la capacidad de exponer datos del hardware de la máquina (no proporcionados por PMCs) expuestos al usuario haciendo uso de hardware moderno, como por ejemplo la tasa de ocupación de la memoria caché.

A pesar del potencial de perf y de las otras herramientas relacionadas, ninguna de ellas implementa un mecanismo que proporcione a nivel del kernel una interfaz independiente de la arquitectura que permita al planificador del sistema operativo aprovechar la información de los *PMCs* para sus decisiones internas. Este es el principal propósito de PMCTrack. Adicionalmente, creemos que el subsistema de *Eventos Perf* de Linux, en el cual se basa perf,  es demasiado complejo, siendo difícil añadir el soporte necesario. Al contrario, los módulos de monitorización de PMCTrack constituyen una forma más directa de exponer este tipo de métricas a los usuarios y al planificador del sistema operativo.

Al igual que PMCTrack, algunas herramientas de *PMCs* requieren la realización de modificaciones en el kernel Linux para que puedan funcionar correctamente AÑADIR REFERENCIAS. KerMon AÑADIR REFERENCIA se basa en una clase de planificación separada en el kernel para llevar a cabo el acceso a bajo nivel a los *PMCs*. Para extraer los datos de los PMCs de una aplicación a través de KerMon, la aplicación debe ser programada con la nueva clase de planificación. Esta clase de planificación realmente no es más que un clon de la clase del Planificador Completamente Justo (CFS), por lo que no explota la información de los *PMCs* para tomar decisiones.

PMCTrack, por otra parte, hace posible que prácticamente cualquier clase de planificación creada en el kernel pueda obtener métricas de rendimiento a través de un mecanismo independiente de la arquitectura. Para este fin es necesario realizar pequeños cambios en el kernel, ya que como se muestra en la siguiente sección, la gran mayoría de la funcionalidad de PMCTrack se encapsula en módulos del kernel.

# Diseño de PMCTrack

Esta sección describe la arquitectura interna de PMCTrack tal y como era antes de iniciarse nuestro TFG, así como los distintos modos de uso que soportaba.

\begin{figure}[tbp]
\centering
\selectlanguage{english}
\input{Imagenes/Fuentes/architecture}
\caption{Arquitectura de PMCTrack}
\label{fig:arch}
\end{figure}

## Arquitectura

La figura \ref{fig:arch} representa la arquitectura interna de PMCTrack antes de comenzar nuestro desarrollo del TFG. La herramienta consta de un conjunto de componentes en el espacio de usuario y del kernel. A un alto nivel, el usuario final interactúa con PMCTrack a través de las herramientas de línea de comandos disponibles. Estos componentes se comunican con el módulo del kernel de PMCTrack por medio de un conjunto de entradas */proc* del sistema de ficheros Linux exportadas por el módulo.

El módulo del kernel implementa la gran mayoría de la funcionalidad de PMCTrack. Para recopilar los datos de los contadores de rendimiento de cada hilo es necesario que el módulo sea plenamente consciente de los eventos de planificación que suceden en todo momento, como por ejemplo los cambios de contexto. Además de exponer los datos de los *PMCs* de las aplicaciones a las herramientas del entorno de usuario, el módulo implementa una API sencilla para proporcionar datos de los *PMCs* a cualquier clase de planificación que requiera esa información para su correcto funcionamiento. Debido a que tanto el núcleo del planificador de Linux como las clases de planificación son implementadas en su totalidad en el kernel, para el módulo de PMCTrack del kernel pueda ser consciente de estos eventos y solicitudes es imprescindible la realización de pequeñas modificaciones en el propio kernel Linux. Estas modificaciones, representadas en la figura \ref{fig:arch} con el nombre de "PMCTrack kernel API", consisten en dar la funcionalidad al núcleo del planificador de enviar un conjunto de notificaciones al módulo. Para poder recibir estas notificaciones, el módulo PMCTrack del kernel implementa la siguiente interfaz:

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

Tal y como se ilustra en la figura \ref{fig:arch}, el módulo PMCTrack del kernel consta de varios componentes. La capa del núcleo de PMCTrack independiente de la arquitectura implementa un interfaz llamado \texttt{pmc\_ops\_t} e interactúa con la herramienta PMCTrack de línea de comandos a través del sistema de ficheros */proc* de Linux. El componente independiente de la arquitectura se basa en una Unidad de Monitorización de Rendimiento del Backend (conocida como PMU BE por sus siglas en inglés) para llevar a cabo el acceso de bajo nivel a los *PMCs* y para realizar la traducción de los strings de configuración proporcionados por el usuario en estructuras de datos internas para la plataforma en cuestión. Actualmente existen cuatro backends compatibles con la mayoría de los procesadores modernos de Intel y AMD, así como con algunos modelos de procesador ARM Cortex. Además, se llevó a cabo el desarrollo de un backend compatible con las Intel Xeon Phi de forma simultánea al desarrollo de nuestro TFG. El módulo PMCTrack del kernel también incluye un conjunto de *módulos de monitorización* específicos de la plataforma. El propósito principal de un módulo de monitorización es proporcionar un algoritmo de planificación implementado en el kernel que use métricas de rendimiento de alto nivel.

Dotar al kernel Linux de soporte a PMCTrack implica incluir dos nuevos ficheros en el propio kernel y añadir 18 líneas de código a las fuentes del núcleo del planificador. Estos cambios pueden ser aplicados fácilmente a diferentes versiones del kernel.

## Modos de uso de PMCTrack

Antes de iniciar nuestro desarrollo del TFG, PMCTrack soportaba tres modos de uso: modo de planificación, muestreo basado en tiempo y muestreo basado en eventos.

\begin{figure}[tbp!]
\centering
\selectlanguage{english}
\input{Imagenes/Fuentes/mmon}
\caption{Módulos de monitorización de PMCTrack}
\label{fig:mmon}
\end{figure}

### Modo de planificación

Este modo permite que cualquier algoritmo de planificación en el kernel (es decir, clase de planificación) pueda obtener datos de monitorización de cada hilo, haciendo posible la toma de decisiones en función de estos datos. La activación de este modo en un determinado hilo desde el código del planificador se reduce a la activación del flag \texttt{prof\_enabled} en el descriptor del hilo. (Este flag es añadido a la estructura \texttt{task\_struct} de Linux cuando se aplica el parche del kernel)

Para garantizar que la implementación del algoritmo de planificación que se beneficia de esta característica se mantiene independiente de la arquitectura, el propio planificador (implementado en el kernel) no configura ni se ocupa de los *PMCs* directamente. En lugar de eso, uno de los *módulos de monitorización* se encarga de proporcionar a la clase de planificación las métricas de monitorización de alto nivel necesarias para que pueda llevarse a cabo el algoritmo, como por ejemplo el ratio de instrucciones por ciclo o la tasa de fallos de cache.

Como puede verse en la figura \ref{fig:mmon}, PMCTrack puede incluir varios *módulos de monitorización* compatibles con una plataforma dada. Sin embargo, sólo uno de ellos puede estar habilitado al mismo tiempo: el que proporciona al planificador la información de los *PMCs* para que pueda llevar a cabo su función. En el caso de que haya disponibles varios módulos de monitorización, el administrador del sistema puede indicar al sistema cual de ellos usar, escribiéndolo en el fichero \texttt{/proc/pmc/mmon\_manager}. De manera similar, el período de muestreo de datos de los *PMCs* utilizado en el módulo de monitorización se puede configurar a través del sistema de ficheros */proc*.

El planificador puede comunicarse con el módulo de monitorización activo para obtener datos de monitorización de un hilo a través de la siguiente función de la API de PMCTrack del kernel:

\begin{lstlisting}[backgroundcolor=,basicstyle=\tt\footnotesize]
int pmcs_get_current_metric_value(struct task_struct*
   task, int metric_id, uint64_t* value);
\end{lstlisting}

Por simplicidad, a cada métrica se le asigna un ID numérico, conocido por el planificador y el módulo de monitorización. Para poder obtener datos de métricas actualizados, la función mencionada podrá ser invocada desde la función de tratamiento de señal del planificador.

Los módulos de monitorización hacen posible que una política de planificación que está basada en el uso de contadores de rendimiento pueda ser usada en nuevas arquitecturas o modelos de procesador que aparezcan en un futuro. Todo lo que hay que hacer es construir un módulo de monitorización o adaptar uno existente a la plataforma en cuestión. Desde el punto de vista del programador, la creación de un módulo de monitorización implica la implementación de una interfaz muy similar a \texttt{pmc\_ops\_t}. En concreto, se compone de varias llamadas a funciones que permiten notificar al módulo sobre activaciones y desactivaciones solicitadas por el administrador del sistema, cambios de contexto de hilos, salidas y entradas de un hilo del sistema, solicitudes de valores de métricas de *PMCs* por parte del planificador, etcétera. Sin embargo, el programador normalmente implementa el subconjunto de llamadas a funciones requeridas para llevar a cabo el proceso interno necesario.

La creación de nuevos módulos de monitorización es una tarea bastante sencilla por varias razones. En primer lugar, el programador no necesita acceder directamente a los registros de los *PMCs*. En lugar de ello, el módulo PMCTrack del kernel ofrece una API independiente de la arquitectura que permite al módulo de monitorización especificar la configuración del contador a través de strings, para recibir muestras de *PMCs* periódicamente y controlar la multiplexación de eventos. En segundo lugar, debido a que se le notifica al módulo cuando se crea un nuevo hilo o sale del sistema, el módulo de monitorización puede asignar datos referentes a un hilo concreto para simplificar cualquier tipo de procesamiento de un hilo específico. En tercer lugar, porque el código de un módulo de monitorización "vive" en el módulo PMCTrack del kernel, la solución de la mayoría de los bugs no requieren reiniciar el sistema. En lugar de eso, el módulo del kernel puede descargarse y volverse a cargar una vez se hayan arreglado los errores.

### Muestreo basado en tiempo (TBS)

Esta característica permite al usuario recopilar datos de rendimiento de una aplicación de espacio de usuario a intervalos de tiempo regulares. La herramienta \texttt{pmctrack} de línea de comandos, cuya interfaz de usuario está inspirada en el programa \texttt{cputrack} de Solaris, hace posible esta función. Para ilustrar el funcionamiento de la herramienta consideremos el siguiente ejemplo:

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









# Contadores Hardware para monitorización
 Los contadores hardware para monitorización (o \ac{PMC} por sus siglas en inglés) son registros con contador localizados dentro de los microprocesadores modernos y que cuentan ciertos eventos que ocurren en la CPU.
 Así pues, ejemplos de eventos que se podrían monitorizar de esta manera son: aciertos/fallos en accesos a memoria caché de distintos niveles, fallos en la predicción de saltos, instrucciones en coma flotante ejecutadas, etc.

 Estos contadores pueden ser de dos tipos: fijos, si siempre cuentan los mismos eventos; o configurables, si se puede elegir qué eventos, entre los proveídos por el fabricante, se quiere que el contador cuente.

 El uso de estos contadores es, principalmente, la monitorización del rendimiento del hardware y del software en el procesador en el que se encuentran instalados.
 Hay varias razones por las que puede ser más recomendable o beneficioso el uso de estos contadores en la monitorización del rendimiento de programas en lugar de usar herramientas software.
 Entre otras, la monitorización a través de los PMC permite obtener métricas muy cercanas al hardware; asímismo, la monitorización por software puede ser errónea o poco exacta debido a particularidades tecnológicas del procesador como la ejecución en desorden o las arquitecturas de memoria distribuida.

# Antecedentes: PMCTrack
PMCTrack es una herramienta de línea de comandos integrada en el kernel Linux que permite monitorizar el rendimiento de las aplicaciones haciendo uso de los contadores hardware del procesador.

La herramienta fue desarrollada inicialmente en un proyecto de sistemas informáticos por estudiantes de esta misma facultad en el año 2012 \cite{MSDTFG12}, y su uso y desarrollo se ha mantenido por el Grupo de Arquitectura y Tecnología de Sistemas Informáticos de esta universidad.

Para que la herramienta pueda acceder a la configuración y datos de los contadores hardware, se necesita soporte del núcleo del sistema operativo. Es por eso que se usa una versión del kernel *ad hoc* que contiene las modificaciones necesarias para que esta herramienta funciones.

La herramienta tiene un diseño modular, de modo que por un lado están las modificaciones al código del kernel y por otro el código en modo usuario  que es el que realmente implementa la funcionalidad de la herramienta. De esta manera, se permite independencia de la versión del kernel mientras que se mantiene facilidad para el desarrollo y el mantenimiento.

\begin{figure}[tbp]
\centering
\selectlanguage{english}
\input{Imagenes/Fuentes/architecture}
\selectlanguage{spanish}
\end{figure}

# Otras herramientas para la monitorización mediante contadores hardware
Además de PMCTrack, existen muchas otras herramientas que hacen uso de estos contadores para dar información de rendimiento al usuario.

A continuación destacaremos las más conocidas.

* Perf. Perf viene ya incluido en el kernel de linux dentro del directorio tools/perf. Permite mucha configuración y trazabilidad.
* OProfile. Herramienta instalable en linux. Permite monitorización de una sola aplicación o de todo el sistema.



# Objetivos

# Plan de trabajo
## Etapas de desarrollo del proyecto
1. Planificación
2. Lectura de documentación
3. *Mockups* de la GUI
4. Comienzo implementación *backend* de la GUI
5. Implementación multithreading
6. Implementación frontend de la GUI
7. Implementación libpmctrack y refactorización código pmctrack línea de comandos

## Contribuciones
% Al menos dos páginas de cada uno!

### Abel Serrano Juste

### Jorge Casas
