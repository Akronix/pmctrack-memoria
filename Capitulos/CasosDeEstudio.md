\chapter{Casos de estudio}

En este capítulo evaluamos las nuevas extensiones de PMCTrack realizadas en este TFG, mediante tres casos de estudio. En el primer caso de estudio explotamos el potencial de PMCTRack-GUI y PMCTrack en su conjunto para recabar información de rendimiento mediante contadores hardware en distintas arquitecturas y diversos modelos de procesador. El segundo caso de estudio ilustra las capacidades de PMCTrack-GUI para monitorizar el rendimiento de hilos individuales de las aplicaciones paralelas. Finalmente, este capítulo concluye con un caso de estudio que pone a prueba la librería libpmtrack para estudiar la efectividad de distintas soluciones de un mismo problema o implementaciones alternativas de una estructura de datos.


# Monitorización del rendimiento con PMCTrack-GUI

\input{Capitulos/CasoDeEstudio-multiarch}

# Análisis de aplicaciones multihilo con PMCTrack-GUI


La idea sería hacer un análisis de dos aplicaciones paralelas. Una (`rnaseq`) en la que los hilos hagan lo mismo con distintos datos, y otra en la que los hilos cooperen realizando tareas diferentes.

	$ pmctrack -T 1 -c instr,cycles,llc_misses ./benchmarks/solaris-x86/parsec3/ferret_p3 2
		- Mirar LLCMR y IPC de hilos 1 y 4 de la lista

 	$ pmctrack -T 1 -c instr,cycles,llc_misses ./benchmarks/solaris-x86/misc/rnaseq 4


# Análisis de fragmentos de código con libpmctrack

En esta sección vamos a usar la librería *libpmctrack* para analizar el comportamiento del hardware en distintos fragmentos de código.

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

### Primer análisis

La ejecución se realiza en un procesador intel core i7-3520M a 2.9GHz con 8GB de RAM. Después de ejecutar el benchmark una primera vez con cada montículo, obtenemos los siguientes tiempos: $232,859ms$ para el montículo binario y $1690.336ms$ para el montículo de Fibonacci. Es decir, el montículo de Fibonacci es siete veces más lento que el montículo binario.

Para ver si esta gran diferencia de tiempo es debido a la memoria caché, necesitamos alguna forma de monitorizar directamente cómo se está comportando la memoria caché. Esta es una situación donde libpmctrack resulta tremendamente útil, ya que nos permite obtener información del hardware e incluso analizar diferentes fragmentos de código de forma aislada.

De modo que ahora añadimos al benchmark anterior la librería pmctrack, inicializamos el descriptor con espacio para 15 samples, fijamos el intervalo para obtener samples en $250ms$ y configuramos los contadores. Nos interesa que los contadores nos den información acerca del número de instrucciones retiradas, y los accesos y los fallos de la caché de último nivel (Nivel 3 en nuestro caso). De modo que activamos el contadore fijo pmc0, que cuenta el número de instrucciones, y asignamos a los contadores configurables pmc3 y pmc4 los eventos de contar accesos a caché y fallos de caché respectivamente.

\begin{figure}
\caption{Resultados monitorización global montículo binario}
Elapsed time: 476022 microseconds
Profiling data extracted from PMCs every 250ms:
nsample    pid      event          pmc0          pmc3          pmc4
      1   7377       tick     561444260       3966742        339785
      2   7377       self     549334613       4032294        151245
\end{figure}

\begin{figure}
\caption{Resultados monitorización global montículo Fibonacci}
Elapsed time: 3178255 microseconds
Profiling data extracted from PMCs every 250ms:
nsample    pid      event          pmc0          pmc3          pmc4
      1   7558       tick     629554817        555265        339547
      2   7558       tick     365243640       2111969        967323
      3   7558       tick     363263873       2174515        943288
      4   7558       tick     366034887       2190378        888714
      5   7558       tick     361822568       2208562        914895
      6   7558       tick     361998147       2201110        893159
      7   7558       tick     358977538       2206190        879025
      8   7558       tick     376751462       2220617        815036
      9   7558       tick     371586535       2229520        828087
     10   7558       tick     371069310       2196560        795315
     11   7558       tick     376280116       2186783        740499
     12   7558       tick     388247900       2161197        641935
     13   7558       self     341342501       1586504        322759
\end{figure}

Empezamos situando los start y stop counters al principio y al final del benchmark y obtenemos los resultados de las tablas \ref{} y \ref{}. Lo primero que vemos es que el montículo de Fibonacci tiene 13 entradas o *ticks* y el binario solo dos puesto que, como dijimos antes, el montículo binario es siete veces más rápido. Si sumamos los valores de todas las muestras, aproximadamente obtenemos los siguientes datos:

* 1150 millones de instrucciones el montículo binario y 5000 el de Fibonacci (casi cinco veces más instrucciones el montículo de Fibonacci). Probablemente debido a la mayor complejidad de las operaciones que realiza el montículo de Fibonacci.

* 7,5 millones de accesos a memoria caché en el binario y 25 millones en el de Fibonacci, por tanto, tres veces más accesos a caché por el montículo de Fibonacci. Como vemos, aunque la entrada es la misma: un millón de enteros, el montículo de Fibonacci tiene que acceder muchas más veces a memoria caché de último nivel.

* 0.4 millones de fallos a memoria caché de último nivel por el montículo binario y 10.5 millones por el montículo de Fibonacci. Aquí podemos comprobar como, efectivamente, la diferencia de fallos de acceso a la memoria caché es abismal, más de 20 veces más fallos en la memoria caché tiene el montículo de Fibonacci frente al montículo binario.

Resulta también de gran relevancia calcular la tasa de fallos por acceso a datos, esta sería de un 5,33\% en el caso del montículo binario, y de un 42\% en el caso del montículo de Fibonacci. De nuevo, una muy grande diferencia.

Por tanto, todo apunta a que esta gran diferencia en la cantidad del acceso a memoria caché y, sobre todo, en sus porcentajes de aciertos, hace muy superior en la práctica al montículo binario frente al montículo de Fibonacci, a pesar de que la teoría predijera lo contrario.

### Segundo análisis

No obstante, podemos afinar aún más y obtener mayor información. Revisando el análisis anterior, observamos que la primera muestra del montículo de fibonacci no está equilibrada con el resto de muestras: ejecuta el doble de instrucciones que el resto, y, sin embargo, hace muchos menos accesos a memoria; lo que nos lleva a pensar que podría haber una fase inicial en las que el montículo invierta menos tiempo y menos acceso a recursos que el resto. Para comprobar esto, también mediante libpmctrack podemos monitorizar fragmentos de código aislados. Para ello, situamos tres bloques start y stop counters entorno a tres partes clave de nuestro pequeño benchmark: Uno para la inicialización del montículo, otro para la inserción del millón de números y un tercero para la eliminación de éstos. Los resultados los podemos ver en las tablas \ref{} y \ref{}.

\begin{figure}
\caption{Resultados monitorización por fases montículo binario}
Profiling, through libpmctrack, cache behaviour when using a William's heap.
Profiling data for initializing the heap:
nsample    pid      event          pmc0          pmc3          pmc4
      1  13464       self           833            10             7
Profiling data for inserting into the heap:
nsample    pid      event          pmc0          pmc3          pmc4
      1  13464       self     194528249         19764         17205
Profiling data for deleting from the heap:
nsample    pid      event          pmc0          pmc3          pmc4
      1  13464       self     916232599       7383241        467662
Elapsed time: 229741 microseconds
\end{figure}

\begin{figure}
\caption{Resultados monitorización por fases montículo Fibonacci}
Profiling, through libpmctrack, cache behaviour when using a Fibonacci heap.
Profiling data for initializing the heap:
nsample    pid      event          pmc0          pmc3          pmc4
      1  13271       self           835            11            10
Profiling data for inserting into the heap:
nsample    pid      event          pmc0          pmc3          pmc4
      1  13271       self     377048052         15204          9962
Profiling data for deleting from the heap:
nsample    pid      event          pmc0          pmc3          pmc4
      1  13271       self    4655118486      37307044      14266564
Elapsed time: 1692031 microseconds
\end{figure}

Con estos nuevos datos, podemos ver claramente que la fase de inicialización y reserva inicial de memoria es prácticamente la misma para ambas estructuras en cuanto a número de instrucciones y acceso a memoria. En la fase de inserción, la diferencia tampoco es demasiado grande, de hecho, aunque el montículo de Fibonacci realiza más instrucciones, efectivamente cumple su teoría en cuanto a que realiza menos accesos a memoria y éstos son más exitosos que el montículo bibario. La gran diferencia llega en la última fase, la fase de borrado de elementos, en ésta el número de instrucciones ejecutadas es mucho mayor para ambos montículos. Es en esta fase cuando el montículo de Fibonacci se dispara en cuanto a número de accesos a memoria y la tasa de fallos es del tan alta como el 40\% mencionado anteriormente, eclipsando cualquier buen resultado que se podía haber obtenido en fases anteriores; mientras que el montículo binario, mantiene una buena tasa de fallos y un número de accesos relativamente mucho menor.

### Conclusiones

Después de un primer análisis global y, posteriormente, un segundo análisis pormenorizando el benchmark en tres fases clave. Hemos comprobado, gracias a la librería libpmctrack, que la teoría de la computación puede fallar a la hora de predecir los tiempos de computación de las estructuras de datos que hacen uso de la memoria dinámica, al pasar por alto la jerarquía en el acceso a memoria que existe en las computadoras actuales.

En particular, hemos observado como la implementación del montículo de Fibonacci, que teóricamente tiene un coste amortizado constante en el borrado, se comporta peor en la práctica que una implementación con memoria estática como es el montículo binario, cuyo coste en tiempo en el borrado es siempre logarítmico.
