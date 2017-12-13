try:
    import numpy as np
    import scipy as sp
    import matplotlib.pyplot as plt
    import networkx as nx
    #import Louvain
    import os 
    import sys
    import re
    import commands
    import metric_cut

except ImportError as e:
    print "Application depends on numpy, scipy, matplotlib, networkx"
    print "Stack trace:"
    print e.strerror

import time



def convert_soft_membership(G,map_here,inputfile_mode,CPD_output):
  with open(inputfile_mode) as f:
    mode3 = [map(float,line.split()) for line in f]
  mode3_t=np.transpose(mode3)
  C,N =mode3_t.shape
  if C>10:
    thresh = [float(2./C), float(3./C), float(5./C), float(10./C)]
  else :
    thresh = [float(1./C), float(2./C), float(3./C), float(4./C)]
  thresh = [float(1./C)]
  with open(CPD_output, 'w') as f:
    for comm in mode3_t :
      cnt=0
      cond =[]
      for th in thresh:
        temp_th = [map_here[n] for n in range(N) if comm[n]>th ]
        cond_temp=metric_cut.conductance(G,temp_th)
        if cond_temp is not None:
          cond.append(cond_temp)
        cnt=cnt+1
      if cond==[]:
        temp=[n+1 for n in range(N) if comm[n]>(1./C) ]
      else:
        cond_min =min(cond)
      
        cnt=0
        for c in cond:
          if c==cond_min:
            th_winner=thresh[cnt]
            #print th_winner
          else:
            cnt=cnt+1
        temp = [n + 1 for n in range(N) if comm[n] > th_winner]
       
        
      for m in temp:
        f.write(('%d ' % m ))
      f.write('\n')
  return CPD_output



def convert_comm2node(filename_input,filename_output):
  dict_comm={};
  with open(filename_input) as f:
    content = f.readlines()
  for line in content: 
            # each line starts with the node Id and is followed by the communities to which it is associated with (as long as the following numbers are integers, which is not the case for infomap output file *.clu)
    pair =  line.strip().split()
    if pair[0] !='#':
      #print pair
      for comm in pair[1:]:
        if comm in dict_comm:
          dict_comm[comm].append(pair[0])
        else:
          #print comm, 1, str(float(comm) % 1)
          if (float(comm) % 1) ==0:
            dict_comm[comm] = [pair[0]]
        
  #print dict_comm
  #print dict_comm.keys()

  open(filename_output, 'w')
  with open(filename_output, 'a') as f:
    #print(comm for comm in dict_comm.keys())
    for comm in dict_comm.keys():
  
      f.write((' ').join('%d' % int(mmbr) for mmbr in dict_comm[comm]))
      f.write('\n')
  f.close()
  return len(dict_comm.keys())

'''def convert_comm2node(filename_input,filename_output):
  dict_comm={};
  with open(filename_input) as f:
    content = f.readlines()
  for line in content:
    pair =  line.strip().split(',')
    if pair[0] !='#':
      if pair[1] in dict_comm:
        dict_comm[pair[1]].append(pair[0])
      else:
        dict_comm[pair[1]] = [pair[0]]
        
  print dict_comm.keys()

  open(filename_output, 'w')
  with open(filename_output, 'a') as f:
    print(comm for comm in dict_comm.keys())
    for comm in dict_comm.keys():
  
      f.write((' ').join( str(int(mmbr)+1) for mmbr in dict_comm[comm]))
      f.write('\n')
  f.close()'''
