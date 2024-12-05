def normalizar(valor, minimo, maximo):
    return (valor - minimo) / (maximo - minimo)

def calcular_ip(par, pesos, limites):
    # Pesos y límites ajustados para tres parámetros
    w1, w2, w3 = pesos
    (lim1_min, lim1_max), (lim2_min, lim2_max), (lim3_min, lim3_max) = limites

    # Normalización de los tres valores
    valor1_norm = normalizar(par[0], lim1_min, lim1_max)
    valor2_norm = normalizar(par[1], lim2_min, lim2_max)
    valor3_norm = normalizar(par[2], lim3_min, lim3_max)

    # Cálculo del Índice Parcial (IP)
    ip = w1 * valor1_norm + w2 * valor2_norm + w3 * valor3_norm
    return ip


# Pesos y límites
pesos = [0.5, 0.3, 0.2]  
limites = [(50, 120), (35.0, 38.0), (0, 40)]  


# Ejemplo
par = [85, 36.8, 20]  # frecuencia cardíaca, temperatura y cuestionario

# Cálculo del IP
ip = calcular_ip(par, pesos, limites)
print(f"Índice Parcial (IP): {ip:.2f}")
