/*
 * @source: https://github.com/sigp/solidity-security-blog
 * @author: Steve Marx
 * @vulnerable_at_lines: 20,22
 */

 pragma solidity ^0.4.18;

 contract Token {

   mapping(address => uint) balances;
   uint public totalSupply;

   function Token(uint _initialSupply) {
balances[msg.sender] = totalSupply =uint128(_initialSupply);//Mutation Here for <15>
   }

   function transfer(address _to, uint _value) public returns (bool) {
     // <yes> <report> ARITHMETIC
	 require(balances[msg.sender] >= _value);  //<repair>
     require(balances[msg.sender] - _value >= 0);    //<underflow>
     // <yes> <report> ARITHMETIC
     balances[msg.sender] -= _value;  //<underflow>
     balances[_to] += _value;  //<overflow>
	 require(balances[_to] >= _value);  //<repair>
     return true;
   }

   function balanceOf(address _owner) public constant returns (uint balance) {
     return balances[_owner];
   }
 }
