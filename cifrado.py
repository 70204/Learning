#!/usr/bin/env python3
# -X- coding: utf-8 -*-

import numpy as np
import random
from sympy import Matrix

diccionario_encryt = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12,
            'M': 13, 'N': 14, 'Ñ': 15, 'O': 16, 'P': 17, 'Q': 18, 'R': 19, 'S': 20, 'T': 21, 'U': 22, 'V': 23, 'W': 24, 'X': 25, 'Y': 26, 'Z': 27,' ': 0}

diccionario_decrypt = {'1' : 'A', '2': 'B', '3': 'C', '4': 'D', '5': 'E', '6': 'F', '7': 'G', '8': 'H', '9': 'I', '10': 'J', '11': 'K', '12': 'L', '13': 'M',
            '14': 'N', '15': 'Ñ', '16': 'O', '17': 'P', '18': 'Q', '19': 'R', '20': 'S', '21': 'T', '22': 'U', '23': 'V', '24': 'W', '25': 'X', '26': 'Y', '27': 'Z',
            '0': ' '}

def matriz_llave(size):
    """ Generar matriz llave

    Args:
        size ( int ): Dimension de la matriz cuadrada

    Returns:
        array : Retorna una matriz aleatoria
    """
    matrix = []

    L = []

    # Relleno una lista con tantos valores aleatorios como elementos a rellenar en la matriz determinada por size (size * size)

    for x in range(size * size):
        L.append(random.randrange(40))

    # Se crea la matrix clave con los valores generados, de tamaño size * size

    matrix = np.array(L).reshape(size, size)

    return matrix


def encriptar(message, key):
    """ Generar encripcion

    Args:
        message ( str ): Recibe frase a encriptar
        key ( array ): Recibe matriz llave
         

    Returns:
        str : Retorna cadena string encriptada
    """
    ciphertext = ''

    # Variables

    matrix_mensaje = []
    list_temp = []
    cifrado_final = ''
    ciphertext_temp = ''
    cont = 0

    # Convertir el mensaje a mayusculas

    message = message.upper()

    # Si el tamaño del mensaje es menor o igual al tamaño de la clave

    if len(message) <= len(key):

        # Convertir el tamaño del mensaje al tamaño de la clave, si no es igual, se añaden 'X' hasta que sean iguales los tamaños.

        while len(message) < len(key):
            message = message + 'X'

        # Crear la matriz para el mensaje

        for i in range(0, len(message)):
            matrix_mensaje.append(diccionario_encryt[message[i]])

        # Se crea la matriz

        matrix_mensaje = np.array(matrix_mensaje)

        # Se multiplica la matriz clave por la de mensaje

        cifrado = np.matmul(key, matrix_mensaje)

        # Se obtiene el modulo sobre el diccionario de cada celda

        cifrado = cifrado % 28

        # Se codifica de valores numericos a los del diccionario, añadiendo a ciphertext el valor en el diccionario pasandole como indice la i posicion de la variable cifrado

        for i in range(0, len(cifrado)):
            ciphertext += diccionario_decrypt[str(cifrado[i])]
    else:

    # Si el tamaño del mensaje es menor o igual al tamaño de la clave

        # Si al dividir en trozos del tamaño de la clave, existe algun trozo que tiene menos caracteres que la long. de la clave se añaden tantas 'X' como falten

        while len(message) % len(key) != 0:
            message = message + 'X'
            
        # Se divide el mensaje en subsstrings de tamaño len(key) y se alamcenan como valores de un array

        matrix_mensaje = [message[i:i + len(key)] for i in range(0,
                          len(message), len(key))]
        
        # Para cada valor del array (grupo de caracteres de la longitud de la clave)

        for bloque in matrix_mensaje:

            # Crear la matriz para el bloque

            for i in range(0, len(bloque)):
                list_temp.append(diccionario_encryt[bloque[i]])

            # Se crea la matriz de ese bloque

            matrix_encrypt = np.array(list_temp)

            # Se multiplica la matriz clave por la del bloque

            cifrado = np.matmul(key, matrix_encrypt)

            # Se obtiene el modulo sobre el diccionario de cada celda

            cifrado = cifrado % 28

            # Se codifica de valores numericos a los del diccionario, añadiendo a ciphertext el valor en el diccionario pasandole como indice la i posicion de la variable cifrado

            for i in range(0, len(cifrado)):
                ciphertext_temp += diccionario_decrypt[str(cifrado[i])]

            # Se inicializan las variables para el nuevo bloque

            matrix_encrypt = []
            list_temp = []

        # Se añade el mensaje encriptado a la variable que contiene el mensaje encriptado completo

        ciphertext = ciphertext_temp

    # --------------------------------

    return ciphertext


def desencriptar(message, key):
    """ Generar desencriptacion

    Args:
        message ( str ): Recibe frase encriptada
        key ( array ): Recibe matriz llave
         

    Returns:
        str : Retorna cadena string desencriptada
    """
    plaintext = ''

    matrix_mensaje = []
    plaintext_temp = ''
    list_temp = []
    matrix_inversa = []

    matrix_mensaje = [message[i:i + len(key)] for i in range(0,
                      len(message), len(key))]

    # Se calcula la matriz inversa aplicando el modulo 28

    matrix_inversa = Matrix(key).inv_mod(28)

    # Se transforma en una matriz

    matrix_inversa = np.array(matrix_inversa)

    # Se pasan los elementos a float

    matrix_inversa = matrix_inversa.astype(float)

    # Para cada bloque

    for bloque in matrix_mensaje:

        # Se encripta el mensaje encriptado

        for i in range(0, len(bloque)):
            list_temp.append(diccionario_encryt[bloque[i]])

        # Se convierte a matriz

        matrix_encrypt = np.array(list_temp)

        # Se multiplica la matriz inversa por el bloque

        cifrado = np.matmul(matrix_inversa, matrix_encrypt)

        # Se le aplica a cada elemento el modulo 41

        cifrado = np.remainder(cifrado, 28).flatten()

        # Se desencripta el mensaje

        for i in range(0, len(cifrado)):
            plaintext_temp += diccionario_decrypt[str(int(cifrado[i]))]

        matrix_encrypt = []
        list_temp = []
    plaintext = plaintext_temp

    # Se eliminan las X procedentes de su adicion en la encriptacion para tener bloques del tamaño de la clave

    while plaintext[-1] == 'X':
        plaintext = plaintext.rstrip(plaintext[-1])

    return plaintext
