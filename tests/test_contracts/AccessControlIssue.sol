// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title AccessControlIssue
 * @notice VULNERABLE contract - Contains access control issues
 * @dev DO NOT USE IN PRODUCTION
 */
contract AccessControlVulnerable {
    address public owner;
    uint256 public value;
    
    constructor() {
        owner = msg.sender;
    }
    
    // VULNERABILITY: Missing access control
    function changeOwner(address _newOwner) public {
        owner = _newOwner;
    }
    
    // VULNERABILITY: Using tx.origin instead of msg.sender
    function withdraw() public {
        require(tx.origin == owner, "Not owner");
        payable(owner).transfer(address(this).balance);
    }
    
    // VULNERABILITY: Anyone can call this critical function
    function updateValue(uint256 _newValue) public {
        value = _newValue;
    }
    
    receive() external payable {}
}

/**
 * @title AccessControlSecure
 * @notice SECURE version with proper access control
 */
contract AccessControlSecure {
    address public owner;
    uint256 public value;
    
    error NotOwner();
    error InvalidAddress();
    
    modifier onlyOwner() {
        if (msg.sender != owner) revert NotOwner();
        _;
    }
    
    constructor() {
        owner = msg.sender;
    }
    
    // SECURE: Only owner can change owner
    function changeOwner(address _newOwner) public onlyOwner {
        if (_newOwner == address(0)) revert InvalidAddress();
        owner = _newOwner;
    }
    
    // SECURE: Using msg.sender instead of tx.origin
    function withdraw() public onlyOwner {
        payable(owner).transfer(address(this).balance);
    }
    
    // SECURE: Protected with onlyOwner
    function updateValue(uint256 _newValue) public onlyOwner {
        value = _newValue;
    }
    
    receive() external payable {}
}