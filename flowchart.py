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

filePath = r'C:\Sluzba\git_test\python-flowChart\src\dummy.c'
functionName = 'dinputp'

with open(filePath, 'r', encoding='utf-8') as file:
    testFunction = file.readlines()

#List of special words, representing reference comments.
refComment = ['fc:startStop',
              'fc:process',
              'fc:ifBranch',
              'fc:forLoop',
              'fc:subFunc',
              'fc:subRoutine',
              'fc:middleware',
              'fc:end']

flow = []

for line in testFunction:
    for comment in refComment:
        if comment in line:
            #start and end index of refComment
            start, end = re.search(comment, line).span()
            description = re.sub('[/* \n\t]', '', line[end:])
            flow.append({comment: description})


g = Graph('G', filename=functionName, engine='dot')
g.attr(rank='same')
g.attr(rankdir='LR')
g.attr(splines='ortho')
g.node_attr = {'shape': 'plaintext',
               'fontname': 'MS Gothic',
               'fontsize': '10',
               'fixedsize': 'true',
               'width': '2.165', #inch
               'height': '0.472'} #inch

shapes={'fc:startStop': 'daido_start.png',
        'fc:process': 'daido_process.png',
        'fc:ifBranch': 'daido_if.png',
        'fc:forLoop': 'daido_for.png',
        'fc:subFunc': 'daido_subfunction.png',
        'fc:subRoutine': 'daido_subroutine.png',
        'fc:middleware': 'daido_middleware.png'}

nodes = []
node = {'level': None, 'index': None, 'shape': None, 'label': None}
index = 0
level = 1
maxLvl = 1
for element in flow:
    elementID = list(element)[0]
    if elementID == 'fc:end':
        level -= 1
        continue
    node['level'] = level
    node['index'] = index
    node['shape'] = elementID
    node['label'] = element[elementID]
    nodes.append(dict(node))

    if elementID == 'fc:ifBranch' or elementID == 'fc:forLoop':
        level += 1
    if level > maxLvl:
        maxLvl = level
    index += 1

#Create level structure
for level in range(1, maxLvl + 1):
    g1 = Graph(str(level))
    for node in nodes:
        if node['level'] == level:
            index = str(node['index'])
            label = node['label']
            shape = node['shape']
            #g1.attr('node', image=shape)
            if shape == 'fc:startStop':
                g1.node(index,
                        label=label,
                        image=shapes[shape],
                        width="1.299",
                        height="0.394")
            else:
                g1.node(index,
                        label=label,
                        image=shapes[shape])
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