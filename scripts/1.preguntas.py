def calcular_pss10(respuestas):
    preguntas_inversas = [3, 4, 6, 7, 9]  # Índices de preguntas inversas (basado en índice 0)
    resultado = 0
    
    for i, respuesta in enumerate(respuestas):
        if i in preguntas_inversas:
            resultado += (4 - respuesta)  # Ajustar las preguntas inversas
        else:
            resultado += respuesta  # Sumar directamente
    
    return resultado

# Ejemplo
respuestas = [3, 2, 4, 1, 0, 3, 2, 1, 4, 2]
print(calcular_pss10(respuestas))  # Output: 30
