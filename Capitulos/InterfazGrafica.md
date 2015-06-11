\chapter{PMCTrack GUI: Algo más que un interfaz gráfico}
# Motivación
$PMCTrack$ es una herramienta muy potente desarrollada principalmente para ayudar al *planificador* del sistema operativo, por lo que aunque da soporte para ser usada por un usuario final, tiene grandes limitaciones en este sentido.

En primer lugar, proporciona al usuario el valor de cada contador configurado en determinados instantes de tiempo, por lo que para que el usuario pueda interpretar esos datos es necesario que realice de forma "manual" gráficas con herramientas como $Gnuplot$, teniéndolas que generar una vez PMCTrack ha terminado de extraer toda la información de los contadores.

Además, para la asignación de eventos a contadores es necesario para el usuario el uso de un manual de la arquitectura de la máquina, ya que deberá buscar el evento que desea contabilizar en un contador e indicar al comando PMCTrack los valores de configuración para los contadores.

# PMCTrack GUI, una herramienta única

Como ya hemos visto, PMCTrack posee limitaciones importantes al usarse por un usuario final. Estas limitaciones han sido nuestra motivación para desarrollar PMCTrack GUI, y el resultado final es una herramienta que no sólo supera estas limitaciones si no que supera grandes limitaciones de las aplicaciones alternativas disponibles en el mercado.

A día de hoy no hay otra herramienta en el mercado como PMCTrack GUI, ya que actualmente es la única aplicación que permite visualizar la monitorización de benchmarks siendo multiarquitectura. En el mercado sólo están disponibles las herramientas de monitorización de cada fabricante, como el *Intel Performance Counter Monitor* de \cite{Intel} o el *Streamline Performance Analyzer* de \cite{ARM}.

Además, PMCTrack GUI es de código libre y completamente gratuita, mientras que las aplicaciones alternativas disponibles en el mercado no son libres y las licencias de uso son de un alto coste económico.

# Características de PMCTrack GUI

* Visualización de gráficas de monitorización en tiempo real.
* Multiarquitectura, pudiendo monitorizar benchmarks en máquinas Intel, AMD y ARM.
* Multiplataforma, pudiéndose ejecutar en GNU/Linux y MacOS X.
* Selección de eventos sin necesidad de usar ningún manual de arquitectura (aunque se puede usar para especificar opciones avanzadas)
* Asignación amigable de eventos a los contadores hardware.
* Generación sencilla de métricas a partir de fórmulas de alto nivel.
* Posibilidad de monitorización de máquinas remotas, desacoplando la GUI de la propia monitorización.
* Detección de las dependencias software no satisfechas.
* Detección automática de la arquitectura de la máquina a monitorizar, cargando los contadores y eventos propios de dicha arquitectura.
* Permite observar simultáneamente y en tiempo real 2 o más gráficas.
* Soporta la monitorización de aplicaciones multihilo, pudiendo observar gráficas propias de un hilo concreto de la aplicación.
* Permite parar y reanudar la ejecución del benchmark que se está monitorizando.
* Permite realizar una nueva configuración a partir de otra anterior cuya monitorización se está llevando a cabo.
* Permite personalizar las gráficas a gusto del usuario.
* Permite realizar capturas de las gráficas.
* Permite redimensionar las gráficas en tiempo real.
* Ajuste automático de los ejes de las gráficas en función de los valores y del tamaño de la ventana.
* Multilenguaje, soportando actualmente los idiomas inglés y español.

# Diseño de PMCTrack GUI

PMCTrack GUI ha sido desarrollada en *Python*, eligiéndose este lenguaje principalmente por ser multiplataforma, pudiendo ser ejecutado en cualquier sistema que soporte la instalación de un intérprete de Python, además de que cuenta con una biblioteca muy potente para la generación de gráficas a partir de datos contenidos en listas o arrays, la biblioteca *Matplotlib*. Esta biblioteca es la que ha permitido en gran parte que PMCTrack GUI cuente con un indudable atractivo visual.

Ha sido diseñada para ser fácilmente escalable y mantenible. Consta de diversos componentes que podemos dividir en dos grandes grupos según la función que desempeñan: *Frontend* y *Backend*. El Frontend comprende todos los componentes puramente gráficos de la aplicación para su interacción con el usuario; el Backend consta de todos los componentes que proveen de la información para ser mostrada en el Frontend. Los componentes del Backend son muy diferentes entre sí, proveyendo cada uno de ellos información muy diferente, por ello analizaremos cada uno de ellos por separado.

## Frontend

Está compuesto por todos los componentes eminentemente gráficos de la aplicación.

Para el desarrollo de los frames y diálogos se ha utilizado la biblioteca *WX* de Python. El desarrollo se inició sobre la versión 2.8 aunque hoy en día la aplicación también es compatible con la última versión, la 3.0, esto ha hecho posible que PMCTrack GUI pueda ser ejecutada sobre la interfaz gráfica nativa de $MacOS X$.

Para la generación de gráficas se ha usado la biblioteca *Matplotlib*, que como ya se ha comentado antes, permite la generación de gráficos de alta calidad y precisión a partir de datos contenidos en listas o arrays, todo esto consumiendo pocos recursos y utilizando una notación muy parecida a la de $MATLAB$.

En la figura \ref{fig:frontend} puede observar una vista del frontend en las dos plataformas soportadas por PMCTrack GUI.

\begin{figure}
\centering
\subfloat[Interfaz GNOME]{\includegraphics[scale=0.23]{Imagenes/Bitmap/screenshotCountersConfGnome}}\vspace{10mm}
\subfloat[GUI nativa de MacOS X]{\includegraphics[scale=0.23]{Imagenes/Bitmap/screenshotCountersConfMac}}
\caption{PMCTrack GUI ejecutándose en GNU/Linux y MacOS X} \label{fig:frontend}
\end{figure}

## Backend - Objetos de procesamiento

Esta parte consta de información sobre la máquina y los eventos hardware que puede monitorizar, así como de las clases Python que permiten su procesado y le facilitan dicha información al *frontend* de la aplicación. Para desacoplar esta parte del resto de la aplicación, la información es servida al frontend usando el \glosstex{patrón de diseño} *Fachada*, implementado en la clase `FacadeXML`. En el apéndice \ref{app:UML.XML} se puede encontrar un diagrama \ac{UML} completo del diseño que corresponde a toda esta parte.

Para obtener la información servida por la fachada, en primer lugar, el frontend necesitará construir un objeto fachada y a través de ese objeto podrá obtener la información que quiera haciendo uso de las funciones que dicho objeto provee. La fachada es suficientemente inteligente para obtener la información del modelo que se está usando automáticamente y devolver sus eventos, sin que el frontend tenga que especificar el modelo, si bien éste podría ser especificado si así se desease. Además, la fachada también detectará si estamos en una arquitectura asimétrica o heterogénea \cite{single-isa-perf} en la cual las \ac{CPU} que podemos tener pueden disponer de eventos diferentes y también necesitar de configuraciones diferentes.

Muchas veces, los valores de retorno serán objetos Python que encapsulan todos los datos necesarios. Por ejemplo, la fachada provee de la función `getAvailableEvents` que devuelve una lista de objetos `Event` los cuales contienen todos los campos para describir a un evento y ser usado desde la parte gráfica: nombre, descripción, código, flags y subeventos.

Internamente, cuando se le solicita información a la fachada, ésta crea las estructuras de datos necesarias, procesa los argumentos, hace diversas llamadas a las funciones necesarias para obtener la información deseada y devuelve la información procesada como valores de retorno. En particular, disponemos de una clase Parser que es la encargada de tratar con los archivos \ac{XML}, siguiendo su formato de entrada bien definido por los ficheros \ac{DTD} (*Document Type Definition*). En la figura \ref{fig:objproc} se muestra un pequeño esquema que ilustra el flujo de acceso a los objetos de procesamiento.

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
Los ficheros xml son archivos escritos con la información organizada por etiquetas y permiten el almacenaje y procesado de la información de una manera sencilla y rápida. Además, son fáciles de leer y de editar manualmente. Por estas razones, hemos escogido almacenar toda la información sobre los eventos y los \ac{PMC} que necesitábamos para la interfaz en este formato.\newline
Para mantener una definición formal del formato de XML que queremos leer como entrada y así también poder verificar que los datos del fichero XML son sintácticamente correctos, hemos creado un fichero \ac{DTD} para cada tipo de XML que queremos usar.\newline

En particular, los tipos de fichero XML que necesitamos son dos:

1. {nombre_fabricante}\_layout.xml: Este fichero suele ser común a todos los modelos de un mismo fabricante y sirve para definir los campos configurables de cada contador y sus valores por defecto. Su definición se puede ver en el dtd de la figura \ref{fig:dtdlayout}.

2. {nombre_modelo}.xml: Este fichero contiene información relativa a los eventos, subeventos y contadores fijos de un modelo en particular. Aunque modelos del mismo fabricante tienen algunos eventos en común, sucede que muchos eventos cambian de modelo en modelo o de contadores fijos, de modo que se debe tener un xml por cada modelo de \ac{CPU} que queramos soportar en la interfaz gráfica. Su definición se puede ver en el dtd de la figura \ref{fig:dtdevents}.

\lstset{
  language=XML,
  deletekeywords={version,default}
}

\begin{figure}
\caption{Fichero de definición DTD para los ficheros XML que definen el layout de los PMC}
\label{fig:dtdlayout}
\begin{lstlisting}[frame=single]
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
\begin{lstlisting}[frame=single]
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
Además de los ficheros XML, existen dos ficheros proveídos por el kernel modificado para PMCTrack que resultan relevantes para nuestra interfaz y que son procesados por esta parte de ella. Procedemos a explicarlos brevemente a continuación:

* `/proc/pmc/info`: De este fichero se obtiene información relativa al número de contadores que ofrece la máquina, el nombre del modelo (o nombres de los modelos si se tratase de una arquitectura heterogénea) y alguna otra información que pudiera se necesaria en un futuro. Este fichero es proveído por el módulo común a todas las arquitecturas del kernel de PMCTrack.

* `/proc/cpuinfo`: De este fichero se obtiene el número de *cores* que hay en la máquina que se quiere monitorizar. Este fichero está disponible en cualquier versión del kernel Linux.

## Backend - PMC Connect

Es un objeto que, dada una configuración de conexión a una máquina, provee métodos para obtener todo tipo de información de esa máquina. Permite comprobar la conectividad con esa máquina, comprobar la existencia de un fichero, leer contenido de ficheros y determinar si la máquina tiene un determinado paquete instalado.

Este objeto es usado por el frontend para chequear las dependencias software tanto en la máquina donde se está ejecutando la GUI como en la máquina donde se llevará a cabo la monitorización.

Además, es usado por los *Objetos de procesamiento* para leer los archivos en texto plano. Usando este objeto conseguimos una total independencia entre los *Objetos de procesamiento* y la máquina donde se desea llevar a cabo la monitorización, no teniendo por tanto que hacer distinciones en estos objetos dependiendo de si se desea realizar la monitorización en una máquina remota o en la propia máquina en la cual se está ejecutando PMCTrack GUI.

## Backend - User Config

Es un conjunto de objetos que almacenan toda la configuración del usuario. Son enviados de un frame de configuración a otro y cada uno de estos frames se encarga de almacenar en estos objetos la parte de configuración que le corresponde.

En el apéndice \ref{app:UML.UserConfig} podrá encontrar un diagrama \ac{UML} de este conjunto de objetos.

## Backend - PMC Extract

PMC Extract es el objeto encargado de llevar a cabo la comunicación con la herramienta PMCTrack de interfaz de comandos.

En su inicialización, procesa los objetos de configuración del usuario generando el comando PMCTrack que lanza en la máquina que se haya configurado para monitorizar. Adicionalmente, crea un hilo encargado de extraer toda la información proveniente del comando PMCTrack, guardándola de forma organizada en un array de datos que será utilizado por el frontend para pintar las gráficas en tiempo real. Si durante la lectura el comando PMCTrack genera un error, PMC Extract lo capturará y almacenará, de tal manera que el frontend podrá leer ese error y mostrárselo al usuario mediante un pop-up.

PMC Extract cuenta con atributos a los que puede acceder el frontend para saber en cualquier momento el estado del benchmark, así como métodos que permiten enviar señales a dicho benchmark (señal de parada *SIGSTOP*, señal de reanudación *SIGCONT* y señal de matar proceso *SIGKILL*).

# Modo de uso

Al iniciar PMCTrack GUI se inicia con el idioma que hay configurado en la máquina que lo arranca (español si la máquina está en español e inglés en otro caso). El usuario lo primero que debe hacer es seleccionar la máquina que desea monitorizar, pudiéndose elegir la máquina donde se está ejecutando PMCTrack GUI u otra máquina remota. En cualquiera de los casos PMCTrack GUI hará un chequeo para comprobar que está instalado el software necesario tanto en la máquina a monitorizar como en la máquina donde se está ejecutando la GUI, y en caso de que falte algún requerimiento se informará debidamente al usuario.

Si todas las dependencias software están resueltas (y hay conectividad con la máquina remota si la hubiera), aparecerá una nueva ventana donde el usuario podrá configurar muy fácilmente los contadores hardware con los que cuenta la máquina a monitorizar, asignando eventos de la arquitectura de la máquina a contadores de propósito general, todo de una manera muy sencilla (aunque se permiten hacer configuraciones avanzadas pudiéndose asignar manualmente parámetros como el Umask, Cmask o EBS). En la imagen *(b)* de la figura \ref{fig:countersConf} puede visualizar una ventana de configuración de un contador.

\begin{figure}
\centering
\subfloat[]{\includegraphics[scale=0.23]{Imagenes/Bitmap/screenshotCountersConfMac}}\vspace{10mm}
\subfloat[]{\includegraphics[scale=0.23]{Imagenes/Bitmap/screenshotCounterConf}}
\caption{Ventanas de configuración de contadores y métricas} \label{fig:countersConf}
\end{figure}

Una vez configurados los contadores que se quieren utilizar, debajo de la sección de configuración de contadores el usuario se encontrará con la configuración de métricas. Esta sección permite al usuario configurar métricas de alto nivel que podrán verse posteriormente en forma de gráfica en tiempo real. Para la generación de métricas se usan fórmulas cuyas variables son los contadores que el usuario configuró anteriormente (pmc0, pmc1\ldots). No hay ninguna limitación a la hora de generar las fórmulas, de tal manera que el usuario podrá escribir fórmulas tan complejas como quiera, como por ejemplo $(pmc0 ^ 2) / pmc1 * 1000) * pmc4$. En la imagen *(a)* de la figura \ref{fig:countersConf} puede observar la ventana de configuración de contadores y métricas donde hay añadidos otros ejemplos de fórmulas.

Cabe destacar que es posible crear más de un experimento, esto es, más de un conjunto de contadores y métricas, de tal manera que es posible configurar un contador con un determinado evento y usarlo en una métrica y, en otro experimento, configurar el mismo contador con otro evento distinto y usarlo en otra métrica distinta.

\begin{figure}
\centering
\subfloat[]{\includegraphics[scale=0.23]{Imagenes/Bitmap/screenshotFinalConf}}\vspace{10mm}
\subfloat[]{\includegraphics[scale=0.23]{Imagenes/Bitmap/screenshotStyleGraphConf}}
\caption{Fase final de la configuración} \label{fig:finalConf}
\end{figure}

Cuando el usuario haya terminado de configurar todos los experimentos que quiera y haya pinchado en el botón Siguiente aparecerá una nueva ventana, esta ventana permite realizar las últimas configuraciones antes de iniciar la monitorización. Permite elegir el benchmark que se desea monitorizar, el tiempo entre cada muestra, la ruta del archivo donde guardar los resultados del comando PMCTrack generado (si es que el usuario quiere guardarlo), y la personalización de las gráficas, pudiéndose elegir un modo ya configurado (modo por defecto, modo hacker, modo aqua... etcétera) o personalizar uno. Véanse las dos imágenes de la figura \ref{fig:finalConf} para ver un ejemplo gráfico de lo comentado en este párrafo.

Una vez esté todo configurado y el usuario esté listo para iniciar la monitorización, pinchará en el botón "Iniciar monitorización" de la última ventana de configuración. Al pinchar se abrirá una nueva ventana donde se visualizará la gráfica en tiempo real de la primera métrica del primer experimento configurado (si el benchmark fuera multihilo se mostrará la gráfica del hilo principal). En cualquier momento podemos realizar las siguientes acciones:

* *Mostrar otra gráfica distinta.* Seleccionando el experimento, métrica de ese experimento y PID del hilo (en el caso de que el benchmark sea multihilo). El usuario podrá elegir entre mostrar la gráfica en la ventana actual o en una nueva ventana independiente, esto proporciona una gran flexibilidad al poder visualizar simultáneamente tantas gráficas como desee el usuario.

* *Mostrar gráfica acumulada o parcial.* Por defecto el usuario visualiza la última parte de la gráfica, es decir, la parte actual de la monitorización, sin embargo, es posible cambiar el modo de la gráfica a gráfica acumulada, visualizando la gráfica desde que se inició la monitorización.

* *Hacer captura de la gráfica actual.* El usuario puede hacer en cualquier momento de la monitorización una captura de una gráfica tal y como se está visualizando en ese instante, guardándola con formato de imagen PNG.

* *Ocultar controles.* Para ver una gráfica lo mejor posible se le da la posibilidad al usuario de ocultar todos los controles de la ventana, de esta manera la gráfica ocupa el tamaño entero de la ventana.

* *Parar el benchmark.* El usuario puede parar la ejecución del benchmark cuando lo desee, pudiéndolo reanudar posteriormente. Esto puede servir para sacar capturas de gráfica más precisas.

En la figura \ref{fig:monitoring} puede ver un ejemplo gráfico de lo explicado anteriormente.

\begin{figure}
\centering
\includegraphics[scale=0.27]{Imagenes/Bitmap/screenshotMonitoring}
\caption{Monitorización de un benchmark, visualizándose simultáneamente en tiempo real dos métricas} \label{fig:monitoring}
\end{figure}

Cabe destacar que mientras se está realizando la monitorización, el usuario puede seguir desplazándose por las ventanas de configuración para preparar una nueva monitorización. Cuando tenga lista la nueva configuración (se permite incluso monitorizar otra máquina distinta a la que se está monitorizando) el usuario pinchará en el botón "Cancelar monitorización" (en el caso de que se esté llevando a cabo una monitorización) para matar el proceso de monitorización en la máquina, el botón pasará a llamarse "Iniciar monitorización" y al pincharse se pondrá en marcha la nueva monitorización.

Cuando el benchmark termina se le notifica al usuario mediante un pop-up, pero en ningún caso se cierran las gráficas, pudiéndo el usuario seguir realizando las acciones que hemos visto anteriormente.
