# Relative Permeability Models

Simple, readable Python implementations of the relative permeability models used in reservoir engineering and simulation. Each model is one plain function (NumPy only, no plotting code), so you can read the equations and follow them step by step.

<img width="1600" height="820" alt="image" src="https://github.com/user-attachments/assets/ebdadc69-5fed-49ba-8c8e-6d16a0ef7845" />

## Models

| File | Model | Phases | Returns |
|---|---|---|---|
| `burdine_brooks_corey.py` | Brooks-Corey with Burdine integration (exponents from the pore-size index λ) | two-phase | `krw, krnw` |
| `modified_brooks_corey.py` | Modified Brooks-Corey (Corey exponents set directly) | two-phase | `krw, krnw` |
| `stone_model_I.py` | Stone I (Aziz and Settari form) | three-phase | `krw, kro, krg` |
| `stone_model_II.py` | Stone II | three-phase | `krw, kro, krg` |

`krw` and `krg` always come from the two-phase curves. The Stone models only estimate the **three-phase oil relative permeability, `kro`**, from the oil-water and gas-oil curves.

## Quick start

```bash
pip install numpy
```

```python
import numpy as np
from stone_model_II import stone_model_II
from stone_model_I import stone_model_I

# three-phase: water and gas saturations (oil is So = 1 - Sw - Sg)
krw, kro, krg = stone_model_II(Sw=0.3, Sg=0.2)
print(krw, kro, krg)            # 0.048  0.1472  0.0160

# works on arrays too
Sw, Sg = np.meshgrid(np.linspace(0.1, 0.9, 50), np.linspace(0, 0.9, 50))
krw, kro, krg = stone_model_II(Sw, Sg)
```

```python
from burdine_brooks_corey import burdine_brooks_corey
from modified_brooks_corey import modified_brooks_corey

Sw = np.linspace(0.2, 0.9, 50)
krw, kro = burdine_brooks_corey(Sw, Swr=0.2, Snwr=0.1, krwo=0.3, krnwo=0.8, lambda_=2)
krw, kro = modified_brooks_corey(Sw, Swr=0.2, Snwr=0.1, krwo=0.3, krnwo=0.8, nw=2, nnw=2)
```

## Default parameters (three-phase models)

| Parameter | Meaning | Default |
|---|---|---|
| `Swr` | irreducible water saturation | 0.10 |
| `Sgr` | critical gas saturation | 0.05 |
| `Sor_ow` | residual oil saturation, oil-water system | 0.40 |
| `Sor_og` | residual oil saturation, gas-oil system | 0.20 |
| `kro_ow`, `kro_og` | oil end points | 0.8 |
| `krwo`, `krgo` | water and gas end points | 0.3 |
| `nw, now, ng, nog` | Corey exponents | 2 |

All of them can be changed through keyword arguments, for example `stone_model_II(Sw, Sg, Swr=0.15, Sor_ow=0.3)`.

## Equations

Step-by-step equations, a worked example, and a side-by-side comparison of the Stone I variants are in
[`Materials/stone_I_II_equations.pdf`](Materials/stone_I_II_equations.pdf).

Short version:

- Normalized saturations: `Swd = (Sw - Swr) / (1 - Swr - Sor_ow)`, `Sgd = (Sg - Sgr) / (1 - Swr - Sor_og - Sgr)`

Why each one differs:

Water (SwD): this comes from the oil-water two-phase curve, with no gas present. Water goes from S_wr up to the point where oil is stuck at S_orw. The gas residual doesn’t appear because gas isn’t part of that system.

Gas (SgD): this comes from the gas-oil curve, with connate water S_wr sitting in the pores. Gas starts flowing at S_gr and can fill everything except the water and the residual oil of the gas-oil system, S_org. The residual oil here is S_org, not S_orw, because the oil is being displaced by gas rather than water.

Oil (SoD): oil flows above S_orw, and at most it fills what is left after the water sits at S_wr and the gas at S_gr. That gives 1 − S_wr − S_gr as the top. It uses S_orw as the lower end, which is why oil’s formula has S_gr but water’s doesn’t.

- Two-phase curves: `krw = krwo·Swd^nw`, `krg = krgo·Sgd^ng`, `krow = kro_ow·(1 - Swd)^now`, `krog = kro_og·(1 - Sgd)^nog`
- **Stone II:** `kro = kro_ow · [ (krow/kro_ow + krw)(krog/kro_ow + krg) − (krw + krg) ]`, floored at 0
- **Stone I:** `kro = So* · krow · krog / ( kro_ow (1 − Sw*)(1 − Sg*) )`, with normalized saturations `Sw*, So*, Sg*` built from a minimum oil saturation `Som` that varies with `Sg`

## Notes

- The Stone I implementation follows the textbook form, including the `SoD` gate (`kro = 0` below `Sor_ow`). The PDF explains the alternative that gates on `Som` instead.
- Stone II gives `kro = 0` wherever the formula goes negative, and it can return nonzero `kro` below `Sor_ow`. Stone I does not, because of its gate.
- Saturations are fractions (0 to 1). Water below `Swr` is outside the model's range.

## Repository contents

```
├── burdine_brooks_corey.py
├── modified_brooks_corey.py
├── stone_model_I.py
├── stone_model_II.py
├── Materials/
│   └── stone_I_II_equations.pdf
└── README.md
```

## Author

Mahammad, MSc Petroleum Engineering. Reservoir engineering visualizations on LinkedIn.
