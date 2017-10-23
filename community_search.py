import igraph as ig
import numpy as np
import scipy.linalg as la
import random
from scipy.sparse.linalg import svds

def community_search(X,k,w,th,n):
	#------------------------------------------------------------------
	#Partition nodes into four sets P1, P2, P3, P4 at random.Let ni=|Pi|
	indice_vec=np.array(range(n))
	random.shuffle(indice_vec)
	place_holder1=random.randint(1,n-3)
	place_holder2=random.randint(place_holder1,n-2)
	place_holder3=random.randint(place_holder2,n-1)

	#place_holder1=n//4
	#place_holder2=n//2
	#place_holder3=3*n//4


	P1=indice_vec[0:place_holder1]
	P2=indice_vec[place_holder1:place_holder2]
	P3=indice_vec[place_holder2:place_holder3]
	P4=indice_vec[place_holder3:n]
	n1=place_holder1
	n2=place_holder2-place_holder1
	n3=place_holder3-place_holder2
	n4=n-place_holder3
	print ("N1 is " + str(n1)+" N2 is " + str(n2)+" N3 is " + str(n3)+" N4 is " + str(n4))
	
	#----------------------------------------------------------------
	#Compute matrices A1=(X1,3)/√n3, A2 =(X2,3)/√n3
	row_idx=P1
	col_idx=P3
	A1=X[row_idx[:,None],col_idx]/np.sqrt(n3)
	print (A1.shape)
	print(np.count_nonzero(A1))
	row_idx=P2
	A2=X[row_idx[:,None],col_idx]/np.sqrt(n3)
	print (A2.shape)
	print(np.count_nonzero(A2))
	_,D,_=la.svd(A1)
	print(D)
	_,D,_=la.svd(A2)
	print(D)
	#----------------------------------------------------------------
	#Compute vector m1=(\sum_{j \in P1} X1,j)/n1
	row_idx=P1
	col_idx=P1
	temp=X[row_idx[:,None],col_idx]
	m1=np.matrix([np.sum(temp[i]) for i in range(row_idx.size)]).T

	#----------------------------------------------------------------
	#Compute matrix B=(\sum_{j \in P4} wjX1,j(X2,j).T)/n4
	B=np.zeros(shape=(n1,n2))
	for j in P4:
		row_idx1=P1
		row_idx2=P2		
		B=B+w[j]*X[row_idx1[:,None],j]*X[row_idx2[:,None],j].T

	#----------------------------------------------------------------
	#Call Search Subroutine
	up1,alpha1=SearchSubroutine(A1,A2,B,m1,k)

	#----------------------------------------------------------------
	#Compute Vp1
	Vp1=[1 if up1[i]>th else 0 for i in P1]
	print (Vp1)


def SearchSubroutine(A1,A2,B,m1,k):
	#----------------------------------------------------------------
	#Compute Rank k svds of A1,A2
	U1,S1,V1t=svds(A1,k)
	D1=np.diag(S1)
	print(S1)
	V1=V1t.T
	U2,S2,V2t=svds(A2,k)
	D2=np.diag(S2)
	print(S2)
	V2=V2t.T

	#----------------------------------------------------------------
	#Compute matrices W1=U1*inv(D1), W2=U2*inv(D2)
	W1=U1*la.inv(D1)
	W2=U2*la.inv(D2)

	#----------------------------------------------------------------
	#u1 <- largest left singular vector of W1.T*B*W2
	mat=W1.T*B*W2
	u1_v,_,_=svds(mat,1)
	u1=np.matrix(u1_v)

	#----------------------------------------------------------------
	#compute z=U1*D1*u1, a=u1.T*W1.T*m1
	z=U1*D1*u1
	a=u1.T*W1.T*m1

	return z/a,(a*a)


	