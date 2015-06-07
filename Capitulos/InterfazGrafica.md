\chapter{PMCTrack GUI: Algo más que un interfaz gráfico}
# Motivación
$PMCTrack$ es una herramienta muy potente desarrollada principalmente para ayudar al *planificador* del sistema operativo, por lo que aunque da soporte para ser usada por un usuario final, tiene grandes limitaciones en este sentido:

* Proporciona al usuario el valor de cada contador configurado en determinados instantes de tiempo, por lo que para que el usuario pueda interpretar esos datos es necesario que realice de forma "manual" gráficas con herramientas como $Gnuplot$, teniéndolas que generar una vez PMCTrack ha terminado de extraer toda la información de los contadores.

* Para la asignación de eventos a contadores es necesario para el usuario el uso de un manual de la arquitectura de la máquina, ya que deberá buscar el evento que desea contabilizar en un contador e indicar al comando PMCTrack los valores de configuración para los contadores.

# PMCTrack GUI, una herramienta única

Como ya hemos visto, PMCTrack posee limitaciones importantes al usarse por un usuario final. Estas limitaciones han sido nuestra motivación para desarrollar PMCTrack GUI, y el resultado final es una herramienta que no sólo supera estas limitaciones si no que supera grandes limitaciones de las aplicaciones alternativas disponibles en el mercado.

A día de hoy no hay otra herramienta en el mercado como PMCTrack GUI, por los siguientes dos motivos:

* Única aplicación que permite visualizar la monitorización de benchmarks siendo multiarquitectura. En el mercado sólo están disponibles las herramientas de monitorización de cada fabricante, como el *Intel Performance Counter Monitor* de \cite{Intel} o el *Streamline Performance Analyzer* de \cite{ARM}.

* Única aplicación de código libre y completamente gratuita. Las aplicaciones alternativas disponibles en el mercado no son libres y las licencias de uso son de un alto coste económico.

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

Ha sido diseñada para ser fácilmente escalable y sostenible. Consta de diversos componentes que podemos dividir en dos grandes grupos según la función que desempeñan: *Frontend* y *Backend*.

## Frontend

Está compuesto por todos los componentes gráficos de la aplicación.

Para el desarrollo de los frames y diálogos se ha utilizado la biblioteca *WX* de Python. El desarrollo se inició sobre la versión 2.8 aunque hoy en día la aplicación también es compatible con la última versión, la 3.0, esto ha hecho posible que PMCTrack GUI pueda ser ejecutada sobre la interfaz gráfica nativa de $MacOS X$.

Para la generación de gráficas se ha usado la biblioteca *Matplotlib*, que como ya se ha comentado antes, permite la generación de gráficos de alta calidad y precisión a partir de datos contenidos en listas o arrays, todo esto consumiendo pocos recursos y utilizando una notación muy parecida a la de $MATLAB$.

\todo{Incluir captura de GUI en MacOS y Linux}

## Backend

Consta de todos los componentes que proveen información para ser mostrada en el frontend. Estos componentes son muy diferentes entre sí, proveyendo cada uno de ellos información muy diferente, por ello vamos a analizar cada uno de estos componentes por separado.

### Objetos de procesamiento

Esta parte consta de información sobre la máquina y los eventos hardware que puede monitorizar, así como de las clases python que permiten su procesado y le facilitan dicha información al *frontend* de la aplicación. Para desacoplar esta parte del resto de la aplicación, la información es servida al frontend usando el \glosstex{patrón de diseño} Fachada, implementado en la clase `FacadeXML`.

En la figura \ref{fig:UML_XML} se puede observar un diagrama UML de lo que correspondería a toda esta parte.\\
Podemos observar como la información está repartida en dos formatos posibles:
\begin{inparaenum}[(i)]
\item XML: Dependientes de cada modelo, contienen la información de eventos e información de ese modelo de máquina en particular necesaria para la \ac{GUI};
\item texto plano: tienen información más general de la máquina, proveída por el kernel de Linux.
\end{inparaenum} En los siguientes apartados, profundizaremos más detalladamente sobre qué información contienen y cómo están estructurados cada uno de estos elementos.



####


Consta de varios objetos Python relacionados entre sí encargados de almacenar información de archivos en formato XML o en texto plano. Los XML almacenan información de los eventos hardware de las distintas arquitecturas soportadas (hay un XML para cada arquitectura), los archivos en texto plano contienen información acerca de la máquina, gracias a estos archivos los *Objectos de procesamiento* cargan de forma automática los contadores y eventosHW de la arquitectura de la máquina a monitorizar, almacenando estos datos en objetos Python a los que el frontend puede acceder fácilmente.

\todo{Incluir captura de UML}

### PMC Connect

Se encarga de la lectura de archivos de una máquina así como proporcionar métodos que ayudan a realizar chequeos sobre el software instalado en la máquina. Algunos de estos métodos son determinar si existe un determinado archivo en la máquina indicada, determinar si tiene un determinado paquete instalado, o comprobar si se puede establecer conexión con la máquina. Este componente es usado por el frontend para chequear las dependencias software y por los *Objetos de procesamiento* para leer los archivos en texto plano (de esta manera se mantiene una independencia entre los *Objetos de procesamiento* y la máquina que se desea monitorizar, sea local o remota)

### PMC Extract

Es el componente del backend encargado de crear el subproceso que lanzará el comando pmctrack generado por este mismo objeto a partir de la configuración del usuario. Un vez lanzado obtiene los datos devueltos por el comando PMCTrack y los almacena de forma ordenada en un array de datos que será usado por el frontend para mostrar la información. Tiene atributos que indican al frontend el estado de la ejecución de PMCTrack así como métodos que permiten al frontend enviar señales al benchmark (señal de parada, reanudación o muerte).

### User Config

Es un conjunto de objetos Python que almacenan toda la configuración que el usuario va generando al interactuar con la GUI. Estos objetos son transferidos de un frame a otro hasta que acaban siendo enviados al PMC Extract, donde son procesados generando el comando PMCTrack que será lanzado en la máquina en cuestión.

\todo{Incluir captura de UML}

# Modo de uso

Al iniciar PMCTrack GUI se inicia con el idioma que hay configurado en la máquina que lo arranca (español si la máquina está en español e inglés en otro caso). El usuario lo primero que debe hacer es seleccionar la máquina que desea monitorizar, pudiéndose elegir la máquina donde se está ejecutando PMCTrack GUI u otra máquina remota. En cualquiera de los casos PMCTrack GUI hará un chequeo para comprobar que está instalado el software necesario tanto en la máquina a monitorizar como en la máquina donde se está ejecutando la GUI, y en caso de que falte algún requerimiento se informará debidamente al usuario.

Si todas las dependencias software están resueltas (y hay conectividad con la máquina remota si la hubiera), aparecerá una nueva ventana donde el usuario podrá configurar muy fácilmente los contadores hardware con los que cuenta la máquina a monitorizar, asignando eventos de la arquitectura de la máquina a contadores de propósito general, todo de una manera muy sencilla (aunque se permiten hacer configuraciones avanzadas pudiéndose asignar manualmente parámetros como el Umask, Cmask o EBS).

Una vez configurados los contadores que se quieren utilizar, debajo de la sección de configuración de contadores el usuario se encontrará con la configuración de métricas. Esta sección permite al usuario configurar métricas de alto nivel que podrán verse posteriormente en forma de gráfica en tiempo real. Para la generación de métricas se usan fórmulas cuyas variables son los contadores que el usuario configuró anteriormente (pmc0, pmc1\ldots). No hay ninguna limitación a la hora de generar las fórmulas, de tal manera que el usuario podrá escribir fórmulas tan complejas como quiera, como por ejemplo $(pmc0 ^ 2) / pmc1 * 1000) * pmc4$

Cabe destacar que es posible crear más de un experimento, esto es, más de un conjunto de contadores y métricas, de tal manera que es posible configurar un contador con un determinado evento y usarlo en una métrica y, en otro experimento, configurar el mismo contador con otro evento distinto y usarlo en otra métrica distinta.

Cuando el usuario haya terminado de configurar todos los experimentos que quiera y haya pinchado en el botón Siguiente aparecerá una nueva ventana, esta ventana permite realizar las últimas configuraciones antes de iniciar la monitorización. Permite elegir el benchmark que se desea monitorizar, el tiempo entre cada muestra, la ruta del archivo donde guardar los resultados del comando PMCTrack generado (si es que el usuario quiere guardarlo), y la personalización de las gráficas, pudiéndose elegir un modo ya configurado (modo por defecto, modo hacker, modo aqua... etcétera) o personalizar uno.

Una vez esté todo configurado y el usuario esté listo para iniciar la monitorización, pinchará en el botón "Iniciar monitorización" de la última ventana de configuración. Al pinchar se abrirá una nueva ventana donde se visualizará la gráfica en tiempo real de la primera métrica del primer experimento configurado (si el benchmark fuera multihilo se mostrará la gráfica del hilo principal). En cualquier momento podemos realizar las siguientes acciones:

* *Mostrar otra gráfica distinta.* Seleccionando el experimento, métrica de ese experimento y PID del hilo (en el caso de que el benchmark sea multihilo). El usuario podrá elegir entre mostrar la gráfica en la ventana actual o en una nueva ventana independiente, esto proporciona una gran flexibilidad al poder visualizar simultáneamente tantas gráficas como desee el usuario.

* *Mostrar gráfica acumulada o parcial.* Por defecto el usuario visualiza la última parte de la gráfica, es decir, la parte actual de la monitorización, sin embargo, es posible cambiar el modo de la gráfica a gráfica acumulada, visualizando la gráfica desde que se inició la monitorización.

* *Hacer captura de la gráfica actual.* El usuario puede hacer en cualquier momento de la monitorización una captura de una gráfica tal y como se está visualizando en ese instante, guardándola con formato de imagen PNG.

* *Ocultar controles.* Para ver una gráfica lo mejor posible se le da la posibilidad al usuario de ocultar todos los controles de la ventana, de esta manera la gráfica ocupa el tamaño entero de la ventana.

* *Parar el benchmark.* El usuario puede parar la ejecución del benchmark cuando lo desee, pudiéndolo reanudar posteriormente. Esto puede servir para sacar capturas de gráfica más precisas.

Cabe destacar que mientras se está realizando la monitorización, el usuario puede seguir desplazándose por las ventanas de configuración para preparar una nueva monitorización. Cuando tenga lista la nueva configuración (se permite incluso monitorizar otra máquina distinta a la que se está monitorizando) el usuario pinchará en el botón "Cancelar monitorización" (en el caso de que se esté llevando a cabo una monitorización) para matar el proceso de monitorización en la máquina, el botón pasará a llamarse "Iniciar monitorización" y al pincharse se pondrá en marcha la nueva monitorización.

Cuando el benchmark termina se le notifica al usuario mediante un pop-up, pero en ningún caso se cierran las gráficas, pudiéndo el usuario seguir realizando las acciones que hemos visto anteriormente.
