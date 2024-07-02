"""
    PCC Tests
    Jorge F. García-Samartín
    www.gsamartin.es
    2024-07-01
"""

import numpy as np

import kinematics.pcc

def main():

    # Setup parameters
    n_lengths = 100

    # Generate random lengths
    l = np.random.rand(n_lengths, 3) * 100

    # Test FK
    for i in range(n_lengths):
        T, params = kinematics.pcc.fk(l[i,:])

        xP = np.array([T[0, 3], T[1, 3], T[2, 3]])
        l_, params2 = kinematics.pcc.ik(xP)

        # Compare params (lr, phi, kappa) with tolerance
        np.testing.assert_allclose(params['lr'], params2['lr'], atol=1e-6)
        np.testing.assert_allclose(params['phi'], params2['phi'], atol=1e-6)
        np.testing.assert_allclose(params['kappa'], params2['kappa'], atol=1e-6)

        # Compare lengths
        np.testing.assert_allclose(l[i,:], l_, atol=1e-6)


if __name__ == '__main__':
    main()