import numpy as np


def stone_model_I(Sw, Sg, Swr=0.1, Sgr=0.05, Sor_ow=0.4, Sor_og=0.2,
                  kro_ow=0.8, kro_og=0.8, krwo=0.3, krgo=0.3,
                  nw=2, now=2, ng=2, nog=2):
    """Stone I: returns krw, kro, krg. Sw and Sg are arrays with Sw >= Swr and Sw + Sg <= 1."""
    So = 1 - Sw - Sg

    # two-phase curves
    Swd = np.clip((Sw - Swr) / (1 - Swr - Sor_ow), 0, 1)
    Sgd = np.clip((Sg - Sgr) / (1 - Swr - Sor_og - Sgr), 0, 1)

    krw = krwo * Swd**nw
    krg = krgo * Sgd**ng
    krow = kro_ow * (1 - Swd)**now
    krog = kro_og * (1 - Sgd)**nog

    # normalized oil saturation (not clipped): used as the on/off gate
    Sod = (So - Sor_ow) / (1 - Swr - Sor_ow - Sgr)

    # minimum oil saturation
    a = np.clip(Sg / (1 - Swr - Sor_og), 0, 1)
    Som = (1 - a) * Sor_ow + a * Sor_og

    # three-phase normalized saturations
    Sw_star = (Sw - Swr) / (1 - Swr - Som)
    So_star = (So - Som) / (1 - Swr - Som)
    Sg_star = Sg / (1 - Swr - Som)

    # Stone I (denominator set to 1 where So* <= 0 to avoid dividing by zero)
    denominator = np.where(So_star > 0, (1 - Sw_star) * (1 - Sg_star), 1)
    stone = np.where(So_star > 0, So_star * krow * krog / (kro_ow * denominator), 0)

    # gate: Sod < 0 -> 0, Sod > 1 -> kro_ow, otherwise Stone I
    kro = np.where(Sod < 0, 0, np.where(Sod > 1, kro_ow, stone))
    return krw, kro, krg


if __name__ == "__main__":
    print(stone_model_I(np.array([0.3]), np.array([0.2])))   # kro about 0.1170
