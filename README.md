# 🧪 Calculadora de Índice de Viscosidad — ASTM D2270

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://astm-d2270-viscosity-index-calculator.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Licencia](https://img.shields.io/badge/Licencia-MIT-green)
![Norma](https://img.shields.io/badge/Norma-ASTM%20D2270--10%20(2016)-orange)

Herramienta web de código abierto para el cálculo del **Índice de Viscosidad (IV)** de aceites lubricantes e hidrocarburos, implementando íntegramente el método **ASTM D2270 – 10 (2016)**.

Diseñada con trazabilidad completa del cálculo para su **validación bajo ISO/IEC 17025:2017** — el estándar internacional de competencia para laboratorios de ensayo y calibración.

---

## ¿Por qué esta herramienta?

Los laboratorios acreditados bajo ISO/IEC 17025 deben validar todo software o herramienta informática utilizada en cálculos de ensayo (§6.4.7). Esto exige demostrar que:

- El algoritmo implementado es fiel a la norma de referencia.
- Los valores intermedios del cálculo son auditables.
- Existe trazabilidad entre el código y el resultado reportado.

Esta app cubre esos tres requisitos de forma explícita y verificable.

---

## Funcionalidades

| Característica | Detalle |
|---|---|
| **Método Sencillo** | Interpolación lineal en Tabla 1 (numeral 5.2.1) — válido para Y ≤ 70 mm²/s |
| **Método Preciso** | Ecuaciones cuadráticas Tabla X2.1 (Apéndice X2) — válido para todo el rango |
| **Trazabilidad** | Muestra L, H, N e IV sin redondear en cada cálculo |
| **Transparencia** | Código fuente del motor de cálculo visible dentro de la propia app |
| **Tablas completas** | Tabla 1 (168 entradas) y Tabla X2.1 (16 rangos) con fuente normativa |
| **Gráfica L y H** | Visualización de las curvas de referencia en función de Y |
| **Validación integrada** | 4 casos de prueba oficiales de la norma ejecutables en un clic |
| **Redondeo correcto** | Redondeo bancario (round-half-to-even) según ASTM E29 |

---

## Demo

🔗 **[Abrir aplicación →](https://astm-d2270-viscosity-index-calculator.streamlit.app/)**

La app tiene cuatro pestañas:

- **📊 Calculadora** — ingresa U y Y, selecciona el método y obtén el IV con todos los intermedios.
- **💻 Transparencia de código** — el código fuente exacto que realiza el cálculo, visible para cualquier auditor.
- **📋 Tablas de constantes** — Tabla 1 y Tabla X2.1 completas, con gráfica de curvas L y H.
- **✅ Validación ISO/IEC 17025** — ejecuta los casos de prueba de la norma y confirma conformidad.

---

## Estructura del proyecto

```
astm-d2270-viscosity-index/
├── app.py               # Aplicación Streamlit (interfaz y pestañas)
├── requirements.txt     # Dependencias
├── README.md
└── src/
    ├── __init__.py
    └── calculations.py  # Motor de cálculo: ambos métodos, Tabla 1, Tabla X2.1
```

---

## Ejecución local

```bash
git clone https://github.com/roilouis/astm-d2270-viscosity-index.git
cd astm-d2270-viscosity-index
pip install -r requirements.txt
streamlit run app.py
```

La app se abre en `http://localhost:8501`.

---

## Despliegue en Streamlit Community Cloud

1. Haz fork de este repositorio o usa el tuyo propio.
2. Ve a [share.streamlit.io](https://share.streamlit.io) e inicia sesión con GitHub.
3. Selecciona el repositorio, rama `main` y archivo principal `app.py`.
4. Haz clic en **Deploy** — listo en ~2 minutos.

Cada `git push` a `main` actualiza la app automáticamente.

---

## Casos de validación incluidos

Los siguientes casos son los ejemplos oficiales del método ASTM D2270 y se ejecutan automáticamente desde la pestaña de validación:

| Caso | U (mm²/s) | Y (mm²/s) | IV esperado | Resultado |
|------|-----------|-----------|-------------|-----------|
| §5.2.3.1 — U > H | 73.30 | 8.86 | 92 | ✅ |
| §5.2.4.1 — U < H | 22.83 | 5.05 | 156 | ✅ |
| §5.2.4.2 — U < H | 53.47 | 7.80 | 111 | ✅ |
| Apéndice X2.5 | 73.50 | 8.860 | 92 | ✅ |

---

## Referencias normativas

- **ASTM D2270 – 10 (2016)** — Standard Practice for Calculating Viscosity Index from Kinematic Viscosity at 40 °C and 100 °C
- **ISO/IEC 17025:2017** §6.4.7 — Requisitos para equipos informáticos y software en laboratorios
- **ASTM E29** — Practice for Using Significant Digits in Test Data to Determine Conformance with Specifications

---

## Licencia

MIT — libre para uso, modificación y distribución, con atribución.
