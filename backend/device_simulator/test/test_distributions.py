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

def test_normal_ge_99():
    dist = NormalDist(10,1)
    value = dist.generate_ge_99_pc_value()
    assert isinstance(value, float)
    assert value < 20

def test_beta_ge_99():
    dist = BetaDist(1,1,10)
    value = dist.generate_ge_99_pc_value()
    assert isinstance(value, float)
    assert value < 20