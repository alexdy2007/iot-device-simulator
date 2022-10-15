from scipy.stats import beta, gamma, norm
from abc import ABC, abstractmethod
from typing import List, Dict, Any


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

    def generate_values(self, n:int=100) -> List[float]:
        random_gen = norm.rvs(loc=self.mean, scale=self.sd, size=100)    
        return random_gen

if __name__ == "__main__":
    norm_dist = NormalDist(10,1)
    print(norm_dist.generate_value())
    beta_dist = BetaDist(1,1,10)
    print(beta_dist.generate_value())

