\chapter{Interfaz gráfica}
# Motivación
PMCTrack es una herramienta muy potente desarrollada principalmente para ayudar al planificador del Sistema Operativo, por lo que aunque da soporte para ser usada por un usuario final, tiene grandes limitaciones en este sentido. Por ejemplo, para poder interpretar conjuntamente los datos que provee hace falta realizar un procesamiento de la información obtenida, generando de forma "manual" los resultados en forma de gráfica. Además, para una persona es imposible interpretar los datos globalmente en tiempo real (mientras que se está ejecutando el benchmark).

PMCTrack GUI ha surgido para superar estas limitaciones de PMCTrack, pero el resultado final es una herramienta con una extraordinaria funcionalidad a la altura de otras alternativas de alto coste económico de grandes empresas como IBM.

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

PMCTrack GUI ha sido desarrollada en Python, se eligió este lenguaje principalmente porque es multiplataforma, pudiendo ser ejecutado en cualquier sistema que soporte la instalación de un intérprete de Python, además de que cuenta con una biblioteca muy potente para la generación de gráficas a partir de datos contenidos en listas o arrays, la biblioteca matplotlib. Gran parte de la culpa del atractivo visual que tiene PMCTrack GUI la tiene esta biblioteca.

Ha sido diseñada para ser fácilmente escalable y sostenible. Consta de diversos componentes que podemos dividir en dos grandes grupos: Frontend y backend.

Frontend: Compuesto por todos los componentes gráficos de la aplicación. Para el desarrollo de los frames y diálogos se ha utilizado la biblioteca WX de Python, y para la generación de gráficas Matplotlib como ya se ha comentado antes.

Backend: Consta de todos los componentes que proveen información para ser mostrada en el frontend. Estos componentes son muy diferentes entre sí, proveyendo cada uno de ellos información muy diferente, por ello vamos a analizar cada uno de estos componentes por separado.

- Modelos de objetos XML: Consta de varios objetos python relacionados entre sí encargados de obtener información de los XML, XML que almacenan información de los eventos hardware de las distintas arquitecturas soportadas.

- PMC Connect:

- PMC Extract:

- User Config:
