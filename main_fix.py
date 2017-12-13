try:
  import csv

except ImportError as e:
    print "Application depends on numpy, scipy, matplotlib, networkx"
    print "Stack trace:"
    print e.strerror

def main(): 
  fix_adj(sys.argv[1])


def fix_adj(input_adj):

  content = open(input_adj,'r').read().splitlines()
  #dict_comm={};
  #with open(inputfile_mode) as f:
    #content = f.readlines()
  #matrix = np.zeros((n,Comm))
  cnt = 1
  dict_map =dict()

  open('ordered_'+input_adj, 'w')
  with open('ordered_'+input_adj, 'w') as f:
   
      # let's creat a dictionary mapping new node numbers with the original
    for line in content:  
      
      l =  line.strip().split()
      if l[0] is not '#':
        edge_this_line = list()
        for n in l:
          if n in dict_map:
            edge_this_line.append(dict_map[n])
          else :
            dict_map[n]=cnt
            edge_this_line.append(cnt)
            cnt=cnt+1

        f.write('%d ' % edge_this_line[0])
        f.write('%d \n' % edge_this_line[1])
      #f.write(('%d %d \n' % edge_this_line[0],edge_this_line[1] ))
   

  f.close()
  return dict_map      

if __name__=='__main__':

  import sys

       
  main()


