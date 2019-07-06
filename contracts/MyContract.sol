pragma solidity ^0.5.0;

contract Aggregator{

	// x and z are our primal variables.
	// y is the dual variable, managed by the aggregator.
	// x_final and z_final will store the final solution variables.

	// Note: All variables are made public for better exposition.
	int256 public P1;
	int256 public P1_final;
	int256 public P2;
	int256 public P2_final;
	int256 public y;
	uint8  public p;
	int256 public A;
	int256 public B;
	int256 public P_total;

	uint256 public eps_pri;  // Tolerance on primal residual
	uint256 public eps_dual;  // Tolerance on dual residual
	int256 public r;         // Primal residual
	int256 public s;         // Dual residual

	bool   public problemSolved;

	uint16 public iteration;
	address[] public whitelist;
	mapping (address => bool) public waiting;

// Having ADMM without a whitelist doesn't make sense


	constructor (address[] memory _whitelist) public{
		P1 = 0;
		y = 0;
		P2 = 0;
		p = 2;
		A = 1;
		B = 1;
		P_total = 4 * 1e6;

		P1_final = 0;
		P2_final = 0;

		eps_pri  = 1;
		eps_dual = 1;
		r = 0;
		s = 0;

		whitelist = _whitelist;
		iteration = 1;
		problemSolved = false;
		resetWaiting();
	}


   function submitValue (int256 myGuess, uint16 myiteration)public {

    	assert(! problemSolved);
    	assert(iteration == myiteration);

    	if (waiting[msg.sender]){
            // If we are still waiting for this sender, go ahead with the assignment.
            if (msg.sender == whitelist[0]){
                P1 = myGuess;
            } else if (msg.sender == whitelist[1]){
            	s = p * A * B * (myGuess - P2);
                P2 = myGuess;
            } else {revert();}
            waiting[msg.sender] = false;
    	} else { revert(); }

    	if (! stillWaiting() ){
    		updateY();
    		resetWaiting();
    		iteration += 1;
    	}
    }

	function updateY() public {
		// This is the critical

		r = A * P1 + B * P2 - P_total;
		if (r<0){r = r * -1;} // Equivalent to taking the absolute value (1-norm) of the residuals
		if (s<0){s = s * -1;}
		y = y + p * (A * P1+ B * P2 - P_total);

		if ((uint(r) < eps_pri) && (uint(s) < eps_dual)){
			P1_final = P1;
			P2_final = P2;
			problemSolved = true;
		}
		return;
	}

    function stillWaiting () view  public returns (bool) {
        for (uint8 i=0; i<whitelist.length; i++){
            if ( waiting[ whitelist[i] ] ){ return true; }
        }
        return false;
    }

    function resetWaiting () public returns(bool){
        // Reset the flag for each address
        for(uint8 i=0; i<whitelist.length; i++){
            waiting[whitelist[i]] = true;
        }
        return true;
    }

    function reset() public {
    	// Helper function to allow the problem to be poked multiple times.
		P1 = 0;
		P2 = 0;
		y = 0;
		P1_final = 0;
		P2_final = 0;
		iteration = 1;
		problemSolved = false;
		resetWaiting();
    	return;
    }

}
