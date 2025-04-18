import streamlit as st
from plaxis_interface import run_plaxis_model
from pdf_generator import generate_pdf_report

st.set_page_config(page_title="Diseño Paramétrico Geotécnico", layout="centered")
st.title("🧱 Diseño Paramétrico Geotécnico")

st.markdown("Esta herramienta permite definir un modelo geotécnico paramétrico, simularlo en PLAXIS y generar un informe PDF con los resultados.")

# 🔧 Parámetros de entrada
with st.form("param_form"):
    tipo_suelo = st.selectbox("Tipo de suelo", ["Arena", "Arcilla", "Grava"])
    espesor_capa = st.number_input("Espesor de capa (m)", min_value=0.1, max_value=100.0, value=5.0, step=0.1)
    estructura = st.selectbox("Estructura de contención", ["Muro pantalla", "Pilotes", "Tablestacado"])

    st.markdown("---")
    modo_demo = st.checkbox("Ejecutar en modo demo (sin conexión a PLAXIS)", value=True)

    ip_host = st.text_input("IP del servidor PLAXIS (solo si desactivas el modo demo)", "127.0.0.1")
    puerto = st.number_input("Puerto", value=10000)
    password = st.text_input("Contraseña PLAXIS", value="", type="password")

    submitted = st.form_submit_button("Ejecutar Modelo")

# ▶️ Lógica al presionar botón
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
        st.success("Modelo ejecutado exitosamente.")
        st.subheader("📊 Resultados")
        for k, v in resultados.items():
            st.markdown(f"**{k}**: {v}")

        # 📄 Generar informe
        with st.spinner("Generando informe PDF..."):
            pdf_path = generate_pdf_report(tipo_suelo, espesor_capa, estructura, resultados)
            with open(pdf_path, "rb") as file:
                st.download_button("📥 Descargar Informe PDF", file, file_name="informe_modelo.pdf")

st.markdown("---")
st.caption("Desarrollado por Cristóbal Díaz — Versión demo conectable a PLAXIS 3D")
