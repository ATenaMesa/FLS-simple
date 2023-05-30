'''
----------- SIMPLIFIED FLS CHECK --------------

    Eurocode 3: Design of steel structures - Part 1-9: Fatigue, 2007 [15]
    DNVGL-RP-C203: Fatigue design of offshore steel structures. Section 5
    OFFSHORE STANDARD DET NORSKE VERITAS DNV-OS-C101. DESIGN OF OFFSHORE STEEL STRUCTURES, GENERAL (LRFD METHOD)
    
NOTAS:
    ENV = "AIR" or "SEAWATER"

    DFF = [1, 2, 3]   Design_Fatigue_Factor ([-]) DNV-OS-C101, Sec.6 – Page 45. Table A1
        # (DFF)   Structural element
        # 1       Internal structure, accessible and not welded directly to the submerged part.
        # 1       External structure, accessible for regular inspection and repair in dry and clean conditions.
        # 2       Internal structure, accessible and welded directly to the submerged part.
        # 2       External structure not accessible for inspection and repair in dry and clean conditions.
        # 3       Non-accessible areas, areas not planned to be accessible for inspection and repair during operation.
    
    DL = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50] Design life of structure (years)

    h = [0.50 to 1.20] # Weibull shape parameter (Classification Notes No. 30.7 page 18-19):
        # For semisubmersible                          h = 1.10
        # For deck longitudinals;                      h = h0
        # For ship side above water line;              h = ho + ha * ((D - z)/(D - T_act))
        # For ship side at the water line;             h = h0 + ha
        # For ship side below the water line;          h = ho + (h_a * z)/T_act - 0.005 * (T_act - z)
        # For bottom longitudinals;                    h = h0 - 0.005 * T_act
        # For longitudinal and transverse bulkheads;   h = h0 + ha
            # h0  = 2.21 - 0.54 log10(L);   L= deck length
            # ha = 0.05 in general
            # ha = 0.00 for plating subjected to forces related to roll motions for vessels with roll period TR > 14 sec
            # z = vertical distance from baseline/seabed to considered longitudinal (m)
            # T_act = draft
            # D = puntal
    
    S_N_Curve = "B1", "B2", "C", "C1", "C2", "D", "T", "E", "F", "F1", "F3", "G", "W1", "W2", "W3" # See APPENDIX A CLASSIFICATION OF STRUCTURAL DETAILS DNVGL-RP-C203

    S_N_Curve_red = "B1_B2" or "C_W3"

    t = 10  # Plate_thickness[mm] thickness through which a crack will most likely grow. t = tref is used for thickness less than t_ref
    
    t_ref = 16  # DNVGL-RP-C203 (Page 22)
        # Reference thickness equal 25 mm for welded connections other than tubular joints.
        # For tubular joints the reference thickness is 16 mm.
        # For bolts tref = 25 mm
    

    n = [DFF-DL] Damage utilization factor. See Table 5-8 DNVGL-RP-C203
    Red_factor = [n-h] Reduction factor. See tables 5-4, 5-5, 5-6 and 5-7 DNVGL-RP-C203
    Stress_0 = [S-N curve-h] Allowable base Δσ [Mpa]. See Table 5-2 or 5-3 for (20 years; 10^8 cicles and DFF=1) DNVGL-RP-C203
    k = [S-N curve] thickness exponent. See Table 2-1 DNVGL-RP-C203

'''

import pandas as pd
import os
from scipy.interpolate import LinearNDInterpolator
import numpy as np

class FLS:
    def __init__(self, ENV, DFF, DL, h, S_N_Curve_red, S_N_Curve, t, t_ref, file_n):
        self.ENV = ENV
        self.DFF = DFF
        self.DL = DL
        self.h = h
        self.S_N_Curve_red = S_N_Curve_red
        self.S_N_Curve = S_N_Curve
        self.t = t
        self.t_ref = t_ref
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.file_n = os.path.join(self.path, file_n)
        self.n = self.damage_utilisation_factor()
        self.reduction_factor = self.calc_reduction_factor(self.reduction_factor_filename())
        self.stress_0 = self.calc_stress_0(self.stress_o_filename())
        self.k_exp = self.calc_k_exponent()
        self.stress = self.calc_stress()

    def damage_utilisation_factor(self):
        df = pd.read_csv(self.file_n, sep=";", index_col=0, header=0)
        COL, IDX = np.meshgrid(df.columns.astype(float), df.index.astype(float))
        int_data = LinearNDInterpolator(list(zip(COL.flatten(), IDX.flatten())), df.to_numpy().flatten())
        n = int_data(self.DL, self.DFF)
        print("n =", n)
        return n

    def reduction_factor_filename(self):
        if self.ENV == "AIR" and self.S_N_Curve_red == "B1_B2":
            archivo = "Red_factor_air_B1_B2.csv"
        elif self.ENV == "AIR" and self.S_N_Curve_red == "C_W3":
            archivo = "Red_factor_air_C_W3.csv"
        elif self.ENV == "SEAWATER" and self.S_N_Curve_red == "B1_B2":
            archivo = "Red_factor_seawater_B1_B2.csv"
        elif self.ENV == "SEAWATER" and self.S_N_Curve_red == "C_W3":
            archivo = "Red_factor_seawater_C_W3.csv"
        else:
            raise ValueError("Los valores de S_N_Curve_red y/o ENV no son válidos.")
        print("Reduction_factor_filename =", archivo)
        return archivo

    def calc_reduction_factor(self, archivo):
        df = pd.read_csv(os.path.join(self.path, archivo), sep=";", skiprows=1, index_col=0, header=0)
        COL, IDX = np.meshgrid(df.columns.astype(float), df.index.astype(float))
        int_data = LinearNDInterpolator(list(zip(COL.flatten(), IDX.flatten())), df.to_numpy().flatten())
        red_factor = int_data(self.h, self.n)
        print("Red_factor =", red_factor)
        return red_factor

    def stress_o_filename(self):
        if self.ENV == "AIR":
            archivo = "S_N_curve_air.csv"
        elif self.ENV == "SEAWATER":
            archivo = "S_N_curve_seawater.csv"
        else:
            raise ValueError("ENV no son válidos.")
        print("Stress_o_filename =", archivo)
        return archivo

    def calc_stress_0(self, archivo):
        df = pd.read_csv(os.path.join(self.path, archivo), sep=";", skiprows=1, header=0, index_col=0)
        row = df.loc[self.S_N_Curve]
        stress_0 = np.interp(self.h, row.index, row.values)
        print("Stress_0 =", stress_0)
        return stress_0

    def calc_k_exponent(self):
        k_a = pd.DataFrame(
            {'S_N_curve': ['B1', 'B2', 'C', 'C1', 'C2', 'D', 'E', 'F', 'F1', 'F3', 'G', 'W1', 'W2', 'W3'],
             'k': [0, 0, 0.05, 0.10, 0.15, 0.2, 0.2, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]})
        k_w = pd.DataFrame(
            {'S_N_curve': ['B1', 'B2', 'C', 'C1', 'C2', 'D', 'E', 'F', 'F1', 'F3', 'G', 'W1', 'W2', 'W3'],
             'k': [0, 0, 0.05, 0.10, 0.15, 0.2, 0.2, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]})
        if self.ENV == "AIR":
            k = k_a
        elif self.ENV == "SEAWATER":
            k = k_w
        else:
            raise ValueError("Los valores de S_N_Curve")
        k_exp = k.loc[k['S_N_curve'] == self.S_N_Curve, 'k'].values[0]
        print("K_exp =", k_exp)
        return k_exp

    def calc_stress(self):
        stress = self.stress_0 * self.reduction_factor * (self.t_ref/self.t) ** self.k_exp
        print("Stress =", stress)
        return stress

Umaine = FLS("AIR", 2, 25, 1.00, "C_W3", "F3", 10, 16, "Utilisation_factor.csv")
print(Umaine.calc_stress())

