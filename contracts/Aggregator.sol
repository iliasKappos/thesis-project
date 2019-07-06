
pragma solidity ^0.5.0;

contract aggregator{
    uint public N;
    int[6][100] public l;
    int [6][100] public z;
    int p=1;
    int Pd=150000;
    int [100] public h;
    int[6][100] public x;
    int[6][100] public y;
    uint16 public k;
    int epsilon;
    address[] public whitelist;
    	mapping (address => bool) public waiting;
    	bool public problemSolved;
    	bool public init;


    constructor (address[] memory _whitelist,uint _N ,int _p) public{
    	p=_p;
    	N=_N;
    	whitelist=_whitelist;
    	resetWaiting();
    	problemSolved=false;
    	init=true;
    	k=0;
        epsilon = 10;
    }




    function submitInitialValue(int initialValue,uint i ) public{
    require(!problemSolved);
    require(init);


    if(waiting[msg.sender])
     {
    	 if(msg.sender==whitelist[i])
    	 {
    			 x[0][i]=initialValue;
    			 y[0][i]=x[0][i];
    			 waiting[msg.sender]=false;
    	 }
    	 else{revert();}
    }
    else{revert();}

    if(!stillWaiting()){
    	resetWaiting();
    	init=false;
    }
    }

    function submitValue(int value,uint i, uint16 iteration ) public{
    	require(!problemSolved);
    	require(iteration==k);
    	 if(waiting[msg.sender])
     {
    	 if(msg.sender==whitelist[i])
    	 {
    			 x[k+1][i]=value;
    			 waiting[msg.sender]=false;
    	 }
    	 else{revert();}
    }
    else{revert();}

    if(!stillWaiting()){
     updateY();
     resetWaiting();
     k++;

    }

    }

    function updateY() public {
        for(uint i=0; i<N; i++){
            if(i==0) z[k][i]=x[k+1][i]+(l[k][i])/p;
            else z[k][i]=z[k][i-1]+x[k+1][i]+(l[k][i])/p;

        }

         h[k]=(p*((Pd)-z[k][N-1]))/int(N);

        for(uint i; i<N; i++){

          y[k+1][i]=(h[k]/p)+x[k+1][i]+(l[k][i])/p;
          l[k+1][i]=l[k][i]+p*(x[k+1][i]-y[k+1][i]);
        }


        //elegxoume an sugkliname
        for(uint i=0; i<N; i++){
            if(abs(x[k+1][i],y[k+1][i]) > epsilon) return;
            if(abs(y[k+1][i],y[k][i]) > epsilon) return;
        }

        problemSolved = true;


    }

    function abs(int a, int b) public pure returns (int){
        if(a>b) return a-b;
        return b-a;
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
    	k = 0;
    	problemSolved = false;
    	resetWaiting();
    	init=true;
    		return;
    	}


}
