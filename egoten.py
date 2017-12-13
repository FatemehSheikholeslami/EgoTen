try:
    import numpy as np
    import scipy as sp
    import metric_cut
    import os , glob, shutil
    import commands
    import convert
    from anytree import Node, RenderTree, iterators
    from anytree.dotexport import RenderTreeGraph

except ImportError as e:
    print "Application depends on numpy, scipy, matplotlib, networkx"
    print "Stack trace:"
    print e.strerror




def EgoTen_splatt(Comm,input_tens):
  regularization = 1./(10*Comm)
  cmd = './splatt cpd '+input_tens+' -r '+ str(Comm) + '  --con=rowsimp,1  --reg=ntf-frob,'+str(regularization)+',2,3  --iters=50 --tol=1e-3 --stem=' + input_tens
  #cmd = './splatt cpd '+input_tens+' -r '+ str(Comm) + '  --con=rowsimp,3  --reg=ntf-frob,0.01,1,2  --iters=100 --tol=1e-4'
  # print cmd
  (status,output) =   commands.getstatusoutput(cmd)
  if status:
    print 'Error in Running SPLATT'
    print output
    #return
  #else:
    #print output 
  shutil.move(input_tens+'.mode1.mat' , input_tens+'_soft.mat')
  '''cmd = 'mv '+ input_tens+'.mode1.mat ' +input_tens+'_soft.mat'
  (status,output) =   commands.getstatusoutput(cmd)
  if status:
    print 'Error in splatt output file copy'
  #else:
    #print output''' 

  for item in glob.glob(input_tens):
    os.remove(item)
  return input_tens+'_soft.mat'




def DO_SPLATT(G,map_here,input_tens,Comm,runs,THRESH,CPD_output):
  splatt_output= EgoTen_splatt(Comm,input_tens)
  output_splatt =  convert.convert_soft_membership(G,map_here,splatt_output,CPD_output)
  return output_splatt
