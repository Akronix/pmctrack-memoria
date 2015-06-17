\chapter{PMCTrack-GUI}

Para ampliar el potencial de la herramienta PMCTrack, en lo que respecta a la monitorización de aplicaciones desde modo usuario, hemos desarrollado PMCTrack-GUI. Esta aplicación permite la visualización de gráficas de rendimiento en tiempo real de programas de usuario, usando por debajo la herramienta de línea de comandos \texttt{pmctrack} para obtener los datos de monitorización proporcionados por el módulo del kernel.

Este capítulo se estructura como sigue. En la sección \ref{sec:motivacion} se justifica la necesidad del desarrollo de PMCTrack-GUI. La sección \ref{sec:caracteristicas} presenta las características principales de la aplicación PMCTrack-GUI y se realiza una breve comparativa de ésta con otras aplicaciones gráficas disponibles en el mercado. La sección \ref{sec:uso} describe detalladamente cómo se usa la aplicación. Finalmente, la sección \ref{sec:diseno} explica detalles del diseño de la aplicación, las tecnologías usadas y sus principales componentes internos.

# Motivación
\label{sec:motivacion}

Como se mencionó en el Capítulo 1, a pesar del gran potencial de la herramienta PMCTrack, ésta cuenta con limitaciones al ser usada para monitorizar aplicaciones desde el espacio de usuario. El principal problema consiste en que la herramienta \texttt{pmctrack} de línea de comandos proporciona tanta información al usuario a través de los PMCs que éste no puede interpretar toda esa cantidad de información, siendo necesario procesarla a posteriori.

Además, tal y como se explicó en el Capítulo 1 de esta memoria, el usuario no puede proporcionar al comando \texttt{pmctrack} el nombre del evento que desea contabilizar en un PMC ("Instrucciones retiradas" por ejemplo). En lugar de ello, debe proporcionar los códigos hexadecimales que se correspondan con el evento en cuestión, siendo estos códigos diferentes según la arquitectura y el modelo de procesador que estemos usando. Esto obliga al usuario a utilizar un manual de la arquitectura que esté usando para buscar los códigos hexadecimales del evento que quiera contabilizar.

Para solucionar estos dos problemas, es necesario el desarrollo de un _frontend_ gráfico que facilite al usuario la tarea de monitorización de aplicaciones usando PMCs.

# Ventajas y características
\label{sec:caracteristicas}

PMCTrack-GUI ha sido desarrollado para superar las limitaciones comentadas en la sección anterior, pero el resultado final es una herramienta que no sólo supera estas limitaciones sino que ofrece características que no soportan otras aplicaciones alternativas disponibles en el mercado.

A la fecha de escritura de estas líneas, PMCTrack-GUI es la única aplicación que permite visualizar gráficas de rendimiento de aplicaciones en tiempo real en múltiples arquitecturas usando PMCs. Actualmente distintos fabricantes de microprocesadores como Intel y ARM proporcionan herramientas gráficas compatibles únicamente con sus modelos de procesador. Ejemplos destacados de estas herramientas, son el *Intel Performance Counter Monitor* \cite{Intel} y el *Streamline Performance Analyzer* de ARM \cite{ARM}.

PMCTrack-GUI, por el contrario, no solo ofrece soporte multiarquitectura sino que abstrae completamente al usuario de la arquitectura que esté utilizando. Esencialmente la aplicación proporciona de forma visual y totalmente automática la lista de PMCs disponibles y permite configurarlos haciendo clic en el evento que se desea asociar con cada contador hardware. PMCTrack-GUI se encargará internamente de obtener los códigos hexadecimales asociados a los eventos y a la arquitectura en cuestión. No obstante, la aplicación cuenta con una configuración avanzada en la que se permite al usuario asignar eventos a contadores proporcionando los códigos hexadecimales asociados. Cabe destacar que PMCTrack-GUI también soporta la monitorización de aplicaciones multihilo, de forma que es posible visualizar gráficas en tiempo real de un determinado hilo de la aplicación que se esté monitorizando.

Para especificar las métricas de alto nivel que serán visualizadas posteriormente en gráficas en tiempo real, el usuario tan sólo debe escribir fórmulas de alto nivel en las cuales las variables serán los nombres de los contadores configurados previamente (_pmc0_, _pmc1_, _pmc2_, ...). Por ejemplo si el contador 0 lleva la cuenta del número de instrucciones retiradas y el contador 3 contabiliza el número de fallos de último nivel de caché (LLC), la fórmula $(pmc3 * 1000) / pmc0$ define la métrica de rendimento "_Número de fallos de LLC por cada 1K instrucciones_".

El código fuente de PMCTrack-GUI será liberado en los próximos meses con licencia GPL, junto con el resto del código de la herramienta PMCTrack, estando disponible para todo el mundo de forma gratuita. Esto proporciona otra ventaja sobre la mayoría de aplicaciones alternativas, ya que estas no suelen ser libres y sus licencias de uso suelen ser de un alto coste económico.

Aunque ya se han comentado las principales características con las que cuenta PMCTrack-GUI, a continuación destacamos otras características relevantes:

* Permite la monitorización de máquinas remotas accesibles por SSH, desacoplando la GUI de la propia monitorización.
* Permite observar simultáneamente y en tiempo real dos o más gráficas de métricas de rendimiento, para el mismo o distintos hilos de ejecución de la aplicación monitorizada.
* Permite parar/reanudar la ejecución de la aplicación que se está monitorizando.
* Permite realizar una nueva configuración a partir de otra anterior cuya monitorización se está llevando a cabo.
* Permite personalizar el aspecto visual de las gráficas.
* Permite realizar capturas de las gráficas.

# Modo de uso
\label{sec:uso}

Al ejecutar PMCTrack-GUI se inicia con el idioma que se encuentre configurado en el sistema operativo de la máquina que lo arranca. Actualmente se proporciona la traducción para los idiomas español e inglés únicamente, de modo que la aplicación se visualizará en español si la sesión del usuario del SO está configurada en español, o inglés en otro caso. No obstante, incluir soporte para otros idiomas no requeriría modificar el código fuente de PMCTrack-GUI sino que simplemente se ha de proporcionar un fichero, con formato reconocible por _gettext_, con la traducción para el idioma en cuestión.

En primer lugar, el usuario debe seleccionar la máquina que desea monitorizar, pudiéndose elegir la máquina donde se está ejecutando PMCTrack-GUI u otra máquina remota accesible por SSH. En cualquiera de los casos PMCTrack-GUI hará un chequeo para comprobar que está instalado el software necesario tanto en la máquina a monitorizar como en la máquina donde se está ejecutando la GUI. En caso de que falte algún componente software requerido se informará debidamente al usuario.

Si todas las dependencias software están resueltas y se establece correctamente la conexión con la máquina remota (si fuera necesario), se mostrará una nueva ventana donde el usuario podrá configurar los PMCs con los que cuenta la máquina a monitorizar, asignando eventos a dichos contadores. La figura \ref{fig:countersConf}(a) muestra una captura de dicha ventana. Para realizar la asignación de eventos, el usuario sólo tiene que hacer clic en el botón "Asignar evento" del contador que quiera configurar, y a continuación, hacer clic en el evento y subevento(s) que quiera asignar de entre todo el listado de eventos y subeventos disponibles que se mostrarán por pantalla. Adicionalmente, se le da la posiblidad a los usuarios avanzados de asignar eventos al contador proporcionando los códigos hexadecimales correspondientes a los eventos en cuestión, a través del cuadro de "Opciones avanzadas". En la imagen de la figura \ref{fig:countersConf}(b)  se puede visualizar una ventana de configuración de un contador.

\begin{figure}
\centering
\subfloat[]{\includegraphics[scale=0.23]{Imagenes/Bitmap/screenshotCountersConfMac}}\vspace{10mm}
\subfloat[]{\includegraphics[scale=0.23]{Imagenes/Bitmap/screenshotCounterConf}}
\caption{Ventanas de configuración de contadores y métricas} \label{fig:countersConf}
\end{figure}

Una vez configurados los contadores que se quieren utilizar, debajo del cuadro de configuración de contadores el usuario se encontrará con la configuración de métricas. Este cuadro permite al usuario configurar métricas de alto nivel que podrán verse posteriormente en forma de gráfica en tiempo real. Para la generación de métricas se usan fórmulas cuyas variables son los contadores que el usuario configuró anteriormente (_pmc0_, _pmc1_, \ldots). No hay ninguna limitación a la hora de generar las fórmulas, de tal manera que el usuario podrá escribir fórmulas tan complejas como desee, como por ejemplo $((pmc0 \textasciicircum{} 2) / pmc1 * 1000) * pmc4$. En la figura \ref{fig:countersConf}(a) se puede observar la ventana de configuración de contadores y métricas donde hay añadidos otros ejemplos de fórmulas.

Cabe destacar que es posible crear más de un experimento, esto es, más de un conjunto de contadores y métricas. De este modo, es posible configurar un contador con un determinado evento y usarlo en una métrica y, en otro experimento, configurar el mismo contador con otro evento distinto y usarlo en otra métrica distinta.

\begin{figure}
\centering
\subfloat[]{\includegraphics[scale=0.23]{Imagenes/Bitmap/screenshotFinalConf}}\vspace{10mm}
\subfloat[]{\includegraphics[scale=0.23]{Imagenes/Bitmap/screenshotStyleGraphConf}}
\caption{Fase final de la configuración} \label{fig:finalConf}
\end{figure}

Cuando el usuario haya terminado de configurar todos los experimentos que quiera y haya hecho clic en el botón "Siguiente" aparecerá una nueva ventana, en esta ventana se realizan las últimas configuraciones antes de iniciar la monitorización. Permite elegir la aplicación que se desea monitorizar, el tiempo entre cada muestra y la ruta del archivo donde guardar los resultados del comando PMCTrack generado (si es que el usuario quiere guardarlo). Adicionalmente, en esta ventana también se da la posibilidad al usuario de personalizar el aspecto visual de las gráficas que serán visualizadas posteriormente, pudiéndose elegir un modo ya configurado (modo por defecto, modo de contraste, modo hacker, modo aqua\ldots) o personalizar uno. En la figura \ref{fig:finalConf} se puede ver de forma gráfica lo comentado en este párrafo.

Una vez esté todo configurado y el usuario esté listo para iniciar la monitorización, hará clic en el botón "Iniciar monitorización" de la última ventana de configuración. Al hacer clic se abrirá una nueva ventana donde se visualizará la gráfica en tiempo real de la primera métrica del primer experimento configurado. En el caso de que la aplicación a monitorizar fuera multihilo se mostrará la gráfica del hilo _main_. En cualquier momento podemos realizar las siguientes acciones:

* *Mostrar otra gráfica distinta.* Seleccionando el experimento, métrica de ese experimento y PID del hilo (en el caso de que la aplicación sea multihilo). El usuario podrá elegir entre mostrar la gráfica en la ventana actual o en una nueva ventana independiente, esto proporciona una gran flexibilidad al poder visualizar simultáneamente tantas gráficas como desee el usuario.

* *Mostrar gráfica acumulada o parcial.* Por defecto el usuario visualiza la última parte de la gráfica, es decir, la parte actual de la monitorización. Sin embargo, es posible cambiar el modo de la gráfica a gráfica acumulada, visualizando la gráfica desde que se inició la monitorización.

* *Hacer captura de la gráfica actual.* El usuario puede hacer en cualquier momento de la monitorización una captura de una gráfica tal y como se está visualizando en ese instante, guardándola con formato de imagen PNG.

* *Ocultar controles.* Para ver una gráfica lo mejor posible se le da la posibilidad al usuario de ocultar todos los controles de la ventana, de esta manera la gráfica ocupa todo el espacio de la ventana.

* *Parar/reanudar la aplicación.* El usuario puede parar la ejecución de la aplicación que se está monitorizando cuando lo desee, pudiéndola reanudar posteriormente. Esto puede servir para realizar capturas de gráficas en un punto escogido de la ejecución con más precisión.

En la figura \ref{fig:monitoring} se puede ver un ejemplo gráfico de lo explicado anteriormente.

\begin{figure}
\centering
\includegraphics[scale=0.27]{Imagenes/Bitmap/screenshotMonitoring}
\caption{Monitorización de una aplicación de usuario en la que se están visualizando simultáneamente en tiempo real dos métricas} \label{fig:monitoring}
\end{figure}

Cabe destacar que mientras se está realizando la monitorización, el usuario puede seguir desplazándose por las ventanas de configuración para preparar una nueva monitorización a partir de la ya existente. No hay ninguna restricción a la hora de cambiar parámetros de configuración, se permite incluso establecer otra máquina distinta accesible por SSH donde llevar a cabo la monitorización, y en ningún momento estos cambios afectarán a la monitorización que se está llevando a cabo. Cuando el usuario tenga lista la nueva configuración, hará clic en el botón "Cancelar monitorización", en el caso de que se esté llevando a cabo una monitorización, para matar el proceso de monitorización en la máquina en cuestión. Al hacerlo, se cerrarán todas las ventanas de monitorización, y el botón pasará a llamarse "Iniciar monitorización". Al volver a hacer a clic sobre ese botón se pondrá en marcha la nueva monitorización.

Cuando la aplicación que se está monitorizando termina, se le notifica al usuario mediante un cuadro de diálogo, pero en ningún caso se cierran las ventanas de monitorización. De este modo, el usuario puede seguir realizando las acciones que hemos visto anteriormente.

# Diseño y detalles de implementación
\label{sec:diseno}

La aplicación PMCTrack-GUI ha sido implementada en Python, eligiéndose este lenguaje principalmente por dos motivos. En primer lugar,  por ser multiplataforma, de tal manera que su código puede ser ejecutado en cualquier sistema que soporte la instalación de un intérprete de Python. En segundo lugar, porque cuenta con una librería que permite la generación de gráficos de alta calidad y precisión a partir de datos contenidos en listas o arrays, la denominada librería *matplotlib*. El proceso de generación de gráficas con esta librería consume pocos recursos. Hemos observado que aún realizando la monitorización de una aplicación en la misma máquina que ejecuta la GUI, los resultados de monitorización apenas se ven afectados por la propia ejecución de PMCTrack-GUI para intervalos de muestreo moderados.

Para el desarrollo de las ventanas y diálogos con los que interactúa el usuario se ha utilizado la librería *wxPython*, un _wrapper_ de Python de la librería _wxWidgets_ escrita en C++. Al igual que Python, esta librería es multiplataforma, y adicionalmente, permite incluir dentro de las ventanas gráficos generados con la librería *matplotlib* antes mencionada. Gracias a que tanto la librería *wxPython* como el propio Python son multiplataforma, PMCTrack-GUI también lo es. No obstante, a pesar de que teóricamente PMCTrack-GUI puede ejecutarse en cualquier sistema con un intérprete de Python, por motivos de implementación internos\footnote{Esencialmente, el modo de monitorización por SSH de PMCTrack-GUI se basa en el uso de comandos que no están disponibles actualmente en Microsoft Windows.} la aplicación sólo es completamente funcional en GNU/Linux y Mac OS X. En la figura \ref{fig:sistema de ventanas} se puede observar una vista de la aplicación en las dos plataformas soportadas.

PMCTrack-GUI ha sido diseñada para ser fácilmente extensible y mantenible. La justificación de esta afirmación es que, puesto que PMCTrack es una herramienta en continuo desarrollo, se ha dado soporte a PMCTrack-GUI para el uso de nuevas funcionalidades de la herramienta PMCTrack que fueron añadidas por desarrolladores externos simultáneamente al desarrollo de nuestro proyecto. Un ejemplo de esto es el soporte al muestreo basado en eventos (EBS) de la herramienta \texttt{pmctrack} de línea de comandos. Además, se ha otorgado a PMCTrack-GUI funcionalidades que no estaban inicialmente previstas, pero que dado el gran potencial que podían ofrecer a la aplicación, se decidieron incluir. Un ejemplo de ello es la posiblidad de monitorizar máquinas remotas accesibles por SSH.

En las siguientes secciones de este capítulo analizaremos los principales componentes internos con los que cuenta PMCTrack-GUI para proveer al sistema de ventanas de la aplicación los datos necesarios para poder llevar a cabo sus funciones.

\begin{figure}
\centering
\subfloat[Interfaz GNOME]{\includegraphics[scale=0.23]{Imagenes/Bitmap/screenshotCountersConfGnome}}\vspace{10mm}
\subfloat[GUI nativa de MacOS X]{\includegraphics[scale=0.23]{Imagenes/Bitmap/screenshotCountersConfMac}}
\caption{PMCTrack-GUI ejecutándose en GNU/Linux y MacOS X} \label{fig:sistema de ventanas}
\end{figure}

## Objetos de procesamiento

Esta parte consta de información sobre la máquina y los eventos hardware que puede monitorizar, así como de las clases Python que permiten su procesado y le facilitan dicha información al *sistema de ventanas* de la aplicación. Para desacoplar esta parte del resto de la aplicación, la información es servida al sistema de ventanas usando el \glosstex{patrón de diseño} *Fachada*, implementado en la clase `FacadeXML`. En el apéndice \ref{app:UML.XML} se puede encontrar un diagrama \ac{UML} completo del diseño que corresponde a toda esta parte.

Para obtener la información servida por la fachada, en primer lugar, el sistema de ventanas necesitará construir un objeto fachada y a través de ese objeto podrá obtener la información que quiera haciendo uso de las funciones que dicho objeto provee. La fachada es suficientemente inteligente para obtener la información del modelo que se está usando automáticamente y devolver sus eventos, sin que el sistema de ventanas tenga que especificar el modelo, si bien éste podría ser especificado si así se desease. Además, la fachada también detectará si estamos en una arquitectura asimétrica o heterogénea \cite{single-isa-perf} en la cual las \ac{CPUs} que podemos tener pueden disponer de eventos diferentes y también precisar de configuraciones diferentes.

Muchas veces, los valores de retorno serán objetos Python que encapsulan todos los datos necesarios. Por ejemplo, la fachada provee de la función `getAvailableEvents` que devuelve una lista de objetos `Event` los cuales contienen todos los campos para describir a un evento y ser usado desde la parte gráfica: nombre, descripción, código, flags y subeventos.

Internamente, cuando se le solicita información a la fachada, ésta crea las estructuras de datos necesarias, procesa los argumentos, hace diversas llamadas a las funciones necesarias para obtener la información deseada y devuelve la información procesada como valores de retorno. En particular, disponemos de una clase `Parser` que es la encargada de tratar con los archivos \ac{XML}, siguiendo su formato de entrada bien definido por los ficheros \ac{DTD} (*Document Type Definition*). En la figura \ref{fig:objproc} se muestra un pequeño esquema que ilustra el flujo de acceso a los objetos de procesamiento.

\begin{figure}
\centering
\caption{Flujo de acceso a cada uno de los objetos de procesamiento}
\label{fig:objproc}
\begin{center}
\includegraphics[scale=0.8]{Imagenes/Vectorial/parser-diagram.pdf}
\end{center}
\end{figure}

Los objetos de procesamiento se pueden dividir según su formato, en dos grupos: XML y texto plano.

1. XML: Dependientes de cada modelo de \ac{CPU}, contienen la información de eventos e información de ese modelo de máquina en particular necesaria para la \ac{GUI},

2. Texto plano: tienen información más general de la máquina, proveída por el kernel Linux.

En los siguientes apartados, profundizaremos más detalladamente sobre qué información contienen y cómo están estructurados cada uno de estos elementos.

### XML
Los ficheros XML son archivos escritos con la información organizada por etiquetas y permiten el almacenaje y procesado de la información de una manera sencilla y rápida. Además, son fáciles de leer y de editar manualmente. Por estas razones, hemos escogido almacenar toda la información sobre los eventos y los PMCs que necesitábamos para la interfaz en este formato.\newline
Para mantener una definición formal del formato de XML que queremos leer como entrada y así también poder verificar que los datos del fichero XML son sintácticamente correctos, hemos creado un fichero \ac{DTD} para cada tipo de XML que queremos usar.\newline

En particular, los tipos de fichero XML que necesitamos son dos:

1. `{nombre_fabricante}_layout.xml`: Este fichero suele ser común a todos los modelos de un mismo fabricante y sirve para definir los campos configurables de cada contador y sus valores por defecto. Su definición se puede ver en el dtd de la figura \ref{fig:dtdlayout}.

2. `{nombre_modelo}.xml`: Este fichero contiene información relativa a los eventos, subeventos y contadores fijos de un modelo en particular. Aunque modelos del mismo fabricante tienen algunos eventos en común, sucede que muchos eventos cambian de modelo en modelo o de contadores fijos, de modo que se debe tener un fichero XML por cada modelo de \ac{CPU} que queramos soportar en la interfaz gráfica. Su definición se puede ver en el DTD de la figura \ref{fig:dtdevents}.

Estos ficheros XML han sido generados de dos maneras diferentes. Los de tipo layout para cada fabricante y para algunos de los eventos de cada modelo han sido escritos manualmente. Para otros modelos de procesador, sobre los que el grupo \ac{ArTeCS} estaba investigando con la herramienta PMCTrack, ya existían unos ficheros \ac{CSV} que describían los eventos y PMCs de esos modelos. Para reutilizar estos ficheros, escribimos un script Bash que genera automáticamente los XML equivalentes a esos ficheros CSV dados.

\begin{figure}
\caption{Fichero de definición DTD para los ficheros XML que definen el layout de los PMCs}
\label{fig:dtdlayout}
\begin{lstlisting}[language=XML,deletekeywords={version,default},frame=single]
<!ELEMENT layout (field*)>
<!ATTLIST layout
vendor (intel|amd|arm|undefined) #IMPLIED
family CDATA #IMPLIED
version CDATA #IMPLIED>

<!ELEMENT field (name,nbits,default)>
<!ELEMENT name (#PCDATA)>
<!ELEMENT nbits (#PCDATA)>
<!ELEMENT default (#PCDATA)>
\end{lstlisting}

\end{figure}

\begin{figure}
\caption{Fichero de definición DTD para los ficheros XML que definen los contadores fijos y los eventos de cada modelo}
\label{fig:dtdevents}
\begin{lstlisting}[language=XML,deletekeywords={version,default},frame=single]
<!ELEMENT pmcs_and_events (pmcs?,events)>

<!ELEMENT pmcs (pmc*)>
<!ELEMENT pmc (pmc_name,pmc_type,pmc_number)>
<!ELEMENT pmc_name (#PCDATA)>
<!ELEMENT pmc_type (#PCDATA)>
<!ELEMENT pmc_number (#PCDATA)>

<!ELEMENT events (event+)>
<!ELEMENT event (name,descp?,code,flags?,subevents?)>
<!ELEMENT name (#PCDATA)>
<!ELEMENT code (#PCDATA)>
<!ELEMENT descp (#PCDATA)>
<!ELEMENT flags (flag*)>
<!ELEMENT subevents (subevent+)>

<!ELEMENT subevent (subevt_name,subevt_descp?,flags)>
<!ELEMENT subevt_name (#PCDATA)>
<!ELEMENT subevt_descp (#PCDATA)>

<!ELEMENT flag (flag_name,flag_value)>
<!ELEMENT flag_name (#PCDATA)>
<!ELEMENT flag_value (#PCDATA)>
\end{lstlisting}

\end{figure}

### Texto plano
Además de los ficheros XML, existen dos ficheros de texto plano que resultan relevantes para nuestra interfaz y que son procesados por esta parte de ella. Procedemos a explicarlos brevemente a continuación:

* `/proc/pmc/info`: De este fichero se obtiene información relativa al número de contadores que ofrece la máquina, el nombre del modelo (o nombres de los modelos si se tratase de una arquitectura heterogénea) y alguna otra información que pudiera se necesaria en un futuro. Este fichero es proveído por el módulo común a todas las arquitecturas del kernel de PMCTrack.

* `/proc/cpuinfo`: De este fichero se obtiene el número de *cores* que hay en la máquina que se quiere monitorizar. Este fichero está disponible en cualquier versión del kernel Linux.

## Objetos de configuración de usuario

Es un conjunto de objetos que almacenan toda la configuración del usuario. Son enviados de un _frame_ de configuración a otro y cada uno de estos frames se encarga de almacenar en estos objetos la parte de configuración que le corresponde.

Cuando toda la configuración de usuario está almacenada, estos objetos son procesados por el componente *PMCExtract* que comentaremos en una sección posterior.

En el apéndice \ref{app:UML.UserConfig} se puede encontrar un diagrama \ac{UML} de este conjunto de objetos.

## El componente PMCConnect

Es un objeto que, dada una configuración de conexión a una máquina (encapsulada en un objeto de configuración de usuario), provee métodos para obtener todo tipo de información de esa máquina. Permite comprobar si es posible establecer una conexión con la máquina a través de SSH, comprobar la existencia de un fichero, leer el contenido de ficheros y determinar si la máquina tiene un determinado paquete instalado.

Este objeto es usado por el sistema de ventanas para chequear las dependencias software tanto en la máquina donde se está ejecutando PMCTrack-GUI como en la máquina donde se llevará a cabo la monitorización.

Además, es usado por los *Objetos de procesamiento* para leer los archivos en texto plano.

Usando este objeto conseguimos una total independencia entre el resto de componentes de PMCTrack-GUI y la máquina donde se desea llevar a cabo la monitorización. Ni los *Objetos de procesamiento* ni el sistema de ventanas conocen la máquina en sí donde se va a llevar a cabo la monitorización. Gracias a esto, no hay que hacer distinciones en estos objetos dependiendo de si se realiza la monitorización en una máquina remota o en la propia máquina en la cual se está ejecutando PMCTrack-GUI. En vez de ello, cada vez que haya que obtener datos de la máquina, los componentes que requieran esos datos usarán este objeto.

## El componente PMCExtract

*PMCExtract* es el objeto encargado de llevar a cabo la comunicación con la herramienta \texttt{pmctrack} de línea de comandos.

En su inicialización, procesa los objetos de configuración del usuario generando el comando \texttt{pmctrack} que lanza en la máquina que se haya configurado para monitorizar. Adicionalmente, crea un hilo encargado de extraer toda la información proveniente del comando \texttt{pmctrack}, guardándola de forma organizada en un diccionario de datos a medida que el comando \texttt{pmctrack} va generando nuevas muestras. Este diccionario de datos será utilizado por el sistema de ventanas para generar las gráficas en tiempo real. Si durante la obtención de muestras el comando \texttt{pmctrack} genera un error, el componente *PMCExtract* lo capturará y almacenará, de tal manera que el sistema de ventanas podrá recibir ese error y mostrárselo al usuario mediante un cuadro de diálogo.

*PMCExtract* cuenta con atributos a los que puede acceder el sistema de ventanas para saber en cualquier momento el estado de la aplicación que se está monitorizando, así como métodos que permiten enviar señales a dicha aplicación (señal de parada *SIGSTOP*, señal de reanudación *SIGCONT* y señal de matar proceso *SIGKILL*).
