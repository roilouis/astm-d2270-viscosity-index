# 📦 Instrucciones de despliegue en GitHub y Streamlit Cloud

## Paso 1 — Preparar los archivos localmente

Asegúrate de tener la siguiente estructura de archivos lista:

```
astm-d2270-viscosity-index/
├── app.py
├── requirements.txt
├── README.md
├── DEPLOY_INSTRUCTIONS.md   (este archivo)
└── src/
    ├── __init__.py
    └── calculations.py
```

---

## Paso 2 — Subir los cambios a GitHub

### Opción A: Si ya tienes el repositorio clonado localmente

```bash
# Navega a la carpeta del proyecto
cd astm-d2270-viscosity-index

# Copia los nuevos archivos en las rutas correctas
# (reemplaza los existentes app.py y requirements.txt,
#  y agrega la carpeta src/ con __init__.py y calculations.py)

# Agrega todos los cambios al staging
git add .

# Crea el commit con un mensaje descriptivo
git commit -m "feat: add precise method (Appendix X2), tables tab, and validation tab

- Add src/calculations.py with both simple (Table 1) and precise (X2.1) methods
- Full Table 1 data (all 168 entries) embedded in calculations.py
- Full Table X2.1 coefficients (16 quadratic equation sets) embedded
- app.py: 4 tabs: Calculator, Code Transparency, Constants Tables, ISO Validation
- Validation tab runs 4 official test cases from ASTM D2270 norm
- Plotly chart for L and H curves
- Banker's rounding (ASTM E29) implemented via Python built-in round()"

# Sube los cambios a la rama principal
git push origin main
```

### Opción B: Subir directamente desde la interfaz web de GitHub

1. Ve a https://github.com/roilouis/astm-d2270-viscosity-index
2. Para **reemplazar** `app.py`:
   - Haz clic en `app.py` → botón del lápiz (✏️ Edit) → pega el nuevo contenido → **Commit changes**
3. Para **reemplazar** `requirements.txt`:
   - Mismo proceso que app.py
4. Para **crear** `src/__init__.py`:
   - Haz clic en **Add file → Create new file**
   - En el nombre escribe: `src/__init__.py`
   - Contenido: (déjalo vacío o escribe `# src/__init__.py`)
   - Haz clic en **Commit new file**
5. Para **crear** `src/calculations.py`:
   - Haz clic en **Add file → Create new file**
   - En el nombre escribe: `src/calculations.py`
   - Pega el contenido de `calculations.py`
   - Haz clic en **Commit new file**

---

## Paso 3 — Verificar que Streamlit Cloud se actualiza automáticamente

Si la app ya está desplegada en Streamlit Community Cloud, se actualizará
automáticamente en cuanto detecte el push a `main`. Esto suele tardar
entre 1 y 3 minutos.

Para verificar:
1. Ve a https://share.streamlit.io/
2. Busca tu app `astm-d2270-viscosity-index`
3. Verifica que el estado sea **Running** ✅
4. Si hay error, haz clic en los logs para ver el detalle

---

## Paso 4 — Si es la primera vez que desplegas en Streamlit Cloud

1. Ve a https://share.streamlit.io/ e inicia sesión con tu cuenta de GitHub
2. Haz clic en **New app**
3. Selecciona:
   - **Repository**: `roilouis/astm-d2270-viscosity-index`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. (Opcional) Elige una URL personalizada, por ejemplo: `astm-d2270-vi-calculator`
5. Haz clic en **Deploy!**
6. Espera que termine el proceso de build (2-5 minutos)

---

## Paso 5 — Solución de problemas comunes

| Problema | Solución |
|---|---|
| `ModuleNotFoundError: No module named 'src'` | Verifica que `src/__init__.py` existe en el repositorio |
| `ModuleNotFoundError: No module named 'plotly'` | Verifica que `plotly>=5.18.0` está en `requirements.txt` |
| La app no se actualiza tras el push | Ve a Streamlit Cloud → tu app → **Reboot app** |
| Error `streamlit.errors.StreamlitAPIException` | Revisa la consola de logs en Streamlit Cloud |

---

## Notas para auditoría ISO/IEC 17025

Para evidencia de validación, se recomienda:

1. **Captura de pantalla** de la pestaña "✅ Validación ISO/IEC 17025" mostrando los 4 casos aprobados.
2. **Registro del hash del commit** de GitHub como identificador de versión del software.
3. **Fecha de validación** en el registro de laboratorio.
4. Guardar el archivo `src/calculations.py` como evidencia del código bajo control de versiones.

El hash del commit se obtiene con:
```bash
git log --oneline -1
```
O en GitHub: pestaña **Commits** → copiar el hash SHA del commit validado.
