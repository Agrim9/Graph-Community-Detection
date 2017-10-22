import igraph as ig
import numpy as np
import rand
def community_search(X,k,w,th,n):
	#------------------------------------------------------------------
	#Partition nodes into four sets P1, P2, P3, P4 at random.Let ni=|Pi|
	place_holder1=random.randint(1,n)
	place_holder2=random.randint(place_holder1,n)
	place_holder3=random.randint(place_holder2,n)

	P1=np.array([0:place_holder1])
	P2=np.array([place_holder1:place_holder2])
	P3=np.array([place_holder2:place_holder3])
	P4=np.array([place_holder3:n])
	n1=place_holder1
	n2=place_holder2-place_holder1
	n3=place_holder3-place_holder2
	n4=n-place_holder3

	#----------------------------------------------------------------
	#Compute matrices A1=(X1,3)/√n3, A2 =(X2,3)/√n3
	row_idx=P1
	col_idx=P3
	A1=X[row_idx[:,None],col_idx]/np.sqrt(n3)
	row_idx=P2
	A2=X[row_idx[:,None],col_idx]/np.sqrt(n3)

	#----------------------------------------------------------------
	#Compute vector m1=(\sum_{j \in P1} X1,j)/n1
	row_idx=P1
	col_idx=P1
	temp=X[row_idx[:,None],col_index]
	m1=np.matrix([np.sum(temp[i]) for i in row_idx.size]).T

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


