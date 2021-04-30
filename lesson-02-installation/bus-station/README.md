# Bus Station
We're going to the pool party!

![Pool Party!](poolparty.jpg)

## Vision

Awesome Ethereum dApps like Curve are like a virtual Pool Party... full of beautiful people having fun.  But you can't go.

The problem is it costs $50 to get there, $50 to restake, $50 to withdraw.  Gas fees are brutal, so it's like you have to rent a limo to get to the party.

Our mission is to provide affordable public transportation so everybody can party.  

We're set up a highly gas efficient dumb contracts that do nothing but take money for bus tickets.  At first it's on Ethereum (so maybe $10) but eventually on even cheaper chains.

When we have enough riders for the bus (whatever number makes it gas efficient), we have a "bus driver" contract that spends the gas to transport and stake on everybody's behalf as a group.  Bus driver keeps track of all account gains, and a small percentage goes to the bus driver to fund fees.  If it's rewards type, it's also becomes efficient for the bus driver to claim and potentially restake rewards if applicable (compounding).

Withdrawal works the same way... you can wait for a bus to fill up and we batch withdraw.  Also an optional express withdrawal option that pays full gas price, in case you need funds immediately.

Drawbacks are flexibility (may take time for buses to fill up), but if you can wait to get into pools then batching should be more efficient.

This is super early version, so we're open to adjusting based on thoughts and feedback, or if there's flaws we've missed.  Good idea?  Garbage idea?  Thoughts?  Ideas?

## How it Works

Our proof of concept contract is at [contracts/BusStation.sol](contracts/BusStation.sol)

Our first destination will be to the gas station to fill up.  It's not sexy, there's nobody in swimsuits yet.  

Nobody will get anything for taking the frst bus trip, except a receipt that proves they were on the first party bus.  It's not much, but at least you can prove you had a fun time.

If the bus successfully makes its frst trip, we'll have a proof of concept.  We'll use the funds to set up infrastructure to build the bus station.  This means...

## License

This repository is licensed under the [MIT License](LICENSE).
