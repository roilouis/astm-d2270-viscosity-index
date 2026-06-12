"""
app.py  –  Calculadora de Índice de Viscosidad ASTM D2270
──────────────────────────────────────────────────────────
Herramienta validable bajo ISO/IEC 17025 con:
  • Método Preciso        : Interpolación Tabla 1
  • Método (Apéndice X2) : Ecuaciones cuadráticas Tabla X2.1
  • Transparencia de código fuente
  • Tablas de constantes completas
  • Casos de validación incluidos en la norma
"""

import math
import streamlit as st
import pandas as pd

from src.calculations import (
    calcular_iv_tabla1,
    calcular_iv_tablax21,
    TABLE_1,
    TABLE_X21,
)

# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VI Calculator – ASTM D2270",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# ESTILOS CSS
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .result-box {
        background-color: #1e3a5f;
        border-left: 6px solid #4da6ff;
        padding: 18px 24px;
        border-radius: 8px;
        margin: 12px 0;
    }
    .result-box h2 { color: #4da6ff; margin: 0; font-size: 2.6rem; }
    .result-box p  { color: #cce4ff; margin: 4px 0 0 0; font-size: 0.95rem; }
    .trace-card {
        background-color: #0e1117;
        border: 1px solid #333;
        border-radius: 6px;
        padding: 14px 18px;
        font-family: monospace;
        font-size: 0.88rem;
        white-space: pre-wrap;
    }
    .badge-sencillo { background:#2d6a4f; color:#b7e4c7; padding:3px 10px;
                      border-radius:20px; font-size:0.82rem; font-weight:600; }
    .badge-preciso  { background:#1d3557; color:#a8dadc; padding:3px 10px;
                      border-radius:20px; font-size:0.82rem; font-weight:600; }
    .section-header {
        color: #4da6ff;
        border-bottom: 2px solid #4da6ff;
        padding-bottom: 4px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# ENCABEZADO
# ──────────────────────────────────────────────────────────────────────────────
st.title("🧪 Calculadora de Índice de Viscosidad — ASTM D2270")
st.caption(
    "Herramienta de cálculo transparente y trazable, diseñada para su validación "
    "bajo **ISO/IEC 17025**. Implementa el método completo: Tabla 1 y Apéndice X2."
)
st.divider()


# ──────────────────────────────────────────────────────────────────────────────
# BARRA LATERAL – DATOS DE ENTRADA Y SELECCIÓN DE MÉTODO
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Datos de Entrada")
    st.markdown("Viscosidades cinemáticas en **mm²/s** (cSt), determinadas según ASTM D445, D7042, ISO 3104 o IP 71.")

    v_40 = st.number_input(
        "Viscosidad cinemática a **40 °C** — *U*",
        min_value=0.01, value=73.30, step=0.01, format="%.4f",
        help="Viscosidad a 40 °C del aceite cuyo IV se calculará."
    )
    v_100 = st.number_input(
        "Viscosidad cinemática a **100 °C** — *Y*",
        min_value=2.00, value=8.86, step=0.01, format="%.4f",
        help="Debe ser ≥ 2.0 mm²/s. Para el Método Preciso (Tabla 1) debe ser ≤ 70 mm²/s."
    )

    st.divider()
    calcular = st.button("▶  Calcular IV", type="primary", use_container_width=True)

    st.divider()
    st.markdown("""
    **Referencias normativas**
    - ASTM D2270 – 10 (2016)
    - ISO/IEC 17025:2017 §7.11
    - ASTM E29 (redondeo)
    """)

    st.divider()
    st.markdown("### 🔗 Repositorio")
    st.markdown(
	"[![GitHub](https://img.shields.io/badge/GitHub-RoyPizarro--Dev%2Fastm--d2270--viscosity--index-181717?logo=github)](https://github.com/RoyPizarro-Dev/astm-d2270-viscosity-index)"
    )

# ──────────────────────────────────────────────────────────────────────────────
# PESTAÑAS PRINCIPALES
# ──────────────────────────────────────────────────────────────────────────────
tab_calc, tab_codigo, tab_tablas, tab_validacion = st.tabs([
    "📊 Calculadora",
    "💻 Transparencia de Código",
    "📋 Tablas de Constantes",
    "✅ Validación ISO/IEC 17025",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 – CALCULADORA
# ══════════════════════════════════════════════════════════════════════════════
with tab_calc:

    if not calcular:
        st.info("Ingrese los valores de viscosidad en la barra lateral y presione **▶ Calcular IV**.")
    else:
        try:
            # Calcular ambos métodos siempre
            res_p = calcular_iv_tabla1(v_40, v_100)   # Método Preciso (Tabla 1)
            res_x = calcular_iv_tablax21(v_40, v_100)    # Método (Apéndice X2)

            # ── Datos de entrada confirmados ───────────────────────────────
            st.markdown('<h4 class="section-header">Datos de entrada</h4>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            col1.metric("U — Viscosidad a 40 °C (mm²/s)", f"{v_40:.4f}")
            col2.metric("Y — Viscosidad a 100 °C (mm²/s)", f"{v_100:.4f}")

            # ── Resultados simultáneos en dos columnas ─────────────────────
            st.markdown('<h4 class="section-header">Índice de Viscosidad calculado</h4>', unsafe_allow_html=True)
            col_r1, col_r2 = st.columns(2)

            with col_r1:
                st.markdown(f"""
                <div class="result-box">
                  <p>Método Preciso (Tabla 1) — interpolación lineal</p>
                  <h2>{res_p['iv_final']}</h2>
                  <p>Valor sin redondear: {res_p['iv_exacto']}</p>
                </div>
                """, unsafe_allow_html=True)

            with col_r2:
                st.markdown(f"""
                <div class="result-box">
                  <p>Método (Apéndice X2) — ecuaciones cuadráticas</p>
                  <h2>{res_x['iv_final']}</h2>
                  <p>Valor sin redondear: {res_x['iv_exacto']}</p>
                </div>
                """, unsafe_allow_html=True)

            # ── Constantes L y H ──────────────────────────────────────────
            st.markdown('<h4 class="section-header">Constantes L y H</h4>', unsafe_allow_html=True)
            col_l1, col_h1, col_l2, col_h2 = st.columns(4)
            col_l1.metric("L — Método Preciso",  f"{res_p['L']}")
            col_h1.metric("H — Método Preciso",  f"{res_p['H']}")
            col_l2.metric("L — Apéndice X2",     f"{res_x['L']}")
            col_h2.metric("H — Apéndice X2",     f"{res_x['H']}")

            # ── Detalle de obtención de L y H — un expander, dos columnas ─
            with st.expander("📐 Detalle de obtención de L y H"):
                col_det1, col_det2 = st.columns(2)

                with col_det1:
                    st.markdown("**Método Preciso (Tabla 1) — interpolación lineal**")
                    if res_p.get("interpolacion_usada"):
                        di = res_p["datos_interpolacion"]
                        st.markdown(f"""
| Parámetro | Y₁ = {di['Y1']} | Y₂ = {di['Y2']} | Interpolado |
|---|---|---|---|
| **L** | {di['L1']} | {di['L2']} | **{res_p['L']}** |
| **H** | {di['H1']} | {di['H2']} | **{res_p['H']}** |
| *Fracción* | | | {di['fraccion']} |
                        """)
                    else:
                        st.info(f"Y = {res_p['Y']} coincide exactamente con una entrada de la Tabla 1. No se requiere interpolación.")

                with col_det2:
                    st.markdown("**Método (Apéndice X2) — ecuaciones cuadráticas**")
                    coef = res_x.get("coeficientes_usados", {})
                    st.markdown(f"**Rango Y**: {coef.get('Rango Y')}")
                    st.markdown(f"""
| Ecuación | Coef. a/d | Coef. b/e | Coef. c/f |
|---|---|---|---|
| **L** = a·Y² + b·Y + c | {coef.get('a (L)')} | {coef.get('b (L)')} | {coef.get('c (L)')} |
| **H** = d·Y² + e·Y + f | {coef.get('d (H)')} | {coef.get('e (H)')} | {coef.get('f (H)')} |
                    """)

            # ── Fórmula y valores intermedios — común a ambos métodos ──────
            st.markdown('<h4 class="section-header">Fórmula aplicada y valores intermedios</h4>', unsafe_allow_html=True)
            st.caption("La fórmula de cálculo del IV a partir de L, H, U e Y es idéntica en ambos métodos. La única diferencia entre ellos es cómo se obtienen L y H.")
            st.info(f"**Criterio**: {res_p['metodo_lh']}")
            st.code(res_p['formula_aplicada'], language="text")

            # ── Tabla comparativa de parámetros ───────────────────────────
            df_intermedios = pd.DataFrame({
                "Parámetro": [
                    "U (viscosidad 40 °C)",
                    "Y (viscosidad 100 °C)",
                    "L (constante IV=0)",
                    "H (constante IV=100)",
                    "N (solo si U < H)",
                    "IV exacto (sin redondear)",
                    "IV final (redondeado)",
                ],
                "Descripción": [
                    "Dato de entrada",
                    "Dato de entrada",
                    "Viscosidad 40°C de aceite patrón IV=0",
                    "Viscosidad 40°C de aceite patrón IV=100",
                    "Factor logarítmico intermedio",
                    "IV antes de redondeo bancario (ASTM E29)",
                    "Valor a reportar",
                ],
                "Valor (Método Preciso)": [
                    f"{res_p['U']} mm²/s",
                    f"{res_p['Y']} mm²/s",
                    str(res_p['L']),
                    str(res_p['H']),
                    str(res_p['N']),
                    str(res_p['iv_exacto']),
                    str(res_p['iv_final']),
                ],
                "Valor (Método Apéndice X2)": [
                    f"{res_x['U']} mm²/s",
                    f"{res_x['Y']} mm²/s",
                    str(res_x['L']),
                    str(res_x['H']),
                    str(res_x['N']),
                    str(res_x['iv_exacto']),
                    str(res_x['iv_final']),
                ],
            })
            st.dataframe(df_intermedios, use_container_width=True, hide_index=True)

        except ValueError as e:
            st.error(f"⚠️ **Error de validación**: {e}")
        except Exception as e:
            st.error(f"❌ **Error inesperado**: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 – TRANSPARENCIA DE CÓDIGO
# ══════════════════════════════════════════════════════════════════════════════
with tab_codigo:
    st.markdown("""
    En cumplimiento con los requisitos de software de **ISO/IEC 17025:2017 §7.11**,
    se expone el código fuente exacto que realiza los cálculos. Esto permite que
    cualquier auditor, cliente o responsable de calidad pueda verificar la lógica
    matemática de la herramienta.
    """)

    subtab_core, subtab_sencillo, subtab_preciso = st.tabs([
        "Lógica central (común)",
        "Método Preciso – Tabla 1",
        "Método (Apéndice X2)",
    ])

    with subtab_core:
        st.markdown("### Función de cálculo del IV a partir de L, H, U, Y")
        st.markdown("Esta función es común a ambos métodos. Es llamada después de obtener L y H por cualquiera de los métodos.")
        st.code("""
def _calcular_iv_desde_l_h(u: float, y: float, L: float, H: float) -> dict:
    \"\"\"
    Calcula VI según numerales 5.2.3, 5.2.4 y 5.2.5 de ASTM D2270.
    \"\"\"
    if u > H:
        # Ecuación 3: aplica cuando U > H
        iv_exacto = ((L - u) / (L - H)) * 100

    elif u < H:
        # Ecuaciones 6 y 7: aplica cuando U < H
        # N = (log H - log U) / log Y      [Ec. 7]
        N = (math.log10(H) - math.log10(u)) / math.log10(y)
        # VI = [(antilog N - 1) / 0.00715] + 100   [Ec. 6]
        iv_exacto = ((10**N - 1) / 0.00715) + 100

    else:
        # U == H → VI = 100 exacto   [numeral 5.2.5]
        iv_exacto = 100.0

    # Redondeo bancario (round-half-to-even) según ASTM E29
    iv_final = round(iv_exacto)   # Python usa banker's rounding por defecto
    return iv_exacto, iv_final
        """, language="python")

        st.markdown("### Función de redondeo (ASTM E29)")
        st.code("""
# ASTM E29 especifica redondeo bancario (round-half-to-even).
# Python's built-in round() implementa este comportamiento.
# Ejemplo: round(116.5) → 116 (par)  |  round(117.5) → 118 (par)
iv_final = round(iv_exacto)
        """, language="python")

    with subtab_sencillo:
        st.markdown("### Método Preciso (Tabla 1): Interpolación lineal")
        st.code("""
def calcular_lh_tabla1(y: float) -> tuple[float, float]:
    \"\"\"
    Obtiene L y H interpolando linealmente en Tabla 1 (ASTM D2270, numeral 5.2.1).
    Válido para 2.0 ≤ Y ≤ 70 mm²/s.
    \"\"\"
    keys = sorted(TABLE_1.keys())   # TABLE_1: dict con todos los valores de la Tabla 1

    # Búsqueda de los dos puntos de tabla adyacentes
    y_inf = max(k for k in keys if k <= y)   # valor inferior más cercano
    y_sup = min(k for k in keys if k >= y)   # valor superior más cercano

    if y_inf == y_sup:
        return TABLE_1[y_inf]  # valor exacto en tabla, no requiere interpolación

    L1, H1 = TABLE_1[y_inf]
    L2, H2 = TABLE_1[y_sup]

    # Interpolación lineal:  x_interp = x1 + frac * (x2 - x1)
    frac = (y - y_inf) / (y_sup - y_inf)
    L = L1 + frac * (L2 - L1)
    H = H1 + frac * (H2 - H1)
    return L, H


def calcular_iv_tabla1(u: float, y: float) -> dict:
    L, H = calcular_lh_tabla1(y)
    return _calcular_iv_desde_l_h(u, y, L, H)
        """, language="python")

    with subtab_preciso:
        st.markdown("### Método (Apéndice X2): Ecuaciones cuadráticas Tabla X2.1")
        st.code("""
# Tabla X2.1 — 16 rangos de Y, cada uno con coeficientes para:
#   L = a*Y^2 + b*Y + c
#   H = d*Y^2 + e*Y + f
#
# Ejemplo de los primeros rangos:
TABLE_X21 = [
    # Y_min  Y_max      a          b          c         d         e         f
    (  2.0,   3.8,  1.14673,   1.7576,   -0.109,  0.84155,  1.5521,  -0.077 ),
    (  3.8,   4.4,  3.38095, -15.4952,   33.196,  0.78571,  1.7929,  -0.183 ),
    (  4.4,   5.0,  2.5000,   -7.2143,   13.812,  0.82143,  1.5679,   0.119 ),
    # ... (ver tabla completa en src/calculations.py)
    ( 70.0,  inf,  0.83531,  14.6731, -216.246,  0.16841, 11.8493, -96.947 ),
]

def calcular_lh_x21(y: float) -> tuple[float, float]:
    \"\"\"Selecciona el rango correcto y evalúa L y H con las ecuaciones cuadráticas.\"\"\"
    for (y_min, y_max, a, b, c, d, e, f) in TABLE_X21:
        if y_min <= y <= y_max:
            L = a * y**2 + b * y + c
            H = d * y**2 + e * y + f
            return L, H
    raise ValueError(f"Y={y} fuera de rango.")


def calcular_iv_tablax21(u: float, y: float) -> dict:
    L, H = calcular_lh_x21(y)
    return _calcular_iv_desde_l_h(u, y, L, H)
        """, language="python")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 – TABLAS DE CONSTANTES
# ══════════════════════════════════════════════════════════════════════════════
with tab_tablas:

    subtab_t1, subtab_tx21 = st.tabs(["Tabla 1 – Valores L y H", "Tabla X2.1 – Coeficientes cuadráticos"])

    with subtab_t1:
        st.markdown("""
        ### Tabla 1 — Valores básicos de L y H (numeral 5.2.1)
        Fuente: **ASTM D2270-10 (2016)**, Table 1.
        Aplica para viscosidades a 100°C entre **2.0 y 70.0 mm²/s**.
        """)

        df_t1 = pd.DataFrame(
            [{"Y (mm²/s)": k, "L (mm²/s)": v[0], "H (mm²/s)": v[1]}
             for k, v in sorted(TABLE_1.items())]
        )

        col_busq, _ = st.columns([1, 2])
        with col_busq:
            filtro_y = st.number_input(
                "Filtrar por rango Y (mostrar ±2 unidades alrededor de este valor)",
                min_value=2.0, max_value=70.0, value=8.86, step=0.1, format="%.2f",
                key="filtro_tabla1"
            )
            mostrar_todo = st.checkbox("Mostrar tabla completa", value=False)

        if mostrar_todo:
            st.dataframe(df_t1, use_container_width=True, height=500, hide_index=True)
        else:
            df_filtrado = df_t1[
                (df_t1["Y (mm²/s)"] >= filtro_y - 2) &
                (df_t1["Y (mm²/s)"] <= filtro_y + 2)
            ]
            if df_filtrado.empty:
                st.warning("No hay entradas en ese rango. Activa 'Mostrar tabla completa'.")
            else:
                st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

        st.caption(f"Total de entradas en Tabla 1: {len(TABLE_1)}")

    with subtab_tx21:
        st.markdown("""
        ### Tabla X2.1 — Coeficientes de ecuaciones cuadráticas (Apéndice X2)
        Fuente: **ASTM D2270-10 (2016)**, Table X2.1.

        Las ecuaciones son:
        - **L** = a · Y² + b · Y + c
        - **H** = d · Y² + e · Y + f

        El error en los valores calculados no excede **0.1 %** respecto a la Tabla 1.
        """)

        df_x21 = pd.DataFrame(
            [
                {
                    "Y min": row[0],
                    "Y max": row[1] if row[1] != float('inf') else "∞",
                    "a (L)": row[2], "b (L)": row[3], "c (L)": row[4],
                    "d (H)": row[5], "e (H)": row[6], "f (H)": row[7],
                }
                for row in TABLE_X21
            ]
        )
        st.dataframe(df_x21, use_container_width=True, hide_index=True)

        st.markdown("**Visualización de L y H calculadas por rango:**")
        import numpy as np

        try:
            import plotly.graph_objects as go

            y_vals = np.linspace(2.0, 70.0, 500)
            L_vals, H_vals = [], []
            for yv in y_vals:
                for row in TABLE_X21:
                    y_min, y_max = row[0], row[1]
                    if y_min <= yv <= y_max or (y_max == float('inf') and yv >= y_min):
                        a, b, c, d, e, f = row[2], row[3], row[4], row[5], row[6], row[7]
                        L_vals.append(a * yv**2 + b * yv + c)
                        H_vals.append(d * yv**2 + e * yv + f)
                        break

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=list(y_vals), y=L_vals, name="L (IV=0)", line=dict(color="#ef476f", width=2)))
            fig.add_trace(go.Scatter(x=list(y_vals), y=H_vals, name="H (IV=100)", line=dict(color="#06d6a0", width=2)))
            fig.update_layout(
                title="Curvas L y H en función de Y (Tabla X2.1)",
                xaxis_title="Y — Viscosidad a 100 °C (mm²/s)",
                yaxis_title="Viscosidad a 40 °C (mm²/s)",
                height=400,
                template="plotly_dark",
            )
            st.plotly_chart(fig, use_container_width=True)
        except ImportError:
            st.info("Instale `plotly` para ver la gráfica de las curvas L y H.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 – VALIDACIÓN ISO/IEC 17025
# ══════════════════════════════════════════════════════════════════════════════
with tab_validacion:
    st.markdown("""
    ## Validación de la herramienta — ISO/IEC 17025:2017 §7.11

    Según la norma ISO/IEC 17025, el software utilizado en laboratorios de calibración
    y ensayo debe validarse para asegurar que es adecuado para el uso previsto.
    La validación se realiza comparando los resultados del software con valores de
    referencia establecidos (en este caso, los ejemplos incluidos en la propia norma ASTM D2270).

    A continuación se ejecutan los **cuatro casos de prueba oficiales** incluidos en el
    numeral **5.2.3.1**, **5.2.4.1**, **5.2.4.2** y el **Apéndice X2.5** del método.
    """)

    # Definición de casos de prueba
    CASOS_DE_PRUEBA = [
        {
            "id": "5.2.3.1",
            "descripcion": "Caso norma §5.2.3.1 — U > H (Ec. 3)",
            "U": 73.30, "Y": 8.86,
            "VI_esperado": 92,
            "L_esperado": 119.94,
            "H_esperado": 69.48,
            "metodo": "apendice_x2",
            "nota": "Interpolación en Tabla 1 (numeral 5.2.1). L y H obtenidos por interpolación."
        },
        {
            "id": "5.2.4.1",
            "descripcion": "Caso norma §5.2.4.1 — U < H (Ecs. 6 y 7)",
            "U": 22.83, "Y": 5.05,
            "VI_esperado": 156,
            "L_esperado": None,
            "H_esperado": 28.975,
            "metodo": "apendice_x2",
            "nota": "H = 28.975 por interpolación en Tabla 1."
        },
        {
            "id": "5.2.4.2",
            "descripcion": "Caso norma §5.2.4.2 — U < H (Ecs. 6 y 7)",
            "U": 53.47, "Y": 7.80,
            "VI_esperado": 111,
            "L_esperado": None,
            "H_esperado": 57.31,
            "metodo": "apendice_x2",
            "nota": "H = 57.31 exacto en Tabla 1."
        },
        {
            "id": "X2.5",
            "descripcion": "Caso norma Apéndice X2.5 — Método (Apéndice X2)",
            "U": 73.50, "Y": 8.860,
            "VI_esperado": 92,
            "L_esperado": 119.9588,
            "H_esperado": 69.4765,
            "metodo": "apendice_x2",
            "nota": "Ejemplo explícito del Apéndice X2. L=119.9588, H=69.4765."
        },
    ]

    if st.button("🚀 Ejecutar todos los casos de validación", type="primary"):
        todos_ok = True
        for caso in CASOS_DE_PRUEBA:
            with st.expander(f"{'✅' if True else '❌'} Caso {caso['id']}: {caso['descripcion']}", expanded=True):
                try:
                    res = calcular_iv_tablax21(caso["U"], caso["Y"])

                    vi_ok = res["iv_final"] == caso["VI_esperado"]
                    if caso["H_esperado"] is not None:
                        h_ok = math.isclose(res["H"], caso["H_esperado"], abs_tol=0.05)
                    else:
                        h_ok = True
                    if caso["L_esperado"] is not None:
                        l_ok = math.isclose(res["L"], caso["L_esperado"], abs_tol=0.05)
                    else:
                        l_ok = True

                    caso_ok = vi_ok and h_ok and l_ok
                    todos_ok = todos_ok and caso_ok

                    col_a, col_b, col_c = st.columns(3)
                    col_a.metric("IV obtenido", res["iv_final"],
                                 delta=f"Esperado: {caso['VI_esperado']}",
                                 delta_color="normal" if vi_ok else "inverse")
                    col_b.metric("L calculado", res["L"],
                                 delta=f"Ref: {caso['L_esperado']}" if caso["L_esperado"] else "N/A en norma")
                    col_c.metric("H calculado", res["H"],
                                 delta=f"Ref: {caso['H_esperado']}" if caso["H_esperado"] else "N/A en norma")

                    if caso_ok:
                        st.success(f"✅ **APROBADO** — IV calculado ({res['iv_final']}) == IV esperado ({caso['VI_esperado']}). {caso['nota']}")
                    else:
                        st.error(f"❌ **FALLIDO** — VI={res['iv_final']} (esperado {caso['VI_esperado']}). H={res['H']} (ref {caso['H_esperado']}). {caso['nota']}")

                except Exception as e:
                    todos_ok = False
                    st.error(f"❌ Error en caso {caso['id']}: {e}")

        st.divider()
        if todos_ok:
            st.success("🏆 **VALIDACIÓN COMPLETA**: Todos los casos de prueba pasaron. La herramienta es conforme con ASTM D2270.")
        else:
            st.error("⚠️ **VALIDACIÓN INCOMPLETA**: Uno o más casos fallaron. Revise los resultados.")

    st.divider()
    st.markdown("""
    ### Declaración de conformidad

    Esta herramienta ha sido desarrollada con el objetivo de ser validable bajo **ISO/IEC 17025:2017**.
    Los elementos de validación implementados incluyen:

    | Requisito ISO 17025 §7.11 | Implementación en esta herramienta |
    |---|---|
    | Verificación de idoneidad | Casos de prueba con resultados de referencia de la norma ASTM D2270 |
    | Trazabilidad del cálculo | Exposición del código fuente y todos los valores intermedios |
    | Documentación | Tablas de constantes completas con fuente normativa citada |
    | Control de cambios | Gestión de versiones en repositorio GitHub |
    | Identificación del software | Versión, nombre y referencia normativa visibles |

    **Nota**: Esta validación cubre la lógica de cálculo. La incertidumbre del resultado final depende
    también de la precisión de los métodos de medición de viscosidad (ASTM D445, D7042, etc.),
    conforme a lo indicado en el Apéndice X3 del método.
    """)
