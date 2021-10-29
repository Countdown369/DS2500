#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 18:22:09 2021

@author: cabrown802
"""

class Graph:
    
    def __init__(self, V = [], E = []):
        self.G = {} # empty graph (key -> set())
        for v in V:
            self.addVertex(v)
        for v, u in E:
            self.addEdge(v, u)
            
    def addVertex(self, v):
        if v not in self.G:
            self.G[v] = set()
            
    def addEdge(self, v, u):
        # add vertices
        self.addVertex(u)
        self.addVertex(v)
        # add edge
        self.G[u].add(v)
        self.G[v].add(u)
        
    def adjacent(self, v):
        return self.G.get(v, set())
    
    def __repr__(self):
        return str(self.G)
    
def main():
    V = list("ABCDEFGH")
    E = [('A', 'B'), ('A', 'C')]
    g = Graph(V, E)
    # g.addEdge('A', 'B')
    print(g)

if __name__ == '__main__':
    main()