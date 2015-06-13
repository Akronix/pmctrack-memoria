\chapter{Casos de estudio}

En este capítulo evaluamos las nuevas extensiones de PMCTrack realizadas en este TFG, mediante tres casos de estudio. En el primer caso de estudio explotamos el potencial de PMCTRack-GUI y PMCTrack en su conjunto para recabar información de rendimiento mediante contadores hardware en distintas arquitecturas y diversos modelos de procesador. El segundo caso de estudio ilustra las capacidades de PMCTrack-GUI para monitorizar el rendimiento de hilos individuales de las aplicaciones paralelas. Finalmente, este capítulo concluye con un caso de estudio que pone a prueba la librería libpmtrack para estudiar la efectividad de distintas soluciones de un mismo problema o implementaciones alternativas de una estructura de datos.


# Monitorización del rendimiento con PMCTrack-GUI

\input{Capitulos/CasoDeEstudio-multiarch}

# Análisis de aplicaciones multihilo con PMCTrack-GUI


La idea sería hacer un análisis de dos aplicaciones paralelas. Una (`rnaseq`) en la que los hilos hagan lo mismo con distintos datos, y otra en la que los hilos cooperen realizando tareas diferentes.

	$ pmctrack -T 1 -c instr,cycles,llc_misses ./benchmarks/solaris-x86/parsec3/ferret_p3 2
		- Mirar LLCMR y IPC de hilos 1 y 4 de la lista
 	
 	$ pmctrack -T 1 -c instr,cycles,llc_misses ./benchmarks/solaris-x86/misc/rnaseq 4


# Análisis de fragmentos de código con _libpmctrack_

TODO (Abel)