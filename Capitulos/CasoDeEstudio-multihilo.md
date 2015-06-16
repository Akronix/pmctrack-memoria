En esta sección ponemos a prueba la aplicación PMCTrack-GUI desarrollada en este TFG para monitorizar el rendimiento de aplicaciones multihilo. En este caso de estudio nos interesa estudiar el comportamiento de los hilos de dos aplicaciones paralelas muy diferentes. La primera aplicación es `rnaseq`, un benchmark OpenMP de bioinformática. En esta aplicación OpenMP regular, los hilos realizan esencialmente el mismo cómputo sobre distintos datos. La segunda aplicación considerada es `ferret`, que pertenece a la suite de benchmarks PARSEC v1.3 \cite{parsec}. Esta aplicación POSIX threads sigue el paradigma de programación paralela tipo _pipeline_. En este paradigma, la aplicación consta de distintos tipos de hilos; cada tipo de hilo se ocupa de realizar una fase de procesamiento y el resultado que genera sirve como de entrada para otro tipo de hilo que se encarga de realizar otra fase de procesamiento. En la aplicación `ferret` se espera que el paradigma tipo _pipeline_ se refleje en distintos perfiles de rendimiento para cada tipo de hilo, debido al distinto tipo de procesamiento que realizan.

\begin{figure}[tbp]
    \centering
    \subfloat[]{\includegraphics[width=0.8\textwidth]{Imagenes/Bitmap/rnaseq_27880}\label{fig:rnaseq_27880}}%
    \qquad
    \subfloat[]{\includegraphics[width=0.8\textwidth]{Imagenes/Bitmap/rnaseq_27881}\label{fig:rnaseq_27881}}%
\caption{Gráficas de rendimiento asociadas a los hilos con PID 27880 (arriba) y 27881 (abajo) de la aplicación \texttt{rnaseq}.}%
\label{fig:rnaseq}%
\end{figure}


<!-- \begin{figure}[tbp]
\centering
\includegraphics[width=0.6\textwidth]{Imagenes/Bitmap/rnaseq_27880}
\caption{Gráficas de rendimiento asociadas al hilo con PID 27880 de la aplicación \texttt{rnaseq}.} \label{fig:rnaseq_27880}
\end{figure}

\begin{figure}[tbp]
\centering
\includegraphics[width=0.6\textwidth]{Imagenes/Bitmap/rnaseq_27881}
\caption{Gráficas de rendimiento asociadas al hilo con PID 27881 de la aplicación \texttt{rnaseq}.} \label{fig:rnaseq_27881}
\end{figure}
 -->

 \begin{figure}[tbp]
    \centering
    \subfloat[]{\includegraphics[width=0.8\textwidth]{Imagenes/Bitmap/ferret_27774}\label{fig:ferret_27774}}%
    \qquad
    \subfloat[]{\includegraphics[width=0.8\textwidth]{Imagenes/Bitmap/ferret_27777}\label{fig:ferret_27777}}%
\caption{Gráficas de rendimiento asociadas a los hilos con PID 27774 (arriba) y 27777 (abajo) de la aplicación \texttt{ferret}.}%
\label{fig:ferret}%
\end{figure}



En nuestro estudio ejecutamos ambas aplicaciones con cuatro hilos en el sistema con el procesador Intel Xeon ``Haswell'' usado también en el caso de estudio previo, y cuyas especificaciones técnicas se detallan en la tabla \ref{tab:morcuera}. Usando PMCTrack-GUI empleando el modo SSH hemos monitorizado las dos aplicaciones paralelas, configurando la herramienta para que muestre las gráficas de rendimiento en tiempo real de dos métricas: instrucciones por ciclo del procesador (_IPC_) y fallos del último nivel de caché por cada mil instrucciones retiradas (_LLCMR_). Puesto que PMCTrack-GUI permite visualizar las gráficas de cada hilo individual de la aplicación, podemos comparar el comportamiento de estas dos aplicaciones analizando las gráficas de rendimiento de cada uno de sus respectivos hilos. Las figuras \ref{fig:rnaseq} y \ref{fig:ferret} muestran los resultados obtenidos.


Centrándonos en la aplicación \texttt{rnaseq}, hemos escogido las gráficas de rendimiento de dos de sus hilos, pudiéndose visualizar en las figuras \ref{fig:rnaseq_27880} y \ref{fig:rnaseq_27881}. Comparando las gráficas de los dos hilos de la aplicación observamos que, a pesar de que no se tratan de las mismas gráficas, los resultados obtenidos son muy parecidos cuantitativamente hablando en cuanto a IPC y tasa de fallos de último nivel de caché. Además, podemos observar que ambos hilos atraviesan fases de ejecución muy similares. Estos resultados son perfectamente razonables ya que todos los hilos de la aplicación paralela realizan el mismo procesamiento con distintos datos.  

Al igual que en la aplicación \texttt{rnaseq}, para la aplicación \texttt{ferret} también hemos escogido las gráficas de rendimiento de dos de sus hilos. Las gráficas de estos hilos se pueden visualizar en las figuras \ref{fig:ferret_27774} y \ref{fig:ferret_27777}. En este caso, los resultados revelan patrones de rendimiento muy diferentes en ambos hilos. El hilo con PID 27774 (figura \ref{fig:ferret_27774}) ejecuta de media algo más de 2 instrucciones por ciclo, mientras que el hilo con PID 27777 (figura \ref{fig:ferret_27777}) ejecuta entre 1 y 1,5 instrucciones por ciclo. El primer hilo por tanto está ejecutando entre un 50 y un 100% de instrucciones por ciclo más que el segundo hilo. En el caso de la segunda métrica (LLCMR) la diferencia de resultados entre los dos hilos en aún más notoria, el hilo con PID 27774 apenas tiene fallos de caché de último nivel (de 0,13 a 0,35 fallos por cada 1000 instrucciones retiradas), mientras que el hilo con PID 27777 tiene entre 1,5 y 3 fallos. El segundo hilo por tanto tiene de media 9 veces más fallos de caché de último nivel que el primero. De estos resultados podemos concluir que en la ejecución del hilo 27777 se realizan muchos más accesos a memoria que en el hilo 27774. Estas diferencias sustanciales en el patrón de rendimiento de ambos hilos se deriva del hecho de que realizan procesamientos muy diferentes en el contexto de la aplicación paralela tipo _pipeline_.


