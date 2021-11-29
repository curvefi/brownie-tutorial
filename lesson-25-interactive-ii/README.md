# Interactive Debugging II

## [🎥 Video 25: Interactive Debugging II 🎬](https://youtu.be/4NQrPkHtk3Y)

The Brownie interactive flag allows for extra convenience with debugging and development of smart contracts.  When a test fails, it drops you right on a console at the exact point of failure with access to all relevant variables.


## PYTEST MARK SKIP
Use the pytest skip decorator to unconditionally skip a test. 

        > import pytest
        >
        > @pytest.mark.skip(reason="Description")
        > ...

## HYPOTHESIS SETTINGS
Adjust a setting for one particular function.  Brownie specific settings include deadline, max_examples, report_multiple_bugs, stateful_step_count

        > from hypothesis import settings
        >
        > @settings(setting=value)
        > ...

## TRACEBACK
Returns an error traceback for the transaction, similar to a regular python traceback. 

        > tx.traceback()
