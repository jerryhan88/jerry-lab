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
dvar int z[1..T][1..n][1..m] in 0..1;
dvar float+ lambda[1..T][1..n][1..m];
dvar float+ y[1..T][1..n][1..m];

minimize
  sum( t in 1..T , i in 1..n , j in 1..m )
    C * w_j[j] * x[t][i][j];
    
subject to {
  forall( t in 1..T, i in 1..n)
    ct1:
      sum( j in 1..m)
        x[t][i][j] <= 1;
        
  forall( t in 1..T, i in 1..n)
    ct2:
      sum( j in 1..m)
        z[t][i][j] == 1;
        
  forall( l in 1..D )
    ct3:
      sum( t in 1..d_l[l] ,i in 1..n )
        y[t][i][f_l[l]] >= Q_l[l];
  
  forall( t in 1..T )
    ct4:
      sum( i in 1..n ,j in 1..m )
        b_j[j]*x[t][i][j] <= B;
      
  forall( i in 1..n, j in 1..m )
    ct5:
      lambda[1][i][j] == lamda_ij[i][j];
      
  forall( t in 2..T, i in 1..n, j,k in 1..m )
    ct6:
      lambda[t][i][k] == lambda[t-1][i][k] + beta * alpha_jk[j][k] + M * ( 1 - x[t-1][i][j]) ;
//      lambda[t][i][k] <= lamda_ij[i][k] + beta * alpha_jk[j][k] * 
//      				( sum(s in 1..(t-1))x[s][i][j] )
//      				+ M * ( 2 - x[t][i][k] - z[t][i][j]);
//      lambda[t][i][j] == lambda[t-1][i][j] + beta * alpha_jk[i][j] * x[t-1][i][j];
  
  forall( t in 1..T, i in 1..n, j,k in 1..m )
    ct7:
      y[t][i][k] <= lambda[t][i][k] * C + M * ( 1 - x[t][i][k]) ;
  
//  forall( t in 1..T, i in 1..n, j in 1..m )
//    ct8:
//      lambda[t][i][j] <= 1;
  forall( t in 1..T, i in 1..n, j in 1..m )
    ct9:
      y[t][i][j] <= C * x[t][i][j];
      
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
	
	fp.writeln("About z value")
	for (i = 1 ; i <= n ; i++) {
	  fp.write("(")
	  for (t = 1 ; t <= T ; t++){
	    for (j = 1 ; j <= m ; j++)
		  if (z[t][i][j] == 1) {
		    fp.write(j)
	      }	      
	    if (t!=T) {
	        fp.write(",")
	    }
      }	    
	  fp.writeln(")")
    }	  
    fp.writeln("About lambda value")
	for (i = 1 ; i <= n ; i++) {
	  fp.write("(")
	  for (t = 1 ; t <= T ; t++){
	    fp.write(lambda[t][i])
	    if (t!=T) {
	        fp.write(",")
	    }
      }	    
	  fp.writeln(")")
    }
    
    
	fp.close()
}
