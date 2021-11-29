# Interactive Debugging

## [🎥 Video 24: Interactive Debugging I 🎬](https://youtu.be/zHQ4cjzIg1Y)

The Brownie interactive flag allows for extra convenience with debugging and development of smart contracts.  When a test fails, it drops you right on a console at the exact point of failure with access to all relevant variables.


## INTERACTIVE DEBUGGING MODE
When a test fails, open a console and interact with any variables at the point of failure.

        > brownie test --interactive
        > brownie test -I


## STRATEGY EXCLUSION
Pass the exclude flag to filter an object, iterable or callable 

        > strategy(strategy_type, excludes=...)

