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

float lamda_ij[1..n][1..m] = ...;
float alpha_jk[1..m][1..m] = ...;

float M = C;

dvar int x[1..T][1..n][1..m] in 0..1;
dvar float+ y[1..T][1..n][1..m];
dvar int z[1..T][1..n][1..m] in 0..1;

minimize
  sum( t in 1..T , i in 1..n , j in 1..m )
    C * w_j[j] * x[t][i][j];
    
subject to {
  
  forall( l in 1..D )
    ct2:
      sum( t in 1..d_l[l] ,i in 1..n )
        y[t][i][f_l[l]] >= Q_l[l];
  
  forall( t in 1..T )
    ct3:
      sum( i in 1..n ,j in 1..m )
        b_j[j]*x[t][i][j] <= B;
        
  forall( t in 1..T, i in 1..n)
    ct4:
      sum( j in 1..m ) x[t][i][j] <= 1;
      
  forall( t in 1..T, i in 1..n, j in 1..m )
    ct5:
      y[t][i][j] <= C * x[t][i][j];
      
  forall( t in 2..T, i in 1..n)
    ct6:
      sum( j in 1..m ) z[t][i][j] == 1;
  
  forall( t in 1..T, i in 1..n, j,k in 1..m)
    ct7:
      y[t][i][k] <= lamda_ij[i][k] + alpha_jk[j][k] * beta *
      ( sum(s in 1..(t-1))x[s][i][j] - (1 - ( (j==k) ? 1 : 0 ) ) ) 
	      + M * (2 - x[t][i][k] - z[t][i][j]);
      
  forall( t in 1..T, i in 1..n, j,k in 1..m)
    ct8:
      y[t][i][k] <= alpha_jk[j][k] * C * x[t][i][k]
	      + M * (2 - x[t][i][k] - z[t][i][j] );
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
