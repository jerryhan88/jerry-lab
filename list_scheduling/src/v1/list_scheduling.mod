/*********************************************
 * OPL 6.3 Model
 * Author: Apple
 * Creation Date: 2012. 7. 10. at ���� 8:18:33
 *********************************************/
 
int Nbj = ...;    // # of jobs
int Nbm = ...;

range J = 1..Nbj;

float p[J] = ...;
float s[J][J] = ...;


// decision variables
dvar int A[J] in 1..Nbm;
dvar float+ C[J];

// objective
minimize
	max (k in J) (C[k]);
	
// constraints
subject to {
	forall (j in J) forall (k in J: k > j) {
		(A[j] != A[k]) || (C[j] + s[j][k] + p[k] <= C[k] || C[k] + s[k][j] + p[j] <= C[j]);
	}
	
	forall (j in J) {
		C[j] >= p[j];
	}
}

execute {
	var fp = new IloOplOutputFile("list_scheduling.sol")
	fp.writeln(cplex.getObjValue())
	fp.close()
}
