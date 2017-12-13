try:
    import numpy as np
    import scipy as sp
    import networkx as nx
    import timeit
    import os 
    import sys
    import re
    import commands
    import convert
    import multiprocessing
    from multiprocessing import Queue, Manager, Pool

except ImportError as e:
    print "Application depends on numpy, scipy, matplotlib, networkx"
    print "Stack trace:"
    print e.strerror

import time
 
def make_ego_tensor_undirected (G,output_file,nworker):


  cnt=1
  map_dict=dict()
  map_tensor2node = np.zeros(len(G.nodes()))
  for n in G.nodes():
    map_dict[n]=cnt
    map_tensor2node[cnt-1]=n
    cnt=cnt+1

  list_nodes_all=G.nodes()
  chunk_size=len(list_nodes_all)/int(nworker)
  #chunk_size=1000
  chunky_nodes =chunks(G.nodes(),chunk_size)
  
  cnt=0
  for pr in chunky_nodes:
    exec('p'+str(cnt)+' = multiprocessing.Process(target=ego_sub_undirected, args=(G,map_dict,pr,cnt,output_file))')
    exec('p'+str(cnt)+'.start() ')
    cnt=cnt+1
  num_proc=cnt

  for cnt in range(num_proc):
    exec('p'+str(cnt)+'.join() ')
    cnt=cnt+1


  with open(output_file, 'w') as f :
    for index in range(num_proc):
      content = open(output_file+str(index)+'.txt','r').read()
      f.write(content)
      f.write('\n')
      cmd = 'rm '+output_file+str(index)+'.txt'
      (status,output) =   commands.getstatusoutput(cmd)
      if status:
        print 'Error in deleting subprocess output file copy'
      #else:
        #print output 
     
  f.close()
  return map_tensor2node


def make_ego_tensor_directed (G,output_file,nworker):

  #open(output_file, 'w')
  cnt=1
  map_dict=dict()
  map_tensor2node = np.zeros(len(G.nodes()))
  for n in G.nodes():
    map_dict[n]=cnt
    map_tensor2node[cnt-1]=n
    cnt=cnt+1
  
  list_nodes_all=G.nodes()
  chunk_size=len(list_nodes_all)/int(nworker)
  #chunk_size=1000
  chunky_nodes =chunks(G.nodes(),chunk_size)

  
  cnt=0
  for pr in chunky_nodes:
    exec('p'+str(cnt)+' = multiprocessing.Process(target=ego_sub_directed, args=(G,map_dict,pr,cnt,output_file))')
    exec('p'+str(cnt)+'.start() ')
    cnt=cnt+1
  num_proc=cnt

  for cnt in range(num_proc):
    exec('p'+str(cnt)+'.join() ')
    cnt=cnt+1


  with open(output_file, 'w') as f :
    for index in range(num_proc):
      content = open(output_file+str(index)+'.txt','r').read()
      f.write(content)
      f.write('\n')
      cmd = 'rm '+output_file+str(index)+'.txt'
      (status,output) =   commands.getstatusoutput(cmd)
      if status:
        print 'Error in deleting subprocess output file copy'    
  f.close()
  return map_tensor2node


def chunks(L, n):
  list_out=list()
  """Yield successive n-sized chunks from l."""
  for i in xrange(0, len(L), n):
    list_out.append( L[i:i + n])
  return list_out



def ego_sub_directed(G,map_dict,list_nodes,index,output_file):
  #print 'in subprocess'+ str(index)
  with open(output_file+str(index)+'.txt', 'w') as f :
    for n in list_nodes:
    
      neigh_n = G.neighbors(n)
      neigh_n.append(n)
      Gn = nx.subgraph(G,neigh_n)
      for m in Gn.nodes():
        Gn.add_edge(m,m)
      edg = [(map_dict[n],map_dict[e[0]],map_dict[e[1]]) for e in Gn.edges()]
      f.write(('\n').join('%d %d %d 1' % x for x in edg))
      f.write(('\n'))
    
  f.close()




def ego_sub_undirected(G,map_dict,list_nodes,index,output_file):
  #print 'in subprocess'+ str(index)
  with open(output_file+str(index)+'.txt', 'w') as f :
    for n in list_nodes:
    
      neigh_n = G.neighbors(n)
      neigh_n.append(n)
      Gn = nx.subgraph(G,neigh_n)
      for m in Gn.nodes():
        Gn.add_edge(m,m)
      edg2= [(map_dict[n],map_dict[e[1]],map_dict[e[0]]) for e in Gn.edges()]    
      edg = [(map_dict[n],map_dict[e[0]],map_dict[e[1]]) for e in Gn.edges()]
      f.write(('\n').join('%d %d %d 1' % x for x in edg))
      f.write(('\n'))
      f.write(('\n').join('%d %d %d 1' % x for x in edg2))
      f.write(('\n'))
  f.close()
  #print 'finishing subprocess'+ str(index)





def generate_synth_LFR(input_adj,input_comm,input_tens,cmd):

  gen_adj_LFR(cmd,input_adj)
  G=edgelist2networkxG_undirected(input_adj)
  Comm =convert.convert_comm2node('community.dat',input_comm)
  
  return Comm ,G







def edgelist2networkxG_undirected(input_adj):
  G = nx.Graph()
  f =open(input_adj,'rU')
  #a =nx.normalized_cut_size(Gn)
  
  lines = f.read().splitlines()
  for l in lines:
    if l[0]!='#':
      e = tuple(l.split()) 

      if len(e)> 1:
        ee = (int(e[0]) ,int(e[1]))
        G.add_edge(*ee)
  return G

def edgelist2networkxG_directed(input_adj):
  G = nx.DiGraph()
  f =open(input_adj,'rU')
  #a =nx.normalized_cut_size(Gn)
  
  lines = f.read().splitlines()
  for l in lines:
    if l[0]!='#':
      e = tuple(l.split()) 

      if len(e)> 1:
        ee = (int(e[0]) ,int(e[1]))
        G.add_edge(*ee)
  return G
