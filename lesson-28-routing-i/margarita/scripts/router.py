from brownie import *

from scripts.helpers.router import CurveRouter


def main():
    dai_router = CurveRouter(Contract("dai"))
    dai_router.summarize()
