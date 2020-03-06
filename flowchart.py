##
#    Python program for generating flow chart from source code.
#
#    Copyright (C) 2020  Jernej Pangerc; https://github.com/jernejp21
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

import re
from graphviz import Digraph, Graph

with open('test.c', 'r', encoding='utf-8') as file:
    testFunction = file.readlines()

#List of special words, representing reference comments.
refComment = ['startStop',
              'process',
              'ifBranch',
              'forLoop',
              'IO',
              'subProc',
              'middleware',
              'fc:end']

flow = []

for line in testFunction:
    for comment in refComment:
        if comment in line:
            #start and end index of refComment
            start, end = re.search(comment, line).span()
            description = re.sub('[/* \n\t]', '', line[end:])
            flow.append({comment: description})


g = Digraph('G', filename='process', engine='dot')
g.attr(rank='same')
g.attr(rankdir='LR')
g.node_attr = {'fontname': 'MS Gothic'}

shapes={'startStop': 'oval',
        'process': 'box',
        'ifBranch': 'diamond',
        'forLoop': 'component',
        'IO': 'cds',
        'subProc': 'folder',
        'middleware': 'tab'}
nodes = []
node = {'level': None, 'index': None, 'shape': None, 'label': None}
index = 0
level = 1
maxLvl = 1
for element in flow:
    elID = list(element)[0]
    if elID == 'fc:end':
        level -= 1
        continue
    shape = shapes[elID]
    node['level'] = level
    node['index'] = index
    node['shape'] = shape
    node['label'] = element[elID]
    nodes.append(dict(node))
    #g.attr('node', shape=shape, fontname="MS Gothic")
    #g.node(str(index), label=element[elID])
    if elID == 'ifBranch' or elID == 'forLoop':
        level += 1
    if level > maxLvl:
        maxLvl = level
    index += 1

#Create level structure
for level in range(1, maxLvl + 1):
    g1 = Digraph(str(level))
    for node in nodes:
        if node['level'] == level:
            index = str(node['index'])
            label = node['label']
            shape = node['shape']
            g1.attr('node', shape=shape)
            g1.node(index, label=label)
    g.subgraph(g1)

#Connect nodes
previousLevel = 1
branches = []
for index in range(1, len(nodes)):
    currentLevel = nodes[index]['level']
    if previousLevel == currentLevel:
        g.edge(str(index-1), str(index))
    if currentLevel > previousLevel:
        g.edge(str(index-1), str(index))
        branches.append(index-1)
    if currentLevel < previousLevel:
        levelDiff = currentLevel - previousLevel
        g.edge(str(branches[levelDiff]), str(index))
        del(branches[-1])
    
    previousLevel = currentLevel



#for index in range(1, len(flow)):
#    g.edge(str(index-1), str(index))

g.view()

print('konec')