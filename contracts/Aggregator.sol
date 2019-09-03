pragma solidity ^0.5.0;

contract aggregator{
    uint public N;
    int[50][1000] public l;
    int [50][1000] public z;
    int p=1;
    int Pd;
    int [1000] public h;
    int[50][1000] public x;
    int[50][1000] public y;
    uint16 public k;
    int epsilon;
    int f_flag;
    address[] public whitelist;
    	mapping (address => bool) public waiting;
    	bool public problemSolved;
    	bool public init;


    constructor (address[] memory _whitelist,uint _N ,int _p, int _Pd, int _epsilon, int _f_flag) public{
    	p=_p;
    	N=_N;
    	Pd=_Pd*1000;
    	whitelist=_whitelist;
    	resetWaiting();
    	problemSolved=false;
    	init=true;
    	k=0;
        epsilon = _epsilon;
        f_flag = _f_flag;
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
     if (f_flag == 0) updateY();
     else updateY_float();
     resetWaiting();
     k++;

    }

    }


    function updateY() public {
        for(uint i=0; i<N; i++){
             // compute y[k+1][i], l[k+1][i] if p int

            if(i==0) z[k][i]=x[k+1][i]+(l[k][i])/p;
            else z[k][i]=z[k][i-1]+x[k+1][i]+(l[k][i])/p;

        }

         h[k]=(p*((Pd)-z[k][N-1]))/int(N);

        for(uint i; i<N; i++){

          y[k+1][i]=(h[k]/p)+x[k+1][i]+(l[k][i])/p;
          l[k+1][i]=l[k][i]+p*(x[k+1][i]-y[k+1][i]);
        }

        //check for convergence


        for(uint i=0; i<N; i++){
            if(abs(x[k+1][i],y[k+1][i]) >epsilon) return;
            if((abs(y[k+1][i],y[k][i]))*p>epsilon) return;
        }
        problemSolved = true;
    }

    function updateY_float() public {
           // compute y[k+1][i], l[k+1][i] if p int

        for(uint i=0; i<N; i++){
            if(i==0) z[k][i]=x[k+1][i]+(l[k][i])*p;
            else z[k][i]=z[k][i-1]+x[k+1][i]+(l[k][i])*p;

        }

         h[k]=(((Pd)-z[k][N-1]))/(p*int(N));

        for(uint i; i<N; i++){

          y[k+1][i]=(h[k]*p)+x[k+1][i]+(l[k][i])*p;
          l[k+1][i]=l[k][i]+(x[k+1][i]-y[k+1][i])/p;
        }


        //check for convergence

        for(uint i=0; i<N; i++){
            if(abs(x[k+1][i],y[k+1][i]) >epsilon) return;
            if(((abs(y[k+1][i],y[k][i]))/p)>epsilon) return;
        }
        problemSolved = true;

    }


    function abs(int a, int b) public pure returns (int){
        if(a>=b) return a-b;
        return b-a;
    }

    function stillWaiting () view  public returns (bool) {
    			for (uint8 i=0; i<whitelist.length; i++){
    					if ( waiting[ whitelist[i] ] ){ return true; }
    			}
    			return false;
    	}

    	function resetWaiting () public returns(bool){
    			// Reset the boolean waiting for each address
    			for(uint8 i=0; i<whitelist.length; i++){
    					waiting[whitelist[i]] = true;
    			}
    			return true;
    	}
    	 function reset() public {
    		// Helper function in order to solve multiple times.
    	k = 0;
    	problemSolved = false;
    	resetWaiting();
    	init=true;
    		return;
    	}


}
