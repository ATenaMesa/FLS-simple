
def Stress(Stress_0, Red_factor, t_ref, t):
    Stress = Stress_0 * Red_factor * (t_ref/t) ** k  # Allowable Δσ [Mpa] for designed case
    print(Stress)
    return Stress

Stress = Stress(Stress_0, Red_factor, t_ref, t)