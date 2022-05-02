def test_deploy_new_gauge(alice, factory):
    tx = factory.deploy_gauge(alice, 2**256 - 1, {"from": alice})

    assert factory.get_gauge_count() == 1
    assert factory.get_gauge_by_idx(0) == tx.return_value
    assert tx.events["NewGauge"].values() == [tx.return_value, alice, 2**256 - 1]
