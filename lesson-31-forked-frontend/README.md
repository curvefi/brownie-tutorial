# Forked Frontend

## [🎥 Video 31: Simulate Frontend Transactions on Forked Mainnet Backend 🎬](https://youtu.be/E4teMcWNX_Y)

It's often useful to connect a frontend with a mainnet-fork backend.  This is certainly useful for frontend developers, but it's also useful for regular users looking to extend the [recent lesson on safety](https://youtu.be/ZetFUZbQMo4).

This lesson demonstrated how to simulate a mainnet transaction using Brownie by launching the transaction in your browser wallet on mainnet, and decoding the transaction parameters in Brownie before you execute the transaction.

However, this process may not work well for multi-part transactions.  Typically the first transaction is an approval, so the process above would only let you decipher the least interesting step.  However, sometimes you can easily get information on the transaction process by connecting the frontend to a forked mainnet.

Some websites process web3 calls on the backend, so this method would not work.  However, if this works, you can run through the entire process using the frontend to simulate your transaction against a mainnet-fork and verify it looks correct before you run it for real.

The most important step here is to create a network in your browser wallet (ie Metamask) that points to your localhost with a Chain ID of 1.  You may also need to reset your transaction history (or set your nonce manually) if you use this method frequently.

## UNLOCKED ACCOUNTS
On development networks brownie can unlock accounts without the private key.
Accounts can be unlocked in the brownie config file or with the following command.

	> accounts.at(<address>, force=True)


