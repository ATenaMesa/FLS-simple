import pandas as pd
import os
import numpy as np

def Stress_0(h, ENV, S_N_Curve):
    if ENV == "AIR":
        archivo = "S_N_curve_air.csv"
    elif ENV == "SEAWATER":
        archivo = "S_N_curve_seawater.csv"
    else:
        print("Los valores de S_N_Curve y/o ENV no son válidos.")

    ruta_archivo_python = os.path.abspath(__file__)
    directorio_actual = os.path.dirname(ruta_archivo_python)
    ruta_archivo_csv = os.path.join(directorio_actual, archivo)
    df = pd.read_csv(ruta_archivo_csv, sep=";", skiprows=1, header=0, index_col=0)
    row = df.loc[S_N_Curve]
    Stress_0 = np.interp(h, row.index, row.values)
    print(Stress_0)
    return Stress_0

Stress_0 = Stress_0(1.10, "AIR", "F3")
