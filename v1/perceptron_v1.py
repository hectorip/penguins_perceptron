import csv
import random

# cargar el archivo CSV con los datos de entrenamiento como diccionario
with open("../data/penguins.csv") as csvfile:
    data = list(csv.DictReader(csvfile))

# Limpiando los datos
data = [
    row
    for row in data
    if row["bill_depth_mm"] != "NA" and row["flipper_length_mm"] != "NA"
]


for row in data:
    row["bill_depth_mm"] = float(row["bill_depth_mm"])
    row["flipper_length_mm"] = float(row["flipper_length_mm"])


def paso(x):
    """
    Convierte cualquier número a 0 o 1
    """
    if x < 0:
        return 0
    else:
        return 1


def f(x, w1, w2, b):
    return w1 * x["bill_depth_mm"] + w2 * x["flipper_length_mm"] + b


def clasificar(x, w1, w2, b):
    """Recibe una fila de datos y devuelve 1 si es Gentoo y 0 si no lo es"""
    return paso(f(x, w1, w2, b))


def entrenar(datos, iteraciones, lr=0.01):
    # inicializamos los parámetros, esto puede ser aleatorio o cero, como lo hacemos aquí
    w1 = w2 = b = 0
    while iteraciones > 0:
        iteraciones -= 1
        for x in datos:
            etiqueta_real = int(x["species"] == "Gentoo")
            clase = clasificar(x, w1, w2, b)

            if etiqueta_real == 1 and clase == 0:
                # Aquí tenemos un Gentoo mal clasificado, tenemos que
                # aumentar w1 y w2 para que la función lineal se acerque
                # a la etiqueta real
                w1 += x["bill_depth_mm"] * lr
                w2 += x["flipper_length_mm"] * lr
                b += 1 * lr  # Valor escogido arbitrariamente
            elif etiqueta_real == 0 and clase == 1:
                # Aquí tenemos un NO Gentoo mal clasificado, tenemos que
                # disminuir w1 y w2 para que la función lineal se acerque
                # a la etiqueta real
                w1 -= x["bill_depth_mm"] * lr
                w2 -= x["flipper_length_mm"] * lr
                b -= 1 * lr  # valor escogido arbitrariamente
        print("Iteración", iteraciones, "w1:", w1, "w2:", w2, "b:", b)
    return w1, w2, b


w1, w2, b = entrenar(data, 100)


def probar(data, w1, w2, b):
    correctos = 0
    incorrectos = 0
    for x in data:
        clase = clasificar(x, w1, w2, b)
        etiqueta_real = int(x["species"] == "Gentoo")

        if clase == etiqueta_real:
            print("Correcto", x["species"], clase, f(x, w1, w2, b))
            correctos += 1
        else:
            incorrectos += 1
            if clase == 1:
                print("Es NO Gentoo etiquetado Incorrectamente")
            else:
                print("Es Gentoo etiquetado Incorrectamente")

    print("\n\nResultados:")
    print(f"Correctos: {correctos} - {(correctos / len(data)) * 100}%")
    print(f"Incorrectos: {incorrectos} - {(incorrectos / len(data)) * 100}%")


# Separando los datos de entrenamiento y pruebas
random.shuffle(data)
entrenamiento = data[: int(len(data) * 0.8)]
pruebas = data[int(len(data) * 0.8) :]

w1, w2, b = entrenar(entrenamiento, 100)
probar(pruebas, w1, w2, b)
