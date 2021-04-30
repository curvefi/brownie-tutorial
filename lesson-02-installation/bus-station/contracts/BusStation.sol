// SPDX-License-Identifier: MIT
// Pool Party proof of concept, a one-way bus trip

/*-+++++++--\                                                                         
     /    :####:   \                                                   
    /     .####.    \                                                     
   /==-    .##.   -==\                                                          
   +#####++.##.++####+                                                                  
   +#####++.##.++####+........................................................             
   \==-    .##.   -==/.-----------------------------------------------------+.             
    \     .####.    / ~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:|.             
     \    :####:   /~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:|.
      \--+++++++--/~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.::|.
                .|~:.:~:.::      ~::  \   / ~:.:~:.:~:.:~::  ~::~:.:~:.:~:~.|.
                :|::~:.:~~:   :  ~:    .:.   ~:   |    ~:.:  ~:.:~:.:~:.:~::|.
                :|~:.:~:.::      ~:---=:::=--: \ .::./  ~::  ::~:.:~~:.:~:~.|.
                :|:~.~:.~:.   ~:.::     .    :   ::::   ~::  ~:.:~:.:~:.:~::|.
                :|~:.:~:.:.   ~:.:~::  / \  .: /  .. \  ~::      :.:~:.:~::~|.
                :|:~:.:~:.:~:.:~:.:~:.:~:.:~:.::.  |  .~:.:~:.:~::~:.:~:.:~:|.
                :|~:.:~:.::.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:~|.
                :|~::~:.:~:      ~::   ~::      :       :  :  ~:.:~:.:~:.:~:|.
                :|~:.:~:.:~   :  ~:     ~:   :  ~::   ~::  .  ~:.:~:.:~:.:~:|.
                :|:~:.:~:.:      ~:  :  ~:     .~::   ~:.:   ~:.:~:.:~:.:~::|.
                :|~:.:~:.:~   ~:.::     ~:  .   ~::   ~:~:   ~:.:~:/--+++++++--\  
                :|:.:~:.:~:   ~:..:  :  ~:  ~:  ~::   ~:.:. .~:.::/    :####:   \    
                :|~:~.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:/     .####.    \  
                :|:.:~:.:~:.:~:.:.~:.:~:.:~:.:~:.:~:.:~:.:~:.:~:/=-     .##.    -=\  
                :|~:.:~:.:~:.:~:.:~::~:.:~:.:~:.:~:.:~:.:~~:.:~:+#####++.##.++####+      
                :+----------------------------------------------+#####++.##.++####+      
                ................................................\=-     .##.    -=/      
                                                                 \     .####.    /       
                                                                  \    :####:   /        
                                                                   \--+++++++-*/

pragma solidity ^0.8.0;

contract BusStation {
    /* ==== Variables ===== */

    mapping(uint256 => BusRoute) public routes;
    mapping(address => mapping(uint256 => uint256)) public tickets; // User -> Route -> value
    mapping(uint256 => uint256) public routeBalance;

    struct BusRoute {
        address payable _destination;
        uint256 _minTicketValue;
        uint256 _maxTicketValue;
        uint256 _minWeiToLeave;
        uint256 _endOfTimelock;
        bool _hasBusLeft;
    }

    uint256 public _routeId; // Current Bus Route Counter

    /* ==== Functions ===== */
    // Create a bus route
    function deployRoute(
        address payable destination,
        uint256 minTicketValue,
        uint256 maxTicketValue,
        uint256 minWeiToLeave,
        uint256 timelockSeconds
    ) external returns (uint256) {
        _routeId += 1;
        routes[_routeId] = BusRoute(
            destination,
            minTicketValue,
            maxTicketValue,
            minWeiToLeave,
            block.timestamp + timelockSeconds,
            false
        );
        return _routeId;
    }

    // Purchase a bus ticket if eligible
    function buyBusTicket(uint256 routeId)
        external
        payable
        canPurchaseTicket(routeId)
    {
        uint256 _maxTicketValue = routes[routeId]._maxTicketValue;
        uint256 seatvalue = tickets[msg.sender][routeId];
        require(
            msg.value + seatvalue <= _maxTicketValue,
            "Cannot exceed max ticket value."
        );
        tickets[msg.sender][routeId] = msg.value + seatvalue;
        routeBalance[routeId] += msg.value;
    }

    // If bus is eligible, anybody can trigger the bus ride
    function triggerBusRide(uint256 routeId) external isReadyToRide(routeId) {
        uint256 amount = routeBalance[routeId];
        routeBalance[routeId] = 0;
        routes[routeId]._hasBusLeft = true;
        routes[routeId]._destination.transfer(amount);
    }

    // If eligible to withdraw, then pull money out
    function withdraw(uint256 routeId) external {
        //uint256 memory my_balance = tickets[msg.sender][routeId] = 0;
        //routeBalance[routeId] -= my_balance;

        // Cannot withdraw after bus departs
        require(routes[routeId]._hasBusLeft == false, "Bus has already left.");

        // Retrieve user balance
        uint256 amount = tickets[msg.sender][routeId];
        require(amount > 0, "Address does not have a ticket.");

        // Write data before transfer to guard against re-entrancy
        tickets[msg.sender][routeId] = 0;
        routeBalance[routeId] -= amount;
        payable(msg.sender).transfer(amount);
    }

    function hasBusLeft(uint256 routeId) public view returns (bool) {
        return (routes[routeId]._hasBusLeft);
    }

    function routeValue(uint256 routeId) public view returns (uint256) {
        return (routeBalance[routeId]);
    }

    /* === Modifiers === */

    // Can only purchase ticket if bus has not left and ticket purchase amount is small
    modifier canPurchaseTicket(uint256 routeId) {
        require(routes[routeId]._hasBusLeft == false, "The bus already left.");
        require(
            msg.value > routes[routeId]._minTicketValue,
            "Need to pay more for ticket."
        );
        _;
    }

    // Bus can ride if timelock is passed and tickets exceed reserve price
    modifier isReadyToRide(uint256 routeId) {
        require(
            routes[routeId]._endOfTimelock <= block.timestamp,
            "Function is timelocked."
        );
        require(routes[routeId]._hasBusLeft == false, "Bus is already gone.");
        require(
            routeBalance[routeId] >= routes[routeId]._minWeiToLeave,
            "Not enough wei to leave."
        );
        _;
    }
}
