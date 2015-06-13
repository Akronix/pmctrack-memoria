
En este caso de estudio se ilustra el potencial de PMCTRack-GUI y PMCTrack en su conjunto para recabar información de rendimiento en distintas arquitecturas y diversos modelos de procesador. Para llevar a cabo nuestro estudio, seleccionamos un subconjunto de 9 benchmarks diversos de la _suite_ SPEC CPU2006 \cite{henning-spec2006} y los ejecutamos en múltiples plataformas que integran procesadores multicore de ARM, Intel y AMD. En particular, experimentamos con la placa de desarrollo Juno de ARM, que integra un procesador big.LITTLE \cite{arm-big-little}; y con tres servidores con arquitectura x86 que integran procesadores Intel Atom, Intel Xeon "Haswell" y AMD Opteron "Magny-Cours", respectivamente. La especificación detallada de las cuatro plataformas multicore exploradas se  
muestra en las tablas \ref{tab:quickia}-\ref{tab:morcuera}. Nótese que la plataforma de ARM integra un procesador asimétrico con 2 tipos de cores: Cortex-A57 ("big") y Cortex-A53 ("LITTLE"). En esta plataforma usamos PMCTrack para monitorizar el rendimiento en cada tipo de core.

<!--
http://ark.intel.com/products/35641/Intel-Atom-Processor-330-1M-Cache-1_60-GHz-533-MHz-FSB
-->

\begin{table}[t]
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

\begin{table}[t]
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

\begin{table}[t]
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


\begin{table}[t]
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

\begin{figure}[tbp]
\centering
\includegraphics[width=0.85\textwidth]{Imagenes/Vectorial/metric_2.pdf}
\caption{Número de fallos de último nivel de cache (LLC) por cada 1K instruciones retiradas para los distintos \textit{benchmarks}.\label{img:llcmr}}
\end{figure}

\begin{figure}[tbp]
\centering
\includegraphics[width=0.85\textwidth]{Imagenes/Vectorial/metric_0.pdf}
\caption{Número de fallos de predicción de saltos por cada 1K instruciones retiradas para los distintos \textit{benchmarks}.\label{img:mispred}}
\end{figure}