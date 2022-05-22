"""Conversion examples python side."""
import numpy as np

import carma_py_example as carma

def test_1():
    sample = np.asarray(
        np.random.random(size=(10, 2)),
        dtype=np.float64,
        order='F'
    )

    _ = carma.manual_example(sample)
    _ = carma.automatic_example(sample)


def test_2():
    sample = np.asarray(
        np.random.random(size=(10, 2)),
        dtype=np.float64,
        order='F'
    )
    sample2 = np.asarray(
        np.random.random(size=(10, 2)),
        dtype=np.float64,
        order='F'
    )

    example_class = carma.ExampleClass(sample, sample2)
    np.testing.assert_array_equal(example_class.member_func(), sample + sample2)

def test_3():
    n = 100
    y = np.linspace(1, n, num=n) + np.random.normal(0, 0.5, n)
    X = np.hstack((
        np.ones(n)[:, None],
        np.arange(1, n+1)[:, None]
    ))
    _, p = X.shape
    coeff, std_err = carma.ols(y, X)

    np_coeffs, _, _, _ = np.linalg.lstsq(X, y)
    np_resid = y - X@np_coeffs

    np_sig2 = np_resid.T@np_resid/(n-p);
    np_std_errs = np.sqrt(np_sig2*np.diag(np.linalg.inv(X.T@X)))

    np.testing.assert_array_almost_equal(coeff.flatten(), np_coeffs)
    np.testing.assert_array_almost_equal(std_err.flatten(), np_std_errs)

