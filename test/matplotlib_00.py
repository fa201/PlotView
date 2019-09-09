#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tracer un graphique de fonction dans MATPLOTLIB
Sources :
https://www.youtube.com/watch?v=kjesUtf5s3U&list=PLQW7kM0PhTV7oyb5hgL65U8Uz2FzvrjNY&index=11&t=0s
https://openclassrooms.com/fr/courses/4452741-decouvrez-les-librairies-python-pour-la-data-science/4740942-maitrisez-les-possibilites-offertes-par-matplotlib
"""

import matplotlib.pyplot as plt
from matplotlib import style

style.use('dark_background')

# Création des listes de coordonées des points
x = []
y1 = []
y2 = []
x_start = 0  # Début de la plage d'abscisse à considérer
step = 1  # Pas de la liste des abscisses
number_point = 30

# Fonctions mathématiques à tracer
def f1(t):
    return t**2-2*t
def f2(t):
    return 5*t

# Création des points à tracer.
# Alternativement utiliser numpy.linspace
for i in range(0, number_point, 1):
    x.append(x_start)
    y1.append(f1(x_start))
    y2.append(f2(x_start))
    x_start += step

# fig est un conteneur qui contient tous les objets (axes, labels, données, etc.)
fig = plt.figure(figsize=(6.0,4.0))  # figsize in inches, facecolor='white' 
ax = plt.axes()  # facecolor='white'

# Tracer de la courbe
# ls -> linestyle
# lw -> linewidth
plt.plot(x, y1, color='blue', ls='solid', lw='2', label='f1', marker='+', markersize=7.0)
plt.plot(x, y2, color='red', ls='dotted', lw='3', label='f2', marker='x', markersize=5.5)
# Limites des axes : choix parmi les 3 possibilités suivantes
# plt.axis([-1, 10, -1, 100])  # Définition manuelle
plt.axis('tight')  # Zone gaphique au plus près
# plt.axis('equal')  # Axes ayant la même échelle
# Labels
plt.title('Titre')
plt.legend(loc='lower right')
ax = ax.set(xlabel='Axe X', ylabel='Axe Y')
plt.grid(True)  # Affiche la grille
# Export du graphique en image
#plt.savefig("export_fig_matplotlib.png")
# Affichage du graphique
plt.show()

# Fonctions intéressantes:
# annotate