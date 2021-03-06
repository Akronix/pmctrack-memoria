\chapter{Casos de estudio}

En este capítulo evaluamos las nuevas extensiones de PMCTrack realizadas en este proyecto, mediante tres casos de estudio. En el primer caso de estudio explotamos el potencial de PMCTrack-GUI y PMCTrack en su conjunto para recabar información de rendimiento mediante contadores hardware en distintas arquitecturas y diversos modelos de procesador. El segundo caso de estudio ilustra las capacidades de PMCTrack-GUI para monitorizar el rendimiento de hilos individuales de las aplicaciones paralelas. Finalmente, este capítulo concluye con un caso de estudio que pone a prueba la librería libpmtrack para estudiar la efectividad de distintas implementaciones alternativas de una estructura de datos.

# Monitorización del rendimiento con PMCTrack-GUI
\label{sec:case-multiarch}

\input{Capitulos/CasoDeEstudio-multiarch}

# Análisis de aplicaciones multihilo con PMCTrack-GUI
\label{sec:case-multithreading}

\input{Capitulos/CasoDeEstudio-multihilo}

\section[Análisis de fragmentos de código con libpmctrack]{Análisis de fragmentos de código con libpmctrack: comportamiento de la memoria caché en estructuras de datos con memoria dinámica}
\label{sec:case-libpmctrack}

En esta sección empleamos la librería *libpmctrack* para analizar el comportamiento del hardware en distintos fragmentos de código.

Como bien sabemos, el acceso a memoria principal en los ordenadores no se hace directamente con peticiones a la RAM, si no que sigue una jerarquía de memorias caché ordenadas por niveles según su tamaño y latencia. Las memorias caché contienen bloques de memoria contiguos buscando explotar así la localidad espacial de los programas. Esto significa que es mucho más lento acceder a direcciones de memoria no contiguas que a direcciones contiguas solo debido a la memoria caché. Cuando en un programa reservamos memoria de forma estática, ya sea en la memoria global o en la pila del programa, se reservan bloques contiguos de memoria, y es por ello que podemos acceder a cada elemento mediante un índice (en realidad, el índice marca un desplazamiento respecto al inicio del array). Sin embargo, cuando reservamos memoria de forma dinámica, es decir en la *heap* del proceso, los bloques de memoria son asignados según la conveniencia del sistema operativo y muchas veces estos bloques se encuentran en direcciones muy distanciadas dentro de la memoria.

En esta sección, queremos analizar cuánto podría afectar esta diferencia de tiempos de acceso para la implementación de estructuras de datos. Como ejemplo, usaremos dos posibles implementaciones de un montículo o cola de prioridad (en inglés *heap*) según hagan uso de memoria dinámica mediante el uso de punteros, o de memoria estática.

La primera de ellas es el conocido montículo de Fibonacci (*Fibonacci heap*), que tiene muy buenos costes amortizados, siendo sus operaciones de crear, insertar, obtener el mínimo y unir de coste constante en el caso peor; y solo siendo sus operaciones de eliminar de coste amortizado logarítmico. Para conseguir estos costes, el montículo se limita a hacer el mínimo trabajo posible cuando inserta elementos, manteniendo siempre un puntero al mínimo elemento, y se reestructura cuando tiene que hacer una operación de borrar el elemento mínimo.\newline
Los montículos de Fibonacci hacen un uso intensivo de punteros.
La estructura consiste en una lista dinámica de árboles de distinto grado donde cada nodo del montículo tiene cuatro punteros: al nodo padre, al nodo hijo, y a sus nodos hermanos izquierdo y derecho.\newline
La reestructuración de nodos que realiza en el caso de borrar va creciendo según la secuencia de Fibonacci (he de aquí su nombre).

La segunda de ellas es una implementación que solamente hace uso de memoria estática, la conocida como montículo de William o montículo binario (*Williams' heap*, *binary heap* o *bi-parental heap*). En esta implementación se simula el comportamiento de una estructura de árbol binario balanceado en un array de elementos. El árbol se simula estructurándolo de tal manera que cada nodo siempre tiene su padre en la posición $i/2$, su hijo izquierdo en la posición $2i$ y su hijo derecho en la posición $2i + 1$ del array.\newline
La estructura debe mantener el invariante de que todos los nodos, excepto el nodo raíz, tienen una clave mayor o igual que la clave de su padre. De esta manera se garantiza que, a la hora de actualizar el árbol, solo un logaritmo de todos los elementos tendrá que ser recorrido. Por tanto, en este caso sus costes en el caso peor de insertar y de eliminar son logarítmicos, aunque el de obtener el mínimo elemento sigue siendo constante puesto que siempre estará en el nodo raíz.

Ahora vamos a comprobar si en la práctica se confirman los costes que predice la teoría. Para ello hemos implementado un sencillo benchmark que simplemente inserta y elimina un millón de números en un montículo. Estos números son generados al azar en un rango que va de -5000 a 5000. El benchmark, al terminar, nos dice cuánto tiempo ha transcurrido desde el comienzo de la ejecución con precisión de microsegundos.

\subsection{Primer análisis}

La ejecución se realiza en un sistema con un procesador Intel Core i7-3520M a 2.9GHz y 8GB de RAM. Después de ejecutar el benchmark una primera vez con cada montículo, obtenemos los siguientes tiempos: $232.859ms$ para el montículo binario y $1690.336ms$ para el montículo de Fibonacci. Es decir, el montículo de Fibonacci es siete veces más lento que el montículo binario.

Para ver si esta gran diferencia de tiempo es debido a la memoria caché, necesitamos alguna forma de monitorizar directamente cómo se está comportando. Ésta es una situación donde libpmctrack resulta tremendamente útil, ya que nos permite obtener información del hardware e incluso analizar diferentes fragmentos de código de forma aislada.

Ahora procedemos a instrumentar el código del benchmark anterior usando la librería libpmctrack. Más concretamente, inicializamos el descriptor \texttt{pmctrack\_desc\_t} con espacio para 15 muestras, fijamos el intervalo de muestreo a $250ms$ y configuramos los contadores hardware. Nos interesa que los contadores nos den información acerca del número de instrucciones retiradas, y los accesos y los fallos de la caché de último nivel (Nivel 3 en nuestra plataforma). Para ello, activamos el contador fijo _pmc0_, que cuenta el número de instrucciones, y asignamos
a los contadores configurables _pmc3_ y _pmc4_ los eventos para contabilizar accesos y fallos en el último nivel de caché, respectivamente. Comenzaremos situando las llamadas a \texttt{pmctrack\_start\_counters()} y \texttt{pmctrack\_stop\_counters()} counters al principio y al final del c\'odigo del benchmark.

\begin{table}[h]
\caption{Resultados monitorización global montículo binario}
\label{tab:gloBin}
\centering
%Elapsed time: 476022 microseconds
%Profiling data extracted from PMCs every 250ms:
\begin{tabular} {|r|r|r|r|r|r|}
\hline
\multicolumn{1}{|c|}{nsample} & \multicolumn{1}{c|}{pid} & \multicolumn{1}{c|}{event} & \multicolumn{1}{c|}{pmc0} & \multicolumn{1}{c|}{pmc3}  & \multicolumn{1}{c|}{pmc4} \\ \hline
%nsample  &  pid   &   event     &     pmc0     &     pmc3     &     pmc4 \\ \hline
      1  & 7377   &    tick   &  561444260     &  3966742     &   339785 \\ \hline
      2  & 7377   &    self   &  549334613    &   4032294     &   151245 \\ \hline
\end{tabular}
\end{table}

\begin{table}[h]
\caption{Resultados monitorización global montículo Fibonacci}
\label{tab:gloFib}
\centering
% Elapsed time: 3178255 microseconds
% Profiling data extracted from PMCs every 250ms:
\begin{tabular} {|r|r|r|r|r|r|}
\hline
\multicolumn{1}{|c|}{nsample} & \multicolumn{1}{c|}{pid} & \multicolumn{1}{c|}{event} & \multicolumn{1}{c|}{pmc0} & \multicolumn{1}{c|}{pmc3}  & \multicolumn{1}{c|}{pmc4} \\ \hline
      1  & 7558    &   tick  &   629554817    &    555265    &    339547 \\ \hline
      2  & 7558    &   tick  &   365243640    &   2111969    &    967323 \\ \hline
      3  & 7558    &   tick  &   363263873    &   2174515    &    943288 \\ \hline
      4  & 7558    &   tick  &   366034887    &   2190378    &    888714 \\ \hline
      5  & 7558    &   tick  &   361822568    &   2208562    &    914895 \\ \hline
      6  & 7558    &   tick  &   361998147    &   2201110    &    893159 \\ \hline
      7  & 7558    &   tick  &   358977538    &   2206190    &    879025 \\ \hline
      8  & 7558    &   tick  &   376751462    &   2220617    &    815036 \\ \hline
      9  & 7558    &   tick  &   371586535    &   2229520    &    828087 \\ \hline
     10  & 7558    &   tick  &   371069310    &   2196560    &    795315 \\ \hline
     11  & 7558    &   tick  &   376280116    &   2186783    &    740499 \\ \hline
     12  & 7558    &   tick  &   388247900    &   2161197    &    641935 \\ \hline
     13  & 7558    &   self  &   341342501    &   1586504    &    322759 \\ \hline
\end{tabular}
\end{table}

Los resultados obtenidos se encuentran en las tablas \ref{tab:gloBin} y \ref{tab:gloFib}. Lo primero que podemos apreciar es que el montículo de Fibonacci tiene 13 muestras o *ticks* y el binario solo dos puesto que, como dijimos antes, el montículo binario es siete veces más rápido en este caso. Si sumamos los valores de todas las muestras, aproximadamente obtenemos los siguientes datos:

* 1150 millones de instrucciones el montículo binario y 5000 el de Fibonacci (casi cinco veces más instrucciones el montículo de Fibonacci). Probablemente debido a la mayor complejidad de las operaciones que realiza el montículo de Fibonacci.

* 7,5 millones de accesos a memoria caché en el binario y 25 millones en el de Fibonacci; por tanto, tres veces más accesos a caché por el montículo de Fibonacci. Como vemos, aunque el tamaño de los datos de entrada es el mismo --un millón de enteros--, el montículo de Fibonacci tiene que acceder muchas más veces a memoria caché de último nivel.

* 0.4 millones de fallos a memoria caché de último nivel por el montículo binario y 10.5 millones por el montículo de Fibonacci. Aquí podemos comprobar como, efectivamente, la diferencia de fallos de acceso a la memoria caché es abismal, más de 20 veces más fallos en la memoria caché tiene el montículo de Fibonacci frente al montículo binario.

Resulta también de gran relevancia calcular la tasa de fallos de la memoria caché, esta sería de un 5,33\% en el caso del montículo binario, y de un 42\% en el caso del montículo de Fibonacci. De nuevo, una diferencia muy significativa.

Por tanto, todo apunta a que esta gran diferencia en el número de accesos a memoria caché y, sobre todo, en sus porcentajes de aciertos, hace muy superior en la práctica al montículo binario frente al montículo de Fibonacci, a pesar de que la teoría predijera lo contrario.

\subsection{Segundo análisis}

No obstante, podemos afinar aún más y obtener mayor información. Revisando el análisis anterior, observamos que la primera muestra del montículo de fibonacci no está equilibrada con el resto de muestras: ejecuta el doble de instrucciones que el resto, y, sin embargo, hace muchos menos accesos a memoria; lo que nos lleva a pensar que podría haber una fase inicial en las que el montículo invierta menos tiempo y menos acceso a recursos que el resto. Para comprobar esto, también mediante libpmctrack podemos monitorizar fragmentos de código aislados.

Para ello, situamos tres bloques \texttt{pmctrack\_start\_counters()}/\texttt{pmctrack\_stop\_counters()} en torno a tres partes clave de nuestro pequeño benchmark: uno para la inicialización del montículo, otro para la inserción del millón de números y un tercero para la eliminación de éstos. Estas tres partes se corresponderían con tres fases o etapas diferentes de operaciones con la estructura de datos. Además, puesto que las franjas de start y stop ahora son suficientemente pequeñas, también cambiamos la configuración para que no se haga captura de muestras por tiempo, fijando el timeout a 0, y tener de esta manera todos los datos de cada fase en una sola muestra.\newline
Los resultados los podemos ver en las tablas \ref{tab:fragsBin} y \ref{tab:fragsFib}.

\begin{table}[h]
\caption{Resultados monitorización por fases montículo binario}
\label{tab:fragsBin}
\centering
\begin{tabular} {|c|r|r|r|r|r|r|}
\hline

%Profiling, through libpmctrack, cache behaviour when using a William's heap.

\multicolumn{1}{|c|}{stage} & \multicolumn{1}{c|}{nsample} & \multicolumn{1}{c|}{pid} & \multicolumn{1}{c|}{event} & \multicolumn{1}{c|}{pmc0} & \multicolumn{1}{c|}{pmc3}  & \multicolumn{1}{c|}{pmc4} \\ \hline
%stage    nsample    pid      event          pmc0          pmc3          pmc4
  initialization  &  1  & 13464   &    self     &      833     &       10      &       7 \\ \hline
  insertion  &  1 & 13464    &   self   &  194528249       &  19764     &    17205 \\ \hline
  deletion & 1 & 13464   &    self   &  916232599   &    7383241     &   467662 \\ \hline
%Elapsed time: 229741 microseconds
\end{tabular}
\end{table}


\begin{table}[h]
\caption{Resultados monitorización por fases montículo Fibonacci}
\label{tab:fragsFib}
\centering

%Profiling, through libpmctrack, cache behaviour when using a Fibonacci's heap.

\begin{tabular} {|c|r|r|r|r|r|r|}
\hline
\multicolumn{1}{|c|}{stage} & \multicolumn{1}{c|}{nsample} & \multicolumn{1}{c|}{pid} & \multicolumn{1}{c|}{event} & \multicolumn{1}{c|}{pmc0} & \multicolumn{1}{c|}{pmc3}  & \multicolumn{1}{c|}{pmc4} \\ \hline
%stage nsample    pid      event          pmc0          pmc3          pmc4
  initialization &  1 & 13271    &   self     &      835      &      11     &       10 \\ \hline
  insertion &  1 & 13271    &   self   &  377048052    &     15204      &    9962 \\ \hline
  deletion  &  1 & 13271    &   self   & 4655118486    &  37307044  &    14266564 \\ \hline
%Elapsed time: 1692031 microseconds
\end{tabular}
\end{table}

Con estos nuevos datos, podemos ver claramente que la fase de inicialización y reserva inicial de memoria es prácticamente la misma para ambas estructuras en cuanto a número de instrucciones y acceso a memoria.

En la fase de inserción, la diferencia tampoco es demasiado grande, de hecho, aunque el montículo de Fibonacci realiza más instrucciones, efectivamente cumple su teoría en cuanto a que ejecuta menos accesos a memoria y éstos son más exitosos que el montículo binario.

La gran diferencia llega en la última fase, la fase de borrado de elementos, en ésta el número de instrucciones ejecutadas es mucho mayor para ambos montículos. Es en esta fase cuando el montículo de Fibonacci se dispara en cuanto a número de accesos a memoria y la tasa de fallos es tan alta como el 40\% mencionado anteriormente, eclipsando cualquier buen resultado que se podía haber obtenido en fases anteriores; mientras que el montículo binario, mantiene una buena tasa de fallos y un número de accesos relativamente mucho menor.

\subsection{Conclusiones}

Después de un primer análisis global y, posteriormente, un segundo análisis pormenorizando el benchmark en tres fases clave. Hemos comprobado, gracias a la librería libpmctrack, como la estructura de datos montículo o *heap* puede tener un rendimiento muy diferente en el borrado, según si la implementación hace uso de memoria dinámica o, por el contrario, hace uso de memoria estática.

En general, con este caso de estudio observamos que el uso de memoria dinámica para la implementación de estructuras de datos puede perjudicar en gran medida sus tiempos de ejecución, debido a la jerarquía de acceso a la memoria que existe en las computadoras actuales.\newline
Debemos de aclarar, no obstante, que este análisis se ha realizado con tipos primitivos (enteros) como elementos contenidos en la estructura de datos. Los resultados tendrían que ser revisados si dichos elementos fuesen objetos o punteros a otras estructuras, lo cual estropearía la ventaja que tiene el montículo binario gracias a la localidad espacial de sus elementos.
