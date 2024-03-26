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
    # Zéros, pôles
    z1, p1, k1 = signal.butter(order, wn, typefiltre, analog=True, output='zpk')
    hp.pzmap1(z1, p1, titre)

    b1, a1 = signal.butter(order, wn, typefiltre, analog=True, output='ba')
    print(f'{titre}: Butterworth Numérateur {b1}, Dénominateur {a1}')
    print(f'{titre}: Racine butterworth Zéros:{z1}, Pôles:{p1}')

    print(f'{titre}: Gain butterworth {k1}')

    # Lieu de bode
    mag1, ph1, w1, fig, ax = hp.bodeplot(b1, a1, titre)

    # Délai de groupe
    delay = - np.diff(ph1) / np.diff(w1)  # calcul
    hp.grpdel1(w1, delay, titre)  # affichage

    return z1, p1, k1


def circuit():

    # Liste des fréquences et leur type de filtre
    liste = {700: "low", 1000: "high", 5000: "low", 7000: "high"}

    h = []
    for fc in liste:
        h += [filtre(fc, liste[fc])]  # fréquence de coupure, type de filtre

    # X1 = K1 ; X2 = K2
    # H = -X1*H1 + X2*H2*H3 -H4

    # H1 - Passe-bas
    z1, p1, k1 = h[0]

    # H2 - Passe-bande : Haut
    z2, p2, k2 = h[1]

    # H3 - Passe-bande : Bas
    z3, p3, k3 = h[2]

    # H4 - Passe-haut
    z4, p4, k4 = h[3]

    # passe bande en série H2*H3
    zs, ps, ks = hp.seriestf(z2, p2, k2, z3, p3, k3)

    # Passe-bas et passe bande en paralèlle
    x1 = 1  # K1
    x2 = 0.75  # K2

    # x1 en gain négatif pour un déphasage de 180 degrés
    zp1, pp1, kp1 = hp.paratf(z1, p1, -x1 * k1, zs, ps, x2 * ks)

    # Sortie finale
    # k4 en gain négatif pour un déphasage de 180 degrés
    zf, pf, kf = hp.paratf(zp1, pp1, kp1, z4, p4, -k4)

    # Dénominateur et Numérateur du circuit final
    bp1, ap1 = signal.zpk2tf(zf, pf, kf)

    #Génère une onde carrée, ajuster la frequence
    fsquare = 1000  # Hz
    t, step = np.linspace(0, .01, 5000, retstep=True)
    u1 = signal.square(2 * np.pi * fsquare * t, 0.5)

    #Simuler la sortie de chacun des filtres (passe-haut, passe-bas et les deux en parallele) avec la fonction lsim
    toutp, youtp, xoutp = signal.lsim((bp1, ap1), u1, t)  # Circuit final
    tout1, yout1, xout1 = signal.lsim((z1, p1, k1 * -x1), u1, t)  # Filtre passe-bas
    tout2, yout2, xout2 = signal.lsim((zs, ps, ks * x2), u1, t)   # Filtre passe-bande
    tout3, yout3, xout3 = signal.lsim((z4, p4, -k4), u1, t)       # Filtre passe-haut
    yout = [yout1, yout2, yout3, youtp]
    hp.timepltmulti2(t, u1, toutp, yout, f'Égaliseur klow={x1}, khigh={x2}', ['H1', 'H2*H3', 'H4', 'HÉgaliseur'])

    # Lieu de bode du circuit
    mag1, ph1, w1, fig, ax = hp.bodeplot(bp1, ap1, "circuit corrigé")

    # Délai de groupe
    delay = - np.diff(ph1) / np.diff(w1)  # calcul
    hp.grpdel1(w1, delay, "circuit corrigé")  # affichage

    # Poles et zéros
    hp.pzmap1(zf, pf, "circuit corrigé")


def main():
    print("Début du programme")
    circuit()
    plt.show()

if __name__ == '__main__':
    main()
