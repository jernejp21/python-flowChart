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
import jaconv
from graphviz import Digraph, Graph

filePath = r'C:\Sluzba\git_test\python-flowChart\src\dummy2.c'
functionName = 'dinputp'

with open(filePath, 'r', encoding='utf-8') as file:
    testFunction = file.readlines()

#List of special words, representing reference comments.
refComment = ['fc:startStop',
              'fc:process',
              'fc:ifBranch',
              'fc:else',
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
            description = re.sub('[/*\n\t]', '', line[end + 1:])
            description1 = jaconv.zen2han(description, ascii=True, kana=False)
            description2 = re.split('"', description1)
            if len(description2) == 1:
                description3 = description2[0].replace(' ', '\n')
            elif len(description2) == 0:
                description3 = ''
            else:
                #Remove all empty strings
                description2 = [x for x in description2 if x != '']
                #Remove all ' ' strings (space)
                description2 = [x for x in description2 if x != ' ']
                if len(description2) == 1:
                    description3 = description2[0]
                else:
                    #We are left with only 2 strings. We merge them an place newline in between.
                    description3 = description2[0] + '\n' + description2[1]
                
            dictionary = {'comment': comment,
                          'level': None, 'index': None, 'shape': None, 'label': description3,
                          'connectWith': None}
            flow.append(dictionary)


g = Graph('G', filename=functionName, engine='dot')
g.attr(rank='same')
g.attr(rankdir='LR')
#g.attr(splines='ortho')
g.graph_attr = {'fontname': 'MS Gothic',
               'fontsize': '10',}
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
connectWith = None
branches = []
for element in flow:
    elementID = element['comment']
    if elementID == 'fc:end':
        level -= 1
        connectWith = branches[-1]
        del(branches[-1])
        continue
    if elementID == 'fc:else':
        connectWith = branches[-1]
        continue
    element['level'] = level
    element['index'] = index
    element['shape'] = shapes[elementID]
    element['connectWith'] = connectWith
    connectWith = index

    if elementID == 'fc:ifBranch' or elementID == 'fc:forLoop':
        level += 1
        branches.append(index)
    if level > maxLvl:
        maxLvl = level
    nodes.append(dict(element))
    index += 1

#Create level structure
for level in range(1, maxLvl + 1):
    g1 = Graph(str(level))
    for node in nodes:
        if node['level'] == level:
            index = str(node['index'])
            label = node['label']
            shape = node['shape']
            comment = node['comment']
            if comment == 'fc:startStop':
                g1.node(index,
                        label=label,
                        image=shape,
                        width="1.299",
                        height="0.394")
            else:
                g1.node(index,
                        label=label,
                        image=shape)
    g.subgraph(g1)

#Connect nodes
previousLevel = 1
branches = []
label = ''
for node in nodes:
    connectWith = node['connectWith']
    index = node['index']
    comment = node['comment']

    if connectWith == None:
        continue
    else:
        g.edge(str(connectWith), str(index), label=label)

    if comment == 'fc:ifBranch':
        label = 'TRUE'
    elif comment == 'fc:else':
        label = 'FALSE'
    elif comment == 'fc:forLoop':
        label = 'loop'
    else:
        label = ''

g.view()

print('konec')