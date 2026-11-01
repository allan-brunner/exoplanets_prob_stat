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
    return BLUE, GREY, df


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
    df_full = _default_df.copy()
    others_aligned = _others_df.reindex(df_full.index)
    values_default = df_full[NUM_COLS]
    values_filled = values_default.fillna(others_aligned)
    df_full[NUM_COLS] = values_filled
    df_full = df_full.reset_index()

    coverage_cols = df_full[NUM_COLS].notna().mean()
    return (
        PLANET_COLS,
        STAR_COLS,
        coverage_cols,
        coverage_default_cols,
        df_full,
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
def _(df_full):
    df_full["pl_bmassprov"].value_counts()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2 Missing values are not random

    The data will be MNAR (Missing not a random number). It is worth mesuring on the stellar columns because they are the input of the model.
    """)
    return


@app.cell
def _(STAR_COLS, df_full, plt, sns):
    _counts = df_full["discoverymethod"].value_counts()
    _methods = _counts[_counts >= 50].index.tolist()

    _miss = (
        df_full[df_full["discoverymethod"].isin(_methods)]
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
def _(BLUE, GREY, df_full, np, pd):
    # Giant planet: radius > 6 Earth radii and mass > 50 Earth masses.
    df_full["is_gas_giant"] = np.where(
        df_full["pl_rade"].notna(), df_full["pl_rade"] > 6,
        np.where(df_full["pl_bmasse"].notna(), df_full["pl_bmasse"] > 50, np.nan),
    )

    _cols = ["st_met", "st_age", "st_dens", "st_lum"]

    _d = df_full.dropna(subset=["is_gas_giant"])
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


if __name__ == "__main__":
    app.run()
