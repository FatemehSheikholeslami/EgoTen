This toolbox provides a community detection algorithm developed in the paper:

F. Sheikholeslami and G. B. Giannakis, "Overlapping community detection via constrained parafac: a divide and conquer approach," ICDM, New Orleans, LA, Nov. 2017.

To execute, run the command:

python DC_EgoTen.py  dataset_adj.txt   comm_top   comm_below   depth    comm_total   directed_flag    C_max  method bum_of_worker
where

 DC_Egoten.py [-h] [--input [INPUT]] [--output [OUTPUT]]
                    [--workers WORKERS] [--directed] [--undirected]
                    [--max_depth MAX_DEPTH] [--top_K TOP_K]
                    [--lower_K LOWER_K] [--C_max C_MAX] [--verbose]
                    [--ordered] [--unordered]



	--input         (dataset_adj.txt) is the edgeset dataset with a pair of nodes in each line separated by comma ',' (default fixed_facebook_adj.txt)
	--output        is the output file where each lien is the node s assigned to a detected community (default community.txt)
	--top_K         is the K community number for the top EgoTen application (default 100)
	--lower_K	is the K community number for the consequtive EgoTen application (default 2)
	--max_depth	is the maximum allowed depth for the tree (conscutive application of EgoTen) (default 10)
	--directed	use  if edgelist is directed
	--undirected 	use of edgelist is undirected
	--C_max	    	is the desired (maximum size) resolution of a community (set to 10% of the graph size)
	--workers	number of workers (set 1 as default)
	--ordered
	--unordered
        
For instance, run:
	python  DC_Egoten.py --input facebook_adj.edges --top_K 100 --lower_K 2 --max_depth 30 --undirected --C_max 500 --workers 4 --ordered

use the fix python code to fix your adjacency edgelist if the nodes are not consequitvely numbered

The output is a txt file whose name starts with the input adjacency file + 'communities.txt', 
and the detected communities are given in every line.



***************************** NOTE **********************************

The algorithm utilizes the SPLATT software for solving the sparse tensor decomposition, which can be found at:
 https://github.com/ShadenSmith/splatt 

Download the codes available under the 'wip/ao-admm' branch for decomposition with regularization and constraints, 
compile and build, and make a copy of the executable file 'splatt'. Next, make sure to have the executable "splatt" in the same directory as the python codes.



