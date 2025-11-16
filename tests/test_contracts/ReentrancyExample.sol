// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title ReentrancyExample
 * @notice VULNERABLE contract for testing - Contains reentrancy vulnerability
 * @dev DO NOT USE IN PRODUCTION
 */
contract ReentrancyVulnerable {
    mapping(address => uint256) public balances;
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    // VULNERABILITY: Reentrancy attack possible
    function withdraw(uint256 _amount) public {
        require(balances[msg.sender] >= _amount, "Insufficient balance");
        
        // ISSUE: External call before state update
        (bool success, ) = msg.sender.call{value: _amount}("");
        require(success, "Transfer failed");
        
        // State updated AFTER external call - VULNERABLE!
        balances[msg.sender] -= _amount;
    }
    
    function getBalance() public view returns (uint256) {
        return balances[msg.sender];
    }
}

/**
 * @title ReentrancySecure
 * @notice SECURE version - Follows Checks-Effects-Interactions pattern
 */
contract ReentrancySecure {
    mapping(address => uint256) public balances;
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    // SECURE: State updated before external call
    function withdraw(uint256 _amount) public {
        require(balances[msg.sender] >= _amount, "Insufficient balance");
        
        // State updated BEFORE external call - SECURE!
        balances[msg.sender] -= _amount;
        
        // External call happens after state update
        (bool success, ) = msg.sender.call{value: _amount}("");
        require(success, "Transfer failed");
    }
    
    function getBalance() public view returns (uint256) {
        return balances[msg.sender];
    }
}