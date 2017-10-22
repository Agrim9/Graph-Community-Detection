#!/bin/python3
import igraph as ig
import numpy as np
import random

n=1000
k=8
alpha_min=0.1
q=0.01
p=0.3

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
print (Pref_mat.tolist())
g=ig.Graph.SBM(n,Pref_mat.tolist(),block_vec)
ig.plot(g)