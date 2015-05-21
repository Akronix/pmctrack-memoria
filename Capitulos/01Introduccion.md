\chapter{Introducción}
<!-- En castellano y en inglés --->
# Introducción


## Contadores Hardware para monitorización 
 Los contadores hardware para monitorización (o *PMC* por sus siglas en inglés *"Profiling Monitoring Counters"*) son registros con contador localizados dentro de los microprocesadores modernos y que cuentan ciertos eventos que ocurren en la CPU.  
 Así pues, ejemplos de eventos que se podrían monitorizar de esta manera son: aciertos/fallos en accesos a memoria caché de distintos niveles, fallos en la predicción de saltos, instrucciones en coma flotante ejecutadas, etc.
 
 Estos contadores pueden ser de dos tipos: fijos, si siempre cuentan los mismos eventos; o configurables, si se puede elegir qué eventos, entre los proveídos por el fabricante, se quiere que el contador cuente.

 El uso de estos contadores es, principalmente, la monitorización del rendimiento del hardware y del software en el procesador en el que se encuentran instalados.  
 Hay varias razones por las que puede ser más recomendable o beneficioso el uso de estos contadores en la monitorización del rendimiento de programas en lugar de usar herramientas software.  
 Entre otras, la monitorización a través de los PMC permite obtener métricas muy cercanas al hardware; asímismo, la monitorización por software puede ser errónea o poco exacta debido a particularidades tecnológicas del procesador como la ejecución en desorden o las arquitecturas de memoria distribuida.

## Antecedentes: PMCTrack
PMCtrack es una herramienta de línea de comandos integrada en el kernel Linux que permite monitorizar el rendimiento de las aplicaciones haciendo uso de los contadores hardware del procesador.

La herramienta fue desarrollada inicialmente en un proyecto de sistemas informáticos por estudiantes de esta misma facultad en el año 2012 \cite{MSDTFG12}, y su uso y desarrollo se ha mantenido por el Grupo de Arquitectura y Tecnología de Sistemas Informáticos de esta universidad.

Para que la herramienta pueda acceder a la configuración y datos de los contadores hardware, se necesita soporte del núcleo del sistema operativo. Es por eso que se usa una versión del kernel *ad hoc* que contiene las modificaciones necesarias para que esta herramienta funciones.

La herramienta tiene un diseño modular, de modo que por un lado están las modificaciones al código del kernel y por otro el código en modo usuario  que es el que realmente implementa la funcionalidad de la herramienta. De esta manera, se permite independencia de la versión del kernel mientras que se mantiene facilidad para el desarrollo y el mantenimiento.

 > copiar esquema pmctrack?<

## Otras herramientas para la monitorización mediante contadores hardware
Además de PMCTrack, existen muchas otras herramientas que hacen uso de estos contadores para dar información de rendimiento al usuario.

A continuación destacaremos las más conocidas.

* Perf. Perf viene ya incluido en el kernel de linux dentro del directorio tools/perf. Permite mucha configuración y trazabilidad.
* OProfile. Herramienta instalable en linux. Permite monitorización de una sola aplicación o de todo el sistema.



## Objetivos

## Plan de trabajo
