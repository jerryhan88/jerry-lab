int n = ...;
int m = ...;
int T = ...;
int D = ...;
float C = ...;
float B = ...;

int f_l[1..D] = ...;
int d_l[1..D] = ...;
float Q_l[1..D] = ...;

float b_j[1..m] = ...;
float w_j[1..m] = ...;

float lamda_ij[1..n][1..m] = ...;
float alpha_jk[1..m][1..m] = ...;
float u_j[1..m] = ...;

float M = C;

dvar int x[1..T][1..n][1..m] in 0..1;
dvar float+ gamma[2..T][1..n][1..m];
dvar float+ y[1..T][1..n][1..m];

minimize
  sum( t in 1..T , i in 1..n , j in 1..m )
    C * w_j[j] * x[t][i][j];
    
subject to {
  forall( t in 1..T, i in 1..n)
    eq2:
      sum( j in 1..m) x[t][i][j] <= 1;
        
  forall( t in 2..T, i in 1..n, k in 1..m )
    eq5:
      gamma[t][i][k] 
      <= sum( j in 1..m) sum(s in 1..(t-1)) alpha_jk[j][k] * x[s][i][j]
      - sum(s in 1..(t-1)) alpha_jk[k][k] * x[s][i][k];
  
  forall( t in 2..T, i in 1..n, k in 1..m )
    eq6:
      gamma[t][i][k] <= u_j[k];    
  
  forall( t in 2..T, i in 1..n, k in 1..m )
    eq7:
      y[t][i][k] 
      <= lamda_ij[i][k] + gamma[t][i][k] + sum(s in 1..(t-1)) alpha_jk[k][k] * x[s][i][k];
      
  forall( i in 1..n, k in 1..m )
    eq7_:
      y[1][i][k] <= lamda_ij[i][k];  
      
  forall( t in 1..T, i in 1..n, k in 1..m )
    eq8:
      y[t][i][k] <= C * x[t][i][k];
  
   forall( l in 1..D )
    eq9:
      sum( t in 1..d_l[l] ,i in 1..n ) y[t][i][f_l[l]] >= Q_l[l];
      
   forall( t in 1..T )
    eq10:
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
	
	fp.writeln("About x value")
	for (i = 1 ; i <= n ; i++) {
	  fp.write("(")
	  for (t = 1 ; t <= T ; t++){
	    fp.write(x[t][i])
	    if (t!=T) {
	        fp.write(",")
	    }
      }	    
	  fp.writeln(")")
    }
	
	fp.writeln("About gamma value")
	for (i = 1 ; i <= n ; i++) {
	  fp.write("(")
	  for (t = 2 ; t <= T ; t++){
	    fp.write(gamma[t][i])
	    if (t!=T) {
	        fp.write(",")
	    }
      }	    
	  fp.writeln(")")
    }
	fp.close()
}