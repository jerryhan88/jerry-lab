int n = ...;	// # of lines
int m = ...;	// # of types
int T = ...;	// # of periods(planning horizon)
int R = ...;	// # of orders
int fr[1..R] = ...; 	// Type of accumulated order r
int dr[1..R] = ...;		// Due date of order r
int qr[1..R] = ...;		// Quantities of order r
int Qr[r in 1..R] = 	// Quantities of accumulated orders
	sum( _r in 1..R : fr[r] == fr[_r] && dr[_r] <=dr [r]) qr[_r];
int dmax_j[j in 1..m] = // Last due date among type j¡¯s orders
	max(r in 1..R : fr[r] == j ) dr[r];
{int} Jt[t in 1..T] =	// Set of types which need to be considered in period t 
	{j| j in (1..m) : t <= dmax_j[j]};
//{int} lambda_i[]

float beta = ...;
float C = ...;

//////////////
dvar int z[1..n][1..m][1..T] in 0..1;
dvar int a[1..m] in 0..1;
minimize sum(i in 1..n, j in 1..m, t in 1..T) z[i][j][t] + sum (r in 1..R) Qr[r]
 + sum (j in 1..m) dmax_j[j] + sum(x in Jt[1])a[x];
//////////////


//float B = ...;
//int f_l[1..D] = ...;
//int d_l[1..D] = ...;
//int dmax_j[1..m] = ...;
//float Q_l[1..D] = ...;
//float b_j[1..m] = ...;
//float w_j[1..m] = ...;
//
//float C0_ij[1..n][1..m] = ...;
//float alpha_jk[1..m][1..m] = ...;
//
//tuple cPair {
//	int i;
//	int j;
//	int k;
//};
//
//tuple tDep_dom {
//	int i;
//	int j;
//	int t;
//};
//
//tuple cz {
//	int i;
//	int j;
//	int t;
//};
//
//
//{cPair} P = ...;
//{tDep_dom} dvd = {<i, j, t> | i in 1..n, j in 1..m, t in 1..dmax_j[j]};
//
//float M = C;
//
//dvar float+ x[dvd];
//dvar int y[dvd] in 0..1;
//dvar int z[1..n][1..m][1..T] in 0..1;
//
//minimize
//  C * sum (j in 1..m)w_j[j] * sum(t in 1..dmax_j[j])sum( i in 1..n ) y[<i, j, t>];
//    
//subject to {
//  
//  forall( t in 1..T, i in 1..n)
//    eq2:
//      sum( j in 1..m)(t <= dmax_j[j] ? y[<i, j ,t>]: 0) <= 1;
//  
//  forall( i in 1..n, j in 1..m, t in 1..T )
//    eq3:
//      if (t <= dmax_j[j]){
//        x[<i, j, t>] <= C * y[<i, j, t>];
//      }
//              
//  forall( l in 1..D )
//    eq4:
//      sum( t in 1..d_l[l] ,i in 1..n ) x[<i, f_l[l], t>] >= Q_l[l];
//      
//  forall( t in 1..T, <i,j,k> in P)
//    eq5:
//      if (t <= dmax_j[k]){
//    	x[<i, k, t>] <=
//    	alpha_jk[j][k] * 
//    	(C0_ij[i][j] + beta * sum(s in 1..(t-1 <= dmax_j[j] ? t-1 : dmax_j[j])) y[<i, j, s>])
//    	+ beta + M * (2 - y[<i, k , t>] - z[i][j][t]);
//      }        
////
//  forall( i in 1..n, t in 1..T )
//    eq6:
//      sum( j in 1..m ) z[i][j][t] == 1;
//
////  forall( t in 1..T )
////    eq7:
////      sum( i in 1..n ,j in 1..m ) b_j[j]*y[t][i][j] <= B;
//  };
//  
//execute {
//	var fp = new IloOplOutputFile("Shoes Manufacturing.sol")
//	fp.writeln(cplex.getObjValue())
//	
//	for (i in dvd)
//	  fp.write("x" + i + " = " + x[i] + "\n")
//	for (i in dvd)
//	  fp.write("y" + i + " = " + y[i] + "\n")
//	
//	for (i = 1 ; i <= n ; i++) {
//	  for (j = 1 ; j <= m ; j++){
//	    for (t = 1 ; t <= T ; t++){
//	      fp.write("z <" + i + " " + j + " " + t + ">" + " = " + z[i][j][t] + "\n")
//        }	      
//      }	    
// 	}	  
//	fp.close()
//}
 