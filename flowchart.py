##
#    Python program for generating flow chart from source code.
#
#    Copyright (C) 2020  Jernej Pangerc; https://github.com/jernejp21
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public Licence as published by
#    the Free Software Foundation, either version 3 of the Licence, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public Licence for more details.
#
#    You should have received a copy of the GNU General Public Licence
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

import re
import os
import argparse
from graphviz import Digraph, Graph


# ---------------Constants----------------------
# List of special words, representing reference comments.
REF_COMMENT = ['fc:startStop',
               'fc:process',
               'fc:ifBranch',
               'fc:else',
               'fc:forLoop',
               'fc:subFunc',
               'fc:subRoutine',
               'fc:middleware',
               'fc:end']

# List of shapes
SHAPES = {'fc:startStop': 'daido_start.png',
          'fc:process': 'daido_process.png',
          'fc:ifBranch': 'daido_if.png',
          'fc:forLoop': 'daido_for.png',
          'fc:subFunc': 'daido_subfunction.png',
          'fc:subRoutine': 'daido_subroutine.png',
          'fc:middleware': 'daido_middleware.png'}

# List of comments
COMMENTS = {'C': '/*',
            'python': '#'}

# CLI input arguments declaration
SOURCE = None
DEST = None
JAP = None
VIEW = None
FUNCS = None
LANG = None


# ---------------Functions-------------------------
def generateGraph(functionName, flow):
    g = Graph('G', filename=functionName, engine='dot')
    g.attr(rank='same')
    g.attr(rankdir='LR')
    g.graph_attr = {'fontname': 'MS Gothic',
                    'fontsize': '10', }
    g.node_attr = {'shape': 'plaintext',
                   'fontname': 'MS Gothic',
                   'fontsize': '10',
                   'fixedsize': 'true',
                   'width': '2.165',  # inch
                   'height': '0.472'}  # inch

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
            # If fc:end is in flow, we have to return one level back. This element
            # is empty element, no node is needed.
            level -= 1
            connectWith = branches[-1]
            del(branches[-1])
            continue
        if elementID == 'fc:else':
            connectWith = branches[-1]
            continue
        element['level'] = level
        element['index'] = index
        shapePath = os.path.split(os.path.abspath(__file__))[0]
        shape = os.path.join(shapePath, SHAPES[elementID])
        element['shape'] = shape
        element['connectWith'] = connectWith
        connectWith = index

        if elementID == 'fc:ifBranch' or elementID == 'fc:forLoop':
            # For loop and if we create branch which means going into new level.
            level += 1
            branches.append(index)
        if level > maxLvl:
            maxLvl = level
        nodes.append(dict(element))
        index += 1

    # Create level structure
    for level in range(1, maxLvl + 1):
        g1 = Graph(str(level))
        for node in nodes:
            if node['level'] == level:
                index = str(node['index'])
                label = node['label']
                shape = node['shape']
                comment = node['comment']

                # Only startStop element is smaller. Others are bigger.
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

    # Connect nodes
    branches = []
    label = ''
    for node in nodes:
        connectWith = node['connectWith']
        index = node['index']
        comment = node['comment']

        if connectWith == None:
            continue
        else:
            label = ''
            connectingNode = nodes[connectWith]
            if connectingNode['comment'] == 'fc:ifBranch':
                if index == connectWith + 1:
                    label = 'TRUE'
                else:
                    if node['level'] != connectingNode['level']:
                        label = 'FALSE'
            if (connectingNode['comment'] == 'fc:forLoop' and
                    node['level'] != connectingNode['level']):
                label = 'loop'

            g.edge(str(connectWith), str(index), label=label)

    if VIEW:
        g.view(directory=DEST)
    else:
        g.render(directory=DEST)


def main():
    with open(SOURCE, 'r', encoding='utf-8') as file:
        sourceFile = file.readlines()

    flow = []
    startStopCnt = 0
    functionName = ''

    for line in sourceFile:
        for comment in REF_COMMENT:
            if comment in line:
                # Start and end index of REF_COMMENT
                _, end = re.search(comment, line).span()

                # description is parsed line. Everything before reference comment is removed.
                # description1 converts full-widht characters to half-width if -jap argument.
                # description2 creates list of strings. description1 is split at " symbol.
                # description3 in final step and this string is places as label of graph node.
                comm = '[' + COMMENTS[LANG] + '\n\t]'
                description = re.sub(comm, '', line[end + 1:])
                if JAP:
                    import jaconv
                    description1 = jaconv.zen2han(description, ascii=True, kana=False)
                else:
                    description1 = description
                description2 = re.split('"', description1)

                if len(description2) == 1:
                    description3 = description2[0].replace(' ', '\n')
                elif len(description2) == 0:
                    description3 = ''
                else:
                    # Remove all empty strings
                    description2 = [x for x in description2 if x != '']
                    # Remove all ' ' strings (space)
                    description2 = [x for x in description2 if x != ' ']
                    if len(description2) == 1:
                        description3 = description2[0]
                    else:
                        # We are left with only 2 strings. We merge them an place newline in between.
                        description3 = description2[0] + '\n' + description2[1]

                # If string has new line '\n' on last place after parsing, remove it.
                if len(description3):
                    if description3[-1] == '\n':
                        description3 = description3[:-1]

                dictionary = {'comment': comment,
                              'level': None, 'index': None,
                              'shape': None, 'label': description3,
                              'connectWith': None}
                flow.append(dictionary)

                if comment == 'fc:startStop':
                    startStopCnt += 1
                    if startStopCnt == 1:
                        functionName = description3
                    if startStopCnt == 2:
                        startStopCnt = 0
                        if FUNCS:
                            for func in FUNCS:
                                if func == functionName:
                                    generateGraph(functionName, flow)
                        else:
                            generateGraph(functionName, flow)
                        flow = []


def parseCLIArguments():
    global SOURCE
    global DEST
    global JAP
    global VIEW
    global FUNCS
    global LANG

    # Parse CLI input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='source',
                        required=True,
                        help='Absolute or relative path to source code file.')
    parser.add_argument('-d', dest='dest',
                        required=True,
                        help='Absolute or relative path to destination folder.')
    parser.add_argument('-j', '--jaconv',
                        dest='jap',
                        action='store_true',
                        help='If set, jaconv (for Japanese) will be used.')
    parser.add_argument('-v', '--view',
                        dest='view',
                        action='store_true',
                        help='If set, preview will be enabled.')
    parser.add_argument('--func',
                        dest='funcs',
                        action='append',
                        help=('With this argument you can create graph for ' +
                              'only specified functions in source code'))
    parser.add_argument('-l', '--lang',
                        dest='lang',
                        required=True,
                        help=('With this argument you define programming language ' +
                              'you are using.'))
    args = parser.parse_args()

    SOURCE = args.source
    DEST = args.dest
    JAP = args.jap
    VIEW = args.view
    FUNCS = args.funcs
    LANG = args.lang


# ---------------Start of program-----------------------
if __name__ == "__main__":
    parseCLIArguments()
    main()
