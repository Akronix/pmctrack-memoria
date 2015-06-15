En esta sección hemos puesto a prueba la aplicación PMCTrack-GUI desarrollada en este TFG para analizar dos aplicaciones multihilo. A diferencia del caso de estudio anterior, las monitorizaciones las hemos realizado sobre la misma computadora. En este caso de estudio nos interesa estudiar el comportamiento de los hilos de dos aplicaciones paralelas, sin tener en cuenta la arquitectura sobre la que son ejecutadas. Ambas aplicaciones constan de cuatro hilos. Sin embargo, en una aplicación, llamada \texttt{rnaseq}, los hilos realizan el mismo procesamiento usando diferentes datos, mientras que en la otra, llamada \texttt{ferret_p3}, los hilos cooperan entre sí realizando cada uno de ellos procesamientos diferentes.

Hemos monitorizado las dos aplicaciones usando PMCTrack-GUI, configurándolo para que muestre las gráficas de rendimiento en tiempo real de dos métricas: instrucciones por ciclo del procesador (IPC) y fallos del último nivel de cache por cada mil instrucciones retiradas (LLCMR), para cada una de las dos aplicaciones. Puesto que PMCTrack-GUI permite visualizar las gráficas de cada hilo individual de la aplicación, podemos comparar el comportamiento de estas dos aplicaciones analizando las gráficas de rendimiento de cada uno de sus respectivos hilos. Las figuras \ref{fig:ferret_27774}, \ref{fig:ferret_27777}, \ref{fig:rnaseq_27880} y \ref{fig:rnaseq_27881} revelan los resultados obtenidos.

\begin{figure}
\centering
\includegraphics[scale=0.55]{Imagenes/Bitmap/ferret_27774}
\caption{Gráficas de rendimiento asociadas al hilo con PID 27774 de la aplicación \texttt{ferret_p3}.} \label{fig:ferret_27774}
\end{figure}

\begin{figure}
\centering
\includegraphics[scale=0.55]{Imagenes/Bitmap/ferret_27777}
\caption{Gráficas de rendimiento asociadas al hilo con PID 27777 de la aplicación \texttt{ferret_p3}.} \label{fig:ferret_27777}
\end{figure}

Centrándonos en la aplicación \texttt{ferret_p3}, hemos escogido las gráficas de rendimiento de dos de sus hilos, pudiéndose visualizar en las figuras \ref{fig:ferret_27774} y \ref{fig:ferret_27777} (cada figura muestra las gráficas de un hilo). Si comparamos las gráficas de cada hilo que representan la métrica IPC, podemos observar que los resultados mostrados son notablemente diferentes. El hilo con PID 27774 (figura \ref{fig:ferret_27774}) ejecuta de media algo más de 2 instrucciones por ciclo, mientras que el hilo con PID 27777 (figura \ref{fig:ferret_27777}) ejecuta entre 1 y 1,5 instrucciones por ciclo. El primer hilo por tanto está ejecutando entre un 50 y un 100% de instrucciones por ciclo más que el segundo hilo. En el caso de la segunda métrica (LLCMR) la diferencia de resultados entre los dos hilos en aún más notoria, el hilo con PID 27774 apenas tiene fallos de caché de último nivel (de 0,13 a 0,35 fallos por cada 1000 instrucciones retiradas), mientras que el hilo con PID 27777 tiene entre 1,5 y 3 fallos. El segundo hilo por tanto tiene de media 9 veces más fallos de caché de último nivel que el primero. De estos resultados podemos concluir que en la ejecución del hilo 27777 se realizan muchos más accesos a memoria que en el hilo 27774. Por tanto, los hilos de la aplicación \texttt{ferret_p3} realizan procesamientos diferentes.

\begin{figure}
\centering
\includegraphics[scale=0.55]{Imagenes/Bitmap/rnaseq_27880}
\caption{Gráficas de rendimiento asociadas al hilo con PID 27880 de la aplicación \texttt{rnaseq}.} \label{fig:rnaseq_27880}
\end{figure}

\begin{figure}
\centering
\includegraphics[scale=0.55]{Imagenes/Bitmap/rnaseq_27881}
\caption{Gráficas de rendimiento asociadas al hilo con PID 27881 de la aplicación \texttt{rnaseq}.} \label{fig:rnaseq_27881}
\end{figure}

Al igual que en la aplicación \texttt{ferret_p3}, para la aplicación \texttt{rnaseq} también hemos escogido las gráficas de rendimiento de dos de sus hilos. Las gráficas de estos hilos se pueden visualizar en sendas figuras \ref{fig:rnaseq_27880} y \ref{fig:rnaseq_27881}. Comparando las gráficas de los dos hilos de la aplicación observamos que, a pesar de que no se tratan de las mismas gráficas, los resultados obtenidos son muy parecidos. Además, podemos observar que los cambios de tendencia (ascendente o descendente) coinciden en las gráficas de los dos hilos. A la vista de estos resultados podemos concluir que los hilos de la aplicación \texttt{rnaseq}, al contrario que los de la aplicación \texttt{ferret_p3}, realizan el mismo procesamiento.
