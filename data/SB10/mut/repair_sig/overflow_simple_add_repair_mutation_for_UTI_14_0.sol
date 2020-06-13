/*
 * @source: https://smartcontractsecurity.github.io/SWC-registry/docs/SWC-101#overflow-simple-addsol
 * @author: -
 * @vulnerable_at_lines: 14
 */

pragma solidity 0.4.21;

contract Overflow_Add {
    uint public balance = 1;

    function add(uint256 deposit) public {
        // <yes> <report> ARITHMETIC
balance +=int256(deposit);//Mutation Here for <14>
		require(balance > deposit);  //<repair>  
    }
}
