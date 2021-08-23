# Applications II

## [🎥 Video 18: Applications II 🎬](https://youtu.be/tmLNwVJZbro)

Sample application: Search for arbitrage at the expense of Curve TriCrypto 


### CURVE TRICRYPTO
Curve v2 introduces pools among volatilely priced assets without external oracles.
TriCrypto automatically balances among USDT, Bitcoin, and Ethereum.


### TRICRYPTO WHITE PAPER
["Automatic market-making with dynamic peg", Michael Egorov, June 9, 2021](https://curve.fi/files/crypto-pools-paper.pdf)


### CURVE VIRTUAL PRICE
The virtual price affects the rate at which you can deposit and withdraw from a Curve pool.
Usually virtual price only increases from a value of 1 (with 18 decimals), representing interest earned.
Curve v2 Tricrypto virtual price is more complex and can occasionally decrease as asset prices shift.

        > pool.virtual_price()

### CURVE POOL BALANCE
Represents the number of raw tokens deposited into a pool.

        > pool.balances(coin_id)


### PRICE_ORACLE
TriCrypto contains an internal oracle of volatile asset's expected price.
The value is calculated as an exponential moving average, detailed in the white paper.

        > bitcoin_price = tricrypto.price_oracle(0)
        > ethereum_price = tricrypto.price_oracle(1)
 
### PRICE_SCALE
Price scale more closely approximates the pool's asset balance than price oracle.
The pool uses the difference between these values to repeg internally.

        > bitcoin_price_scale = tricrypto.price_scale(0)
        > ethereum_price_scale = tricrypto.price_scale(1)

