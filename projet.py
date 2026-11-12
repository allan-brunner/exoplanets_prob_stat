import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt

    return mo, pd, plt, sns


@app.cell
def _(pd):
    df = pd.read_csv("csv_data/exoplanetes_data.csv", comment="#").query("default_flag == 1")
    df
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Qu'est-ce que tout ça veut dire ?
    Beaucoup de colonnes que je pige pas je me concentre sur les valeurs numériques pour commencer mes recherches
    mais ça fait baucoup trop de colonnes donc il faut commencer à se renseigner pour avancer.

    d'abord les flags: Une planète peut apparaitre plusieurs fois dans le fichier avec des flags différents. pour celui de base c'est "default". je filtre mais ça change pas le nombre de colonnes

    pour se renseigner:
    https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html || OU ||
    https://exoplanetarchive.ipac.caltech.edu/docs/pscp_about.html

    dans un des deux, ils parlent des paramètres des planètes, je vais utiliser ça pour comparer la heatmap (les colonnes numériques) en sachant que j'ai pu en rater une ou deux
    """)
    return


@app.cell
def _(df, plt, sns):
    cols = [
    # planete
        #periode
        "pl_orbper",
        #distance avec l'étoile
        "pl_orbsmax",
        #rayon
        "pl_rade",
        #masse
        "pl_bmasse",
        #densité
        "pl_dens",
        # ? à voir
        "pl_orbeccen",
        # ? à voir
        "pl_insol",
        # temp équilibre, comme en physique wouhou (entre planète et étoile ???)
        "pl_eqt",
    # etoile
        #temperature
        "st_teff",
        #rayon
        "st_rad",
        #masse
        "st_mass",
        #matallicité (expliqué plus ou moins mais je capte tjr pas ce que c'est)
        "st_met",
        #gravité à la surface si j'ai bien compris
        "st_logg",
    ]

    corr = df[cols].corr()
    sns.heatmap(corr, cmap="coolwarm", vmin=-1, vmax=1)
    plt.show()

    return (cols,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ça ressemble déjé plus à qqchose mais il y a encore besoin de faire des rechrches là dessus.
    méthode describe permet d'avoir une ue d'ensemble sur toute les colonnes listés ci-dessus
    """)
    return


@app.cell
def _(cols, df):
    print(df[cols].describe().T) #imprime les calculs
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    trouver aussi où il manque le plus de données peut être sympa
    """)
    return


@app.cell
def _(cols, df, plt, sns):
    trous = df[cols].notna().groupby(df["discoverymethod"]).mean() * 100 #regarde pourcentage des valeurs présentes
    sns.heatmap(trous, annot=True, fmt=".0f", cmap="Reds", vmin=0, vmax=100)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    maintenant il faut encore se rensigner sur chacune des méthodes de découverte, demain :)
    """)
    return


if __name__ == "__main__":
    app.run()
