# Developer Reverts

## [🎥 Video 23: Reverts 🎬](https://www.youtube.com/watch?v=9xaN1QEAch0)

When transactions cause the EVM to raise a revert message, Brownie provides capabilities to include these in tests.


## TESTING BEST PRACTICES
When writing tests, it is useful to first guarantee the test will fail for the reason you expect.  Once you are sure the test will fail, try adjusting your code and making sure the test will pass.  This can provide you confidence that the test will correctly capture the scope of your test.

## REVERTS

### BROWNIE REVERT
Transactions that revert raise a VirtualMachineError exception. 
To write assertions around this you can use brownie.reverts as a context manager.
Brownie will throw an AssertionError if transaction does not revert as expected.

        > with brownie.reverts():
        >      Contract.call_that_should_fail()

### REVERT MESSAGE
Optionally include a string as a brownie.reverts argument. 
The error string must match the contract's revert message to pass.

        > with brownie.reverts("Revert Message"):
        >       Contract.call_that_should_fail()

### DEVELOPER REVERT COMMENT
To save on gas costs on revert messages, they can be interpreted from comments.

*Solidity*

        > require(CONDITION); // dev: REVERT_MSG

*Vyper*

        > assert CONDITION # dev: REVERT_MSG

