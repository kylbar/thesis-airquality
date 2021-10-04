#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 12:26:04 2021

@author: kayla
"""

from standards import *
import matplotlib.patches as patches

x = np.linspace(-100, 100, 201)
y = np.linspace(-50, 50, 101)
X, Y = np.meshgrid(x, y)

groundTruth = np.exp(-1 * ((X-20)**2 + (Y-20)**2)/40**2) + 0.01*(X+Y)
plt.pcolormesh(x, y, groundTruth, shading = 'auto')

kachelCoords, kachelValues, fullKachelData = createKacheln(x, y, groundTruth, 3, 2)
plt.pcolormesh(x, y, fullKachelData, shading = 'auto')

numPoints = 6
pointsX = np.random.randint(0, len(x), size = 6)
pointsY = np.random.randint(0, len(y), size = 6)
pointCoords = [[x[pointsX[i]], y[pointsY[i]]] for i in range(numPoints)]
pointsValues = [groundTruth[pointsY[i], pointsX[i]] for i in range(numPoints)]

def calcDistance(X, Y, coords):
    distance = np.sqrt((X-coords[0])**2 + (Y - coords[1])**2)
    return distance


interpol = twoDimBarnes(x, y, pointCoords, pointsValues, kachelCoords, kachelValues)

plt.pcolormesh(x, y, interpol, shading = 'auto')

residualBarnes = groundTruth - interpol
residualKacheln = groundTruth - fullKachelData
print(np.std(residualBarnes))
print(np.std(residualKacheln))
print(np.mean(np.abs(residualBarnes)))
print(np.mean(np.abs(residualKacheln)))