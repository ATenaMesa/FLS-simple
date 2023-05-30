import pandas as pd
import os
from scipy.interpolate import LinearNDInterpolator
import numpy as np

def Reduction_factor(n, h, ENV, S_N_Curve):
    if ENV == "AIR" and S_N_Curve == "B1_B2":
        archivo = "Red_factor_air_B1_B2.csv"
    elif ENV == "AIR" and S_N_Curve == "C_W3":
        archivo = "Red_factor_air_C_W3.csv"
    elif ENV == "SEAWATER" and S_N_Curve == "B1_B2":
        archivo = "Red_factor_seawater_B1_B2.csv"
    elif ENV == "SEAWATER" and S_N_Curve == "C_W3":
        archivo = "Red_factor_seawater_C_W3.csv"
    else:
        print("Los valores de S_N_Curve y/o ENV no son válidos.")

    ruta_archivo_python = os.path.abspath(__file__)
    directorio_actual = os.path.dirname(ruta_archivo_python)
    ruta_archivo_csv = os.path.join(directorio_actual, archivo)
    df = pd.read_csv(ruta_archivo_csv, sep=";", skiprows=1, index_col=0, header=0)

    COL, IDX = np.meshgrid(df.columns.astype(float), df.index.astype(float))
    int_data = LinearNDInterpolator(list(zip(COL.flatten(), IDX.flatten())), df.to_numpy().flatten())
    Red_factor = int_data(h, n)
    print(Red_factor)
    return Red_factor

Red_factor = Reduction_factor(0.40, 1.10, "AIR", "C_W3")
