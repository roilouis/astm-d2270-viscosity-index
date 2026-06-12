"""
calculations.py
───────────────
Implementación del método ASTM D2270 – 10 (2016)
"Standard Practice for Calculating Viscosity Index from Kinematic Viscosity at 40 °C and 100 °C"

Incluye dos métodos de cálculo:
  1. Método Preciso        : Interpolación lineal de la Tabla 1 del método.
  2. Método (Apéndice X2) : Ecuaciones cuadráticas de la Tabla X2.1.

Autor    : Generado para el proyecto roilouis/astm-d2270-viscosity-index
Revisión : ISO/IEC 17025 – Trazabilidad de cálculo garantizada
"""

import math
from typing import Optional


# ─────────────────────────────────────────────────────────────────────────────
# TABLA 1  –  Valores básicos L y H para viscosidades cinemáticas a 100 °C
# Fuente: ASTM D2270-10 (2016), Table 1
# Estructura: { Y (mm²/s): (L, H) }
# ─────────────────────────────────────────────────────────────────────────────
TABLE_1: dict[float, tuple[float, float]] = {
    2.00: (7.994, 6.394),   2.10: (8.640, 6.894),   2.20: (9.309, 7.410),
    2.30: (10.00, 7.944),   2.40: (10.71, 8.496),   2.50: (11.45, 9.063),
    2.60: (12.21, 9.647),   2.70: (13.00, 10.25),   2.80: (13.80, 10.87),
    2.90: (14.63, 11.50),   3.00: (15.49, 12.15),   3.10: (16.36, 12.82),
    3.20: (17.26, 13.51),   3.30: (18.18, 14.21),   3.40: (19.12, 14.93),
    3.50: (20.09, 15.66),   3.60: (21.08, 16.42),   3.70: (22.09, 17.19),
    3.80: (23.13, 17.97),   3.90: (24.19, 18.77),   4.00: (25.32, 19.56),
    4.10: (26.50, 20.37),   4.20: (27.75, 21.21),   4.30: (29.07, 22.05),
    4.40: (30.48, 22.92),   4.50: (31.96, 23.81),   4.60: (33.52, 24.71),
    4.70: (35.13, 25.63),   4.80: (36.79, 26.57),   4.90: (38.50, 27.53),
    5.00: (40.23, 28.49),   5.10: (41.99, 29.46),   5.20: (43.76, 30.43),
    5.30: (45.53, 31.40),   5.40: (47.31, 32.37),   5.50: (49.09, 33.34),
    5.60: (50.87, 34.32),   5.70: (52.64, 35.29),   5.80: (54.42, 36.26),
    5.90: (56.20, 37.23),   6.00: (57.97, 38.19),   6.10: (59.74, 39.17),
    6.20: (61.52, 40.15),   6.30: (63.32, 41.13),   6.40: (65.18, 42.14),
    6.50: (67.12, 43.18),   6.60: (69.16, 44.24),   6.70: (71.29, 45.33),
    6.80: (73.48, 46.44),   6.90: (75.72, 47.51),   7.00: (78.00, 48.57),
    7.10: (80.25, 49.61),   7.20: (82.39, 50.69),   7.30: (84.53, 51.78),
    7.40: (86.66, 52.88),   7.50: (88.85, 53.98),   7.60: (91.04, 55.09),
    7.70: (93.20, 56.20),   7.80: (95.43, 57.31),   7.90: (97.72, 58.45),
    8.00: (100.0, 59.60),   8.10: (102.3, 60.74),   8.20: (104.6, 61.89),
    8.30: (106.9, 63.05),   8.40: (109.2, 64.18),   8.50: (111.5, 65.32),
    8.60: (113.9, 66.48),   8.70: (116.2, 67.64),   8.80: (118.5, 68.79),
    8.90: (120.9, 69.94),   9.00: (123.3, 71.10),   9.10: (125.7, 72.27),
    9.20: (128.0, 73.42),   9.30: (130.4, 74.57),   9.40: (132.8, 75.73),
    9.50: (135.3, 76.91),   9.60: (137.7, 78.08),   9.70: (140.1, 79.27),
    9.80: (142.7, 80.46),   9.90: (145.2, 81.67),   10.0: (147.7, 82.87),
    10.1: (150.3, 84.08),   10.2: (152.9, 85.30),   10.3: (155.4, 86.51),
    10.4: (158.0, 87.72),   10.5: (160.6, 88.95),   10.6: (163.2, 90.19),
    10.7: (165.8, 91.40),   10.8: (168.5, 92.65),   10.9: (171.2, 93.92),
    11.0: (173.9, 95.19),   11.1: (176.6, 96.45),   11.2: (179.4, 97.71),
    11.3: (182.1, 98.97),   11.4: (184.9, 100.2),   11.5: (187.6, 101.5),
    11.6: (190.4, 102.8),   11.7: (193.3, 104.1),   11.8: (196.2, 105.4),
    11.9: (199.0, 106.7),   12.0: (201.9, 108.0),   12.1: (204.8, 109.4),
    12.2: (207.8, 110.7),   12.3: (210.7, 112.0),   12.4: (213.6, 113.3),
    12.5: (216.6, 114.7),   12.6: (219.6, 116.0),   12.7: (222.6, 117.4),
    12.8: (225.7, 118.7),   12.9: (228.8, 120.1),   13.0: (231.9, 121.5),
    13.1: (235.0, 122.9),   13.2: (238.1, 124.2),   13.3: (241.2, 125.6),
    13.4: (244.3, 127.0),   13.5: (247.4, 128.4),   13.6: (250.6, 129.8),
    13.7: (253.8, 131.2),   13.8: (257.0, 132.6),   13.9: (260.1, 134.0),
    14.0: (263.3, 135.4),   14.1: (266.6, 136.8),   14.2: (269.8, 138.2),
    14.3: (273.0, 139.6),   14.4: (276.3, 141.0),   14.5: (279.6, 142.4),
    14.6: (283.0, 143.9),   14.7: (286.4, 145.3),   14.8: (289.7, 146.8),
    14.9: (293.0, 148.2),   15.0: (296.5, 149.7),   15.1: (300.0, 151.2),
    15.2: (303.4, 152.6),   15.3: (306.9, 154.1),   15.4: (310.3, 155.6),
    15.5: (313.9, 157.0),   15.6: (317.5, 158.6),   15.7: (321.1, 160.1),
    15.8: (324.6, 161.6),   15.9: (328.3, 163.1),   16.0: (331.9, 164.6),
    16.1: (335.5, 166.1),   16.2: (339.2, 167.7),   16.3: (342.9, 169.2),
    16.4: (346.6, 170.7),   16.5: (350.3, 172.3),   16.6: (354.1, 173.8),
    16.7: (358.0, 175.4),   16.8: (361.7, 177.0),   16.9: (365.6, 178.6),
    17.0: (369.4, 180.2),   17.1: (373.3, 181.7),   17.2: (377.1, 183.3),
    17.3: (381.0, 184.9),   17.4: (384.9, 186.5),   17.5: (388.9, 188.1),
    17.6: (392.7, 189.7),   17.7: (396.7, 191.3),   17.8: (400.7, 192.9),
    17.9: (404.6, 194.6),   18.0: (408.6, 196.2),   18.1: (412.6, 197.8),
    18.2: (416.7, 199.4),   18.3: (420.7, 201.0),   18.4: (424.9, 202.6),
    18.5: (429.0, 204.3),   18.6: (433.2, 205.9),   18.7: (437.3, 207.6),
    18.8: (441.5, 209.3),   18.9: (445.7, 211.0),   19.0: (449.9, 212.7),
    19.1: (454.2, 214.4),   19.2: (458.4, 216.1),   19.3: (462.7, 217.7),
    19.4: (467.0, 219.4),   19.5: (471.3, 221.1),   19.6: (475.7, 222.8),
    19.7: (479.7, 224.5),   19.8: (483.9, 226.2),   19.9: (488.6, 227.7),
    20.0: (493.2, 229.5),   20.2: (501.5, 233.0),   20.4: (510.8, 236.4),
    20.6: (519.9, 240.1),   20.8: (528.8, 243.5),   21.0: (538.4, 247.1),
    21.2: (547.5, 250.7),   21.4: (556.7, 254.2),   21.6: (566.4, 257.8),
    21.8: (575.6, 261.5),   22.0: (585.2, 264.9),   22.2: (595.0, 268.6),
    22.4: (604.3, 272.3),   22.6: (614.2, 275.8),   22.8: (624.1, 279.6),
    23.0: (633.6, 283.3),   23.2: (643.4, 286.8),   23.4: (653.8, 290.5),
    23.6: (663.3, 294.4),   23.8: (673.7, 297.9),   24.0: (683.9, 301.8),
    24.2: (694.5, 305.6),   24.4: (704.2, 309.4),   24.6: (714.9, 313.0),
    24.8: (725.7, 317.0),   25.0: (736.5, 320.9),   25.2: (747.2, 324.9),
    25.4: (758.2, 328.8),   25.6: (769.3, 332.7),   25.8: (779.7, 336.7),
    26.0: (790.4, 340.5),   26.2: (801.6, 344.4),   26.4: (812.8, 348.4),
    26.6: (824.1, 352.3),   26.8: (835.5, 356.4),   27.0: (847.0, 360.5),
    27.2: (857.5, 364.6),   27.4: (869.0, 368.3),   27.6: (880.6, 372.3),
    27.8: (892.3, 376.4),   28.0: (904.1, 380.6),   28.2: (915.8, 384.6),
    28.4: (927.6, 388.8),   28.6: (938.6, 393.0),   28.8: (951.2, 396.6),
    29.0: (963.4, 401.1),   29.2: (975.4, 405.3),   29.4: (987.1, 409.5),
    29.6: (998.9, 413.5),   29.8: (1011,  417.6),   30.0: (1023,  421.7),
    30.5: (1055,  432.4),   31.0: (1086,  443.2),   31.5: (1119,  454.0),
    32.0: (1151,  464.9),   32.5: (1184,  475.9),   33.0: (1217,  487.0),
    33.5: (1251,  498.1),   34.0: (1286,  509.6),   34.5: (1321,  521.1),
    35.0: (1356,  532.5),   35.5: (1391,  544.0),   36.0: (1427,  555.6),
    36.5: (1464,  567.1),   37.0: (1501,  579.3),   37.5: (1538,  591.3),
    38.0: (1575,  603.1),   38.5: (1613,  615.0),   39.0: (1651,  627.1),
    39.5: (1691,  639.2),   40.0: (1730,  651.8),   40.5: (1770,  664.2),
    41.0: (1810,  676.6),   41.5: (1851,  689.1),   42.0: (1892,  701.9),
    42.5: (1935,  714.9),   43.0: (1978,  728.2),   43.5: (2021,  741.3),
    44.0: (2064,  754.4),   44.5: (2108,  767.6),   45.0: (2152,  780.9),
    45.5: (2197,  794.5),   46.0: (2243,  808.2),   46.5: (2288,  821.9),
    47.0: (2333,  835.5),   47.5: (2380,  849.2),   48.0: (2426,  863.0),
    48.5: (2473,  876.9),   49.0: (2521,  890.9),   49.5: (2570,  905.3),
    50.0: (2618,  919.6),   50.5: (2667,  933.6),   51.0: (2717,  948.2),
    51.5: (2767,  962.9),   52.0: (2817,  977.5),   52.5: (2867,  992.1),
    53.0: (2918,  1007),    53.5: (2969,  1021),    54.0: (3020,  1036),
    54.5: (3073,  1051),    55.0: (3126,  1066),    55.5: (3180,  1082),
    56.0: (3233,  1097),    56.5: (3286,  1112),    57.0: (3340,  1127),
    57.5: (3396,  1143),    58.0: (3452,  1159),    58.5: (3507,  1175),
    59.0: (3563,  1190),    59.5: (3619,  1206),    60.0: (3676,  1222),
    60.5: (3734,  1238),    61.0: (3792,  1254),    61.5: (3850,  1270),
    62.0: (3908,  1286),    62.5: (3966,  1303),    63.0: (4026,  1319),
    63.5: (4087,  1336),    64.0: (4147,  1352),    64.5: (4207,  1369),
    65.0: (4268,  1386),    65.5: (4329,  1402),    66.0: (4392,  1419),
    66.5: (4455,  1436),    67.0: (4517,  1454),    67.5: (4580,  1471),
    68.0: (4645,  1488),    68.5: (4709,  1506),    69.0: (4773,  1523),
    69.5: (4839,  1541),    70.0: (4905,  1558),
}


# ─────────────────────────────────────────────────────────────────────────────
# TABLA X2.1  –  Coeficientes de ecuaciones cuadráticas (Apéndice X2)
# Fuente: ASTM D2270-10 (2016), Table X2.1
# Estructura: (Y_min, Y_max, a, b, c, d, e, f)
#   L = a*Y² + b*Y + c
#   H = d*Y² + e*Y + f
# ─────────────────────────────────────────────────────────────────────────────
TABLE_X21: list[tuple] = [
    #  Y_min  Y_max      a          b          c         d          e          f
    (  2.0,   3.8,   1.14673,    1.7576,   -0.109,   0.84155,   1.5521,   -0.077 ),
    (  3.8,   4.4,   3.38095,  -15.4952,   33.196,   0.78571,   1.7929,   -0.183 ),
    (  4.4,   5.0,   2.5000,    -7.2143,   13.812,   0.82143,   1.5679,    0.119 ),
    (  5.0,   6.4,   0.10100,   16.6350,  -45.469,   0.04985,   9.1613,  -18.557 ),
    (  6.4,   7.0,   3.35714,  -23.5643,   78.466,   0.22619,   7.7369,  -16.656 ),
    (  7.0,   7.7,   0.01191,   21.4750,  -72.870,   0.79762,  -0.7321,   14.610 ),
    (  7.7,   9.0,   0.41858,   16.1558,  -56.040,   0.05794,  10.5156,  -28.240 ),
    (  9.0,  12.0,   0.88779,    7.5527,  -16.600,   0.26665,   6.7015,  -10.810 ),
    ( 12.0,  15.0,   0.76720,   10.7972,  -38.180,   0.20073,   8.4658,  -22.490 ),
    ( 15.0,  18.0,   0.97305,    5.3135,   -2.200,   0.28889,   5.9741,   -4.930 ),
    ( 18.0,  22.0,   0.97256,    5.2500,   -0.980,   0.24504,   7.4160,  -16.730 ),
    ( 22.0,  28.0,   0.91413,    7.4759,  -21.820,   0.20323,   9.1267,  -34.230 ),
    ( 28.0,  40.0,   0.87031,    9.7157,  -50.770,   0.18411,  10.1015,  -46.750 ),
    ( 40.0,  55.0,   0.84703,   12.6752, -133.310,   0.17029,  11.4866,  -80.620 ),
    ( 55.0,  70.0,   0.85921,   11.1009,  -83.190,   0.17130,  11.3680,  -76.940 ),
    ( 70.0, float('inf'), 0.83531, 14.6731, -216.246, 0.16841, 11.8493,  -96.947 ),
]


# ─────────────────────────────────────────────────────────────────────────────
# FUNCIONES AUXILIARES
# ─────────────────────────────────────────────────────────────────────────────

def _redondear_bancario(valor: float) -> int:
    """
    Redondeo bancario (round-half-to-even) según ASTM E29.
    Ejemplo: 116.5 → 116 (par); 117.5 → 118 (par).
    Python's built-in round() ya implementa este comportamiento.
    """
    return round(valor)


def _calcular_iv_desde_l_h(u: float, y: float, L: float, H: float) -> dict:
    """
    Calcula el VI a partir de los valores L, H, U e Y según las ecuaciones
    del numeral 5.2.3, 5.2.4 y 5.2.5 del método.

    Retorna un dict con todos los valores intermedios para trazabilidad.
    """
    resultado = {
        "U": u,
        "Y": y,
        "L": round(L, 4),
        "H": round(H, 4),
        "N": "N/A (U ≥ H)",
        "formula_aplicada": None,
        "iv_exacto": None,
        "iv_final": None,
        "metodo_lh": None,
    }

    if u > H:
        # Ecuación 3: VI = [(L - U) / (L - H)] × 100
        iv_exacto = ((L - u) / (L - H)) * 100
        resultado["formula_aplicada"] = "Ec. 3: VI = [(L - U) / (L - H)] × 100  [aplica cuando U > H]"
        resultado["metodo_lh"] = "U > H → Fórmula directa (Ec. 3)"
    elif u < H:
        # Ecuaciones 6 y 7: N = (log H - log U) / log Y ; VI = [(antilog N - 1) / 0.00715] + 100
        if y <= 1.0:
            raise ValueError("Y debe ser mayor que 1.0 mm²/s para calcular log(Y).")
        N = (math.log10(H) - math.log10(u)) / math.log10(y)
        iv_exacto = ((10**N - 1) / 0.00715) + 100
        resultado["N"] = round(N, 6)
        resultado["formula_aplicada"] = (
            "Ec. 7: N = (log H − log U) / log Y\n"
            "Ec. 6: VI = [(antilog N − 1) / 0.00715] + 100  [aplica cuando U < H]"
        )
        resultado["metodo_lh"] = "U < H → Fórmula logarítmica (Ecs. 6 y 7)"
    else:
        # U == H → VI = 100
        iv_exacto = 100.0
        resultado["formula_aplicada"] = "U = H → VI = 100 exacto (numeral 5.2.5)"
        resultado["metodo_lh"] = "U = H → VI = 100"

    resultado["iv_exacto"] = round(iv_exacto, 4)
    resultado["iv_final"] = _redondear_bancario(iv_exacto)
    return resultado


# ─────────────────────────────────────────────────────────────────────────────
# MÉTODO 1: CÁLCULO COMPUTACIONAL SENCILLO  (Tabla 1 – Interpolación lineal)
# ─────────────────────────────────────────────────────────────────────────────

def calcular_lh_tabla1(y: float) -> dict:
    """
    Obtiene L y H interpolando linealmente en la Tabla 1 del método.
    Válido para 2.0 ≤ Y ≤ 70 mm²/s.

    Retorna dict con L, H y detalles de interpolación para trazabilidad.
    """
    keys = sorted(TABLE_1.keys())
    y_min_tabla = keys[0]
    y_max_tabla = keys[-1]

    if y < y_min_tabla or y > y_max_tabla:
        raise ValueError(
            f"Para el Método Preciso (Tabla 1), Y debe estar entre {y_min_tabla} y "
            f"{y_max_tabla} mm²/s. Valor ingresado: {y}. "
            f"Use el Método (Apéndice X2) para Y > 70 mm²/s."
        )

    # Verificar si el valor está exactamente en la tabla
    y_rounded = round(y, 2)
    if y_rounded in TABLE_1:
        L, H = TABLE_1[y_rounded]
        return {
            "L": L, "H": H,
            "interpolacion": False,
            "y1": y_rounded, "y2": y_rounded,
            "L1": L, "L2": L, "H1": H, "H2": H,
            "detalle": f"Valor Y={y} encontrado exactamente en Tabla 1."
        }

    # Interpolación lineal entre los dos valores más cercanos
    y_inf = max(k for k in keys if k <= y)
    y_sup = min(k for k in keys if k >= y)

    if y_inf == y_sup:
        L, H = TABLE_1[y_inf]
        return {
            "L": L, "H": H,
            "interpolacion": False,
            "y1": y_inf, "y2": y_sup,
            "L1": L, "L2": L, "H1": H, "H2": H,
            "detalle": f"Valor Y={y} coincide con entrada de tabla Y={y_inf}."
        }

    L1, H1 = TABLE_1[y_inf]
    L2, H2 = TABLE_1[y_sup]
    frac = (y - y_inf) / (y_sup - y_inf)
    L = L1 + frac * (L2 - L1)
    H = H1 + frac * (H2 - H1)

    return {
        "L": round(L, 4), "H": round(H, 4),
        "interpolacion": True,
        "y1": y_inf, "y2": y_sup,
        "L1": L1, "L2": L2, "H1": H1, "H2": H2,
        "fraccion": round(frac, 6),
        "detalle": (
            f"Interpolación lineal entre Y={y_inf} (L={L1}, H={H1}) "
            f"y Y={y_sup} (L={L2}, H={H2}). Fracción={round(frac,6)}."
        )
    }


def calcular_iv_sencillo(u: float, y: float) -> dict:
    """
    MÉTODO SENCILLO: Calcula el Índice de Viscosidad usando la Tabla 1
    (interpolación lineal) según ASTM D2270 numerales 5.2.1, 5.2.3, 5.2.4, 5.2.5.

    Parámetros:
        u : Viscosidad cinemática a 40°C del aceite (mm²/s)
        y : Viscosidad cinemática a 100°C del aceite (mm²/s)

    Retorna dict con todos los valores intermedios para trazabilidad y auditoría.
    """
    _validar_entradas(u, y)
    lh = calcular_lh_tabla1(y)
    L, H = lh["L"], lh["H"]
    resultado = _calcular_iv_desde_l_h(u, y, L, H)
    resultado["metodo_calculo"] = "Método Preciso – Tabla 1 (interpolación lineal)"
    resultado["detalle_lh"] = lh["detalle"]
    resultado["interpolacion_usada"] = lh["interpolacion"]
    if lh["interpolacion"]:
        resultado["datos_interpolacion"] = {
            "Y1": lh["y1"], "Y2": lh["y2"],
            "L1": lh["L1"], "L2": lh["L2"],
            "H1": lh["H1"], "H2": lh["H2"],
            "fraccion": lh.get("fraccion", "N/A"),
        }
    return resultado


# ─────────────────────────────────────────────────────────────────────────────
# MÉTODO 2: MÉTODO (APÉNDICE X2)  –  Ecuaciones cuadráticas Tabla X2.1
# ─────────────────────────────────────────────────────────────────────────────

def calcular_lh_x21(y: float) -> dict:
    """
    Calcula L y H usando las ecuaciones cuadráticas de la Tabla X2.1
    (Apéndice X2 del método).
    Válido para 2.0 ≤ Y (sin límite superior definido, usando extrapolación
    de la última fila para Y > 70).

    Retorna dict con L, H y coeficientes usados para trazabilidad.
    """
    for row in TABLE_X21:
        y_min, y_max, a, b, c, d, e, f = row
        if y_min <= y <= y_max or (y_max == float('inf') and y >= y_min):
            L = a * y**2 + b * y + c
            H = d * y**2 + e * y + f
            return {
                "L": round(L, 4), "H": round(H, 4),
                "y_min": y_min, "y_max": y_max,
                "a": a, "b": b, "c": c,
                "d": d, "e": e, "f": f,
                "detalle": (
                    f"Rango Y=[{y_min}, {y_max}], "
                    f"L = {a}·Y² + {b}·Y + ({c}), "
                    f"H = {d}·Y² + {e}·Y + ({f})."
                )
            }
    raise ValueError(f"No se encontró rango en Tabla X2.1 para Y={y}.")


def calcular_iv_preciso(u: float, y: float) -> dict:
    """
    MÉTODO (APÉNDICE X2): Calcula el Índice de Viscosidad usando las
    ecuaciones cuadráticas de la Tabla X2.1.

    Parámetros:
        u : Viscosidad cinemática a 40°C del aceite (mm²/s)
        y : Viscosidad cinemática a 100°C del aceite (mm²/s)

    Retorna dict con todos los valores intermedios para trazabilidad y auditoría.
    """
    _validar_entradas(u, y)
    lh = calcular_lh_x21(y)
    L, H = lh["L"], lh["H"]
    resultado = _calcular_iv_desde_l_h(u, y, L, H)
    resultado["metodo_calculo"] = "Método (Apéndice X2) – ecuaciones cuadráticas, Tabla X2.1"
    resultado["detalle_lh"] = lh["detalle"]
    resultado["coeficientes_usados"] = {
        "Rango Y": f"[{lh['y_min']}, {lh['y_max']}]",
        "a (L)": lh["a"], "b (L)": lh["b"], "c (L)": lh["c"],
        "d (H)": lh["d"], "e (H)": lh["e"], "f (H)": lh["f"],
    }
    return resultado


# ─────────────────────────────────────────────────────────────────────────────
# ALIAS para compatibilidad con app existente
# ─────────────────────────────────────────────────────────────────────────────

def calcular_iv_computacional(u: float, y: float) -> dict:
    """Alias del método (Apéndice X2) para compatibilidad con código existente."""
    return calcular_iv_preciso(u, y)


# ─────────────────────────────────────────────────────────────────────────────
# VALIDACIONES COMUNES
# ─────────────────────────────────────────────────────────────────────────────

def _validar_entradas(u: float, y: float) -> None:
    """Valida los rangos de entrada según la norma ASTM D2270."""
    if y < 2.0:
        raise ValueError(
            f"La viscosidad cinemática a 100°C (Y={y}) es menor a 2.0 mm²/s. "
            "El método no aplica por debajo de este valor (ver numeral 1.2)."
        )
    if u < 0:
        raise ValueError(f"La viscosidad cinemática a 40°C (U={u}) no puede ser negativa.")
    if u < y:
        raise ValueError(
            f"La viscosidad a 40°C (U={u}) no puede ser menor que la viscosidad a 100°C (Y={y}). "
            "Verifique los valores ingresados."
        )
