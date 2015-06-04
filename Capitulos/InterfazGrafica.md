\chapter{Interfaz gráfica}
# Motivación
PMCTrack es una herramienta muy potente desarrollada principalmente para ayudar al *planificador* del sistema operativo, por lo que aunque da soporte para ser usada por un usuario final, tiene grandes limitaciones en este sentido.

Por ejemplo, para poder interpretar conjuntamente los datos que provee hace falta realizar un procesamiento de la información obtenida, generando de forma "manual" los resultados en forma de gráfica. Además, para una persona es imposible interpretar los datos globalmente en tiempo real (mientras que se está ejecutando el benchmark).

PMCTrack GUI ha surgido para superar estas limitaciones de $PMCTrack$, pero el resultado final es una herramienta con una extraordinaria funcionalidad a la altura de otras alternativas de alto coste económico de grandes empresas como $IBM$.

# Características de PMCTrack GUI

* Visualización de gráficas de monitorización en tiempo real.
* Asignación amigable de eventos a los contadores hardware.
* Generación sencilla de métricas a partir de fórmulas de alto nivel.
* Posibilidad de monitorización de máquinas remotas, desacoplando la GUI de la propia monitorización.
* Detección de las dependencias software no satisfechas.
* Detección automática de la arquitectura de la máquina a monitorizar, cargando los contadores y eventos propios de dicha arquitectura.
* Permite observar simultáneamente y en tiempo real 2 o más gráficas.
* Soporta la monitorización de aplicaciones multihilo, pudiendo observar gráficas propias de un hilo concreto de la aplicación a monitorizar.
* Permite parar y reanudar la ejecución del benchmark que se está monitorizando.
* Permite realizar una nueva configuración a partir de otra anterior cuya monitorización se está llevando a cabo.
* Permite personalizar las gráficas a gusto del usuario.
* Permite realizar capturas de las gráficas.
* Permite redimensionar las gráficas en tiempo real.
* Ajuste automático de los ejes de las gráficas en función de los valores y del tamaño de la ventana.
* Soporte multilenguaje (disponible por ahora en inglés y español)
* Multiplataforma, pudiéndose ejecutar en GNU/Linux y MacOS X.

# Diseño de PMCTrack GUI

PMCTrack GUI ha sido desarrollada en *Python*, eligiéndose este lenguaje principalmente por ser multiplataforma, pudiendo ser ejecutado en cualquier sistema que soporte la instalación de un intérprete de Python, además de que cuenta con una biblioteca muy potente para la generación de gráficas a partir de datos contenidos en listas o arrays, la biblioteca *Matplotlib*. Gran parte de la culpa del atractivo visual que tiene PMCTrack GUI la tiene esta biblioteca.

Ha sido diseñada para ser fácilmente escalable y sostenible. Consta de diversos componentes que podemos dividir en dos grandes grupos: Frontend y backend.

## Frontend

Compuesto por todos los componentes gráficos de la aplicación.

Para el desarrollo de los frames y diálogos se ha utilizado la biblioteca *WX* de Python. El desarrollo se inició sobre $WX-2.8$ aunque hoy en día la aplicación también es compatible con la última versión, la 3.0, esto ha hecho posible que PMCTrack GUI pueda ser ejecutada sobre la interfaz gráfica nativa de $MacOS X$.

Para la generación de gráficas se ha usado la biblioteca *Matplotlib*, como ya se ha comentado antes.

\todo{Incluir captura de GUI en MacOS y Linux}

## Backend

Consta de todos los componentes que proveen información para ser mostrada en el frontend. Estos componentes son muy diferentes entre sí, proveyendo cada uno de ellos información muy diferente, por ello vamos a analizar cada uno de estos componentes por separado.

### Objetos de procesamiento

Consta de varios objetos python relacionados entre sí encargados de almacenar información de archivos en formato XML o en texto plano. Los XML almacenan información de los eventos hardware de las distintas arquitecturas soportadas (hay un XML para cada arquitectura), los archivos en texto plano contienen información acerca de la máquina, gracias a estos archivos los "Objectos de procesamiento" cargan de forma automática los contadores y eventosHW de la arquitectura de la máquina a monitorizar, almacenando estos datos en objetos python a los que el frontend puede acceder fácilmente.

\todo{Incluir captura de UML}

### PMC Connect

Se encarga de la lectura de archivos de una máquina así como proporcionar métodos que ayudan a realizar chequeos sobre el software instalado en la máquina. Algunos de estos métodos son determinar si existe un determinado archivo en la máquina indicada, determinar si tiene un determinado paquete instalado, o comprobar si se puede establecer conexión con la máquina. Este componente es usado por el frontend para chequear las dependencias software y por los Objetos de procesamiento para leer los archivos en texto plano (de esta manera se mantiene una independencia entre los Objetos de procesamiento y la máquina que se desea monitorizar, sea local o remota)

### PMC Extract

Es el componente del backend encargado de crear el subproceso que lanzará el comando pmctrack generado por este mismo objeto a partir de la configuración del usuario. Un vez lanzado obtiene los datos devueltos por el comando pmctrack y los almacena de forma ordenada en un array de datos que será usado por el frontend para mostrar la información. Tiene atributos que indican al frontend el estado de la ejecución de pmctrack así como métodos que permiten al frontend enviar señales al benchmark (señal de parada, reanudación o matado).

### User Config

Es un conjunto de objetos python que almacenan toda la configuración que el usuario va generando al interactuar con la GUI. Estos objetos son transferidos de un frame a otro hasta que acaban siendo enviados al PMC Extract, donde son procesados generando el comando pmctrack que será lanzado en la máquina en cuestión.

\todo{Incluir captura de UML}

## Ejemplo de uso

Al iniciar PMCTrack GUI el usuario selecciona la máquina que desea monitorizar, pudiéndose elegir la máquina donde se está ejecutando PMCTrack GUI u otra máquina remota. En cualquiera de los casos PMCTrack GUI hará un chequeo para comprobar que está instalado el software necesario tanto en la máquina a monitorizar como en la máquina donde se está ejecutando la GUI, y en caso de que falte algún requerimiento se informará debidamente al usuario.

Si todas las dependencias software están resueltas (y hay conectividad con la máquina remota si la hubiera), aparecerá una nueva ventana donde el usuario podrá configurar muy fácilmente los contadores hardware con los que cuenta la máquina a monitorizar, asignando eventos de la arquitectura de la máquina a contadores de propósito general, todo de una manera muy sencilla (aunque se permiten hacer configuraciones avanzadas pudiéndose asignar manualmente parámetros como el Umask, Cmask o EBS).

Una vez configurados los contadores que se quieren utilizar, debajo de la sección de configuración de contadores el usuario se encontrará con la configuración de métricas. Esta sección permite al usuario configurar métricas de alto nivel que podrán verse posteriormente en forma de gráfica en tiempo real. Para la generación de métricas se usan fórmulas cuyas variables son los contadores que el usuario configuró anteriormente (pmc0, pmc1...). No hay ninguna limitación a la hora de generar las fórmulas, de tal manera que el usuario podrá escribir fórmulas tan complejas como quiera (por ejemplo $(pmc0^2)/pmc1\*1000)\*pmc4$)

Cuando el usuario haya creado todas las métricas que quiera y haya pinchado en el botón de Continuar aparecerá una nueva ventana, esta ventana permite realizar las últimas configuraciones antes de iniciar la monitorización. Permite elegir el benchmark que se desea monitorizar, el tiempo entre cada muestra, la ruta del archivo donde guardar los resultados del comando PMCTrack generado (si es que el usuario quiere guardarlo), y la personalización de las gráficas (pudiéndose elegir un modo ya configurado (modo por defecto, modo hacker, modo aqua...) o personalizar uno).


