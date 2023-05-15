import numpy as np
import scipy.stats as ss
from dataclasses import dataclass, field
from .utils import get_z, generate_ci_report


@dataclass
class Metric:
    """
    a Model of metrics that used in an A/B experiment.
    p: float
        metric value.
    n: number of elements in the numenator of the metric.
    d_min: float
        minimum detectable effect.
    """
    p: float
    n: float
    d_min: float
    se: float = field(default=None, init=False)
    
    
    def __post_init__(self):
        if not self.se:
            self.se = self._calculate_se()
    
    
    def _calculate_se(self):
        return np.round( np.sqrt( self.p*(1-self.p)/self.n ), 4)
    

    
class MetricAnalyzer:
    
    def sanity_check(self, n_cont, n_exp, return_report=False):
        p = .5
        n_total = n_cont + n_exp
        p_hat = np.round( n_cont/n_total , 4 )
        se = self.calculate_proportion_se(p, n_total)
        ci = self.construct_CI(p, se)
        
        if return_report:
            generate_ci_report(p_hat, ci, msgs_dict={"type":"p_hat", 
                                                     "success_msg": "PASSED", 
                                                     "fail_msg": "FAILED"})
        else:
            return p_hat, ci
        
        
    def calculate_proportion_se(self, p, n):
        """
        Calculates the standard error given a proportion.
        p: float
            probability.
        n: float
            number of elements in a sample.
        returns:
            (float): standard error of a sample proportion. 
        """
        return np.sqrt( p*(1-p)/n )
            
    
    def construct_CI(self, p, se, q=.05, alternative="two-sides"):
        """
        Construct a confidence interval around the probability p.
        p: float
            probaility to construct a confidence interval around.
        se: float
            standard error.
        q: float
            alpha value, probability of type(I) error.
        alternative: str
            if the alpha value is calculated for one-tail or two-tail test
        """
        z = get_z(q=q, alternative=alternative)
        m = np.round(se * z, 4)
        return np.round(p-m, 4), np.round(p+m, 4)
    
    
    def calculate_pooled_proportion_se(self, pooled_p, n1, n2):
        """
        Calculates the standard error of two pooled proportions.
        pooled_p: float
            pooled proportion of two proportions p1, p2 such that pooled_p = (p1+p2)/2.
        n1: int
            size of the sample corresponding to p1.
        n2: int
            size of the sample corresponding to p2.
        returns:
            (float): standard error of a pooled proportion. 
        """
        return np.round( np.sqrt( pooled_p*(1-pooled_p)*(1/n1 + 1/n2) ) , 4)
    