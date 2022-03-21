from brownie import CRVFunder, accounts


def main():
    return CRVFunder.deploy({"from": accounts[0]})
