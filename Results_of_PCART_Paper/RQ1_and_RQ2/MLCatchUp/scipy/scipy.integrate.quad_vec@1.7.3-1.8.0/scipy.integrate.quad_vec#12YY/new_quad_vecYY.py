import scipy.integrate as spi

def f(x):
    return x ** 2
(result, error) = spi.quad_vec(f, 0, 1, epsabs=1e-200, epsrel=1e-08, args=())