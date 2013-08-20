int n = ...;
int m = ...;
int T = ...;
int D = ...;
float beta = ...;
float C = ...;
float B = ...;

int f_l[1..D] = ...;
int d_l[1..D] = ...;
float Q_l[1..D] = ...;

float b_j[1..m] = ...;
float w_j[1..m] = ...;

float C0_ij[1..n][1..m] = ...;
float alpha_jk[1..m][1..m] = ...;

float M = C;

dvar int x[1..T][1..n][1..m] in 0..1;
dvar float+ y[1..T][1..n][1..m];
dvar int z[1..T][1..n][1..m] in 0..1;

minimize
  sum( t in 1..T , i in 1..n , j in 1..m )
    C * w_j[j] * x[t][i][j];
    
subject to {
  
  forall( t in 1..T, i in 1..n)
    eq2:
      sum( j in 1..m) x[t][i][j] <= 1;
  
  forall( t in 1..T, i in 1..n, j in 1..m )
    eq3:
      y[t][i][j] <= C * x[t][i][j];
  
  forall( l in 1..D )
    eq4:
      sum( t in 1..d_l[l] ,i in 1..n ) y[t][i][f_l[l]] >= Q_l[l];
  
  forall( t in 1..T, i in 1..n, j,k in 1..m)
    eq5:
    y[t][i][k] <= 
    alpha_jk[j][k] * (C0_ij[i][j] + beta * sum(s in 1..(t-1)) x[s][i][j]) + beta 
    + M * (2 - x[t][i][k] - z[t][i][j]);
  
  forall( t in 1..T, i in 1..n )
    eq6:
    sum( j in 1..m ) z[t][i][j] == 1;
  
  forall( t in 1..T )
    eq7:
      sum( i in 1..n ,j in 1..m ) b_j[j]*x[t][i][j] <= B;
  };
  
execute {
	var fp = new IloOplOutputFile("Shoes Manufacturing.sol")
	fp.writeln(cplex.getObjValue())
	for (i = 1 ; i <= n ; i++) {
	  fp.write("[")
	  for (t = 1 ; t <= T ; t++){
	    var ct = 0
		var cq = 0
	    for (j = 1 ; j <= m ; j++)
	      if ( y[t][i][j] > cq ) {
	        ct = j
			cq = y[t][i][j]
	        }
	      fp.write("(" + ct + "," + cq)
	      if (t!=T) {
	        fp.write("),")
	      } else {
	        fp.write(")")
	      }	          
	  }
	  fp.writeln("]")
	}
	fp.close()
}
 