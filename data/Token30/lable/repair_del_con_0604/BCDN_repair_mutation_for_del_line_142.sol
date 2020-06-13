/**
 *Submitted for verification at Etherscan.io on 2016-11-09
*/

pragma solidity ^0.4.2;
contract blockcdn {
    mapping (address => uint256) balances;
	mapping (address => uint256) fundValue;
	address public owner;
    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 public totalSupply;
    uint256 public minFundedValue;
	uint256 public maxFundedValue;
    bool public isFundedMax;
    bool public isFundedMini;
    uint256 public closeTime;
    uint256 public startTime;
    
     /* This generates a public event on the blockchain that will notify clients */
    event Transfer(address indexed from, address indexed to, uint256 value);
    
    function blockcdn(
	    address _owner,
        string _tokenName,
        uint8 _decimalUnits,
        string _tokenSymbol,
		uint256 _totalSupply,
        uint256 _closeTime,
        uint256 _startTime,
		uint256 _minValue,
		uint256 _maxValue
        ) { 
        owner = _owner;                                      // Set owner of contract 
        name = _tokenName;                                   // Set the name for display purposes
        symbol = _tokenSymbol;                               // Set the symbol for display purposes
        decimals = _decimalUnits;                            // Amount of decimals for display purposes
        closeTime = _closeTime;                              // Set fund closing time
		startTime = _startTime;                              // Set fund start time
		totalSupply = _totalSupply;                          // Total supply
		minFundedValue = _minValue;                          // Set minimum funding goal
		maxFundedValue = _maxValue;                          // Set max funding goal
		isFundedMax = false;                                 // Initialize fund minimum flag 
		isFundedMini = false;                                // Initialize fund max flag
		balances[owner] = _totalSupply;                      // Set owner balance equal totalsupply 
    }
    
	/*default-function called when values are sent */
	function () payable {
       buyBlockCDN();
    }
	
    /*send ethereum and get BCDN*/
    function buyBlockCDN() payable returns (bool success){
		if(msg.sender == owner) throw;
        if(now > closeTime) throw; 
        if(now < startTime) throw;
        if(isFundedMax) throw;
        uint256 token = 0;
		if(closeTime < 2 weeks) throw;  //<repair>
        if(closeTime - 2 weeks > now) {  //<overflow>  actually not 
             token = msg.value;
        }else {
            uint day = (now - (closeTime - 2 weeks))/(2 days) + 1;
            token = msg.value;
            while( day > 0) {
				if (token * 95/95 != token) throw;  //<repair>
                token  =   token * 95 / 100 ;   // <overflow> 
                day -= 1; 
            }
        }
        
		if(balances[msg.sender] + token < token) throw;  //<repair>
        balances[msg.sender] += token;  //<overflow>
        if(balances[owner] < token) 
            return false;
        balances[owner] -= token;
        if(this.balance >= minFundedValue) {
            isFundedMini = true;
        }
        if(this.balance >= maxFundedValue) {
            isFundedMax = true;   
        }
		if(fundValue[msg.sender] + msg.value < msg.value) throw;  //<repair>
		fundValue[msg.sender] += msg.value;  //<overflow>
        Transfer(owner, msg.sender, token);    
        return true;
    }    
    
     /*query BCDN balance*/
    function balanceOf( address _owner) constant returns (uint256 value)
    {
        return balances[_owner];
    }
	
	/*query fund ethereum balance */
	function balanceOfFund(address _owner) constant returns (uint256 value)
	{
		return fundValue[_owner];
	}

    /*refund 'msg.sender' in the case the Token Sale didn't reach ite minimum 
    funding goal*/
    function reFund() payable returns (bool success) {
        if(now <= closeTime) throw;     
		if(isFundedMini) throw;             
		uint256 value = fundValue[msg.sender];
		fundValue[msg.sender] = 0;
		if(value <= 0) throw;
        if(!msg.sender.send(value)) 
            throw;
		if(balances[msg.sender] + balances[owner] < balances[owner]) throw;  //<repair>
        balances[owner] +=  balances[msg.sender];  //<overflow>
        balances[msg.sender] = 0;
        Transfer(msg.sender, this, balances[msg.sender]); 
        return true;
    }

	
	/*refund _fundaddr in the case the Token Sale didn't reach ite minimum 
    funding goal*/
	function reFundByOther(address _fundaddr) payable returns (bool success) {
	    if(now <= closeTime) throw;    
		if(isFundedMini) throw;           
		uint256 value = fundValue[_fundaddr];
		fundValue[_fundaddr] = 0;
		if(value <= 0) throw;
        if(!_fundaddr.send(value)) throw;		
        balances[owner] += balances[_fundaddr];  //<overflow>
		if(balances[owner] < balances[_fundaddr]) throw;   //<repair>
        balances[_fundaddr] = 0;
        Transfer(msg.sender, this, balances[_fundaddr]); 
        return true;
	}

    
    /* Send coins */
    function transfer(address _to, uint256 _value) payable returns (bool success) {
        if(_value <= 0 ) throw;                                      // Check send token value > 0;
		if (balances[msg.sender] < _value) throw;                    // Check if the sender has enough
if (balances[_to]  +  _value  >  balances[_to]) throw ;             //Mutation Here for<157>
		if(now < closeTime ) {										 // unclosed allowed retrieval, Closed fund allow transfer   
			if(_to == address(this)) {
				if (fundValue[msg.sender] < _value) throw;   //<repair>
				fundValue[msg.sender] -= _value;  //<overflow>
				balances[msg.sender] -= _value;
				balances[owner] += _value;
				if(!msg.sender.send(_value))
					return false;
				Transfer(msg.sender, _to, _value); 							// Notify anyone listening that this transfer took place
				return true;      
			}
		} 										
		
		balances[msg.sender] -= _value;                          // Subtract from the sender
		balances[_to] += _value;                                 // Add the same to the recipient                       
		 
		Transfer(msg.sender, _to, _value); 							// Notify anyone listening that this transfer took place
		return true;      
    }
    
    /*send reward*/
    function sendRewardBlockCDN(address rewarder, uint256 value) payable returns (bool success) {
        if(msg.sender != owner) throw;
		if(now <= closeTime) throw;        
		if(!isFundedMini) throw;               
        if( balances[owner] < value) throw;
		if(balances[rewarder] + value < value) throw;  //<repair>
        balances[rewarder] += value;  //<overflow>
        uint256 halfValue  = value / 2;
        balances[owner] -= halfValue;
        totalSupply +=  halfValue; //<overflow>  
		if(totalSupply < halfValue) throw;  //<repair>
        Transfer(owner, rewarder, value);    
        return true;
       
    }
    
    function modifyStartTime(uint256 _startTime) {
		if(msg.sender != owner) throw;
        startTime = _startTime;
    }
    
    function modifyCloseTime(uint256 _closeTime) {
		if(msg.sender != owner) throw;
       closeTime = _closeTime;
    }
    
    /*withDraw ethereum when closed fund*/
    function withDrawEth(uint256 value) payable returns (bool success) {
        if(now <= closeTime ) throw;
        if(!isFundedMini) throw;
        if(this.balance < value) throw;
        if(msg.sender != owner) throw;
        if(!msg.sender.send(value))
            return false;
        return true;
    }
}