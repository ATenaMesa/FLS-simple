import pandas as pd
import os
from scipy.interpolate import LinearNDInterpolator
import numpy as np

def Damage_utilisation_factor(nombre_archivo, DFF, DL):
    ruta_archivo_python = os.path.abspath(__file__)
    directorio_actual = os.path.dirname(ruta_archivo_python)
    ruta_archivo_csv = os.path.join(directorio_actual, nombre_archivo)
    df = pd.read_csv(ruta_archivo_csv, sep=";", index_col=0, header=0)  # El argumento header=0 indica que la primera fila debe ser utilizada como indice del DataFrame
                                                                           # El argumento Header=None coge la primera fila como valores ya
                                                                           # El parámetro index_col=0 indica que la primera columna debe ser utilizada como índice del DataFrame.
#    Para valores enteros de tabla
#    row_num = df.index.get_loc(DFF)
#    col_num = df.columns.get_loc(str(DL))
#    n = df.iloc[row_num,col_num]
#    return n

    #   Para valores no enteros de tabla
    COL, IDX = np.meshgrid(df.columns.astype(float), df.index.astype(float))
    int_data = LinearNDInterpolator(list(zip(COL.flatten(), IDX.flatten())), df.to_numpy().flatten())
    n = int_data(DL, DFF)
    print(n)
    return n

n = Damage_utilisation_factor("Utilisation_factor.csv", 2, 25)

