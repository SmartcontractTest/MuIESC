/*
 * @source: https://github.com/trailofbits/not-so-smart-contracts/blob/master/integer_overflow/integer_overflow_1.sol
 * @author: -
 * @vulnerable_at_lines: 14
 */

 pragma solidity ^0.4.15;

 contract Overflow {
     uint private sellerBalance=0;

     function add(uint value) returns (bool){
         // <yes> <report> ARITHMETIC
sellerBalance +=uint128(value);//Mutation Here for <14>
         // possible auditor assert
         assert(sellerBalance >= value);  //<repair>
     }

  // function safe_add(uint value) returns (bool){
  //   require(value + sellerBalance >= sellerBalance);
  // sellerBalance += value;
  // } 
 }