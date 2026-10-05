import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _(mo):
    mo.md(r"""
    ## Introduction

    Before working on the project, it is important to know what's an exoplanet. Exoplanets, as defined by the [Nasa](https://science.nasa.gov/exoplanets/), define planets beyond our solar system. As of today, 6372 exoplanets are proved and recently launched mission, the Nancy Grace Roman telescope is predicted to discover more than 100'000 more. The very first exoplanet was validated in 1992.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Setup
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import seaborn as sns
    import numpy as np
    import matplotlib.pyplot as plt

    return mo, pd, plt, sns


@app.cell
def _(pd):
    # Load dataset
    df = pd.read_csv("./project/exoplanetes_data.csv", skiprows=292, low_memory=False)
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The dataset contains around 40 thousands rows. As its sources says, rows can refer to a same exoplanets and have different parameters. Each row comes with a default flag (`default_flag`) at 1 when the row is the most common accepted one. Therefore, the most common accepted doesn't implies that all values are defined. As it will be discussed later, not all detection methods can determine every parameters of an exoplanet. For example, we can discover an exoplanet, get its radius with the transit method, but we need to use the radial velocity method to find the mass of the planet. This means that not all graphs will display data of all exoplanets, that some graphs can have selection bias due to MNAR (Missing Not At Random) data.
    """)
    return


@app.cell
def _(df):
    # Unique rows
    print(f"Unique rows: {df['pl_name'].nunique()}")
    # 6366 unique planets - For the (at that time) 6366 validated exoplanets

    # Filter for default flag at 1: The most validated data
    df_default = df[df['default_flag'] == 1]
    print(f"Nb with default flag at 1: {len(df_default)}")
    return (df_default,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the introduction, it was said that 6372 were found but this dataset doesn't contain the last 6 recently validated.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The dataset isn't completely normalized everywhere. For example the discoverly locale (`disc_locale` field) has most of the times `Ground` but can also have `ground`. Corrects those errors by normliazing them so they can be used efficiently.
    """)
    return


@app.cell
def _(df_default):
    # Clean dataset
    # Correct locales
    df_default['disc_locale'] = df_default['disc_locale'].str.strip().str.capitalize()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exoplanets discoveries

    Discovering exoplanets is known to be an hard subject. The task require to find an object that reflects mostly nothing in a vast, absolute black world. This means we can't discover some with the naked eye so machines must help us. With this in mind, some technological advancements, new machines, missions, and methods can create spikes of amount of exoplanets discovered in a year.
    """)
    return


@app.cell
def _(df_default, plt, sns):
    # Discoverise / Year
    ax_dy = sns.histplot(data=df_default, x="disc_year", bins=30)
    ax_dy.set_xlabel("Discovery Year")
    ax_dy.set_ylabel("Number of Discoveries")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It can be seen that exoplanets discoveries tends to be more and more common as the year passes and the technology becomes more efficient. We can also see two great spikes in 2014 and 2016.

    From the [wikipedia article](https://en.wikipedia.org/wiki/Discoveries_of_exoplanets#2014), with the help of Kepler telescope a bit more than 700 exoplanets were discovered.

    And in 2016, the spike is explained by Nasa validating in a single batch, over 1 thousand exoplanets from 2015 Catalogue mostly populated by Kepler as explained by [Watchers news](https://watchers.news/2016/05/10/kepler-mission-announces-largest-collection-of-planets-ever-discovered/).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, determining the facilities with the most exoplanets founds can help directing the searches, with the huge amount of facilities that help finding even 1 exoplanets, it becomes understandable to only limit search for the 10 best ones.
    """)
    return


@app.cell
def _(df_default, plt, sns):
    # Discoveries / Facilities
    top_10_facilities = df_default['disc_facility'].value_counts().nlargest(10).index
    df_top_fac = df_default[df_default['disc_facility'].isin(top_10_facilities)]
    ax_df = sns.countplot(data=df_top_fac, y="disc_facility", order=top_10_facilities)
    ax_df.set_xlabel("Number of Discoveries")
    ax_df.set_ylabel("Discovery Facility")
    plt.title("Top 10 Discovery Facilities")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To reflect the saying about the discovery years, we can see, in the Top 10 facilities, Kepler (with K2) leading the way with over 3'000 discoveries and more than the double of the second facilities (TESS) with the most discoveries throughout the years.

    By making some research on those facilities, we can learn first that K2 is an extension mission to the Kepler telescope (Source: [Nasa's Kepler mission official website](https://science.nasa.gov/mission/kepler/)). And we can see that it uses the Transit method for finding new exoplanets, the same one as the TESS (Sources: [MIT's Tess satellite](https://tess.mit.edu/))
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    After learning the methods of the two main programs, it becomes interesting to see the other methods and their efficience.
    """)
    return


@app.cell
def _(df_default, plt, sns):
    # Discoveries / Methods
    top_methods = df_default['discoverymethod'].value_counts().index
    ax_dm = sns.countplot(data=df_default, y="discoverymethod", order=top_methods)
    ax_dm.set_xlabel("Number of Discoveries")
    ax_dm.set_ylabel("Discovery Method")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    There exists multiple methods for finding exoplanets but we can see that mainly 2, Radial Velocity and Transit methods, are efficient with the current technology state.

    We can prove that the 3 main facilities seen before are indeed using Transit method since it's also the main one, having nearly 4 times the discoveries of Radial Velocity.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Another meaningful parameter is the locale from where the discoveries were made. We know the Kepler, K2, and TESS programs discovered exoplanets from space, but what about the discoveries from the ground.
    """)
    return


@app.cell
def _(df_default, plt, sns):
    # Discoveries / Locale
    top_methods_l = df_default['disc_locale'].value_counts().index
    ax_dl = sns.countplot(data=df_default, y="disc_locale", order=top_methods_l)
    ax_dl.set_xlabel("Number of Discoveries")
    ax_dl.set_ylabel("Discovery Locales")

    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can see, while we knew at least around 4'000 exoplanets were made from space that still around 2'000 ones were made from the ground. The space discoveries amount being greater is logical from the fact that there is no more atmosphere adding noise to ground measurements.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Knowing Transit method helped us discover a huge amount of exoplanets, knowing the usage of the different methods through the years can help understanding data accuracy.
    """)
    return


@app.cell
def _(df_default, pd, plt, sns):
    # Heatmap - Methods vs Year
    heatmap_data = pd.crosstab(df_default['discoverymethod'], df_default['disc_year'], normalize="columns")

    plt.figure(figsize=(14, 6))
    sns.heatmap(heatmap_data,
                cmap="flare",
                annot=False,
                linewidths=0.5,
                vmin=0,
                vmax=1
               )

    plt.title("Exoplanet Discoveries: Method vs. Year (Normalized per year)")
    plt.xlabel("Discovery Year")
    plt.ylabel("Discovery Method")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can see, in the early 90s the Pulsar timing method was the most usde to proved the first exoplanets.

    Starting from the late 90s until 2010, the radial velocity was the most efficient before Transit method became more efficient.

    For the others methods, Imaging and Microlensing are less efficient in this field but still led to some discoveries, while the other are less efficient and helped only in a few discoveries.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Then, knowing methods and locale discoveries amount, it can be interesting to see if methods from a specific locale are better than from another.
    """)
    return


@app.cell
def _(df_default, pd, plt, sns):
    # Heatmap - Locale vs Method
    locale_method_data = pd.crosstab(df_default['disc_locale'], df_default['discoverymethod'])

    plt.figure(figsize=(10, 5))
    sns.heatmap(locale_method_data,
                annot=True,
                fmt="d",
                vmax=500,
                linewidths=0.5)

    plt.title("Exoplanet Discoveries: Locale vs. Method")
    plt.xlabel("Discovery Method")
    plt.ylabel("Discovery Locale")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can see that imaging, microlensing and radial velocity discoveries are made from the ground while the transit is mostly made from the Space, a tenth of the discoveries by transit are still made from the ground.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exoplanets parameters

    Discovering exoplanets is one thing, knowing what they are, their parameters is another.

    From the past analysis, we'll focus on the 2 main methods: Radial velocity and Transit methods since they are the ones leading to the most exoplanets discoveries. Now, understanding how those methods works become imperative to make relevant analysis.

    ### Radial velocity method
    When an extrasolar planet orbits its host star, it also attract its star making it wobble from our point of view. When getting the radial velocity of a star, we can detect a doppler effect, wobbling of it, telling there is at least an exoplanet orbiting it.

    ### Transit spectrometry method
    When an exoplanet crosses in front of its parent star disk (transit), then the observed visual brightness of the star drops by a amount relative of the extrasolar planet's size.
    """)
    return


@app.cell
def _(df_default):
    df_methods = df_default[df_default['discoverymethod'].isin(['Transit', 'Radial Velocity'])]
    return (df_methods,)


@app.cell
def _(mo):
    mo.md(r"""
    Knowing how those methods works, we can suppoose the method used biased the type of exoplanet found. A first exoplanet paramter maybe worth comparing is the orbital period.
    """)
    return


@app.cell
def _(df_methods, plt, sns):
    df_clean_orbper = df_methods.dropna(subset=['pl_orbper'])

    sns.boxplot(data=df_clean_orbper, x="discoverymethod", y="pl_orbper", log_scale=True)
    plt.xlabel("Discovery Method")
    plt.ylabel("Orbital Period (Days) - Log Scale")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can see the method used has an impact on the scale of the orbital period of the exoplanets. Transit method tends to detect exoplanets with an orbital period of around 20 days and less, when the radial velocity is from 20 days up to 1'000 thousand days.

    This is logically explained by the fact that telesopes in space, using the Transit method, only points to same points for a few months to a few years only before measuring something else. This makes exoplanets with a long orbital period as less prone to be detected when crossing their star.

    On the other side, radial velocity, doesn't necessarily need the extrasolar planet to pass in front of its host star, a slight deviation of its path is enough to know there is an exoplanet. This explains why we tends to find exoplanets with larger orbital period.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Still with the methods and extrasolar planet parameters, we can htink that there may also be a difference in the mass and size of the exoplanet discovered by a specific method.

    We could suppose mass and size are heavily related but the composition of the planet can make two similar size exoplanets have high difference in their masses. For example, gas giant will have a lighter mass that rocky planets.

    Starting with the mass, at first, a logical hypothesis would be that heavier planets tends to be better recognised by radial velocity method since a greater mass implies a bigger doppler effect, which the radial velocity method relies on.
    """)
    return


@app.cell
def _(df_methods, plt, sns):
    df_clean_masse = df_methods.dropna(subset=['pl_masse'])

    sns.boxenplot(df_clean_masse, x="discoverymethod", y="pl_masse", log_scale=True)
    plt.xlabel("Discovery Method")
    plt.ylabel("Exoplanet mass (Earth mass)")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As we can see on the boxen plot, the hypothesis proved to be true and that radial velocity mainly focuses on bigger mass exoplanets when Transit methods prefer extrasolar planets around 10 and 300 earth masses.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, with the radius, we could suppose that this time it is the transit method that will prefer high radius exoplanets because it would mean, when transitting its host star, having a greater decrease in its star observable brightness.
    """)
    return


@app.cell
def _(df_methods, plt, sns):
    df_clean_rade = df_methods.dropna(subset=["pl_rade"])

    sns.kdeplot(
        data=df_clean_rade, 
        x="pl_rade", 
        hue="discoverymethod", 
        fill=True,
        alpha=0.5,
        common_norm=False,
        log_scale=True,    # Define whether it's better to log or not
    )

    plt.xlabel("Radius (Earth radii)")
    plt.ylabel("Density (Relative frequency)")
    plt.title("Transit vs. Radial Velocity planet radii")

    plt.tight_layout()
    plt.show()
    return (df_clean_rade,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can see that both method's discovered exoplanet's radius density spikes around 2 and 15 times the earth radii. Before saying the Transit method isn't really more impacted by the exoplanet radius, we must analyze what those spikes means.

    We know there is multiple planet types in their composition and we already named the Gas giants and the rocky planets. But there is also some planets types that are defined by their size. From the transit density graph, we can suppose there are some types defined around 2 and 15 times the earth radii. As explained by [Nasa exoplanets types page](https://science.nasa.gov/exoplanets/planet-types/) there are the Super-Earth that are bigger than Earth and littler than Neptune which defines the first spike, and the Gas giants that are at least of the size of Jupiter, which defines the second spike.

    This still doesn't prove whether our hypothesis about transit method was right or not. We see that Super-Earth are the planets mostly detected by the 2 methods, especially the transit one, but this can simply be because of tierce variables we still need to find.

    The next thing to analyse is the correlation between radius and mass to have a validation about whether Gas giant really are lighter than other.
    """)
    return


@app.cell
def _(df_default, plt, sns):
    cols = ["pl_masse", "pl_rade", "discoverymethod"]
    df_mr = df_default.dropna(subset=cols)

    sns.scatterplot(
        data=df_mr,
        x="pl_masse",
        y="pl_rade",
        hue="discoverymethod",
        alpha=0.25,
    )
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Mass ($M_{\\oplus}$)")
    plt.ylabel("Radius ($R_{\\oplus}$)")
    plt.title(f"Mass-Radius Distribution (N = {len(df_mr)} out of {len(df_default)})")
    plt.show()
    return (df_mr,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Taking in account all 1557 exoplanets that share mass and radius measurements in the same line discovered by any kind of method and putting them in a scatterplot, we get 2 clusters of mass-radius relation. We can also observe that those cluster are linear, meaning gas-giant tends to be heavier and larger with around 300 times the Earth mass and being around 15 times larger than Earth. Still on those gas-giants, we can see that after 100 earth masses, their radius doesn't get necessarily bigger and stays around 15 Earth radii.

    This effect, while maybe seeming unlogical, can be explained by physics with the Core Accretion model. Gas giants are formed in multiples phases. The first phase is the slow accumulation of solid materials. Then, when the core reach around 10 $M_\oplus$, the gravitational force is strong enough to gather protoplanetory disk's gas. The final phase, the gas accretion, takes places when the atmoshphere mass is approaching the solid core mass. The planet's intense gravity leads to an extremely rapid, uncontrolled infall of protoplanetary disk's hydrogen and helium. This process continues until the gas supply is exhausted or the entire protoplanetary disk dissipates, resulting in said gas giants.

    While this shows again the 2 main exoplanets types, this still doesn't explain why the Transit method has found more exoplanet with a super-earth like radius than gas-giants radius. It's important not to get mislead by this second graph where it seems to have more gas-giants found by the Transit method, this is due to MNAR data and the drop of rows that are N/A for either the radius or mass parameters.

    A possible reason to the transit method finding less gas-giant even when it's supposed to work is that orbital period of gas giant can take longer because of its mass, we need to see the correlation between those 2 variables.
    """)
    return


@app.cell
def _(df_clean_rade, df_default, df_mr, plt, sns):
    df_clean_orbper_rade = df_clean_rade.dropna(subset='pl_orbper')

    sns.scatterplot(
        data=df_mr,
        x="pl_orbper",
        y="pl_rade",
        hue="discoverymethod",
        alpha=0.25,
    )
    plt.xscale("log")
    plt.xlabel("Orbital period (Days)")
    plt.ylabel("Radius ($R_{\\oplus}$)")
    plt.title(f"Orbital Period-Radius Distribution (N = {len(df_clean_orbper_rade)} out of {len(df_default)})")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can see that the orbital period isn't the reason. There is no relation between the orbital period and the radius of exoxplanets. This graph doesn't tell anything that we didn't know, we just showed that 2 variables we played with earlier were independant.

    With online researches it is explained by the [italian national institute of astronomy](http://www.inaf.it/en/inaf-news/billions-of-rocky-planets-in-the-habitable-zones-around-red-dwarfs) that Super-Earth are very common. The article tells that around red dwarfs, a type of star, it's common to find rocky, thus Super-Earth exoplanets. With this, we know red dwarfs are most likely to have Super-Earth orbiting exoplanets, this could potentially implies that there can be a pattern of exoplanets around specific type of stars.
    """)
    return


if __name__ == "__main__":
    app.run()
