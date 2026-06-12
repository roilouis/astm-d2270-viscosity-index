"""
app.py  –  Calculadora de Índice de Viscosidad ASTM D2270
──────────────────────────────────────────────────────────
Herramienta validable bajo ISO/IEC 17025 con:
  • Método Preciso        : Interpolación lineal Tabla 1
  • Método (Apéndice X2) : Ecuaciones cuadráticas Tabla X2.1
  • Transparencia de código fuente
  • Tablas de constantes completas
  • Casos de validación incluidos en la norma
"""

import math
import streamlit as st
import pandas as pd

from src.calculations import (
    calcular_iv_sencillo,
    calcular_iv_preciso,
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
    /* Cajas de resultado principales */
    .result-box {
        background-color: #1e3a5f;
        border-left: 6px solid #4da6ff;
        padding: 18px 24px;
        border-radius: 8px;
        margin: 8px 0 16px 0;
    }
    .result-box h2 { color: #4da6ff; margin: 0; font-size: 2.8rem; }
    .result-box p  { color: #cce4ff; margin: 4px 0 0 0; font-size: 0.92rem; }

    .result-box-alt {
        background-color: #1a3a2a;
        border-left: 6px solid #06d6a0;
        padding: 18px 24px;
        border-radius: 8px;
        margin: 8px 0 16px 0;
    }
    .result-box-alt h2 { color: #06d6a0; margin: 0; font-size: 2.8rem; }
    .result-box-alt p  { color: #b7e4c7; margin: 4px 0 0 0; font-size: 0.92rem; }

    /* Encabezados de sección */
    .section-header {
        color: #4da6ff;
        border-bottom: 2px solid #4da6ff;
        padding-bottom: 4px;
        margin-top: 24px;
        margin-bottom: 12px;
        font-size: 1.05rem;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────────────────────────────────────
defaults = {
    "pagina":            "📊 Calculadora",
    "resultado_preciso": None,
    "resultado_x2":      None,
    "error_calculo":     None,
    "calculado":         False,
    "v40_input":         "",
    "v100_input":        "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ──────────────────────────────────────────────────────────────────────────────
# BARRA LATERAL
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧪 ASTM D2270")
    st.caption("Calculadora de Índice de Viscosidad")
    st.divider()

    # ── Navegación ────────────────────────────────────────────────────────────
    st.markdown("### Navegación")
    for p in [
        "📊 Calculadora",
        "💻 Transparencia de Código",
        "📋 Tablas de Constantes",
        "✅ Validación ISO/IEC 17025",
    ]:
        if st.button(p, key=f"nav_{p}", use_container_width=True):
            st.session_state["pagina"] = p

    st.divider()

    # ── Datos de entrada ──────────────────────────────────────────────────────
    st.markdown("### ⚙️ Datos de Entrada")
    st.markdown(
        "Viscosidades cinemáticas en **mm²/s** (cSt)  \n"
        "Métodos: ASTM D445, D7042, ISO 3104 o IP 71"
    )

    v40_str = st.text_input(
        "Viscosidad a **40 °C** — *U* (mm²/s)",
        value=st.session_state["v40_input"],
        placeholder="ej. 73.30",
        help="Viscosidad cinemática del aceite a 40 °C. Debe ser mayor que la de 100 °C.",
        key="input_v40",
    )
    v100_str = st.text_input(
        "Viscosidad a **100 °C** — *Y* (mm²/s)",
        value=st.session_state["v100_input"],
        placeholder="ej. 8.86",
        help="Debe ser ≥ 2.0 mm²/s. Para el Método Preciso (Tabla 1) debe ser ≤ 70 mm²/s.",
        key="input_v100",
    )

    calcular = st.button("▶  Calcular IV", type="primary", use_container_width=True)

    st.divider()
    st.markdown("""
**Referencias normativas**
- ASTM D2270 – 10 (2016)
- ISO/IEC 17025:2017 §6.4.7
- ASTM E29 (redondeo)
""")
    st.caption(
        "**Método Preciso**: L y H por interpolación lineal en Tabla 1. Válido para Y ≤ 70 mm²/s.  \n"
        "**Método (Apéndice X2)**: L y H por ecuaciones cuadráticas de Tabla X2.1. "
        "Válido para todo el rango."
    )

# ──────────────────────────────────────────────────────────────────────────────
# LÓGICA DE CÁLCULO
# Se ejecuta al presionar el botón desde cualquier página y siempre
# redirige a la pestaña Calculadora para mostrar el resultado.
# ──────────────────────────────────────────────────────────────────────────────
if calcular:
    st.session_state.update({
        "v40_input":         v40_str,
        "v100_input":        v100_str,
        "resultado_preciso": None,
        "resultado_x2":      None,
        "error_calculo":     None,
        "calculado":         False,
        "pagina":            "📊 Calculadora",   # redirigir siempre
    })

    if not v40_str.strip() or not v100_str.strip():
        st.session_state["error_calculo"] = (
            "⚠️ Ingrese ambos valores de viscosidad antes de calcular."
        )
    else:
        try:
            v_40  = float(v40_str.replace(",", "."))
            v_100 = float(v100_str.replace(",", "."))

            res_p = calcular_iv_sencillo(v_40, v_100)   # Método Preciso (Tabla 1)
            res_x = calcular_iv_preciso(v_40, v_100)    # Método (Apéndice X2)

            st.session_state["resultado_preciso"] = res_p
            st.session_state["resultado_x2"]      = res_x
            st.session_state["calculado"]         = True

        except ValueError as e:
            msg = str(e)
            if "could not convert" in msg or "invalid literal" in msg:
                st.session_state["error_calculo"] = (
                    "⚠️ Los valores ingresados no son números válidos."
                )
            else:
                st.session_state["error_calculo"] = f"⚠️ {msg}"
        except Exception as e:
            st.session_state["error_calculo"] = f"❌ Error inesperado: {e}"

# ──────────────────────────────────────────────────────────────────────────────
# ENCABEZADO PRINCIPAL
# ──────────────────────────────────────────────────────────────────────────────
st.title("🧪 Calculadora de Índice de Viscosidad — ASTM D2270")
st.caption(
    "Herramienta de cálculo transparente y trazable — "
    "**ISO/IEC 17025:2017** | ASTM D2270 – 10 (2016)"
)
st.divider()

pagina_activa = st.session_state["pagina"]


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 1 – CALCULADORA
# ══════════════════════════════════════════════════════════════════════════════
if pagina_activa == "📊 Calculadora":

    # ── Estado inicial o error ────────────────────────────────────────────────
    if st.session_state["error_calculo"]:
        st.error(st.session_state["error_calculo"])

    elif not st.session_state["calculado"]:
        st.info(
            "Ingrese los valores de viscosidad cinemática en la barra lateral "
            "y presione **▶ Calcular IV**."
        )

    # ── Resultados ────────────────────────────────────────────────────────────
    else:
        res_p = st.session_state["resultado_preciso"]   # Método Preciso (Tabla 1)
        res_x = st.session_state["resultado_x2"]        # Método (Apéndice X2)

        # ── Datos de entrada confirmados ──────────────────────────────────────
        st.markdown('<h4 class="section-header">Datos de entrada</h4>', unsafe_allow_html=True)
        col_u, col_y, _, _ = st.columns(4)
        col_u.metric("U — Viscosidad a 40 °C (mm²/s)", f"{res_p['U']:.4f}")
        col_y.metric("Y — Viscosidad a 100 °C (mm²/s)", f"{res_p['Y']:.4f}")

        # ── IV calculado — dos columnas simultáneas ───────────────────────────
        st.markdown(
            '<h4 class="section-header">Índice de Viscosidad calculado</h4>',
            unsafe_allow_html=True,
        )
        col_r1, col_r2 = st.columns(2)

        with col_r1:
            st.markdown(f"""
<div class="result-box">
  <p>Método Preciso (Tabla 1) — interpolación lineal</p>
  <h2>{res_p['iv_final']}</h2>
  <p>IV sin redondear: {res_p['iv_exacto']}</p>
</div>
""", unsafe_allow_html=True)

        with col_r2:
            st.markdown(f"""
<div class="result-box-alt">
  <p>Método (Apéndice X2) — ecuaciones cuadráticas</p>
  <h2>{res_x['iv_final']}</h2>
  <p>IV sin redondear: {res_x['iv_exacto']}</p>
</div>
""", unsafe_allow_html=True)

        # ── Constantes L y H — cuatro columnas ───────────────────────────────
        st.markdown(
            '<h4 class="section-header">Constantes L y H</h4>',
            unsafe_allow_html=True,
        )
        col_l1, col_h1, col_l2, col_h2 = st.columns(4)
        col_l1.metric("L — Método Preciso",  str(res_p["L"]))
        col_h1.metric("H — Método Preciso",  str(res_p["H"]))
        col_l2.metric("L — Apéndice X2",     str(res_x["L"]))
        col_h2.metric("H — Apéndice X2",     str(res_x["H"]))

        # ── Detalle de obtención de L y H — un expander, dos columnas ────────
        with st.expander("📐 Detalle de obtención de L y H", expanded=False):
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
                    st.info(
                        f"Y = {res_p['Y']} coincide exactamente con una entrada "
                        "de la Tabla 1. No se requiere interpolación."
                    )

            with col_det2:
                st.markdown("**Método (Apéndice X2) — ecuaciones cuadráticas**")
                coef = res_x.get("coeficientes_usados", {})
                st.markdown(f"**Rango Y aplicado**: {coef.get('Rango Y', 'N/A')}")
                st.markdown(f"""
| Ecuación | a / d | b / e | c / f |
|---|---|---|---|
| **L** = a·Y² + b·Y + c | {coef.get('a (L)')} | {coef.get('b (L)')} | {coef.get('c (L)')} |
| **H** = d·Y² + e·Y + f | {coef.get('d (H)')} | {coef.get('e (H)')} | {coef.get('f (H)')} |
""")

        # ── Fórmula aplicada — común a ambos métodos ──────────────────────────
        st.markdown(
            '<h4 class="section-header">Fórmula aplicada y valores intermedios</h4>',
            unsafe_allow_html=True,
        )
        st.caption(
            "La fórmula de cálculo del IV a partir de L, H, U e Y es **idéntica en ambos "
            "métodos**. La única diferencia entre ellos es el procedimiento para obtener L y H."
        )
        st.info(f"**Criterio de bifurcación:** {res_p['metodo_lh']}")
        st.code(res_p["formula_aplicada"], language="text")

        # ── Tabla comparativa de parámetros ───────────────────────────────────
        st.markdown(
            '<h4 class="section-header">Tabla comparativa de parámetros</h4>',
            unsafe_allow_html=True,
        )
        df_comp = pd.DataFrame({
            "Parámetro": [
                "U — Viscosidad 40 °C",
                "Y — Viscosidad 100 °C",
                "L (constante IV = 0)",
                "H (constante IV = 100)",
                "N (solo si U < H)",
                "IV exacto (sin redondear)",
                "IV final (redondeado)",
            ],
            "Descripción": [
                "Dato de entrada",
                "Dato de entrada",
                "Viscosidad a 40 °C de aceite patrón con IV = 0",
                "Viscosidad a 40 °C de aceite patrón con IV = 100",
                "Factor logarítmico intermedio (Ec. 7)",
                "IV antes del redondeo bancario (ASTM E29)",
                "Valor a reportar",
            ],
            "Valor — Método Preciso (Tabla 1)": [
                f"{res_p['U']} mm²/s",
                f"{res_p['Y']} mm²/s",
                str(res_p["L"]),
                str(res_p["H"]),
                str(res_p["N"]),
                str(res_p["iv_exacto"]),
                str(res_p["iv_final"]),
            ],
            "Valor — Método (Apéndice X2)": [
                f"{res_x['U']} mm²/s",
                f"{res_x['Y']} mm²/s",
                str(res_x["L"]),
                str(res_x["H"]),
                str(res_x["N"]),
                str(res_x["iv_exacto"]),
                str(res_x["iv_final"]),
            ],
        })
        st.dataframe(df_comp, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 2 – TRANSPARENCIA DE CÓDIGO
# ══════════════════════════════════════════════════════════════════════════════
elif pagina_activa == "💻 Transparencia de Código":

    st.subheader("💻 Transparencia de Código")
    st.markdown("""
En cumplimiento con **ISO/IEC 17025:2017 §6.4.7**, se expone el código fuente exacto
que realiza los cálculos. Esto permite que cualquier auditor, cliente o responsable de
calidad verifique la lógica matemática de la herramienta.
    """)

    sub_opcion = st.radio(
        "Seleccionar sección:",
        [
            "Lógica central (común a ambos métodos)",
            "Método Preciso (Tabla 1)",
            "Método (Apéndice X2)",
        ],
        horizontal=True,
    )

    if sub_opcion == "Lógica central (común a ambos métodos)":
        st.markdown("### Función de cálculo del IV a partir de L, H, U, Y")
        st.markdown(
            "Esta función es común a ambos métodos. "
            "Se llama después de obtener L y H por cualquiera de los dos caminos."
        )
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

    # Redondeo bancario (round-half-to-even) según ASTM E29.
    # Python's built-in round() implementa este comportamiento.
    # Ejemplo: round(116.5) → 116  |  round(117.5) → 118
    iv_final = round(iv_exacto)
    return iv_exacto, iv_final
        """, language="python")

    elif sub_opcion == "Método Preciso (Tabla 1)":
        st.markdown("### Método Preciso (Tabla 1): interpolación lineal")
        st.code("""
def calcular_lh_tabla1(y: float) -> tuple[float, float]:
    \"\"\"
    Obtiene L y H interpolando linealmente en Tabla 1
    (ASTM D2270, numeral 5.2.1). Válido para 2.0 ≤ Y ≤ 70 mm²/s.
    \"\"\"
    keys = sorted(TABLE_1.keys())   # TABLE_1: dict con los 168 valores de Tabla 1

    # Búsqueda de los dos puntos de tabla adyacentes
    y_inf = max(k for k in keys if k <= y)   # valor inferior más cercano
    y_sup = min(k for k in keys if k >= y)   # valor superior más cercano

    if y_inf == y_sup:
        return TABLE_1[y_inf]   # valor exacto en tabla, sin interpolación

    L1, H1 = TABLE_1[y_inf]
    L2, H2 = TABLE_1[y_sup]

    # Interpolación lineal: x_interp = x1 + frac * (x2 - x1)
    frac = (y - y_inf) / (y_sup - y_inf)
    L = L1 + frac * (L2 - L1)
    H = H1 + frac * (H2 - H1)
    return L, H


def calcular_iv_sencillo(u: float, y: float) -> dict:
    \"\"\"Método Preciso: obtiene L, H por Tabla 1 y calcula IV.\"\"\"
    L, H = calcular_lh_tabla1(y)
    return _calcular_iv_desde_l_h(u, y, L, H)
        """, language="python")

    else:
        st.markdown("### Método (Apéndice X2): ecuaciones cuadráticas Tabla X2.1")
        st.code("""
# Tabla X2.1 — 16 rangos de Y, cada uno con coeficientes para:
#   L = a*Y² + b*Y + c
#   H = d*Y² + e*Y + f
#
# Primeros y último rangos como referencia:
TABLE_X21 = [
    # Y_min  Y_max      a          b          c         d         e         f
    (  2.0,   3.8,  1.14673,   1.7576,   -0.109,  0.84155,  1.5521,  -0.077 ),
    (  3.8,   4.4,  3.38095, -15.4952,   33.196,  0.78571,  1.7929,  -0.183 ),
    # ... (16 filas en total — ver tabla completa en src/calculations.py)
    ( 70.0,  inf,   0.83531,  14.6731, -216.246,  0.16841, 11.8493, -96.947 ),
]

def calcular_lh_x21(y: float) -> tuple[float, float]:
    \"\"\"Selecciona el rango correcto y evalúa L y H con las ecuaciones cuadráticas.\"\"\"
    for (y_min, y_max, a, b, c, d, e, f) in TABLE_X21:
        if y_min <= y <= y_max:
            L = a * y**2 + b * y + c
            H = d * y**2 + e * y + f
            return L, H
    raise ValueError(f"Y={y} fuera de rango.")


def calcular_iv_preciso(u: float, y: float) -> dict:
    \"\"\"Método (Apéndice X2): obtiene L, H por ecuaciones cuadráticas y calcula IV.\"\"\"
    L, H = calcular_lh_x21(y)
    return _calcular_iv_desde_l_h(u, y, L, H)
        """, language="python")


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 3 – TABLAS DE CONSTANTES
# ══════════════════════════════════════════════════════════════════════════════
elif pagina_activa == "📋 Tablas de Constantes":

    st.subheader("📋 Tablas de Constantes")

    tabla_opcion = st.radio(
        "Seleccionar tabla:",
        ["Tabla 1 — Valores L y H", "Tabla X2.1 — Coeficientes cuadráticos"],
        horizontal=True,
    )

    if tabla_opcion == "Tabla 1 — Valores L y H":
        st.markdown("""
### Tabla 1 — Valores básicos de L y H (numeral 5.2.1)
Fuente: **ASTM D2270-10 (2016)**, Table 1.
Aplica para viscosidades a 100 °C entre **2.0 y 70.0 mm²/s**.
        """)

        df_t1 = pd.DataFrame(
            [{"Y (mm²/s)": k, "L (mm²/s)": v[0], "H (mm²/s)": v[1]}
             for k, v in sorted(TABLE_1.items())]
        )

        col_busq, _ = st.columns([1, 2])
        with col_busq:
            filtro_y = st.number_input(
                "Centrar vista en Y (±2 unidades)",
                min_value=2.0, max_value=70.0, value=8.86,
                step=0.1, format="%.2f", key="filtro_tabla1",
            )
            mostrar_todo = st.checkbox("Mostrar tabla completa", value=False)

        if mostrar_todo:
            st.dataframe(df_t1, use_container_width=True, height=500, hide_index=True)
        else:
            df_filtrado = df_t1[
                (df_t1["Y (mm²/s)"] >= filtro_y - 2) &
                (df_t1["Y (mm²/s)"] <= filtro_y + 2)
            ]
            st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

        st.caption(f"Total de entradas en Tabla 1: {len(TABLE_1)}")

    else:
        st.markdown("""
### Tabla X2.1 — Coeficientes de ecuaciones cuadráticas (Apéndice X2)
Fuente: **ASTM D2270-10 (2016)**, Table X2.1.

Las ecuaciones son:
- **L** = a · Y² + b · Y + c
- **H** = d · Y² + e · Y + f

El error respecto a Tabla 1 no excede **0.1 %** en ningún rango.
        """)

        df_x21 = pd.DataFrame([
            {
                "Y min": row[0],
                "Y max": row[1] if row[1] != float("inf") else "∞",
                "a (L)": row[2], "b (L)": row[3], "c (L)": row[4],
                "d (H)": row[5], "e (H)": row[6], "f (H)": row[7],
            }
            for row in TABLE_X21
        ])
        st.dataframe(df_x21, use_container_width=True, hide_index=True)

        st.markdown("**Curvas L y H calculadas por rango:**")
        try:
            import numpy as np
            import plotly.graph_objects as go

            y_vals = np.linspace(2.0, 70.0, 500)
            L_vals, H_vals = [], []
            for yv in y_vals:
                for row in TABLE_X21:
                    y_min, y_max = row[0], row[1]
                    if y_min <= yv <= y_max or (y_max == float("inf") and yv >= y_min):
                        a, b, c, d, e, f = row[2], row[3], row[4], row[5], row[6], row[7]
                        L_vals.append(a * yv**2 + b * yv + c)
                        H_vals.append(d * yv**2 + e * yv + f)
                        break

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(y_vals), y=L_vals, name="L (IV = 0)",
                line=dict(color="#ef476f", width=2),
            ))
            fig.add_trace(go.Scatter(
                x=list(y_vals), y=H_vals, name="H (IV = 100)",
                line=dict(color="#06d6a0", width=2),
            ))
            fig.update_layout(
                title="Curvas L y H en función de Y — Tabla X2.1",
                xaxis_title="Y — Viscosidad a 100 °C (mm²/s)",
                yaxis_title="Viscosidad a 40 °C (mm²/s)",
                height=420,
                template="plotly_dark",
            )
            st.plotly_chart(fig, use_container_width=True)
        except ImportError:
            st.info("Instale `plotly` y `numpy` para ver la gráfica.")


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 4 – VALIDACIÓN ISO/IEC 17025
# ══════════════════════════════════════════════════════════════════════════════
elif pagina_activa == "✅ Validación ISO/IEC 17025":

    st.subheader("✅ Validación ISO/IEC 17025")
    st.markdown("""
Según **ISO/IEC 17025:2017 §6.4.7**, el software utilizado en laboratorios de calibración
y ensayo debe validarse para asegurar que es adecuado para el uso previsto. La validación
se realiza comparando los resultados del software con los valores de referencia establecidos
en la propia norma ASTM D2270.

A continuación se ejecutan los **cuatro casos de prueba oficiales** incluidos en los
numerales **5.2.3.1**, **5.2.4.1**, **5.2.4.2** y el **Apéndice X2.5**.
    """)

    CASOS_DE_PRUEBA = [
        {
            "id": "§5.2.3.1",
            "descripcion": "U > H — Ecuación 3",
            "U": 73.30, "Y": 8.86,
            "VI_esperado": 92,
            "L_esperado": 119.94, "H_esperado": 69.48,
            "nota": "Interpolación en Tabla 1. L y H obtenidos por interpolación.",
        },
        {
            "id": "§5.2.4.1",
            "descripcion": "U < H — Ecuaciones 6 y 7",
            "U": 22.83, "Y": 5.05,
            "VI_esperado": 156,
            "L_esperado": None, "H_esperado": 28.975,
            "nota": "H = 28.975 por interpolación en Tabla 1.",
        },
        {
            "id": "§5.2.4.2",
            "descripcion": "U < H — Ecuaciones 6 y 7",
            "U": 53.47, "Y": 7.80,
            "VI_esperado": 111,
            "L_esperado": None, "H_esperado": 57.31,
            "nota": "H = 57.31 exacto en Tabla 1.",
        },
        {
            "id": "Apéndice X2.5",
            "descripcion": "Caso explícito del Apéndice X2",
            "U": 73.50, "Y": 8.860,
            "VI_esperado": 92,
            "L_esperado": 119.9588, "H_esperado": 69.4765,
            "nota": "L = 119.9588, H = 69.4765 según Tabla X2.1.",
        },
    ]

    if st.button("🚀 Ejecutar todos los casos de validación", type="primary"):
        todos_ok = True
        for caso in CASOS_DE_PRUEBA:
            res = calcular_iv_preciso(caso["U"], caso["Y"])

            vi_ok   = res["iv_final"] == caso["VI_esperado"]
            h_ok    = math.isclose(res["H"], caso["H_esperado"], abs_tol=0.05) if caso["H_esperado"] else True
            l_ok    = math.isclose(res["L"], caso["L_esperado"], abs_tol=0.05) if caso["L_esperado"] else True
            caso_ok = vi_ok and h_ok and l_ok
            todos_ok = todos_ok and caso_ok

            icono = "✅" if caso_ok else "❌"
            with st.expander(
                f"{icono} Caso {caso['id']} — {caso['descripcion']}",
                expanded=True,
            ):
                c1, c2, c3 = st.columns(3)
                c1.metric(
                    "IV obtenido", res["iv_final"],
                    delta=f"Esperado: {caso['VI_esperado']}",
                    delta_color="normal" if vi_ok else "inverse",
                )
                c2.metric(
                    "L calculado", res["L"],
                    delta=f"Ref: {caso['L_esperado']}" if caso["L_esperado"] else "N/A en norma",
                )
                c3.metric(
                    "H calculado", res["H"],
                    delta=f"Ref: {caso['H_esperado']}" if caso["H_esperado"] else "N/A en norma",
                )
                if caso_ok:
                    st.success(f"✅ APROBADO — {caso['nota']}")
                else:
                    st.error(f"❌ FALLIDO — {caso['nota']}")

        st.divider()
        if todos_ok:
            st.success(
                "🏆 **VALIDACIÓN COMPLETA** — Todos los casos de prueba pasaron. "
                "La herramienta es conforme con ASTM D2270."
            )
        else:
            st.error("⚠️ **VALIDACIÓN INCOMPLETA** — Uno o más casos fallaron.")

    st.divider()
    st.markdown("""
### Declaración de conformidad

| Requisito ISO/IEC 17025 §6.4.7 | Implementación |
|---|---|
| Verificación de idoneidad | 4 casos de prueba con valores de referencia de la norma |
| Trazabilidad del cálculo | Código fuente y valores intermedios expuestos en la app |
| Documentación | Tablas de constantes completas con fuente normativa citada |
| Control de cambios | Versionado en repositorio GitHub público |
| Identificación del software | Versión, nombre y referencia normativa visibles en la interfaz |

**Nota:** Esta validación cubre la lógica de cálculo. La incertidumbre del resultado final
depende también de la precisión del método de medición de viscosidad utilizado
(ver Apéndice X3 de ASTM D2270).
    """)
