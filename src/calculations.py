# src/calculations.py
import math
from src.constants import COEFICIENTES_X2

def calcular_l_h_computacional(y: float):
    """
    Encuentra las constantes y calcula L y H usando las ecuaciones del Apéndice X2.
    L = a*Y^2 + b*Y + c
    H = d*Y^2 + e*Y + f
    """
    if y < 2.0:
        raise ValueError("La viscosidad cinemática a 100°C no puede ser menor a 2.0 mm²/s.")
    
    for y_min, y_max, a, b, c, d, e, f in COEFICIENTES_X2:
        # El límite superior es exclusivo excepto para el último rango ('inf')
        if y_min <= y < y_max or (y_max == float('inf') and y >= y_min):
            l = a * (y ** 2) + b * y + c
            h = d * (y ** 2) + e * y + f
            return l, h
            
    raise ValueError("Viscosidad fuera de los rangos definidos en la norma.")

def calcular_iv_computacional(u: float, y: float) -> dict:
    """
    Calcula el Índice de Viscosidad de acuerdo al Apéndice X2 de la norma ASTM D2270.
    U = Viscosidad Cinemática a 40°C
    Y = Viscosidad Cinemática a 100°C
    Returns: Un diccionario con el IV redondeado y los valores intermedios (L, H, N).
    """
    # 1. Obtener L y H para la viscosidad Y
    l, h = calcular_l_h_computacional(y)
    
    # 2. Determinar qué caso aplica según la relación entre U y H
    if u > h:
        # Caso 1: IV <= 100 (Ecuación 3)
        iv_exacto = ((l - u) / (l - h)) * 100
        metodo_usado = "U > H (IV <= 100)"
        n_val = None
    elif u < h:
        # Caso 2: IV > 100 (Ecuación 6 y 7)
        # N = (log10(H) - log10(U)) / log10(Y)
        n_val = (math.log10(h) - math.log10(u)) / math.log10(y)
        iv_exacto = ((10**n_val - 1) / 0.00715) + 100
        metodo_usado = "U < H (IV > 100)"
    else:
        # Caso 3: U == H -> IV es exactamente 100
        iv_exacto = 100.0
        metodo_usado = "U == H (IV = 100)"
        n_val = None

    # 3. Redondeo bajo la regla ASTM E29 (Redondeo par/bancario incorporado en round() de Python)
    iv_redondeado = round(iv_exacto)

    return {
        "iv_final": iv_redondeado,
        "iv_exacto": round(iv_exacto, 4),
        "L": round(l, 4),
        "H": round(h, 4),
        "N": round(n_val, 5) if n_val is not None else "N/A",
        "metodo": metodo_usado
    }
