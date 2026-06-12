# 🧪 Calculadora de Índice de Viscosidad — ASTM D2270

Herramienta de cálculo transparente y trazable, diseñada para su validación bajo **ISO/IEC 17025:2017**.

Implementa el método **ASTM D2270 – 10 (2016)** completo:
- **Método Sencillo**: interpolación lineal en Tabla 1 (numeral 5.2.1)
- **Método Preciso**: ecuaciones cuadráticas del Apéndice X2 (Tabla X2.1)

---

## Características

- ✅ Ambos métodos de cálculo de L y H (Tabla 1 e interpolación cuadrática X2.1)
- ✅ Muestra todos los valores intermedios para trazabilidad y auditoría
- ✅ Código fuente expuesto en la interfaz (requisito ISO/IEC 17025 §6.4.7)
- ✅ Tablas de constantes completas con fuente normativa
- ✅ Gráfica de curvas L y H
- ✅ Casos de validación incluidos en la norma (§5.2.3.1, §5.2.4.1, §5.2.4.2, X2.5)
- ✅ Redondeo bancario según ASTM E29

---

## Estructura del proyecto

```
astm-d2270-viscosity-index/
├── app.py                  # Aplicación principal Streamlit
├── requirements.txt        # Dependencias Python
├── README.md               # Este archivo
└── src/
    ├── __init__.py
    └── calculations.py     # Motor de cálculo (ambos métodos + tablas)
```

---

## Instalación y ejecución local

```bash
# 1. Clonar el repositorio
git clone https://github.com/roilouis/astm-d2270-viscosity-index.git
cd astm-d2270-viscosity-index

# 2. (Opcional) Crear entorno virtual
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la app
streamlit run app.py
```

La app se abrirá en `http://localhost:8501`.

---

## Despliegue en Streamlit Community Cloud

Ver instrucciones detalladas en `DEPLOY_INSTRUCTIONS.md`.

---

## Referencias normativas

- **ASTM D2270 – 10 (2016)**: Standard Practice for Calculating Viscosity Index from Kinematic Viscosity at 40 °C and 100 °C
- **ISO/IEC 17025:2017** §6.4.7: Requisitos para el equipo informático y el software
- **ASTM E29**: Practice for Using Significant Digits in Test Data to Determine Conformance with Specifications
