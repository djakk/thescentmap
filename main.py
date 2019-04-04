#!/usr/bin/python

import newick

import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
sys.path.append('/app/.apt/usr/lib/python2.7/dist-packages/')

import mapnik

import io


#print("Hello !")
the_map = mapnik.Map(256,256)

with io.open('the_example_newick_tree.tre', encoding='utf8') as fp:
  trees = newick.load(fp)

#print("tree loaded")
