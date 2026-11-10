import numpy as np


def modified_brooks_corey(Sw, Swr=0.1, Snwr=0.2, krwo=0.3, krnwo=0.8, nw=2, nnw=2):
    """Modified Brooks-Corey: returns krw, krnw."""
    Swd = np.clip((Sw - Swr) / (1 - Swr - Snwr), 0, 1)   # normalized water saturation

    krw = krwo * Swd**nw
    krnw = krnwo * (1 - Swd)**nnw
    return krw, krnw


if __name__ == "__main__":
    Sw = np.linspace(0.1, 0.8, 8)
    print(modified_brooks_corey(Sw))
