# get_dx() 

## [🎥 Video 32: get_dx() 🎬](https://youtu.be/ubCaX-QtV7Q)

Most Curve contracts have a `get_dy` function, telling how many tokens one would receive for a given input number.  Very few have a corresponding `get_dx` function.  This lesson shows three ways to calculate `get_dx`

* **Calculator:** The [Curve Calculator Contract](https://etherscan.io/address/0xc1DB00a8E5Ef7bfa476395cdbcc98235477cDE4E) includes a `get_dx` function for selected inputs.
* **Iterative:** One can randomly guess values until honing in on a final value.
* **Simulation:** Run the transaction on a forked mainnet to confirm results from either method above.

