// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title VulnerableContract
 * @notice VULNERABLE contract with multiple security issues
 * @dev DO NOT USE IN PRODUCTION - For testing purposes only
 */
contract VulnerableContract {
    address public owner;
    mapping(address => uint256) public balances;
    
    // VULNERABILITY: Uninitialized state variable used
    address public unauthorizedAddress;
    
    constructor() {
        owner = msg.sender;
    }
    
    // VULNERABILITY: No access control
    function setOwner(address _newOwner) public {
        owner = _newOwner;
    }
    
    // VULNERABILITY: tx.origin authentication
    function isOwner() public view returns (bool) {
        return tx.origin == owner;
    }
    
    // VULNERABILITY: Timestamp dependence
    function isLotteryTime() public view returns (bool) {
        return block.timestamp % 2 == 0;
    }
    
    // VULNERABILITY: Reentrancy
    function withdraw() public {
        uint256 amount = balances[msg.sender];
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success);
        balances[msg.sender] = 0; // State change after external call
    }
    
    // VULNERABILITY: Unchecked low-level call
    function callExternalContract(address _contract, bytes memory _data) public {
        _contract.call(_data); // Return value not checked
    }
    
    // VULNERABILITY: Delegatecall to untrusted contract
    function delegateCallToUntrusted(address _contract, bytes memory _data) public {
        _contract.delegatecall(_data);
    }
    
    // VULNERABILITY: Potential integer overflow (even with 0.8+, logic error)
    function unsafeMath(uint256 a, uint256 b) public pure returns (uint256) {
        return a + b * 2 / 3; // Unclear operation order
    }
    
    // VULNERABILITY: Locked ether - no withdraw function for contract balance
    receive() external payable {
        // Ether can be sent but never withdrawn
    }
    
    // VULNERABILITY: Uninitialized storage pointer
    function addToBalances(address _user, uint256 _amount) public {
        balances[_user] += _amount;
    }
    
    // GAS ISSUE: Inefficient loop
    function sumBalances(address[] memory _users) public view returns (uint256) {
        uint256 total = 0;
        for (uint256 i = 0; i < _users.length; i++) {
            total += balances[_users[i]]; // Reading from storage in loop
        }
        return total;
    }
    
    // GAS ISSUE: Using strings instead of custom errors
    function requireWithString() public pure {
        require(false, "This is an expensive error message that costs more gas");
    }
}