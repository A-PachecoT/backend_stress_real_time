def normalizar(valor, minimo, maximo):
    return (valor - minimo) / (maximo - minimo)


def calcular_ip(dato, pesos, limites):

    respuesta, facial_result, fc, t_actual, v_angular = dato
    w1, w2, w3, w4, w5 = pesos
    (fc_min, fc_max), (t_min, t_max), (v_min, v_max) = limites

    # Normalización de parámetros
    p_norm = respuesta / 4  # Normalización del puntaje (0 a 4)
    fc_norm = normalizar(fc, fc_min, fc_max)
    t_norm = normalizar(t_actual, t_min, t_max)
    v_norm = normalizar(v_angular, v_min, v_max)

    # Cálculo del IP
    ip = w1 * p_norm + w2 * fc_norm + w3 * t_norm + w4 * v_norm + w5 * facial_result
    return ip


def calcular_ite(datos, pesos, limites):

    ip_totales = [calcular_ip(dato, pesos, limites) for dato in datos]

    # Índice Total de Estrés (ITE)
    ite = sum(ip_totales) / len(ip_totales)
    return ite


# Ejemplo de datos entrantes
datos = [
    [3, 0.7, 85, 36.8, 0.05],
    [2, 0.5, 80, 36.7, 0.04],
    [4, 0.9, 90, 36.9, 0.06],
    [1, 0.3, 75, 36.5, 0.03],
    [0, 0.1, 70, 36.4, 0.02],
    [3, 0.6, 85, 36.8, 0.04],
    [2, 0.5, 78, 36.6, 0.03],
    [1, 0.4, 76, 36.5, 0.02],
    [4, 0.8, 88, 36.7, 0.05],
    [2, 0.5, 82, 36.6, 0.04],
]

# Pesos y límites
pesos = [0.3, 0.25, 0.2, 0.15, 0.1]  # Pesos iniciales
limites = [(50, 120), (35.0, 38.0), (0.0, 0.2)]  # Límites de normalización

# Cálculo del ITE
ite = calcular_ite(datos, pesos, limites)
print(f"Índice Total de Estrés (ITE): {ite:.2f}")
