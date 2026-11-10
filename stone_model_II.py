import numpy as np


def stone_model_II(Sw, Sg, Swr=0.1, Sgr=0.05, Sor_ow=0.4, Sor_og=0.2,
                   kro_ow=0.8, kro_og=0.8, krwo=0.3, krgo=0.3,
                   nw=2, now=2, ng=2, nog=2):
    """Stone II: returns krw, kro, krg. Sw and Sg are arrays."""
    # two-phase curves
    Swd = np.clip((Sw - Swr) / (1 - Swr - Sor_ow), 0, 1)
    Sgd = np.clip((Sg - Sgr) / (1 - Swr - Sor_og - Sgr), 0, 1)

    krw = krwo * Swd**nw
    krg = krgo * Sgd**ng
    krow = kro_ow * (1 - Swd)**now
    krog = kro_og * (1 - Sgd)**nog

    # Stone II
    kro = kro_ow * ((krow / kro_ow + krw) * (krog / kro_ow + krg) - (krw + krg))
    kro = np.maximum(kro, 0)          # negative values are set to 0
    return krw, kro, krg


if __name__ == "__main__":
    print(stone_model_II(np.array([0.3]), np.array([0.2])))  # kro about 0.1472
