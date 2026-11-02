import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import seaborn as sns
    import numpy as np
    import matplotlib.pyplot as plt

    return mo, np, pd, plt, sns


@app.cell
def _(pd):
    # Load dataset
    df = pd.read_csv("exoplanetes_data.csv", skiprows=292, low_memory=False)
    BLUE, ORANGE, AQUA, YELLOW, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#8a8a85"
    return BLUE, GREY, ORANGE, df


@app.cell
def _(mo):
    mo.md(r"""
    # Host stars to the their planets analysis

    The goal is now fixed, we need to guess the parameters of exoplantes based of it's host star. In order to make this we need to answear at two major questions :
    - **Wich columns are worth keeping ?** : Some are valuable, some are not, some are computed based on other...
    - **Fill the hole :** Most stellar columns are incomplete.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1 Column coverage

    Most of the column are uncertainties (err1, err2), limit flags or copies of eachothers. After removing them we only have 30 numerical ones remaining.

    The introduction script written by Allan only kept the rows with `default_flag = 1`, which are the single, internally consistent set of parameters, taken from one publication, that the archive chose as the reference solution for each planet.

    **It is not necessarily the most complete or the most precise for every value.**
    """)
    return


@app.cell
def _(df):
    # Define columns
    STAR_COLS = ["st_teff", "st_rad", "st_mass", "st_met", "st_logg", "st_age", "st_dens", "st_lum", "st_vsin", "st_rotp"]
    SYSTEM_COLS = ["sy_dist", "sy_vmag", "sy_kmag", "sy_gaiamag", "sy_snum", "sy_pnum"]
    PLANET_COLS = ["pl_rade", "pl_bmasse", "pl_orbper", "pl_orbsmax", "pl_orbeccen", "pl_eqt", "pl_insol", "pl_dens"]
    NUM_COLS = STAR_COLS + SYSTEM_COLS + PLANET_COLS
    print(f"{df.shape[1]} columns in total. {len(STAR_COLS)} are stars, {len(PLANET_COLS)} are planets, {len(SYSTEM_COLS)} are system ones") 

    _default_df = df[df["default_flag"] == 1].set_index("pl_name")
    _others_df = df[df["default_flag"] == 0].groupby("pl_name")[NUM_COLS].median()

    # DEF coverage

    coverage_default_cols = _default_df[NUM_COLS].notna().mean()

    # DEF + filling coverage
    df_filled = _default_df.copy()
    others_aligned = _others_df.reindex(df_filled.index)
    values_default = df_filled[NUM_COLS]
    values_filled = values_default.fillna(others_aligned)
    df_filled[NUM_COLS] = values_filled
    df_filled = df_filled.reset_index()

    coverage_cols = df_filled[NUM_COLS].notna().mean()
    return (
        PLANET_COLS,
        STAR_COLS,
        coverage_cols,
        coverage_default_cols,
        df_filled,
    )


@app.cell
def _(
    BLUE,
    GREY,
    PLANET_COLS,
    STAR_COLS,
    coverage_cols,
    coverage_default_cols,
    plt,
):
    _cols = STAR_COLS + PLANET_COLS
    _before_prct = coverage_default_cols[_cols] * 100
    _gain_prct = (coverage_cols[_cols] - coverage_default_cols[_cols]) * 100


    _fig, _ax = plt.subplots()
    _ax.barh(_cols, _before_prct, color=GREY, label="Default row (default_flag = 1)")
    _ax.barh(_cols, _gain_prct, left=_before_prct, color=BLUE, label="Gained from the median of other publications (default flag = 0)")

    for _i, _c in enumerate(_cols):
        _ax.text(coverage_cols[_c] * 100 + 1, _i, f"{coverage_cols[_c]:.0%}", va="center", fontsize=9)

    _ax.invert_yaxis()
    _ax.set_xlabel("Planets with a value (%)")
    _ax.spines[["top", "right"]].set_visible(False)

    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Filling the gaps with non-default rows increases the coverage of the stellar columns :
    - Metallicity 69% -> 87%
    - Stellar mass 86% -> 97%
    - Age 48% -> 73%

    For the planets columns, the other publications barely give us new informations, the radii from 74% to 75%, the mass 50% to 53%. But this is not a problem, because those informations is meant to be predicted by our future model.

    Mixing publications can adds a little noise, since each one may use a different stellar model. Keeping the median and the default row first can limit this problem.

    Another issue, `pl_bmasse` mixes true masses and min masses. `pl_bmassprov` tells them apart.
    """)
    return


@app.cell
def _(df_filled):
    df_filled["pl_bmassprov"].value_counts()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2 Missing values are not random

    The data will be MNAR (Missing not a random number). It is worth mesuring on the stellar columns because they are the input of the model.
    """)
    return


@app.cell
def _(STAR_COLS, df_filled, plt, sns):
    _counts = df_filled["discoverymethod"].value_counts()
    _methods = _counts[_counts >= 50].index.tolist()

    _miss = (
        df_filled[df_filled["discoverymethod"].isin(_methods)]
        .groupby("discoverymethod")[STAR_COLS]
        .apply(lambda g: g.isna().mean() * 100)
        .loc[_methods]
    )

    _fig, _ax = plt.subplots(figsize=(9, 3.5))
    sns.heatmap(_miss, annot=True, fmt=".0f", cmap="Reds", vmin=0, vmax=100,
                linewidths=2, linecolor="white", ax=_ax)

    _ax.set_title("Missing stellar values (%) per discovery method")
    _ax.set_xlabel("")
    _ax.set_ylabel("")

    _fig.tight_layout()
    _fig
    return


@app.cell
def _(BLUE, GREY, df_filled, np, pd):
    # Giant planet: radius > 6 Earth radii and mass > 50 Earth masses.
    df_filled["is_gas_giant"] = np.where(
        df_filled["pl_rade"].notna(), df_filled["pl_rade"] > 6,
        np.where(df_filled["pl_bmasse"].notna(), df_filled["pl_bmasse"] > 50, np.nan),
    )

    _cols = ["st_met", "st_age", "st_dens", "st_lum"]

    _d = df_filled.dropna(subset=["is_gas_giant"])
    _share = pd.DataFrame({
        "Value present": {c: _d.loc[_d[c].notna(), "is_gas_giant"].mean() * 100 for c in _cols},
        "Value missing": {c: _d.loc[_d[c].isna(), "is_gas_giant"].mean() * 100 for c in _cols},
    })

    _ax = _share.plot.bar(color=[BLUE, GREY], figsize=(7, 3.5), rot=0, width=0.75)
    _ax.set_ylabel("Giant gas planets (%)")
    _ax.spines[["top", "right"]].set_visible(False)

    _ax.legend(frameon=False)
    _ax.set_title("Share of gas giant planets depending on whether a stellar value is missing")
    _ax.figure
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Microlensing planets has almost no information about their star. The star is too far away to be studied directly: we are only able to notice it while it bends the light of a star behind it. This information gives us its mass. This method also mostly finds gas giants, because a heavy planet bends light more than a small one.

    So in this dataset, a missing stellar value is already a hint that the planet is a gas giant. When the metallicity is missing, 52% of the planets are gas giants. When it is known, only 31% are.

    We need to keep this in mind for the model !
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Step 3 False lead

    A naive approach is to look at which planet column correlates the most with the star. Spearman correlation is used instead of Pearson since nearly every variable spans several orders of magnitude.

    [Correlation de spearman](https://fr.wikipedia.org/wiki/Corr%C3%A9lation_de_Spearman)
    """)
    return


@app.cell
def _(PLANET_COLS, STAR_COLS, df_filled, plt, sns):
    _corr = df_filled[STAR_COLS + PLANET_COLS].corr(method="spearman").loc[STAR_COLS, PLANET_COLS]

    _fig, _ax = plt.subplots()
    sns.heatmap(_corr, annot=True, fmt=".2f", cmap=sns.diverging_palette(250, 25, as_cmap=True),
                vmin=-0.6, vmax=0.6, cbar_kws={"label": "Spearman ρ"}, ax=_ax)

    _ax.set_title("Planet columns (rows) vs star columns (columns)")

    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The equilibrium temperature `pl_eqt` and the insolation `pl_insol` are the planet columns that correlate the most with the star.

    The temperature is compute with the following formula :

    $$T_{eq} = T_{eff}\,\sqrt{\frac{R_\star}{2a}}\,(1-A)^{1/4}$$

    As we can see it is built from the star temperature, the star radius and the semi-major axis.

    The same applies to `pl_orbsmax`, which is usually derived from Kepler's third law $a^3 = M_\star P^2$. If this is true, the archive values must fall exactly on the recomputed ones.
    """)
    return


@app.cell
def _(BLUE, df_filled, np, plt):
    _fig, _axes = plt.subplots(1, 2, figsize=(11, 4.5))


    # RECOMPUTATION FROM THE STAR
    SUN_RADIUS_AU = 0.00465047

    _m = df_filled.dropna(subset=["pl_eqt", "st_teff", "st_rad", "pl_orbsmax"])
    _teq = _m["st_teff"] * np.sqrt(_m["st_rad"] * SUN_RADIUS_AU / (2 * _m["pl_orbsmax"]))
    _axes[0].scatter(_teq, _m["pl_eqt"], s=6, alpha=0.3, color=BLUE)
    _axes[0].plot([0, 4500], [0, 4500], color="black", lw=1, ls="--")
    _axes[0].set_xlabel("$T_{eq}$ recomputed from the star (K)")
    _axes[0].set_ylabel("pl_eqt in the archive (K)")
    _axes[0].set_title(f"Equilibrium temperature (N = {len(_m)})")


    # RECOMPUTATION OF KEPLER 3rd law
    DAYS_PER_YEAR = 365.25

    _m = df_filled.dropna(subset=["pl_orbsmax", "st_mass", "pl_orbper"])
    _a = (_m["st_mass"] * (_m["pl_orbper"] / DAYS_PER_YEAR) ** 2) ** (1 / 3)
    _axes[1].scatter(_a, _m["pl_orbsmax"], s=6, alpha=0.9, color=BLUE)
    _axes[1].plot([1e-3, 1e4], [1e-3, 1e4], color="black", lw=1, ls="--")
    _axes[1].set_xscale("log")
    _axes[1].set_yscale("log")

    _axes[1].set_xlabel("$a$ from Kepler's 3rd law (AU)")
    _axes[1].set_ylabel("pl_orbsmax in the archive (AU)")
    _axes[1].set_title(f"Semi-major axis (N = {len(_m)})")

    for _ax in _axes:
        _ax.spines[["top", "right"]].set_visible(False)
    _fig.tight_layout()
    _fig

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Conclusions:
    - `pl_eqt` and `pl_insol` are not targets (not independent information about the planet) and not features.
    - `pl_orbsmax` is equivalent to the orbital period once the stellar mass is known. Predicting both is redundant: predict the period, then compute $a$.
    - When those values are undefined, we can precisly found these informations by recomputing them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Step 4 Redundant stellar columns due to physic
    """)
    return


@app.cell(hide_code=True)
def _(STAR_COLS, df_filled, plt, sns):
    _corr = df_filled[STAR_COLS].corr(method="spearman")

    _fig, _ax = plt.subplots()
    sns.heatmap(_corr, annot=True, fmt=".2f", cmap=sns.diverging_palette(250, 25, as_cmap=True),
                vmin=-1, vmax=1, cbar_kws={"label": "Spearman ρ"}, ax=_ax)
    _ax.set_title("Correlation between the stellar columns")

    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The first six columns form one block : temperature, radius, mass, luminosity, gravity and density are linked by physics. This is why the correlation between each of them is strong !

    - $\log g = \log g_\odot + \log M_\star - 2 \log R_\star$ : [Surface gravity](https://en.wikipedia.org/wiki/Surface_gravity)
    - $L_\star = R_\star^2 \, (T_{eff} / T_\odot)^4$ : [Stefan–Boltzmann law](https://en.wikipedia.org/wiki/Stefan%E2%80%93Boltzmann_law)
    - $\rho_\star = \rho_\odot \, M_\star / R_\star^3$ : [Sun](https://en.wikipedia.org/wiki/Sun)

    We also see that the metallicity and the age are nearly independent from this block, so they bring new information.

    Conclusion :
    - A minimal feature set for our model is temperature, mass, radius, metallicity.
    - Gravity, Luminosity, Temperature by  the three formulas above can fill the holes of one column from the two others.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # STEP 5 Model features

    ## - 5.a Metalicity

    Stars with more heavy elements = higher metallicity, host gas giants more often. As we can see in our data, among transit planets, 11% are gas giants with metal-poor stars, against 56% around the most metal-rich ones. The same trend appears despite the method, so it does not come from the detection method.

    This isn't a surprise: astronomers already know that "stars with a higher metallicity are more likely to have planets, especially giant planets" ([Wikipedia: Planet-hosting star](https://en.wikipedia.org/wiki/Planet-hosting_star)). The core accretion model we described earlier explains why. A metal-rich star is born in a disk full of dust and rock, so a planet can build its 10 Earth-mass core faster and still have time to grab gas before the disk is gone.

    We can conclude that `st_met` is one of the most useful columns for the model !
    """)
    return


@app.cell
def _(BLUE, ORANGE, df_filled, pd, plt):
    _bins = [-1, -0.15, 0, 0.15, 0.3, 0.6]
    _labels = ["< -0.15", "-0.15 to 0", "0 to 0.15", "0.15 to 0.3", "> 0.3"]

    _fig, _ax = plt.subplots(figsize=(8, 4.5))
    for _meth, _col in [("Transit", BLUE), ("Radial Velocity", ORANGE)]:
        _m = df_filled[df_filled["discoverymethod"] == _meth].dropna(subset=["st_met", "is_gas_giant"])
        _g = _m.groupby(pd.cut(_m["st_met"], _bins, labels=_labels), observed=True)["is_gas_giant"].agg(["mean", "size"])

        _ax.plot(range(len(_g)), _g["mean"] * 100, color=_col, marker="o", lw=2, label=_meth)
        _ax.text(len(_g) - 0.9, _g["mean"].iloc[-1] * 100, _meth, color="black", va="center")

    _ax.set_ylim(0, 100)
    _ax.set_xlim(-0.3, len(_labels) + 0.4)

    _ax.set_xticks(range(len(_labels)), _labels)
    _ax.set_xlabel("Stellar metallicity [Fe/H] (dex)")
    _ax.set_ylabel("Giant planets (%)")

    _ax.spines[["top", "right"]].set_visible(False)
    _ax.legend(frameon=False, loc="upper left")
    _ax.set_title("Share of giants vs host star metallicity")

    _fig.tight_layout()
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## - 5.b Stellar radius

    The more the radius of the star is bigger the more the planets arounds it are far far far away [Exoplanet orbital and physical parameters](https://en.wikipedia.org/wiki/Exoplanet_orbital_and_physical_parameters)

    [Stellar Classification](https://en.wikipedia.org/wiki/Stellar_classification)
    """)
    return


@app.cell
def _(BLUE, ORANGE, df_filled, np, pd, plt):
    _bins = [0, 0.7, 0.96, 1.15, 1.4, 1.8, 6.6, np.inf]
    _labels = [
        "≤ 0.7 (Classe M - Naines rouges)",
        "0.7 to 0.96 (Classe K - Naines oranges)",
        "0.96 to 1.15 (Classe G - Type Solaire)",
        "1.15 to 1.4 (Classe F - Jaune-Blanc)",
        "1.4 to 1.8 (Classe A - Étoiles Blanches)",
        "1.8 to 6.6 (Classe B - Étoiles Bleues)",
        "> 6.6 (Classe O ou Étoiles Géantes évoluées)"
    ]

    _fig, _ax = plt.subplots(figsize=(12, 6))
    for _meth, _col in [("Transit", BLUE), ("Radial Velocity", ORANGE)]:
        _m = df_filled[df_filled["discoverymethod"] == _meth].dropna(subset=["st_rad", "pl_orbper"])
        _g = _m.groupby(pd.cut(_m["st_rad"], _bins, labels=_labels), observed=False)["pl_orbper"].mean()
        _ax.plot(range(len(_g)), _g.values, color=_col, marker="o", lw=2, label=_meth)
    
        _last_val = _g.iloc[-1] if not np.isnan(_g.iloc[-1]) else _g.dropna().iloc[-1]
        _ax.text(len(_g) - 0.9, _last_val, _meth, color="black", va="center")

    _ax.set_xlim(-0.3, len(_labels) - 0.7)

    _ax.set_xticks(range(len(_labels)))
    _ax.set_xticklabels(_labels, rotation=30, ha="right")

    _ax.set_xlabel("Stellar radii")
    _ax.set_ylabel("Mean Orbital Period (days)")

    _ax.spines[["top", "right"]].set_visible(False)
    _ax.legend(frameon=False, loc="upper left")
    _ax.set_title("Average Planetary Orbital Period by Stellar Type")

    _fig.tight_layout()
    _fig

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can conclude two things by seeing this graph.

    The `discovery_method` can also be a feature of our model. Because here we can clearly see that the transit ones are really close to their star. Wich his indeed expected due to Transit probability equation :

    $$P_{\text{transit}} \approx \frac{R_* + R_p}{a} \approx \frac{R_*}{a}$$

    * $R_*$ est le rayon de l'étoile (`st_rad`)
    * $R_p$ est le rayon de la planète (`pl_rade`)
    * $a$ est le demi-grand axe / la distance à l'étoile (`orbsmax`)

    The problem is `pl_orbsmax` increases much faster than star size, and that it is in the denominator. So the transit method can only detect planets that are extremely close to a star.

    -----

    The other problem is the fall observed for the radial velocity method, as a reminder this method use the doppler effect :

    - One side of the star moves toward us (blueshift), and the other side moves away (redshift).
    The spectrograph gets light from both sides at the same time, so the thin spectral lines become wide and blurry.
    With blurry lines, we can’t measure the tiny shift caused by a planet.

    -  When a star gets bigger, its surface gravity gets weaker, and its outer layers become thin gas. Hot bubbles of gas rise (blueshift) and cool bubbles sink (redshift).
    This movement creates speed changes of about 50 to 100 m/s in the star itself.
    Astronomers call this stellar jitter. It can hide the much smaller signal of a planet.


    [Method of discovering exoplanets](https://en.wikipedia.org/wiki/Methods_of_detecting_exoplanets)

    [Stellar rotation](https://en.wikipedia.org/wiki/Stellar_rotation)

    [Solar granule](https://en.wikipedia.org/wiki/Solar_granule)
    """)
    return


if __name__ == "__main__":
    app.run()
