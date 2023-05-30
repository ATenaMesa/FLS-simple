import pandas as pd

def k_exponent(ENV, S_N_Curve):
    k_a = pd.DataFrame({'S_N_curve': ['B1', 'B2', 'C', 'C1', 'C2', 'D', 'E', 'F', 'F1', 'F3', 'G', 'W1', 'W2', 'W3'],
                        'k': [0, 0, 0.05, 0.10, 0.15, 0.2, 0.2, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]})
    k_w = pd.DataFrame({'S_N_curve': ['B1', 'B2', 'C', 'C1', 'C2', 'D', 'E', 'F', 'F1', 'F3', 'G', 'W1', 'W2', 'W3'],
                        'k': [0, 0, 0.05, 0.10, 0.15, 0.2, 0.2, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]})
    if ENV == "AIR":
        k = k_a
    elif ENV == "SEAWATER":
        k = k_w
    else:
        print("Los valores de S_N_Curve y/o ENV no son válidos.")

    k_exp = k.loc[k['S_N_curve'] == S_N_Curve, 'k'].values[0]
    print(k_exp)
    return k_exp

k_exp = k_exponent("AIR", "F3")