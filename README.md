# Albert & Einstein — Effective Nuclear Charge (Zeff) Calculator

An interactive, high-precision educational web application for calculating Effective Nuclear Charge ($Z_{\text{eff}}$) and shielding constants ($\sigma$) across all 118 elements of the periodic table using Slater's Rules.

---

## ✨ Features

- **Interactive Periodic Table**: Explore all 118 elements with color-coded elemental categories (alkali metals, halogens, noble gases, lanthanides, actinides, etc.).
- **Slater's Rules Engine**:
  - Full support for $s, p$ subshells with canonical Slater groups ($[1s]$, $[2s, 2p]$, $[3s, 3p]$, $[3d]$, $[4s, 4p]$, etc.).
  - Proper handling of $d$ and $f$ electrons (shielded only by groups to their left at 1.00 each, and same group at 0.35 each).
  - Explicit step-by-step breakdown showing exact formula, per-electron shielding contributions, and net $Z_{\text{eff}} = Z - \sigma$.
- **Experimental Aufbau Exceptions**: Accurate electron configurations for anomalous elements (Cr, Cu, Nb, Mo, Ru, Rh, Pd, Ag, Pt, Au, La, Ce, Gd, Ac, Th, Pa, U, Np, Cm, Lr).
- **Interactive UI**:
  - Orbitals visualizer with dynamic electron filling.
  - History tracking & favorites.
  - Dark mode support with sleek modern aesthetics.

---

## 🚀 Deployment

Configured for one-click deployment on [Vercel](https://vercel.com).
Simply connect this repository to Vercel and it will automatically deploy.
