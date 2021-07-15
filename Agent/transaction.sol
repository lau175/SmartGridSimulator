pragma solidity ^0.5.0;

contract transaction {
    address agent;
    mapping(address => uint256) public deposits;
    uint256[20] public meter_info;
    
    constructor () public {
        agent = msg.sender;
    }
    
    function deposit(address payee) public payable {
        uint256 amount = msg.value;
        deposits[payee] = deposits[payee] + amount;
    }
    
    function withdraw(address payable payee) public {
        uint256 payment = deposits[payee];
        deposits[payee] = 0;
        payee.transfer(payment);
    }
    
    function input_meter(uint256[20] memory newData) public returns (uint256[20] memory) {
       meter_info = newData; 
       return meter_info;
    } 
    
    function get_meter() public view returns( uint256[20] memory){
        return meter_info;
    }
    
}
