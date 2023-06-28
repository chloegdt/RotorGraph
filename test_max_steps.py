import unittest
from rotorgraph import RotorGraph
from rotorconfig import RotorConfig
from vector import Vector
from particleconfig import ParticleConfig
from main import better_max_steps

def equal(n, x):
    if not n%2: return (x*n*n + n)//2 # even
    else: return (x*n*n - x + n + 1)//2 # odd

def different(n, x):
    return -2*x + n + 2*n*x

def f(n, x, y):
    if x == y: return equal(n, x)
    else: return different(n, min(x,y))


class TestMaxStep(unittest.TestCase):


    def test_max_steps(self):
        for n in range(1,20):
            for x in range(1,20):
                for y in range(x, x+5):
                    self.assertTrue(f(n,x,y)==better_max_steps(n,x,y))


if __name__ == '__main__':
    unittest.main()


