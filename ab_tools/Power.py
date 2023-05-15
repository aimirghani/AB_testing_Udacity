import numpy as np
import scipy.stats as ss
from .utils import get_z


class Power_analyzer:
    """
    A class that contains a collection of methods to perform power analysis.
    """
    def __init__(self, alpha=.05, beta=.2):
        self.alpha = alpha
        self.beta = beta
        
        
    def _calculate_two_proportions_std(self, p1, p2):
        """
        Calculates the pooled std of 2 samples proportions.
        p1: float
            proportion of the first sample.
        p2: float
            proportion of the second sample.
        returns:
            (float): pooled standard deviation. 
        """
        return np.sqrt( p1*(1-p1) + p2*(1-p2) )
    
    
    def calculate_sample_size(self, p, d_min, alpha=None, beta=None):
        """
        Calculates the sample size needed for a proportions test with a power = 1 - beta.
        p: float
            Metric probability.
        d_min: float
            minimum detectable effect.
        alpha: float
            probability of type(I) error.
        beta: float
            probability of type(II) error.
        returns:
            (int): needed sample size for the test power corresponding to the specified beta.
        """
        alpha = self.alpha if alpha is None else alpha
        beta  = self.beta if beta is None else beta
        # z_alpha = self.get_z(alpha)
        # z_beta = self.get_z(beta, alternative="one-side")
        z_alpha = get_z(alpha)
        z_beta = get_z(beta, alternative="one-side")
        std_alpha = self._calculate_two_proportions_std(p, p)
        std_beta = self._calculate_two_proportions_std( p, p+d_min )
        
        return np.ceil( (z_alpha*std_alpha + z_beta*std_beta)**2 / d_min**2 )
        
    
    # def get_z(self, q, alternative="two-sides"):
    #     """
    #     Calculates z value given an area under the curve of the normal distribution.
    #     q: float
    #         Area under the curve.
    #     alternative: str
    #         define if the test is one tailed or two tailed.
    #         options: ["two-sides", "one-side"]
    #     returns:
    #         (float): z value in the z-axis of the normal distribution.
    #     """
    #     if alternative == "two-sides":
    #         return np.round( ss.norm.ppf(1-q/2), 3 )
    #     elif alternative == "one-side":
    #         return np.round( ss.norm.ppf(1-q), 3 )