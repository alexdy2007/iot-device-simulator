from scipy.stats import beta, gamma, norm
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import random
import numpy as np

class Distribution(ABC):

    def __str__():
        return "String Rep Not Defined"

    @abstractmethod
    def generate_value(self) -> List[float]:
        return NotImplementedError

    @abstractmethod
    def generate_value(self, n:int) -> List[float]:        
        return NotImplementedError
    
    @abstractmethod
    def generate_ge_99_pc_value(self) -> List[float]:        
        return NotImplementedError

    @abstractmethod
    def get_info(self) -> Dict[str, Any]:        
        return NotImplementedError


class BetaDist(Distribution):
    
    def __init__(self, a, b, scale):
        self.a = a
        self.b = b
        self.scale = scale

    def get_info(self):
        return {
            "dist_type":'Beta',
            'a': self.a,
            'b': self.b,
            'scale': self.scale,
            'str_format': self.__str__()
        }

    def __str__(self):
        return f"Beta({self.a}, {self.b}) scale={self.scale}"
    
    def generate_value(self) -> List[float]:
        random_gen = beta.rvs(self.a,self.b,size=1, scale=self.scale)
        return random_gen
    
    def generate_ge_99_pc_value(self) -> List[float]:
        random_gen = beta.ppf(0.99,self.a,self.b, scale=self.scale) + random.random()*self.scale
        return random_gen

    def generate_values(self, n=100) -> List[float]:
        random_gen = beta.rvs(self.a,self.b,size=n, scale=self.scale)
        return random_gen


class NormalDist(Distribution):

    def __init__(self,mean, sd):
        self.mean = mean
        self.sd = sd

    def get_info(self):
        return {
            "dist_type":'Normal',
            'mean': self.mean,
            'sd': self.sd,
            'str_format': self.__str__()
        }

    def __str__(self):
        return f"NormalDist({self.mean}, {self.sd})"

    def generate_value(self) -> List[float]:
        random_gen = norm.rvs(loc=self.mean, scale=self.sd, size=1)    
        return random_gen
    
    def generate_ge_99_pc_value(self) -> List[float]:
        random_gen = norm.ppf(0.99,loc=self.mean, scale=self.sd) + random.random()*self.sd
        return random_gen

    def generate_values(self, n:int=100) -> List[float]:
        random_gen = norm.rvs(loc=self.mean, scale=self.sd, size=100)    
        return random_gen


class CyclicalNormalErrorDist(Distribution):

    def __init__(self,mean=0.1, sd=0.1, readings_per_cycle=10, scale=10):
        self.mean = mean
        self.sd = sd
        self.scale = scale
        self.readings_per_cycle = readings_per_cycle
        self.cycle_num = 0
        self.cycle_inc = 360/readings_per_cycle
        self.cycle_progress = 0

    def get_info(self):
        return {
            "dist_type":'CyclicalNormalErrorDist',
            'mean': self.mean,
            'sd': self.sd,
            'readings_per_cycle':self.readings_per_cycle,
            'str_format': self.__str__()
        }

    def __str__(self):
        return f"NormalDist({self.mean}, {self.sd})"

    def generate_value(self) -> List[float]:
        noise = random.normalvariate(self.mean,self.sd)
        if random.random()>=0.5:
            noise = noise*-1
        value = np.sin(np.deg2rad(self.cycle_progress)) + 1
        self.cycle_num = self.cycle_num + 1
        self.cycle_progress = (self.cycle_progress + self.cycle_inc)%360
        return [float(value+noise)*self.scale]
    
    def generate_ge_99_pc_value(self) -> List[float]:
        random_gen = norm.ppf(0.99,loc=self.mean, scale=self.sd) + random.random()*self.sd
        return random_gen

    def generate_values(self, n:int=100) -> List[float]:
        random_gen = [self.generate_value() for x in range(n)]
        return random_gen

if __name__ == "__main__":
    norm_dist = NormalDist(10,1)
    print(norm_dist.generate_value())
    beta_dist = BetaDist(1,1,10)
    print(beta_dist.generate_value())
    cyc_dist = CyclicalNormalErrorDist()
    print(cyc_dist.generate_value())

