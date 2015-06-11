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
