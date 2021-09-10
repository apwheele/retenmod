'''
pytest for each of the models
Taken from R package example
https://cran.r-project.org/web/packages/foretell/foretell.pdf
'''

import numpy
import pytest
import retenmod

def test_bdw():
    surv = [100,86.9,74.3,65.3,59.3]
    h = 6
    res = retenmod.bdw(surv,h)
    projr = [54.66194,51.03776,48.10526,45.66963,43.60444,41.82391]
    parr = [0.2593549,1.7226948,1.5842688]
    # Projections about equal
    assert res.proj[-6:] == pytest.approx(projr, rel=1e-3)
    # Parameters about equal
    assert res.params == pytest.approx(parr, rel=1e-3)

def test_bg():
    surv = [100,86.9,74.3,65.3,59.3]
    h = 6
    res = retenmod.bg(surv,h)
    projr = [53.44303,48.57783,44.44895,40.90608,37.83658,35.15453]
    parr = [1.281009,7.790563]
    # Projections about equal
    assert res.proj[-6:] == pytest.approx(projr, rel=1e-3)
    # Parameters about equal
    assert res.params == pytest.approx(parr, rel=1e-3)

def test_lcw():
    surv = [100,86.9,74.3,65.3,59.3,55.1,51.7,49.1,46.8,44.5,42.7,40.9,39.4]
    h = 6
    res = retenmod.lcw(surv,h)
    projr = [37.77275,36.24758,34.79929,33.42239,32.11202,30.86382]
    parr = [0.28774527,1.38849908,0.06893826,0.85076666,0.28845976 ]
    # Projections about equal
    assert res.proj[-6:] == pytest.approx(projr, rel=1e-2)
    # Parameters about equal
    assert res.params == pytest.approx(parr, rel=1e-2)