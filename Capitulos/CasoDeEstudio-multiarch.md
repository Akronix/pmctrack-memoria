
<!-- En este caso de estudio se ilustra el potencial de PMCTrack-GUI y PMCTrack en su conjunto para recabar información de rendimiento mediante contadores hardware en distintas arquitecturas y diversos modelos de procesador. -->



Para llevar a cabo nuestro estudio, seleccionamos un subconjunto de 10 benchmarks diversos de la _suite_ SPEC CPU2006 \cite{henning-spec2006} y los ejecutamos en múltiples plataformas con procesadores multicore de ARM, Intel y AMD. En particular, experimentamos con la placa de desarrollo Juno de ARM, que integra un procesador big.LITTLE \cite{arm-big-little}; y con tres servidores con procesadores x86 (Intel Atom, Intel Xeon "Haswell" y AMD Opteron "Magny-Cours"). La especificación detallada de las cuatro plataformas multicore exploradas se muestra en las tablas \ref{tab:quickia}-\ref{tab:morcuera}. 



<!--
http://ark.intel.com/products/35641/Intel-Atom-Processor-330-1M-Cache-1_60-GHz-533-MHz-FSB
-->

\begin{table}[tbp]
\begin{center}
\footnotesize
\begin{tabular}[]{|c|c|}\hline
\textbf{Procesador}           &
\begin{tabular*}{9.3 cm}[c]{p{9.3 cm}|p{9.3 cm}}
\multicolumn{2}{c}{Intel\textregistered{} Atom\textregistered{} N330 @ 1.6 GHz}       \\ \hline
\multicolumn{1}{c|}{Numero total de cores}        &   \multicolumn{1}{c}{2} \\ \hline
\multicolumn{1}{c|}{Topología}        &  \multicolumn{1}{c}{1 chips, 1 \textit{die} por chip} \\ 
\multicolumn{1}{c|}{ }                &  \multicolumn{1}{c}{2 cores por \textit{die} compartiendo la L2} \\       
\multicolumn{1}{c|}{ }                &  \multicolumn{1}{c}{LLC (L2) de 1MB dividida entre cores}       \\ \hline  
\end{tabular*} \\ \hline
\textbf{Memoria}    & 16 GBytes  (DDR2)                                   \\
             				 &   Plataforma UMA                              \\ \hline
\end{tabular}
\end{center}
\caption{\label{tab:quickia} Características de la plataforma que integra un procesador Intel Atom.}
\end{table}


<!--
http://www.arm.com/products/tools/development-boards/versatile-express/juno-arm-development-platform.php
-->

\begin{table}[tbp]
\begin{center}
\footnotesize
\begin{tabular}[]{|c|c|}\hline
\textbf{Procesador}           &
\begin{tabular*}{9.3 cm}[c]{p{9.3 cm}|p{9.3 cm}}
\multicolumn{2}{c}{ARM\textregistered{} Big Little\textregistered{} Dual Cluster (ARM v8-A)}       \\ \hline
\multicolumn{1}{c|}{Numero total de cores}        &   \multicolumn{1}{c}{6 (divididos en dos \textit{clusters})} \\ \hline
\multicolumn{1}{c|}{Cluster Cortex-A57}        &  \multicolumn{1}{c}{2 cores ``big'' @ 1.10Ghz} \\ 
\multicolumn{1}{c|}{ }                &  \multicolumn{1}{c}{Cores comparten la L2 (2MB)} \\  \hline       
\multicolumn{1}{c|}{Cluster Cortex-A53}        &  \multicolumn{1}{c}{4 cores ``LITTLE'' @ 850 Mhz} \\ 
\multicolumn{1}{c|}{ }                &  \multicolumn{1}{c}{Cores comparten la L2 (1MB)} \\  \hline  
\end{tabular*} \\ \hline
\textbf{Memoria}    & 8 GBytes  (DDR3)                                   \\
             				 &   Plataforma UMA                              \\ \hline
\end{tabular}
\end{center}
\caption{\label{tab:juno} Características de la plataforma que integra un procesador ARM big.LITTLE.}
\end{table}


<!--
http://products.amd.com/en-us/OpteronCPUDetail.aspx?id=644&f1=&f2=&f3=Yes&f4=&f5=&f6=&f7=&f8=&f9=&f10=&f11=&
-->

\begin{table}[tbp]
\begin{center}
\footnotesize
\begin{tabular}[]{|c|c|}\hline
\textbf{Procesador}           &
\begin{tabular*}{9.3 cm}[c]{p{9.3 cm}|p{9.3 cm}}
\multicolumn{2}{c}{4x AMD\textregistered{} Opteron\textregistered{} 6172 @ 2.1 GHz}       \\ \hline
\multicolumn{1}{c|}{Numero total de cores}        &   \multicolumn{1}{c}{48} \\ \hline
\multicolumn{1}{c|}{Topología}        &  \multicolumn{1}{c}{4 chips, 2 \textit{dies} por chip} \\ 
\multicolumn{1}{c|}{ }                &  \multicolumn{1}{c}{6 cores por \textit{die} compartiendo la L3} \\       
\multicolumn{1}{c|}{ }                &  \multicolumn{1}{c}{LLC (L3) de 12 MB}       \\ \hline  
\end{tabular*} \\ \hline
\textbf{Memoria}    & 32 GBytes  (DDR3)                                   \\
             				 &   Plataforma NUMA                              \\ \hline
\end{tabular}
\end{center}
\caption{\label{tab:morcuera} Características de la plataforma que integra un procesador AMD Opteron ``Magnycours''.}
\end{table}

<!--
http://ark.intel.com/products/75461/Intel-Xeon-Processor-E3-1225-v3-8M-Cache-3_20-GHz
-->	


\begin{table}[tbp]
\begin{center}
\footnotesize
\begin{tabular}[]{|c|c|}\hline
\textbf{Procesador}           &
\begin{tabular*}{9.3 cm}[c]{p{9.3 cm}|p{9.3 cm}}
\multicolumn{2}{c}{Intel\textregistered{} Xeon\textregistered{} E3-1225 v3 @ 3.2GHz}       \\ \hline
\multicolumn{1}{c|}{Numero total de cores}        &   \multicolumn{1}{c}{4} \\ \hline
\multicolumn{1}{c|}{Topología}        &  \multicolumn{1}{c}{1 chip, 1 \textit{die} por chip} \\ 
\multicolumn{1}{c|}{ }                &  \multicolumn{1}{c}{4 cores por \textit{die} compartiendo la L3} \\       
\multicolumn{1}{c|}{ }                &  \multicolumn{1}{c}{LLC (L3) de 8 MB}       \\ \hline  
\end{tabular*} \\ \hline
\textbf{Memoria}    & 32 GBytes  (DDR3)                                   \\
             				 &   Plataforma UMA                              \\ \hline
\end{tabular}
\end{center}
\caption{\label{tab:morcuera} Características de la plataforma que integra un procesador Intel Xeon ``Haswell''.}
\end{table}


\begin{figure}[tbp]
\centering
\includegraphics[width=0.85\textwidth]{Imagenes/Vectorial/metric_1.pdf}
\caption{Número de instrucciones retiradas por ciclo (IPC) para los distintos \textit{benchmarks}.\label{img:ipc}}
\end{figure}


Las figuras \ref{img:ipc}, \ref{img:llcmr} y \ref{img:mispred} muestran respectivamente el número de instrucciones por ciclo (IPC) medio, el número de fallos de último nivel de caché (LLC) y el número de fallos de predicción de saltos por cada mil instrucciones retiradas para los *benchmarks* seleccionados en los distintos tipos de core\footnote{Nótese que la plataforma de ARM integra un procesador asimétrico con 2 tipos de cores: Cortex-A57 ("big") y Cortex-A53 ("LITTLE"). Por lo tanto, para cada \textit{benchmark} recabamos las métricas de rendimiento en cada tipo de core por separado.} usados en nuestro estudio. El IPC constituye una métrica global del rendimiento de una aplicación secuencial en una determinada plataforma, mientras que las otras dos métricas pueden permitir explicar la disminución del rendimiento de una aplicación debido a paradas en el *pipeline* del procesador. Típicamente, a mayor número de fallos de caché o fallos de prediccion de saltos, menor rendimiento experimentará la aplicación en cuestión tanto en procesadores con *pipeline* con ejecución en orden, como el Intel Atom, o con ejecución fuera de orden, como el AMD Opteron.

Para monitorizar las métricas de rendimiento consideradas, empleamos la herramienta PMCTrack-GUI desarrollada en este TFG. Más concretamente, hicimos uso del modo de monitorización remoto de esta herramienta (por SSH) para obtener los datos de las múltiples plataformas desde un PC de escritorio. PMCTrack-GUI no solo simplifica de forma sustancial la configuración de eventos hardware y automatiza la representación gráfica de métricas de rendimiento, sino que también permite almacenar los resultados obtenidos para su posterior procesamiento. En particular, después de la ejecución de cada benchmark en cada plataforma, PMCTrack-GUI genera un fichero de texto con los resultados con las cuentas de eventos hardware obtenidos a lo largo del tiempo. Los datos que se muestran en las figuras \ref{img:ipc}, \ref{img:llcmr} y \ref{img:mispred} se han obtenido procesando la información almacenada en esos ficheros de texto y capturando la media de cada métrica para la ejecución completa de cada aplicación.



\begin{figure}[tbp]
\centering
\includegraphics[width=0.85\textwidth]{Imagenes/Vectorial/metric_2.pdf}
\caption{Número de fallos de último nivel de caché (LLC) por cada 1K instrucciones retiradas para los distintos \textit{benchmarks}.\label{img:llcmr}}
\end{figure}

Los resultados revelan que los programas `astar`, `gcc`, `mcf`, `soplex` y `xalancbmk` son intensivos en memoria. Como se observa en la figura \ref{img:llcmr} estos benchmarks realizan un número elevado de accesos a memoria (fallos de último nivel de caché) por cada mil instrucciones en todas las plataformas exploradas. En particular, `mcf`, la aplicación con mayor tasa de fallos de caché, es también la que obtiene un menor número de instrucciones por ciclo, seguida de cerca por otras dos aplicaciones intensivas en memoria como `astar` y `soplex`. 

\begin{figure}[tbp]
\centering
\includegraphics[width=0.85\textwidth]{Imagenes/Vectorial/metric_0.pdf}
\caption{Número de fallos de predicción de saltos por cada 1K instrucciones retiradas para los distintos \textit{benchmarks}.\label{img:mispred}}
\end{figure}
 
Los datos obtenidos también revelan que otros benchmarks que podemos considerar *intensivos en CPU*, por su baja tasa de fallos de LLC, exhiben un IPC relativamente reducido, y comparable al de *benchmarks* intensivos en memoria. Este es el caso de las aplicaciones `bzip2` y `gobmk`. La figura \ref{img:mispred} ilustra que estas aplicaciones sufren de numerosos fallos de predicción de saltos, lo cual puede derivar en frecuentes paradas del *pipeline* del procesador. Este efecto explica el bajo valor de IPC observado en todas las plataformas para estas aplicaciones. 

Finalmente, cabe destacar que aquellas aplicaciones con mayores valores de IPC en todas las plataformas (`calculix`, `h264ref` y `hmmer`) tienen asociado, como cabía esperar, una baja tasa de fallos de caché de último nivel y un número reducido de fallos de predicción de saltos. 


<!--
- Métricas: IPC, LLC-miss-rate (LLC misses*1000)/instrucciones , Fallos de Predicción de Saltos (Branch mispredicions*1000)/instrucciones
-->

