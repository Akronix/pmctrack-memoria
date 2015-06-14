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

En esta sección vamos a usar la librería libpmctrack para analizar el comportamiento del hardware en distintos fragmentos de código.

## Comportamiento de la memoria caché en estructuras de datos con memoria dinámica

Como bien sabemos, el acceso a memoria principal en los ordenadores no se hace directamente con peticiones a la RAM, si no que sigue una jerarquía de memorias caché ordenadas por niveles según su tamaño y latencia. Las memorias caché contienen bloques de memoria contiguos buscando explotar así la localidad espacial de los programas. Esto significa que es mucho más lento acceder a direcciones de memoria no contiguas que a direcciones contiguas solo debido a la memoria caché. Cuando en un programa reservamos memoria de forma estática, ya sea en la memoria global o en la *stack* del programa, se reservan bloques contiguos de memoria, y es por esto que podemos acceder a cada elemento mediante un índice (en realidad, el índice marca un desplazamiento respecto al inicio del array). Sin embargo, cuando reservamos memoria de forma dinámica, es decir en la *heap* del programa, los bloques de memoria son asignados según la conveniencia del sistema operativo y muchas veces estos bloques se encuentran en direcciones muy distanciadas dentro de la memoria.

En esta sección, queremos analizar cuánto podría afectar esta diferencia de tiempos de acceso para la implementación de estructuras de datos. Como ejemplo, usaremos dos posibles implementaciones de un montículo o cola de prioridad (en inglés *heap*) según hagan uso de memoria dinámica mediante el uso de punteros, o de memoria estática.

La primera de ellas es el conocido montículo de Fibonacci (*Fibonacci heap*), que tiene muy buenos costes amortizados, siendo sus operaciones de crear, insertar, obtener el mínimo y unir de coste constante en el caso peor; y solo siendo sus operaciones de eliminar de coste amortizado logarítmico. Para conseguir estos costes, el montículo se limita a hacer el mínimo trabajo posible cuando inserta elementos, manteniendo siempre un puntero al mínimo elemento, y se reestructura cuando tiene que hacer una operación de borrar el mínimo elemento.\newline
Los montículos de Fibonacci hacen un uso intenso de punteros.
La estructura consiste en una lista dinámica de árboles de distinto grado donde cada nodo del montículo tiene cuatro punteros: al nodo padre, al nodo hijo, y a sus nodos hermanos izquierdo y derecho.\newline
La reestructuración de nodos que realiza en el caso de borrar va creciendo según la secuencia de Fibonacci, y es de aquí de donde coge el nombre.

La segunda de ellas es una implementación que solamente hace uso de memoria estática, la conocida como montículo de William o montículo binario (*Williams' heap*, *binary heap* o *bi-parental heap*). En esta implementación se simula el comportamiento de una estructura de árbol binario balanceado en un array de elementos. El árbol se simula estructurándolo de tal manera que cada nodo siempre tiene su padre en la posición $i/2$, su hijo izquierdo en la posición $2i$ y su hijo derecho en la posición $2i + 1$ del array.\newline
La estructura debe mantener el invariante de que todos los nodos, excepto el nodo raiz, tienen una clave mayor o igual que la clave de su padre. De esta manera se garantiza que, a la hora de actualizar el árbol, solo un logaritmo de todos los elementos tendrá que ser recorrido, por tanto, en este caso sus costes en el caso peor de insertar y de eliminar son logarítmicos, aunque el de obtener el mínimo elemento sigue siendo constante puesto que siempre estará en el nodo raíz.

Ahora vamos a comprobar si en la práctica se confirman los costes que predice la teoría. Para ello hemos realizado un sencillo benchmark que simplemente inserta y elimina un millón de números de un montículo, estos números son generados al azar en un rango que va de -5000 a 5000. El benchmark, al terminar, nos dice cuánto tiempo ha transcurrido desde que se empezó a ejecutar el benchmark hasta que acaba con precisión de microsegundos.

La ejecución se realiza en un procesador intel core i7-3520M a 2.9GHz con 8GB de RAM. Después de ejecutar el benchmark una primera vez con cada montículo, obtenemos los siguientes tiempos: $232,859ms$ para el montículo binario y $1690.336ms$ para el montículo de fibonacci. Es decir, el montículo de fibonacci es siete veces más lento que el montículo binario.

Para ver si esta gran diferencia de tiempo es debido a la memoria caché, necesitamos alguna forma de monitorizar directamente cómo se está comportando la memoria caché. Esta es una situación donde libpmctrack resulta tremendamente útil, ya que nos permite obtener información del hardware e incluso analizar diferentes fragmentos de código de forma aislada.

De modo que ahora añadimos al benchmark anterior la librería pmctrack, inicializamos el descriptor, fijamos el tiempo para obtener samples en $50ms$ y configuramos los contadores. Nos interesa que los contadores nos den información acerca del número de instrucciones retiradas, y los accesos y los fallos de la caché de último nivel (Nivel 3 en nuestro caso). De modo que activamos el contadore fijo pmc0, que cuenta el número de instrucciones, y asignamos a los contadores configurables pmc3 y pmc4 los eventos de contar accesos a caché y fallos de caché respectivamente.

Empezamos situando los start y stop count al principio y al final del benchmark y obtenemos los resultados de las tablas \ref{} y \ref{}. Lo primero que vemos es que el montículo de fibonacci tiene quince entradas o *ticks* y el binario solo cinco puesto que, como dijimos antes, el montículo binario es significativamente más lento. A continuación, sumamos  que los accesos a memoria caché son 7 millones y 15 millones aproximadamente 16.5 millones de accesos como los 1150 y 2025 millones de instrucciones.

En el análisis anterior también observamos que no hay un equilibrio en los resultados que dan los contadores a lo largo de todo el ciclo del programa, lo que nos lleva a pensar que puede haber fases en las que se invierta más tiempo y más acceso a recursos que otra. Para comprobar esto, situamos tres bloques start y stop count entorno a tres partes clave de nuestro pequeño benchmark: Uno para la inicialización del montículo, otro para la inserción y un tercero para la eliminación del millón de números. Los resultados los podemos ver en las tablas \ref{} y \ref{}.

\begin{figure}
\caption{Resultados monitorización global montículo binario}
Elapsed time: 232654 microseconds
Profiling data extracted from PMCs:
nsample    pid      event          pmc0          pmc3          pmc4
      1  11263       tick     205108717        142359         43550
      2  11263       tick     209954378       2251085        188136
      3  11263       tick     231496240       2215010         36077
      4  11263       tick     235018067       1859839         17076
      5  11263       self     229336746        826241           153
\end{figure}

\begin{figure}
\caption{Resultados monitorización global montículo Fibonacci}
Elapsed time: 1710817 microseconds
Profiling data extracted from PMCs:
nsample    pid      event          pmc0          pmc3          pmc4
      1  11474       tick     135446153       1099369        469118
      2  11474       tick     134271027       1103214        468838
      3  11474       tick     131887895       1109943        472052
      4  11474       tick     134146252       1102410        463599
      5  11474       tick     131120492       1089186        475294
      6  11474       tick     121713433       1057953        443598
      7  11474       tick     124896626       1086301        471523
      8  11474       tick     130228897       1116927        468670
      9  11474       tick     127860082       1095860        466143
     10  11474       tick     129634236       1119603        465937
     11  11474       tick     129913414       1129926        455680
     12  11474       tick     125505644       1103817        464760
     13  11474       tick     128672197       1126770        449822
     14  11474       tick     133428551       1120849        443910
     15  11474       tick     132818159       1136451        446575
\end{figure}
