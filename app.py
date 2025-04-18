import streamlit as st
from plaxis_interface import run_plaxis_model
from pdf_generator import generate_pdf_report

st.set_page_config(page_title="Diseño Paramétrico Geotécnico", layout="centered")
st.title("🧱 Diseño Paramétrico Geotécnico")

st.markdown("""
Esta herramienta permite definir un modelo geotécnico paramétrico, 
simularlo en PLAXIS 3D (de forma remota) o en modo demo, y generar un informe PDF con los resultados.
""")

# ✅ MODO DEMO (fuera del form para que sea reactivo)
modo_demo = st.checkbox("✅ Ejecutar en modo demo (sin PLAXIS conectado)", value=True)

# 🔧 Formulario de parámetros del modelo
with st.form("param_form"):
    tipo_suelo = st.selectbox("Tipo de suelo", ["Arena", "Arcilla", "Grava"])
    espesor_capa = st.number_input("Espesor de capa (m)", min_value=0.1, max_value=100.0, value=5.0, step=0.1)
    estructura = st.selectbox("Estructura de contención", ["Muro pantalla", "Pilotes", "Tablestacado"])

    ip_host = "127.0.0.1"
    puerto = 10000
    password = ""

    # ✅ Solo mostramos los campos si está desactivado el modo demo
    if not modo_demo:
        st.markdown("### 🛜 Conexión remota a PLAXIS 3D")
        st.info("""
Para que esta aplicación funcione correctamente usando **tu instalación local de PLAXIS 3D**, sigue estos pasos detallados:

---

### 🧩 ¿Qué debes hacer?

1. **Abre PLAXIS 3D** en tu computador.
2. Activa el servidor de conexión remota (Remote Scripting Server):
   - Ve a la pestaña **Expert** y haz clic en **Remote Scripting Server**.
   - Verifica que el ícono del candado esté **abierto**.
   - Cuando se abra la ventana, define una **contraseña** (puede ser simple, como `1234`).

3. Encuentra la **IP local** de tu computador:
   - Pulsa `Windows + R`, escribe `cmd` y presiona Enter.
   - Escribe `ipconfig` y presiona Enter.
   - Busca donde dice `Dirección IPv4` (por ejemplo: `192.168.1.34`).
   - Esa será la IP que debes ingresar en esta app.

---

### ✍️ ¿Qué debes escribir en el formulario?

- **IP del servidor PLAXIS**: escribe la IP local que obtuviste en el paso anterior (`192.168.X.X`).
- **Puerto**: deja `10000`, que es el valor por defecto de PLAXIS.
- **Contraseña**: escribe la contraseña que definiste al activar el Remote Scripting Server.

---

### ✅ Ejemplo completo

- IP del servidor PLAXIS: `192.168.1.34`
- Puerto: `10000`
- Contraseña: `1234`

Luego haz clic en **"Ejecutar Modelo"** y la app se conectará automáticamente a tu PLAXIS para procesar el diseño.
""")


        ip_host = st.text_input("🔗 IP del servidor PLAXIS", value="127.0.0.1")
        puerto = st.number_input("Puerto", value=10000)
        password = st.text_input("Contraseña PLAXIS", value="", type="password")

    submitted = st.form_submit_button("Ejecutar Modelo")

# ▶️ Ejecución del modelo
if submitted:
    with st.spinner("Ejecutando modelo..."):
        resultados = run_plaxis_model(
            tipo_suelo=tipo_suelo,
            espesor=espesor_capa,
            estructura=estructura,
            demo=modo_demo,
            host=ip_host,
            port=puerto,
            password=password
        )

    if resultados is None:
        st.error("No fue posible ejecutar el modelo. Revisa los datos de conexión o activa el modo demo.")
    else:
        st.success("✅ Modelo ejecutado exitosamente.")
        st.subheader("📊 Resultados")
        for k, v in resultados.items():
            st.markdown(f"**{k}**: {v}")

        with st.spinner("Generando informe PDF..."):
            pdf_path = generate_pdf_report(tipo_suelo, espesor_capa, estructura, resultados)
            with open(pdf_path, "rb") as file:
                st.download_button("📥 Descargar Informe PDF", file, file_name="informe_modelo.pdf")

st.markdown("---")
st.caption("Desarrollado por Cristóbal Díaz — Versión demo conectable a PLAXIS 3D")
