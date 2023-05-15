import numpy as np
import scipy.stats as ss


def get_z(q, alternative="two-sides"):
    """
    Calculates z value given an area under the curve of the normal distribution.
    q: float
        Area under the curve.
    alternative: str
        define if the test is one tailed or two tailed.
        options: ["two-sides", "one-side"]
    returns:
        (float): z value in the z-axis of the normal distribution.
    """
    if alternative == "two-sides":
        return np.round( ss.norm.ppf(1-q/2), 3 )
    elif alternative == "one-side":
        return np.round( ss.norm.ppf(1-q), 3 )


# def generate_ci_report(d_hat, ci):
#     val = np.round(d_hat, 4)
#     lower = np.round(ci[0], 4)
#     upper = np.round(ci[1], 4)
    
#     if (d_hat < ci[0]):
#             print(f"d_hat={val}, ci=({lower}, {upper}), d_hat < {lower}")
#     elif d_hat > ci[1]:
#         print(f"d_hat={val}, ci=({lower}, {upper}), d_hat > {upper}")
#     else:
#         print(f"d_hat={val}, ci=({lower}, {upper}), {lower} ≤ d_hat ≤ {upper}")
        

def generate_ci_report(d_hat, ci, msgs_dict={"type":"d_hat"}):
    val = np.round(d_hat, 4)
    lower = np.round(ci[0], 4)
    upper = np.round(ci[1], 4)
    
    type_ = "" if not (t_msg := msgs_dict.get("type")) else t_msg
    success_msg = "" if not (s_msg := msgs_dict.get("success_msg")) else s_msg
    fail_msg = "" if not (f_msg := msgs_dict.get("fail_msg")) else f_msg
    
    if (d_hat < ci[0]):
            print(f"{type_}={val}, ci=({lower}, {upper}), {type_} < {lower}, {fail_msg}")
    elif d_hat > ci[1]:
        print(f"{type_}={val}, ci=({lower}, {upper}), {type_} > {upper}, {fail_msg}")
    else:
        print(f"{type_}={val}, ci=({lower}, {upper}), {lower} ≤ {type_} ≤ {upper}, {success_msg}")        
    