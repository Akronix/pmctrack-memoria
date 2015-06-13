#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import math
import os.path
import sys

def processFile(csvfile):
    data = {}
    benchs = []

    file = open(csvfile, 'r')
    line_metrics = file.readline().split(",")
    line_archs = file.readline().split(",")

    for i in range(1, len(line_metrics)):
	metric = line_metrics[i]
	arch = line_archs[i]
	if i == len(line_metrics) - 1:
		metric = metric.replace('\n', '')
		arch = arch.replace('\n', '')
	if not data.has_key(metric):
		data[metric] = {}
	if not data[metric].has_key(arch):
		data[metric][arch] = []

    for line in file:
        info_line = line.split(",")
	for i in range(len(info_line)):
		if i == 0:
			benchs.append(info_line[0])
		elif i == len(info_line) - 1:
			data[line_metrics[i].replace('\n', '')][line_archs[i].replace('\n', '')].append(float(info_line[i].replace('\n', '')))
		else:
			data[line_metrics[i]][line_archs[i]].append(float(info_line[i]))
    file.close()
    return data, benchs

def printGraphs(data, benchs):
    bars = []
    ind = np.arange(len(benchs))
    width = 0.15
    colors = [ "#A8E1ED","#EAF03E","#DB3055","#cccccc","#125580","#7fc7ae"]
    #colors = ["royalblue", "crimson", "gold", "lime", "deeppink", "deepskyblue", "lawngreen", "lightsalmon"]
    n_metric= 0

    for metric in data.keys():
    	fig, ax = plt.subplots()
    	#fig.subplots_adjust(left=0.09, right=0.93, top=0.94, bottom=0.06)
        fig.subplots_adjust(left=0.08, right=0.90, top=0.73, bottom=0.10, wspace=0.2, hspace=0.2)
   
    	i=0
    	for arch in data[metric].keys():
    	    bars.append(ax.bar(ind+(i*width), data[metric][arch], width, color=colors[i]))
    	    i+=1
    	
    	ax.set_ylabel(metric)
    	#ax.set_ybound(upper=50)
        ax.yaxis.grid(True)
    	ax.set_xticks(ind+((i/2.0)*width))
    	ax.set_xticklabels(benchs)
    	
    	ax.legend( bars, data[metric].keys(), bbox_to_anchor=(0., 1.1, 1., .101) ,  ncol=3, mode="expand", borderaxespad=0)
    	plt.show(block=(n_metric == len(data) - 1))
	n_metric += 1

if len(sys.argv) != 2:
    print "Usage:", sys.argv[0], "<CSV Bar data file>"
elif not os.path.isfile(sys.argv[1]):
    print "Error: Csvfile not exists."
else:
    (data, benchs) = processFile(sys.argv[1])
    printGraphs(data, benchs)
