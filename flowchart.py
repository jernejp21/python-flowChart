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