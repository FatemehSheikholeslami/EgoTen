import numpy as np
import networkx as nx
import generation as GEN



__all__ = ['conductance', 'cut_size', 'normalized_cut_size',
           'volume']



def eval_cut(input_adj,input_comm,output_file):
  
  G = GEN.edgelist2networkxG(input_adj)
  #print (min(list(G.nodes())))
  content_comm = open(input_comm,'r').read().splitlines()
  list_of_sets=list()
  set_lengths=list()
  for l in content_comm:
    if l[0]!='#':
      members = l.split()    
      list_of_sets.append(set(map(int,members)))
      if len(members)!=0: 
        set_lengths.append(len(members))
  #print list_of_sets

  #print input_comm
  list_cond=list()
  list_ncut=list()
  
  with open(output_file,'w') as f:
 
    for comm in list_of_sets:
       if len(comm)==1:
         
         f.write('%f ' % 1)
         f.write("".join('%d ' % x for x in list(comm)))
         f.write('\n')
         list_cond.append(1)
         temp=list(comm)
         ###print temp
         list_ncut.append(1)
         ###print G.degree(comm)
         ###print list(comm)[0]
       if  len(comm)>1:

         temp=conductance(G,comm)

         f.write('%f ' % temp)
         f.write("".join('%d ' % x for x in list(comm)))
         f.write('\n')
         list_cond.append(temp)
         list_ncut.append(normalized_cut_size(G,comm))
  print 'cond ' , len(list_cond)
  print 'list_of_sets ',len(list_of_sets)
## UNraveling the coverage
  all_nodes=list()


  for comm in list_of_sets:
    temp = list(comm)
    all_nodes=all_nodes+temp
  # get rid of redundant nodes via making the list of covered nodes into a set and back into a list
  all_nodes_set=(set(all_nodes))
  all_nodes=list(all_nodes_set)
  
  covered_number= len(all_nodes)


  
### Ncut stuff
  with open('ncut'+output_file[4:],'w') as f:
 
    for comm in list_of_sets:
       if len(comm)==1:
         
         '''f.write('%f ' % 1)
         f.write("".join('%d ' % x for x in list(comm)))
         f.write('\n')'''
         
       if  len(comm)>1:

         temp=conductance(G,comm)

         '''f.write('%f ' % normalized_cut_size(G,comm))
         f.write("".join('%d ' % x for x in list(comm)))
         f.write('\n')'''
         


  #print len(list_cond)
  #print (set_lengths)
  #print (list_cond)
  f.close()

  #print 'in metric_cut'
  #print list_cond
  #print set_lengths
  return np.average(list_cond, weights=set_lengths),covered_number#np.average(list_ncut, weights=set_lengths)
#  return sum(list_cond)/float(len(list_cond)),sum(list_ncut)/float(len(list_ncut))
  #return list_cond












def cut_size(G, S, T=None, weight=None):
    """Returns the size of the cut between two sets of nodes.

    A *cut* is a partition of the nodes of a graph into two sets. The
    *cut size* is the sum of the weights of the edges "between" the two
    sets of nodes.

    Parameters
    ----------
    G : NetworkX graph

    S : sequence
        A sequence of nodes in `G`.

    T : sequence
        A sequence of nodes in `G`. If not specified, this is taken to
        be the set complement of `S`.

    weight : object
        Edge attribute key to use as weight. If not specified, edges
        have weight one.

    Returns
    -------
    number
        Total weight of all edges from nodes in set `S` to nodes in
        set `T` (and, in the case of directed graphs, all edges from
        nodes in `T` to nodes in `S`).

    Examples
    --------
    In the graph with two cliques joined by a single edges, the natural
    bipartition of the graph into two blocks, one for each clique,
    yields a cut of weight one::

        >>> G = nx.barbell_graph(3, 0)
        >>> S = {0, 1, 2}
        >>> T = {3, 4, 5}
        >>> nx.cut_size(G, S, T)
        1


    """
    edges = nx.edge_boundary(G, S, T)
    if not G.is_directed():
      return len(edges)
    else:
      #print 'directed graphs'
      #return sum(weight for u, v, weight in edges)
      return len(edges)

def normalized_cut_size(G, S, T=None, weight=None):
    """Returns the normalized size of the cut between two sets of nodes.

    The *normalized cut size* is the cut size times the sum of the
    reciprocal sizes of the volumes of the two sets. [1]

    Parameters
    ----------
    G : NetworkX graph

    S : sequence
        A sequence of nodes in `G`.

    T : sequence
        A sequence of nodes in `G`.

    weight : object
        Edge attribute key to use as weight. If not specified, edges
        have weight one.

    Returns
    -------
    number
        The normalized cut size between the two sets `S` and `T`.

    Notes
    -----
    In a multigraph, the cut size is the total weight of edges including
    multiplicity.

    See also
    --------
    conductance
    cut_size
    edge_expansion
    volume

    References
    ----------
    .. [1] David Gleich.
           *Hierarchical Directed Spectral Graph Partitioning*.
           <https://www.cs.purdue.edu/homes/dgleich/publications/Gleich%202005%20-%20hierarchical%20directed%20spectral.pdf>

    """
    if T is None:
        T = set(G) - set(S)
    num_cut_edges = cut_size(G, S, T=T, weight=weight)
    volume_S = float( volume(G, S, weight=weight))
    volume_T = float( volume(G, T, weight=weight))
    if volume_S==0:
      print 'S volume zeros'
      return 
    volume_T = float(volume(G, T, weight=weight))
    if volume_T==0:
      #print 'T volume zero'
      return None
    return float(num_cut_edges) * float((1 / float(volume_S)) + float(1 / float(volume_T)))


def volume(G, S, weight=None):
    """Returns the volume of a set of nodes.

    The *volume* of a set *S* is the sum of the (out-)degrees of nodes
    in *S* (taking into account parallel edges in multigraphs). [1]

    Parameters
    ----------
    G : NetworkX graph

    S : sequence
        A sequence of nodes in `G`.

    weight : object
        Edge attribute key to use as weight. If not specified, edges
        have weight one.

    Returns
    -------
    number
        The volume of the set of nodes represented by `S` in the graph
        `G`.

    See also
    --------
    conductance
    cut_size
    edge_expansion
    edge_boundary
    normalized_cut_size

    References
    ----------
    .. [1] David Gleich.
           *Hierarchical Directed Spectral Graph Partitioning*.
           <https://www.cs.purdue.edu/homes/dgleich/publications/Gleich%202005%20-%20hierarchical%20directed%20spectral.pdf>

    """
    degree = G.out_degree if G.is_directed() else G.degree
    TEMP=degree(S)
    #print 's',S
    #print  G.nodes(1511)
    '''print TEMP
    print TEMP[0]
    temp = [v in TEMP[0]]
    print temp'''
    #print degree(S, weight=weight)
    return sum(d for v, d in degree(S, weight=weight).iteritems())



def conductance(G, S, T=None, weight=None):
    """Returns the conductance of two sets of nodes.

    The *conductance* is the quotient of the cut size and the smaller of
    the volumes of the two sets. [1]

    Parameters
    ----------
    G : NetworkX graph

    S : sequence
        A sequence of nodes in `G`.

    T : sequence
        A sequence of nodes in `G`.

    weight : object
        Edge attribute key to use as weight. If not specified, edges
        have weight one.

    Returns
    -------
    number
        The conductance between the two sets `S` and `T`.

    See also
    --------
    cut_size
    edge_expansion
    normalized_cut_size
    volume

    References
    ----------
    .. [1] David Gleich.
           *Hierarchical Directed Spectral Graph Partitioning*.
           <https://www.cs.purdue.edu/homes/dgleich/publications/Gleich%202005%20-%20hierarchical%20directed%20spectral.pdf>

    """
    if T is None:
        T = set(G) - set(S)
    num_cut_edges = cut_size(G, S, T, weight=weight)
    volume_S = float( volume(G, S, weight=weight))
    if volume_S==0:
      print 'S volume zeros' , S
      return 
    volume_T = float(volume(G, T, weight=weight))
    if volume_T==0:
      print 'T volume zero'
      return 
    return float(num_cut_edges / min(volume_S, volume_T))
