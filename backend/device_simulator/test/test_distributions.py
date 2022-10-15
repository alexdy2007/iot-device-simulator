from device_simulator.distributions import NormalDist, BetaDist

def test_normal():
    dist = NormalDist(10,1)
    value = dist.generate_value()
    assert isinstance(value[0], float)
    assert value[0] < 20

def test_beta():
    dist = BetaDist(1,1,10)
    value = dist.generate_value()
    assert isinstance(value[0], float)