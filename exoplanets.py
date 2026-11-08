import marimo

__generated_with = "0.25.2"
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
    import re

    return mo, pd, plt, re, sns


@app.cell
def _(pd):
    # Load dataset
    df = pd.read_csv("./exoplanetes_data.csv", skiprows=292, low_memory=False)
    return (df,)


@app.cell
def _(plt, sns):
    # Mathplotlib and seaborn dark theme setup
    plt.style.use('dark_background')

    custom_params = {
        "figure.facecolor": "black",
        "axes.facecolor": "#1c1c1c",
        "axes.edgecolor": "#333333",
        "grid.color": "#333333",
        "text.color": "white",
        "axes.labelcolor": "white",
        "xtick.color": "white",
        "ytick.color": "white"
    }

    sns.set_theme(style="darkgrid", rc=custom_params)
    return


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
        alpha=0.2,
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
    willWe can see that the orbital period isn't the reason. There is no relation between the orbital period and the radius of exoxplanets. This graph doesn't tell anything that we didn't know, we just showed that 2 variables we played with earlier were independant.

    With online researches it is explained by the [italian national institute of astronomy](http://www.inaf.it/en/inaf-news/billions-of-rocky-planets-in-the-habitable-zones-around-red-dwarfs) that Super-Earth are very common. The article tells that around red dwarfs, a type of star, it's common to find rocky, thus Super-Earth exoplanets. This information allows us to move on from the Transit method and exoplanets radius correlation problem and focus onto another problematic, the correlation between exoplanets and their host star. This allows us to move on from the transit method and the radius un-correlation because since Super-Earth are most common and because of MNAR data, we will eventually find more Super-Earth exoplanets than Gas-Giants.

    From the article we can suppose that an exoplanet's parameter can be determined, guessed from its host star parameters. This problematic will be the subject of this study but before diving directly to this, we must understand the remaining planets parameters.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The dataset contains various exoplanet's parameters, in addition to the orbital period, mass and radius some other paramters are useful for the project such as the eccentricity, the orbital semi-major axis, etc. The dataset also provides some data that we won't use for this work such as radial velocity magnitude and other method's related fields since the research focuses on extrasolar planet's parameters given star's ones.

    The exoplanet's paramters that are, at first sight, meaningful to study before applying are:
    1. **The orbital period:** Time of orbit around the host star
    2. **The mass**
    3. **The radius**
    4. **The eccentricity:** Tells how much the orbit deviates from a perfect circle
    5. **The Orbital semi-major axis:** Half the length of the longest orbital ellipse axis
    7. **The equilibrium temperature:** The thoerical temperature if it was a black body heated only by its parent star
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    About stellar parameters, the retained ones are the following:
    1. **The spectral type:** Star classification
    2. **Effective temperature:** The temperature of a theorical black body of the same size emitting the same amount of radiant energy
    3. **The radius**
    4. **The mass**
    5. **The metallicity:** The metal content of the photosphere compared to the Hydrogen content
    6. **The luminosity:** Amount of energy emitted
    7. **Surface gravity**
    8. **Age**
    9. **Rotational velocity / period:** Period for the host star to complete a full rotation at a given speed
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And for the system parameters the one retained are:
    1. **Number of orbiting planets**
    2. **Number of stars**
    3. **Number of moons**
    4. **Total proper motion:** Angular speed of the center of mass at the center of gravity of the system
    5. **Distance:** Distance of the system from the solar system
    6. **Parallax:** Angle of the star from earth's orbit
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Continuing with exoplanet's parameters, we already went over orbital period, mass and radius. We've also seen that MNAR data was leading to unlogical graphs if not intepreted taking in account the MNAR data. It will be important to study if data should be merged from not default rows or being interpolated, predicted using Machine Learning (ML). Let's continue with the rest of the paramters and their correlation with the discovery method to understand better the MNAR data, starting with eccentricity.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can plot the eccentricity and the semi-major axis in a same KDE joint plot and have a grasp about those 2 parameters in the same graph.
    """)
    return


@app.cell
def _(df_methods, plt, sns):
    df_clean_orbsmax_orbeccen = df_methods.dropna(subset=['pl_orbsmax', 'pl_orbeccen'])

    g = sns.jointplot(
        data=df_clean_orbsmax_orbeccen,
        x='pl_orbsmax',
        y='pl_orbeccen',
        hue='discoverymethod',
        kind='kde',
        fill=True,
        alpha=0.65,
        log_scale=(True, False),
        common_norm=False
    )

    g.ax_joint.set_xlabel(f'Orbital Semi-Major Axis [AU] (N = {len(df_methods.dropna(subset='pl_orbsmax'))})')
    g.ax_joint.set_ylabel(f'Orbital Eccentricity (N = {len(df_methods.dropna(subset='pl_orbeccen'))})')
    g.ax_joint.set_ylim(0, 1.0)

    g.ax_marg_x.set_title(f'Eccentricity vs. Semi-Major Axis and marginal distributions (N = {len(df_clean_orbsmax_orbeccen)})')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The graph displays, on the X axis, the density of the orbital semi-major axis and on the Y-axis, the density of the orbital eccentricity. Putting the 2 values on a bivariate KDE plot, we can see a correlation between the 2 parameters.

    What this graphs gives us, for the density curve, is that the Transit discovery method targets mainly small, lower to 1 AU orbital semi-major axis and specifically around 0.05 AU. When, on the other side, the radial velocity method curve has 2 small bumps, one tiny bump around 0.06-0.1 AU and another, slightly bigger around 1-2 AU but has more repartition of data than the Transit discovery method.

    For the orbital eccentricity density we can see that the transit method nearly has all its value near 0 ($e \equiv 0$) when radial velocity discovery method is targets slightly more eccentric orbits ($e \equiv 0.15$) and has more repartition of its data.

    The second graph, that shows the correlation between the eccentricity and the semi-major axis tells us that the closest a planet is to its star, the more its orbit looks like a perfect circle, it's eccentricity is near 0. As the semi-major axis increases, exoplanets orbits are also impacted by other objects such as other exoplanets from the same solar system making eccentricity rise up to 0.85.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Finishing exoplanets parameters with the equilibrium temperature. This will have strong correlation with the star effective temperature parameter but could also hide some other information.
    """)
    return


@app.cell
def _(df_methods, plt, sns):
    df_eqt = df_methods.dropna(subset=['pl_eqt'])

    sns.kdeplot(df_eqt, x='pl_eqt', hue='discoverymethod', common_norm=False)
    plt.title(f"Distribution of exoplanet equilibrium temperature (N = {len(df_eqt)})")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The graph shows that the radial velocity method tends to mainly target "low" temperature exoplanets, around 300° K with tiny bumps around 900° and 1200° K. And the Transit method shows only 2 distinct peaks around 750° K and 1500° K. Those 2 values standing out can maybe be linked to the exoplanets types that we discovered with exoplanets radii and masses.
    """)
    return


@app.cell
def _(df_methods, plt, sns):
    df_clean_eqt_masse = df_methods.dropna(subset=['pl_eqt', 'pl_rade'])
    sns.scatterplot(df_clean_eqt_masse, x='pl_eqt', y='pl_rade', alpha=0.1)
    plt.title(f"Correlation between equilibrium temperature and radii (N = {len(df_clean_eqt_masse)})")
    plt.xlabel(f"Equilibrium temperature [K]")
    plt.ylabel(f"Radius [Earth Radius]")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Plotting the equilibrium temperatures along the exoplanets radius, we can see that the 2 exoplanets categories seems to also stand out, yet less distincitve but starting from a certiain radius, temperature seems to get bigger. We know that the radius nor mass has no direct impact on the equilibrium temperature but can reveals other correlation about density, composition of the exoplanets.
    """)
    return


@app.cell
def _(df_default):
    EXOPLANET_COLS = ['pl_orbper', 'pl_masse', 'pl_rade', 'pl_orbeccen', 'pl_orbsmax', 'pl_eqt']
    df_exoplanets_full = df_default.dropna(subset=EXOPLANET_COLS)
    per_exoplanets = (len(df_exoplanets_full), len(df_default), len(df_exoplanets_full) / len(df_default) * 100)
    print(f'Default flagged columns containing all the retained columns values: {per_exoplanets[0]} / {per_exoplanets[1]} ({per_exoplanets[2]:.2f}%)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In summary, retained columns for exoplanets parameters are:
    1. **Orbital period [days]:** `pl_orbper`
    2. **Mass [Earth mass]:** `pl_masse`
    3. **Radius [Earth radii]:** `pl_rade`
    4. **Orbital eccentricity:** `pl_orbeccen`
    5. **Orbital semi-major axis [AU]:** `pl_orbsmax`
    6. **Equilibrium temperature [K]:** `pl_eqt`

    Those 6 columns will be the expected output from the model hopefully if values can be seen correlating with host stars parameters. Taking in account only default flagged rows and non N/A rows for all the retained columns, there is 954 rows of all the 6566 total rows, a bit less than 15% of rows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Stellar parameters

    Having analyzed all meaningful exoplanets parameters for the project, that is a model to predict exoplanet and system's parameters from stellar ones, the stellar parameters comes next.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The first parameter is the star spectral type. Each star gets a classification mostly based on its temperature and luminosity for the Morgan-Keenan-Kellman (commonly MK) nomenclature. The star classification working allowing multiple class for incertitudes require a bit of pre-processing before working with the data uniformly.
    """)
    return


@app.cell
def _(df_default, plt, sns):
    df_spectype = df_default.dropna(subset=['st_spectype']).copy()

    # Split the spectral type by / or - and remove white space
    df_spectype['st_spectype_list'] = df_spectype['st_spectype'].str.strip().str.split(r'\s*[/-]\s*')

    # Explode the list to get 1 type per row
    df_spectype = df_spectype.explode('st_spectype_list')

    # Keep only the first letter, the main class letter
    df_spectype['main_stellar_class'] = df_spectype['st_spectype_list'].str[0].str.upper()

    # Filter out duplicated luminosity classes and possible artifacts
    valid_classes = ['O', 'B', 'A', 'F', 'G', 'K', 'M']
    df_clean_main_spec_class = df_spectype[df_spectype['main_stellar_class'].isin(valid_classes)]

    sns.countplot(
        df_clean_main_spec_class,
        x='main_stellar_class',
        order=valid_classes
    )
    plt.title(f'Distribution of host stars per spectral type main letter \n(N = {len(df_clean_main_spec_class)} for {len(df_spectype)} rows)')
    plt.xlabel('Main class letters')
    plt.ylabel('Count of exoplanets around stellar temperature classes')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can see with this graph that exoplanets seems to orbit, or at least are discovered mostly around cooler stars. This graph only display the count for main class letters, it doesn't take in account the level nor the luminosity class. To have a grasp for luminosity classes distribution we need to do the similar work:
    """)
    return


@app.cell
def _(df_default, plt, re, sns):
    df_lum = df_default.dropna(subset=['st_spectype']).copy()

    df_lum['st_spectype_list'] = df_lum['st_spectype'].str.strip().str.split(r'\s*[/-]\s*')

    df_lum = df_lum.explode('st_spectype_list')

    def extract_detailed_luminosity(st_type):
        if not isinstance(st_type, str):
            return None

        s = st_type.strip()

        if s.startswith('D'):
            return 'VII / D'
        if s.startswith('sd'):
            return 'VI / sd'
    
        match = re.search(r'(Ia\+|Iab|Ia|Ib|III|II|IV|VII|VI|V)', s)
        if match:
            lum = match.group(1)
            if lum == 'Ia+':
                return '0 / Ia+'
            if lum == 'VI':
                return 'VI / sd'
            if lum == 'VII':
                return 'VII / D'
            return lum
    
        if re.search(r'(?:\s|-)0[a-z]*$', s):
            return '0 / Ia+'

        return None

    df_lum['luminosity_class'] = df_lum['st_spectype_list'].apply(extract_detailed_luminosity)

    table_order = [
        '0 / Ia+',
        'Ia',
        'Iab',
        'Ib',
        'II',
        'III',
        'IV',
        'V',
        'VI / sd',
        'VII / D'
    ]
    df_clean_lum_class = df_lum.dropna(subset=['luminosity_class'])

    sns.countplot(
        data=df_clean_lum_class,
        x='luminosity_class',
        order=table_order,
    )

    plt.title(f'Distribution of host stars per Detailed Luminosity Class \n(N = {len(df_clean_lum_class)} for {len(df_lum)} rows)')
    plt.xlabel('Luminosity Class')
    plt.ylabel('Count of exoplanets around stellar luminosty classes')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can see, on the luminosity side that there is way less distribution, most stars are on the main sequence, the `V` bin and none on the 0 / Ia+ to Ib stars.
    """)
    return


@app.cell
def _(df_default, plt, sns):
    df_mass = df_default.dropna(subset=['st_mass'])

    sns.histplot(df_mass, x='st_mass', bins=20, log_scale=True)
    plt.title(f'Repartition of host stars masses (N = {len(df_mass)} / {len(df_default)})')
    plt.xlabel('Stellar masses Log[Solar mass]')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can see that the repartition isn't that sparse. Most star are roughly the same size as our sun and there are none above 10 solar masses.
    """)
    return


@app.cell
def _(df_default, plt, sns):
    df_radius = df_default.dropna(subset=['st_rad'])

    sns.histplot(df_radius, x='st_rad', bins=20, log_scale=True)
    plt.title(f'Repartition of host stars radii (N = {len(df_radius)} / {len(df_default)})')
    plt.xlabel('Stellar masses Log[Solar radius]')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On the stellar radii, on the other hand, we can see that the values goes higher up to 100 times our sun's radius. Most of the star's radii still are around the same size as our sun's.
    """)
    return


if __name__ == "__main__":
    app.run()
