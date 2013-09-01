int n = ...;			// # of lines
int m = ...;			// # of types
int T = ...;			// # of periods(planning horizon)
int R = ...;			// # of orders
int fr[1..R] = ...; 	// Type of accumulated order r
int dr[1..R] = ...;		// Due date of order r
int qr[1..R] = ...;		// Quantities of order r
{int} A_i[1..n] = ...;	// Set of types line i can produce
float l_j[1..m] = ...;	// # of labors needed for producing type j on a period
float w_j[1..m] = ...;	// Material costs of producing a unit of type j
float u_j[1..m] = ...;	// # of maximum lines type j can be assigned to in a period
float alpha_jk[1..m][1..m] = ...;
						// Coefficient of type k¡¯s learning effect for type j
float C0_ij[1..n][1..m] = ...;
						// Initial capable amount of type j which line i can produce
float beta = ...;		// Ramp-up quantity
float C = ...;			// Line capacity
float L = ...;			// Maximum available labors on a period
float M = C;			// Large number

// constraint option
int p2 = ...;
int p3 = ...;

int Qr[r in 1..R] = 	// Quantities of accumulated orders
	sum( _r in 1..R : fr[r] == fr[_r] && dr[_r] <=dr [r]) qr[_r];
int dmax_j[j in 1..m] = // Last due date among type j¡¯s orders
	max(r in 1..R : fr[r] == j ) dr[r];
{int} Jt[t in 1..T] =	// Set of types which need to be considered in period t 
	{j | j in (1..m) : t <= dmax_j[j]};
// (P2)
float max_jk[j in 1..m] = // find maximum learning effect about type j 
	max(k in 1..m : j !=k ) alpha_jk[j][k]*C;
{int}P_i[i in 1..n] = 	// Set of types whose learning effect is considered firstly
	{j | j in (1..m) : C0_ij[i][j] >= max_jk[j]};
// (P3)
int maxQ_j[j in 1..m] = // find maximum accumulated demand amount for each type
	max(r in 1..R: j == fr[r] && dmax_j[j] == dr[r]) Qr[r];
float minC_j[j in 1..m] = // find minimum line's initial capacity for each type
	min(i in 1..n) C0_ij[i][j];
float H_j[j in 1..m] =	// # of type j¡¯s maximum assignment
	ceil(maxQ_j[j] / minC_j[j]);
						
tuple dom {
	int t;
	int i;
	int j;
};

{dom} xyd = {<t, i, j> | t in 1..T, i in 1..n, j in Jt[t] inter A_i[i] };
{dom} zd = {<t, i, k> | t in 1..T, i in 1..n, k in A_i[i] };

dvar float+ x[xyd];
dvar int y[xyd] in 0..1;
dvar int z[zd] in 0..1;

minimize
  sum(t in 1..T, i in 1..n, j in Jt[t] inter A_i[i] ) w_j[j] * C * y[<t, i, j>]; 
    
subject to {
  
  forall( t in 1..T, i in 1..n )
    eq2:
      sum( j in Jt[t] inter A_i[i] ) y[<t, i, j>] <= 1;

  forall( t in 1..T, i in 1..n, j in 1..m : j in Jt[t] inter A_i[i] )
    eq3:
      x[<t, i, j>] <= C * y[<t, i, j>];
                    
  forall( r in 1..R )
    eq4:
      sum( t in 1..dr[r] ,i in 1..n : fr[r] in A_i[i] ) x[<t, i, fr[r]>] >= Qr[r];
  
  if ( p2 == 0 ) {	
  forall( t in 1..T, i in 1..n, j in 1..m, k in 1..m : j in Jt[t] inter A_i[i] && k in A_i[i])
    eq5:
      x[<t, i, j>] <= alpha_jk[j][k] * 
      (C0_ij[i][k] + beta * sum(s in 1..(t-1 <= dmax_j[k] ? t-1 : dmax_j[k])) y[<s, i, k>] )
      + beta + M * (2 - z[<t, i, k>] - y[<t, i, j>] );
  }  
  forall( t in 1..T, i in 1..n, j in 1..m, k in 1..m : j in Jt[t] inter A_i[i] && k in A_i[i])
    eq6:
      x[<t, i, j>] <= alpha_jk[j][k] * C
      + beta + M * (2 - z[<t, i, k>] - y[<t, i, j>] );
      
  forall( t in 1..T, i in 1..n )
    eq7:
      sum( k in A_i[i] ) z[<t, i, k>] == 1;

  forall( t in 1..T )
    eq8:
	  sum( i in 1..n , j in Jt[t] inter A_i[i] ) l_j[j] * y[<t, i, j>] <= L;

  forall( t in 1..T, j in 1..n : j in Jt[t] )
    eq9:
      sum( i in 1..n : j in A_i[i] ) y[<t, i, j>] <= u_j[j];
      
  if ( p2 == 1 ) {
  //(P2)  
  forall( t in 1..T, i in 1..n, j in 1..m, k in 1..m : j in Jt[t] inter A_i[i] inter P_i[i])
    eq5_1:
      x[<t, i, j>] <= alpha_jk[j][j] * 
      (C0_ij[i][j] + beta * sum(s in 1..(t-1)) y[<s, i, j>] )
      + beta + M * (1 - y[<t, i, j>] );
      
  forall( t in 1..T, i in 1..n, j in 1..m, k in 1..m : j in Jt[t] inter A_i[i] diff P_i[i] && k in A_i[i])
    eq5_2:
      x[<t, i, j>] <= alpha_jk[j][k] * 
      (C0_ij[i][k] + beta * sum(s in 1..(t-1 <= dmax_j[k] ? t-1 : dmax_j[k])) y[<s, i, k>] )
      + beta + M * (2 - z[<t, i, k>] - y[<t, i, j>] );
  }

  if ( p3 == 1 ) {
  //(P3)      
  forall( j in 1..m )
    eq10:
      sum( t in 1..dmax_j[j], i in 1..n : j in A_i[i] ) y[<t, i, j>] <=  H_j[j];
  }      
  };
  
execute {
	var fp = new IloOplOutputFile("Shoes Manufacturing.sol")
	fp.writeln(cplex.getObjValue())
	
	for (i in xyd)
	  fp.write("x" + i + " = " + x[i] + "\n")
	for (i in xyd)
	  fp.write("y" + i + " = " + y[i] + "\n")
	for (i in zd)
	  fp.write("z" + i + " = " + z[i] + "\n")
		  
	fp.close()
}
