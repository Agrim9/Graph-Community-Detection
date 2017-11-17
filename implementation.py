#!/bin/python3
import igraph as ig
import numpy as np
import random
from community_search import community_search 
n=1000
k=5
alpha_min=0.1
q=0.01
p=0.5

#get Pref Matrix, i*p 
Pref_mat=np.matrix(p*np.identity(k)+q*(np.ones(shape=(k,k))-np.identity(k)))
#Get block vector by num=amin*n+random(n-amin)
min_commsize=int(n*alpha_min)
block_vec=[min_commsize]
sum_cnt=min_commsize
left_elem=k-1
for i in range(k-2):
	#print (i)
	while(1):
		print ("Attempt: "+str(sum_cnt))
		random_gen=random.randint(min_commsize,int((n-sum_cnt)/left_elem))
		sum_cnt=sum_cnt+random_gen
		if((n-sum_cnt)<(left_elem*min_commsize)):
			sum_cnt=sum_cnt-random_gen
			continue
		else:
			block_vec.append(random_gen)
			left_elem=left_elem-1
			break
block_vec.append(n-sum_cnt)
print (block_vec)
#print (Pref_mat.tolist())
g=ig.Graph.SBM(n,Pref_mat.tolist(),block_vec)

#Label m vertices as blue, other as pink
m=10
r=3 #5 Hops
'''Wt assignment
#print (g.get_shortest_paths(g.vs[100],g.vs[0:10]))
#print ([1 if len(x)<4 else 0 for x in g.get_shortest_paths(g.vs[100],g.vs[0:10])])
#print (sum([1 if len(x)<4 else 0 for x in g.get_shortest_paths(g.vs[100],g.vs[0:10])]))
less than r hops
'''
w=[sum([1 if len(x)<r else 0 for x in g.get_shortest_paths(g.vs[i],g.vs[0:m])]) for i in range(n)]
#print(w[::4])

g.vs["side_info_wt"]=w
X_list=g.get_adjacency()
X_arr=np.array(X_list[0])
for i in range(1,n):
	X_arr=np.vstack([X_arr,X_list[i]])
X=np.matrix(X_arr)
g.vs["color"]=["red" if i>(m-1) else "pink" for i in range(n)]
ig.plot(g)


colors=["red","green","yellow","black","grey","red","green","yellow","black","grey"]
color_vec=[]
num_iter=1
for count in range(num_iter):
	nodes_in_V1=community_search(X,k,w,0.0012,n)
	if(count==0):
		color_vec=[colors[count] if nodes_in_V1[i]==1 else "blue" for i in range(nodes_in_V1.size)]
		g.vs["color"]=color_vec
		if(num_iter>1):
			ig.plot(g)
	else:
		for i in range(nodes_in_V1.size):
			if((nodes_in_V1[i]==1) and (color_vec[i]=="blue")):
				color_vec[i]=colors[count]

g.vs["color"]=color_vec
ig.plot(g)
ig.summary(g)

