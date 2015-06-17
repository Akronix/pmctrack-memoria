\chapter{Dependencias software de PMCTrack-GUI}
\label{app:DependenciasSW}

En el presente apéndice se adjunta el listado de dependencias software de PMCTrack-GUI para que se puedan utilizar todas sus funcionalidades. Adicionalmente, se incluye una pequeña guía de instalación de todas estas dependencias para los sistemas operativos Debian/Ubuntu y MacOS X. 

PMCTrack-GUI cuenta con un total de cuatro dependencias software que enumeramos a continuación:

* Python v2.7
* Matplotlib
* Comando sshpass
* WxPython v2.8 o superior.

# Instalación de las dependencias software en MacOS X

Para la instalación de los requisitos software de PMCTrack-GUI en el sistema operativo MacOS X basta con ejecutar los siguientes comandos en una terminal:

\usepackage{pythontex}
\setpygmentspygopt{bash}{style=default} %Set syntax highlighting style
\setpygmentsfv{xleftmargin=4ex}
%\begin{lstlisting}[language=bash,basicstyle=\tt\scriptsize]
%\begin{lstlisting}[frame=single,language=]
\noindent Block use:
\begin{pygments}{bash}
  $ sudo port upgrade outdateda
  $ sudo port install py27-matplotlib py27-numpy py27-scipy py27-ipython py27-wxpython-2.8 sshpass
  $ sudo port install 
  $ mkdir  ~/.matplotlib
  $ cp /opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/matplotlib/mpl-data/matplotlibrc  ~/.matplotlib
  $ sudo port select --set python python27
  $ sudo port select --set ipython ipython27
  $ which python
\end{pygments}

# Instalación de las dependencias software en Debian/Ubuntu

Para la instalación de los requisitos software de PMCTrack-GUI en los sistemas operativos basados en Debian basta con ejecutar los siguientes comandos en una terminal:

\begin{lstlisting}[language=bash,basicstyle=\tt\scriptsize]
$ sudo apt-get update
$ sudo apt-get install python-wxgtk2.8 python-matplotlib sshpass
\end{lstlisting}
