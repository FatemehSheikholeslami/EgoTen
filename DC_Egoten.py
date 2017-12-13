#!/usr/bin/env python

try:
    import numpy as np
    import scipy as sp
    import networkx as nx
    import metric_cut
    import os , glob
    import sys
    import re
    import timeit
    import commands
    import convert , egoten
    import generation as GEN
    import argparse
    import csv
    from anytree import Node, RenderTree, iterators
    from anytree.dotexport import RenderTreeGraph
    from operator import itemgetter
    import matplotlib.pyplot as plt
    import time
    
except ImportError as e:
    print "Application depends on numpy, scipy, matplotlib, networkx"
    print "Stack trace:"
    print e.strerror


   




def fix_adj (input_adj):
  cmd = 'python main_fix.py '+ input_adj 
  (status,output) =   commands.getstatusoutput(cmd)
  if status:
    print 'Error in ordering network adjacency'
    print output
  return 'ordered_'+input_adj    


def DC_ego(input_adj,comm_top,comm_below,depth,directed_flag,C_max,nworker,verbose,ordered,output_filename):  

  
  global node_number   
  if not ordered: 
    input_adj = fix_adj(input_adj)
  layer_index=0    
  
  #######################################################################
  ###################    Form networkx graph    #########################
  #######################################################################
  if directed_flag:  
    G=GEN.edgelist2networkxG_directed(input_adj)
  else:   
    G=GEN.edgelist2networkxG_undirected(input_adj)


  
  if C_max<1:
    C_max = int(C_max* len(G.nodes())  )
  
  print 'Network size = ' + str(len(G.nodes())) + ' nodes'
  print 'Max community resolution  = ' + str(C_max) + ' nodes'

  child_index = 1
  layer0 = Node('node0')
  layer_index=0  
  dict_node2member['node'+str(node_number)]=G.nodes()  
  parent_name='node'+str(node_number)
  start = timeit.default_timer()


  ###################################################################
  ###########          Call hierarchy recursively    ################
  ###################################################################
  node_number_now=hierarchy(G,comm_top,layer_index,child_index,layer0,input_adj,comm_below,depth,C_max,directed_flag,nworker,verbose)
  stop = timeit.default_timer()
  print 'Time_DC_egoten= ' 
  print  (stop - start) 


  ###################################################################
  ###################          CLEAN UP      ########################
  ###################################################################

  for item in glob.glob(input_adj+'*.tns'):
    os.remove(item)
  for item in glob.glob(input_adj+'*.mat'):
    os.remove(item)
  for item in glob.glob(input_adj+'*CPD.txt'):
    os.remove(item)
  

  #########################################################################
  #######        Write lit of nodes in detected communities     ###########
  ######################################################################### 

  list_of_leaves= [node.name for node in iterators.PreOrderIter(layer0) if node.is_leaf]
  
  print 'Total number of detected communities = ' + str(len(list_of_leaves)) 
  
  f=open(output_filename,'w') 
  f.close()
  with open(output_filename,'a') as f: 

    for leaf in list_of_leaves:
      str_commnumber = str(leaf) 	
      f.write('#community'+str_commnumber[4:] + '\n ' )
      for node in dict_node2member[leaf]: # node refers to tree node and members are the members in this community (node)    
        f.write(str(node) + ' ' )
      f.write('\n')
  f.close()




def hierarchy(G,n_comm,layer_index,child_index,parent_name,input_adj,comm_below,depth,C_max,directed_flag,nworker,verbose):
  global node_number
  global cnt
  input_tens = input_adj+str(layer_index)+'tens.tns'
  if directed_flag:
    map_here=GEN.make_ego_tensor_directed(G,input_tens,nworker)
  else:
    map_here=GEN.make_ego_tensor_undirected(G,input_tens,nworker)

  THRESH = [float(2./n_comm)]
  runs=range(1)
  CPD_output= input_adj+str(layer_index)+str(child_index)+'CPD.txt'

  #########################################################################
  #############        Run SPLATT for this tree-node    ###################
  ######################################################################### 
  CPD_output=egoten.DO_SPLATT(G,map_here,input_tens,n_comm,runs,THRESH,CPD_output) 

  layer_index=layer_index+1
  with open(CPD_output) as f:
    content = f.readlines()   
    for line in content: # each line consists of the nodes in a community 
        node_number=node_number+1      
        members =  line.strip().split()
        members_updated=list()
        for m in members:    
          members_updated.append(int(map_here[int(m)-1]))
        dict_node2member['node'+str(node_number)]=members_updated
     
        exec("node%d = Node(\"node%d\", parent=parent_name)" % (node_number , node_number));

        cnt=cnt+1
        sub=nx.subgraph(G, members_updated)
        temp=metric_cut.conductance(G,members_updated)
        exec("parent_now = node%d" % (node_number))

        ##########################################################################
        #######       Decide whether we want to go further          ##############
        ####### down the tree and apply anoter EgoTen decomposition ##############
        ##########################################################################
        if len(members) >C_max and  temp is not None and layer_index<depth: 
              if verbose:
                print 'breaking community detected at tree-node #' + str(node_number)
              hierarchy(sub,comm_below,layer_index,cnt,parent_now,input_adj,comm_below,depth,C_max,directed_flag,nworker,verbose)
       
          
  return




  
  

def parse_args():
  
    parser = argparse.ArgumentParser(description="Run tensor_decomp")
    parser.add_argument('--input', nargs='?', default= 'facebook_adj.edges', 
	                    help='Input edgelist file, separated by space, default = facebook_adj.edges')
    parser.add_argument('--output', nargs='?', default= 'communities.txt', 
	                    help='Output file name, default  = communities.txt')	
    parser.add_argument('--workers', type=int, default=8,
	                    help='Number of parallel workers for tensor construction. Default is 8.')
 
    parser.add_argument('--directed', dest='directed', action='store_true',
	                    help='Graph is (un)directed. Default is undirected.')
    parser.add_argument('--undirected', dest='directed', action='store_false')
    parser.set_defaults(directed=False)
    parser.add_argument('--max_depth', type=int, default=5,
	                    help='Maximum depth of the tree. Default is 5.')
    parser.add_argument('--top_K', type=int, default=10,
	                    help='Top level number of  communities. Default is 10.')
    parser.add_argument('--lower_K', type=int, default=2,
	                    help='Lower level number of communities. Default is 2.')
    parser.add_argument('--C_max', type=int, default=0.1,
	                    help='Maximum acceptable size of a community.')
    parser.add_argument('--verbose', dest='verbose' ,action = 'store_true',
	                    help='set verbose. Default is not verbose')
    parser.set_defaults(verbose=False)
    parser.add_argument('--ordered', dest='ordered' ,action = 'store_true',
	                    help='set if nodes in the edgelist are ordered (no gap in numbering).')
    parser.add_argument('--unordered', dest='ordered' ,action = 'store_false',
	                    help='set if ordering of nodes in the edgelist is required. ORIGINAL ORDERING OF NODES WILL BE LOST.')
    parser.set_defaults(ordered='Error')
    return parser.parse_args()




if __name__=='__main__':
  import sys

  cnt=0

  dict_node2member=dict()
  dict_node2parent=dict()
  node_number = 0 
  args = parse_args()
  node0=Node('node0')

  print '************ Running DC_Egoten ****************'
  print 'Edgelist input ' + args.input
  print 'Output file ' + args.output
  print '# of workers for tensor construction : ' + str(args.workers)
  print '# K at top-level '  + str(args.top_K)
  print '# K at lower levers ' + str(args.lower_K)
  if args.directed:
    print 'Network type: Directed'
  else:
    print 'Network type: Undirected'
  print 'Verbose : ' + str(args.verbose)
  if args.ordered:
    print 'Node-numbering status : ordered'
  else:
    print 'Node-numbering status: unordered'
  if args.ordered=='Error':
    print '****Usage error: Need to set whether the edgelist is ordered or not. See help.****'
  else:


    DC_ego(args.input, args.top_K , args.lower_K , args.max_depth,  args.directed , args.C_max , args.workers,args.verbose,args.ordered,args.output)
  #ALL(input_adj,    comm_top,   comm_below,      depth,      ,  directed_flag,    C_max):  




