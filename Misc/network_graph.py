#*******************************************************************************
#* 
#* File: network_graph.py
#* 
#* Author: Alex Snyder
#* Email: alexetsnyder@gmail.com
#* 
#* Date: 09/07/2016
#* 
#* Description: Takes a file of traceroute data and turns 
#* 				it into a directed graph, then it uses a 
#*				couple of python librarys to draw it to the 
#*				screen.
#*
#* Command Line Argument(s): <file_name>.txt : Traceroute data file
#* 
#*******************************************************************************

import sys
import re
import networkx as nx 
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

enn = '[0-9]+'
dot = '\.'

ip_str = enn + dot + enn + dot + enn + dot + enn
dns_str = '^[0-9a-zA-Z\-\.]*[a-zA-Z]'
time_str = '[0-9]+\.[0-9]* ms'

num_re = re.compile('^[1-9][0-9]*')
unre_re = re.compile('\* \* \*')
dns_re = re.compile(dns_str)
ip_re = re.compile(ip_str)
time_re = re.compile(time_str)

class Node:
	def __init__(self, dns, ip, time):
		self.dns = dns
		self.ip = ip 
		self.time = time

	def __eq__(self, other):
		if (other == None):
			return False
		if self.ip == other.ip:
			#Don't want to add node again, but must have minimum time
			self.time = min(self.time, other.time)
			return True
		return False

	def __str__(self):
		if self.dns == '':
			return self.ip + '\n' + self.time
		return self.dns + '\n' + self.time

def contains(node, nodeList):
	for n in nodeList:
		if n[0] == node:
			return True
	return False

def indexOf(node, nodeList):
	for i in range(len(nodeList)):
		if nodeList[i][0] == node:
			return i
	return -1

def printGraph(nodeList):
	for l in nodeList:
		print('[', end='')
		for n in l:
			print ('[' + str(n) + '] ', end='')
		print(']')

def retrieve(match):
	if match == None:
		return ''
	return match.group(0)

def parse_line(line):
	ip_match = ip_re.findall(line)
	dns_match = dns_re.search(line)
	if len(ip_match) == 3 or (len(ip_match) == 2 and not dns_match == None):
		time_match = time_re.search(line)
		return Node(retrieve(dns_match), ip_match[0], retrieve(time_match))
	elif len(ip_match) == 2:
		time_match = time_re.findall(line)
		return Node(retrieve(dns_match), ip_match[0], min(time_match))
	elif len(ip_match) == 1:
		time_match = time_re.findall(line)
		return Node(retrieve(dns_match), ip_match[0], min(time_match))
	else:
		print("Error in parse line")
		sys.exit(1)

file_name = ''
if len(sys.argv) == 2:
	file_name = sys.argv[1]
else:
	print("Need to provide file name as command line argument.")
	sys.exit(1)

node_list = []
begin_flag = True
f1 = open(file_name, 'r')
lastNode = None

for line in f1:
	line = line.strip()
	match = num_re.search(line)	#Does line start with number
	unreported = unre_re.search(line) #Search for * * * line
	if match == None or not unreported == None:
		#Do nothing if it isn't a traceroute line or it is unreported (e.g. 12 * * * )
		continue
	else:
		line = line[len(match.group(0)):].strip() #Remove leading number
		if match.group(0) == '1': 
			begin_flag = True #Start of new traceroute data
		node = parse_line(line)
		if not contains(node, node_list):
			node_list.append([node])
			if not begin_flag:
				index = indexOf(lastNode, node_list)
				#Add edge between last node and current node
				node_list[index].append(node)
			else:
				begin_flag = False
		else:
			begin_flag = False
		lastNode  = node
f1.close()

#printGraph(node_list)

#Make networkx graph
G = nx.DiGraph()
for l in node_list:
	for i in range(1, len(l)):
 		G.add_edge(str(l[0]), str(l[i]))

#Draw networkx graph as a tree
#Must draw graphviz graph this way
#nx.draw_graphviz does not work.
pos = graphviz_layout(G)
nx.draw(G, pos, with_labels=True)
plt.show()