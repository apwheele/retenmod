# retenmod

This is a python port of the R package [foretell](https://cran.r-project.org/web/packages/foretell/foretell.pdf). This projects customer retention rates, see [*“How to Project Customer Retention” Revisited: The Role of Duration Dependence* (Fader et al., 2018)](https://www.sciencedirect.com/science/article/pii/S1094996818300057) for the original formulation and description of the models. 

To install, just use pip:

    pip install retenmod

Only dependencies are scipy and numpy. For a simple example of use for the BdW model:

    import retenmod
    surv = [100, 86.9, 74.3, 65.3, 59.3]
    res = retenmod.bdw(surv,6)
    print(res.params)
    print(res.proj)