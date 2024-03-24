"""
Fichier: app6.py
But: simuler les filtres et imprimer leurs graphiques
Date: 24/03/2024
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal

import helpers as hp


def passebande(fcH, fcB):
    print("passebande")
    """
    Fonction passe bande
    
    :parameter fcH: Fréquence de coupure haute du filtre
    :parameter fcB: Fréquence de coupure basse du filtre
    :return:
    """
    bas = passebas(fcB)
    haut = passehaut(fcH)




def passehaut(fc):
    print("passehaut")

    order = 2
    wn = 2 * np.pi * fc

    b1, a1 = signal.butter(order, wn, 'high', analog=True)

    mag1, ph1, w1, fig, ax = hp.bodeplot(b1, a1, f'filtre passe-haut {fc} Hz')
    return mag1, ph1, w1, fig, ax


def passebas(fc):
    print("passebas")

    order = 2
    wn = 2 * np.pi * fc  # frequence de coupure = 700Hz = 2 * np.pi * 700

    # définit un filtre passe bas butterworth =>  b1 numerateur, a1 dénominateur
    b1, a1 = signal.butter(order, wn, 'low', analog=True)

    mag1, ph1, w1, fig, ax = hp.bodeplot(b1, a1, f'filtre passe-bas {fc} Hz')

    return mag1, ph1, w1, fig, ax


def main():
    print("Début du programme")
    # passebas(700)
    # passehaut(1000)
    passebande(1000, 5000)
    plt.show()


if __name__ == '__main__':
    main()
