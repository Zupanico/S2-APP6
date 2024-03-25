"""
Fichier: app6.py
But: simuler les filtres et imprimer leurs graphiques
Date: 24/03/2024
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal

import helpers as hp


def filtre(fc, typefiltre):
    # Affichage dans le graphique
    nom = "bandpass"
    if typefiltre == 'high':
        nom = "haut"
    if typefiltre == 'low':
        nom = "bas"

    # Titre des graphiques
    titre = f"filtre passe-{nom} {fc} Hz"

    order = 2   # ordre du filtre
    wn = 2 * np.pi * fc  # frequence de coupure = 700Hz = 2 * np.pi * 700

    # numérateur, dénominateur
    b1, a1 = signal.butter(order, wn, typefiltre, analog=True, output='ba')
    print(f'{titre}: Butterworth Numérateur {b1}, Dénominateur {a1}')
    print(f'{titre}: Racine butterworth Zéros:{np.roots(b1)}, Pôles:{np.roots(a1)}')

    # Zéros, pôles
    z1, p1, k1 = signal.butter(order, wn, typefiltre, analog=True, output='zpk')
    hp.pzmap1(z1, p1, titre)

    print(f'{titre}: Gain butterworth {k1}')

    # Lieu de bode
    mag1, ph1, w1, fig, ax = hp.bodeplot(b1, a1, titre)

    # Délai de groupe
    delay = - np.diff(ph1) / np.diff(w1)  # calcul
    hp.grpdel1(w1, delay, titre)  # affichage

    return mag1, ph1, w1, fig, ax


def main():
    print("Début du programme")

    # Liste des fréquences et leur type de filtre
    liste = {700: "low", 1000: "high", 5000: "low", 7000: "high"}

    for fc in liste:
        filtre(fc, liste[fc])  # fréquence de coupure, type de filtre

    plt.show()


if __name__ == '__main__':
    main()
