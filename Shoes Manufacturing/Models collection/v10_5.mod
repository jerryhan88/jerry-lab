int n = ...;			// # of lines
int m = ...;			// # of types
int T = ...;			// # of periods(planning horizon)
int R = ...;			// # of orders
int fr[1..R] = ...; 	// Type of accumulated order r
int dr[1..R] = ...;		// Due date of order r
int qr[1..R] = ...;		// Quantities of order r
int Qr[r in 1..R] = 	// Quantities of accumulated orders
	sum( _r in 1..R : fr[r] == fr[_r] && dr[_r] <=dr [r]) qr[_r];
int dmax_j[j in 1..m] = // Last due date among type j¡¯s orders
	max(r in 1..R : fr[r] == j ) dr[r];
{int} Jt[t in 1..T] =	// Set of types which need to be considered in period t 
	{j | j in (1..m) : t <= dmax_j[j]};
{int} lambda_i[1..n] = ...;
						// Set of types line i can produce
float l_j[1..m] = ...;	// # of labors needed for producing type j on a period
float w_j[1..m] = ...;	// Material costs of producing a unit of type j
float b_j[1..m] = ...;	// # of maximum lines type j can be assigned to in a period
float alpha_jk[1..m][1..m] = ...;
						// Coefficient of type k¡¯s learning effect for type j
float C0_ij[1..n][1..m] = ...;
						// Initial capable amount of type j which line i can produce
float beta = ...;		// Ramp-up quantity
float C = ...;			// Line capacity
float L = ...;			// Maximum available labors on a period
float M = C;			// Large number

tuple dv_dom {
	int t;
	int i;
	int j;
};

{dv_dom} dvd = {<t, i, j> | t in 1..T, i in 1..n, j in Jt[t] inter lambda_i[i] };

dvar float+ x[dvd];
dvar int y[dvd] in 0..1;
dvar int z[1..T][1..n][1..m] in 0..1;

minimize
  sum(t in 1..T, i in 1..n, j in Jt[t] inter lambda_i[i] ) w_j[j] * C * y[<t, i, j>]; 
    
subject to {
  
  forall( t in 1..T, i in 1..n )
    eq2:
      sum( j in Jt[t] inter lambda_i[i] ) y[<t, i, j>] <= 1;

  forall( t in 1..T, i in 1..n, j in 1..m : j in Jt[t] inter lambda_i[i] )
    eq3:
      x[<t, i, j>] <= C * y[<t, i, j>];
                    
  forall( r in 1..R )
    eq4:
      sum( t in 1..dr[r] ,i in 1..n : fr[r] in lambda_i[i] ) x[<t, i, fr[r]>] >= Qr[r];

  forall( t in 1..T, i in 1..n, j in 1..m, k in 1..m : j in Jt[t] inter lambda_i[i] && k in lambda_i[i])
    eq5:
      x[<t, i, j>] <= alpha_jk[j][k] * 
      (C0_ij[i][j] + beta * sum(s in 1..(t-1 <= dmax_j[k] ? t-1 : dmax_j[k])) y[<s, i, k>] )
      + beta + M * (2 - z[t][i][k] - y[<t, i, j>] );

/*
  forall( t in 1..T, i in 1..n )
    eq6:
      sum( k in 1..m ) z[t][i][k] == 1;

  forall( t in 1..T )
    eq7:
	  sum( i in 1..n , j in Jt[t] inter lambda_i[i] ) l_j[j] * y[<t, i, j>] <= L;
	    
  forall( t in 1..T, j in Jt[t] )
    eq8:
      sum( i in 1..n ) y[<t, i, j>] <= b_j[j];
  */    
  };
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




//////////////
//dvar int a[1..m] in 0..1;
//minimize sum(t in 1..T, i in 1..n, j in 1..m ) z[t][i][j] + sum (r in 1..R) Qr[r]
// + sum (j in 1..m) dmax_j[j] + sum(x in Jt[1])a[x] 
// + sum(t in 1..T, i in 1..n, j in Jt[t] inter lambda_i[i]) x[<t,i,j>];
//////////////

//
//tuple cPair {
//	int i;
//	int j;
//	int k;
//};
//

//
//tuple cz {
//	int i;
//	int j;
//	int t;
//};
//
//
//{cPair} P = ...;

//
//float M = C;
//
//dvar float+ x[dvd];
//dvar int y[dvd] in 0..1;
//dvar int z[1..n][1..m][1..T] in 0..1;
//

 