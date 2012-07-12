/*********************************************
 * OPL 6.3 Model
 * Author: Apple
 * Creation Date: 2012. 7. 10. at ¿ÀÀü 8:18:33
 *********************************************/
 
int Nbj = ...;    // # of jobs
int Nbm = ...;

range J = 1..Nbj;

float p[J] = ...;
float s[J][J] = ...;


// decision variables
dvar int a[J] in 1..Nbm;
dvar int y[J][J] in 0..1;
dvar float+ C[J];

// objective
minimize
	max (k in J) (C[k]);
	
// constraints
subject to {
	forall (j in J) forall (k in J: k > j) {
		(a[j] == a[k] && y[j][k] == 1) => (C[j] + s[j][k] + p[k] <= C[k]);
		(a[j] == a[k] && y[j][k] == 0) => (C[k] + s[k][j] + p[j] <= C[j]);  
	}
	
	forall (j in J) {
		C[j] >= p[j];
	}
}

execute {
	var fp = new IloOplOutputFile("list_scheduling.sol")
	writeln(a);
	writeln(y); 
} ;
