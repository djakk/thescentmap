#!/usr/bin/python

import newick
import mapnik

import io


print "Hello !"
the_map = mapnik.Map(256,256)

with io.open('the_example_newick_tree.tre', encoding='utf8') as fp:
  trees = newick.load(fp)

print "tree loaded"
