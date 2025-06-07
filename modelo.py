import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from keras.utils import set_random_seed
set_random_seed(394867)

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from keras import Sequential, Input
from keras.layers import Dense

from keras.optimizers import SGD

# LECTURA
partidas_otelo = pd.read_csv("partidas_ia_vs_ia.csv")
print(partidas_otelo.head())

# SEPARACION ATRIBUTOS Y OBJETIVO
atributos = partidas_otelo.loc[:, '(0, 0)':'turno']
print(atributos.head())

ganador = partidas_otelo.loc[:, 'ganador']
objetivo = np.zeros_like(ganador, dtype=float)
objetivo[ganador == 1] = -1.0  # Negras ganan
objetivo[ganador == 2] = 1.0   # Blancas ganan
print(objetivo[:5])

# SEPARACION TRAIN TEST
(atributos_entrenamiento, atributos_prueba,
    objetivo_entrenamiento, objetivo_prueba) = train_test_split(
        atributos, objetivo,
        test_size=.2
)

# NEURONAS ENTRADA Y SALIDA
red_otelo = Sequential()
red_otelo.add(Input(shape=(65,)))
red_otelo.add(Dense(128, activation='relu'))
red_otelo.add(Dense(64, activation='relu'))
red_otelo.add(Dense(32, activation='relu'))
red_otelo.add(Dense(1, activation='tanh'))

# 3. Compilación con SGD ajustado
optimizador = SGD(learning_rate=0.001)
red_otelo.compile(
    optimizer=optimizador,
    loss='mean_squared_error',
    metrics=['mean_absolute_error']
)

red_otelo.fit(
    atributos_entrenamiento,
    objetivo_entrenamiento,
    batch_size=32,
    epochs=2000,
    verbose=1
)

red_otelo.evaluate(atributos_prueba, objetivo_prueba)

red_otelo.save('red_otelo.h5')