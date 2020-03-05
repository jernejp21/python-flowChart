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
              'middleware']

flow = []

for line in testFunction:
    for comment in refComment:
        if comment in line:
            #start and end index of refComment
            start, end = re.search(comment, line).span()
            description = re.sub('[/* \n\t]', '', line[end:])
            flow.append({comment: description})


g = Digraph('G', filename='process', engine='neato')

shapes={'startStop': 'oval',
        'process': 'box',
        'ifBranch': 'diamond',
        'forLoop': 'component',
        'IO': 'cds',
        'subProc': 'folder',
        'middleware': 'tab'}

index = 0
for element in flow:
    elID = list(element)[0]
    shape = shapes[elID]
    g.attr('node', shape=shape, fontname="MS Gothic")
    g.node(str(index), label=element[elID])
    index += 1

for index in range(1, len(flow)):
    g.edge(str(index-1), str(index))

g.view()

print('konec')