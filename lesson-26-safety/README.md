# 🦧 Ape Safe 🦍

## [🎥 Video 26: Use Web3 Safely Using Brownie 🎬](https://youtu.be/ZetFUZbQMo4)

After some recent high profile hacks, learn how to navigate Web3 safer by running your transactions in Brownie.  Recent hacks have been so brazen as to inject malicious scripts into the UI, meaning you cannot necessarily trust a protocol's website nowadays.

The basic principles to increase your safety are as follows.:

1. Open a forked mainnet console using Brownie
2. Inspect the transaction details in Metamask
3. Decipher the transaction details using Brownie's `decode_input`
4. Run the transaction using Brownie.
5. Test the output matches expectations.
6. Exit the mainnet-fork
7. Launch a console in mainnet
8. Run the same transaction


## MAINNET FORK
Launch a fork of the mainnet to simulate transactions.
Use this to preview the transaction you're about to run.

	> brownie console --network mainnet-fork

## DECODE INPUT
Translate raw hex data from a Metamask contract preview.
Built-in function for any Brownie Contract container.

	> Contract(<address>).decode_input(<hex_data>)

## UNLOCKED ACCOUNTS
On development networks brownie can unlock accounts without the private key.
Accounts can be unlocked in the brownie config file or with the following command.

	> accounts.at(<address>, force=True)

## LOADING ACCOUNTS
To run your transaction on mainnet, you must first provide Brownie your private key

	> brownie accounts new <id>

To later load these accounts you'll provide a password set on import

	> accounts.load(<id>)

## WEI
Convert human readable units of ETH into raw wei (10 ** -18)

	> Wei('1 ether')
	> 1000000000000000000


