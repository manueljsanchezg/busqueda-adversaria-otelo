'''import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from keras.utils import set_random_seed
set_random_seed(394867)

import pandas as pd
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

objetivo = partidas_otelo.loc[:, 'ganador']
print(objetivo.head())

# SEPARACION TRAIN TEST
(atributos_entrenamiento, atributos_prueba,
 objetivo_entrenamiento, objetivo_prueba) = train_test_split(
    atributos, objetivo,
    test_size=.2
)
 
# NEURONAS ENTRADA Y SALIDA
red_otelo = Sequential()
red_otelo.add(Input(shape=(65,)))
red_otelo.add(Dense(128, activation='sigmoid'))
red_otelo.add(Dense(64, activation='sigmoid'))
red_otelo.add(Dense(32, activation='sigmoid'))
red_otelo.add(Dense(1, activation='tanh'))

# 3. Compilación con SGD ajustado
optimizador = SGD(learning_rate=0.01, momentum=0.9)
red_otelo.compile(
    optimizer=optimizador,
    loss='mean_squared_error',
    metrics=['mean_absolute_error']
)

red_otelo.fit(
    atributos_entrenamiento,
    objetivo_entrenamiento,
    batch_size=64,
    epochs=200,
    verbose=1
)'''
#red_otelo.evaluate(atributos_prueba, objetivo_prueba)


##############################


import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Normalization
from keras.optimizers import SGD
from sklearn.model_selection import train_test_split

# Cargar los datos
partidas_otelo = pd.read_csv('partidas_ia_vs_ia.csv')

# Separar características y objetivo
atributos = partidas_otelo.drop('ganador', axis=1).values
objetivo = partidas_otelo['ganador'].values

# Preprocesar los datos
# Convertir el ganador a categorías: 0 (empate), 1 (negras), 2 (blancas)
objetivo_categorical = pd.get_dummies(objetivo).values

# Dividir en conjuntos de entrenamiento y prueba
atributos_train, atributos_test, objetivo_train, objetivo_test = train_test_split(atributos, objetivo_categorical, test_size=0.2, random_state=42)

# Normalizar los datos
normalizer = Normalization()
normalizer.adapt(atributos_train)

# Crear el modelo
model = Sequential([
    normalizer,
    Dense(128, activation='relu'),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(1, activation='tanh')
])

# Compilar el modelo
model.compile(
    optimizer=SGD(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)


model.summary()

history = model.fit(
    atributos_train, objetivo_train,
    epochs=300,
    batch_size=32,
    verbose=1
)

test_loss, test_acc = model.evaluate(atributos_test, objetivo_test)
print(f'Test accuracy: {test_acc}')

model.save('otelo_model.keras')