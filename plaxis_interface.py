def run_plaxis_model(tipo_suelo, espesor, estructura, demo=True, host="localhost", port=10000, password=""):
    if demo:
        # Modo demo con resultados simulados
        return _run_demo_model(tipo_suelo, espesor, estructura)
    else:
        try:
            from plxscripting.easy import new_server
            s_i, g_i = new_server(address=host, port=port, password=password)

            # Ejemplo simplificado de lógica para correr un modelo
            g_i.delete()  # Limpia modelo previo

            # Crear suelo
            line = g_i.line((0, 0), (0, -espesor))
            soil = g_i.soil(line)
            
            # Asignar parámetros de suelo
            if tipo_suelo == "Arena":
                mat = g_i.soilmat(MaterialName="Arena", SoilModel="Mohr-Coulomb", gammaUnsat=17, phi=30, c=0)
            elif tipo_suelo == "Arcilla":
                mat = g_i.soilmat(MaterialName="Arcilla", SoilModel="Mohr-Coulomb", gammaUnsat=16, phi=20, c=15)
            else:
                mat = g_i.soilmat(MaterialName="Grava", SoilModel="Mohr-Coulomb", gammaUnsat=18, phi=35, c=5)

            soil.setmaterial(mat)

            # Crear fase y calcular
            fase = g_i.phase(g_i.InitialPhase)
            g_i.calculate()

            # Obtener desplazamiento vertical máximo (ficticio en este ejemplo)
            disp = g_i.getresults(fase, g_i.Soil, "Vertical displacement", "node")
            max_disp = max(disp)

            return {
                "Máximo asentamiento (m)": round(max_disp, 4),
                "Tipo de suelo": tipo_suelo,
                "Espesor de capa (m)": espesor,
                "Estructura": estructura
            }

        except Exception as e:
            print(f"❌ Error al conectar con PLAXIS: {e}")
            return None


def _run_demo_model(tipo_suelo, espesor, estructura):
    # Simulación de resultados en modo demo
    import random

    base_asentamiento = {
        "Arena": 0.012,
        "Arcilla": 0.034,
        "Grava": 0.008
    }

    factor_estructura = {
        "Muro pantalla": 1.0,
        "Pilotes": 0.7,
        "Tablestacado": 1.3
    }

    # Cálculo ficticio con randomización leve
    base = base_asentamiento.get(tipo_suelo, 0.015)
    estructura_factor = factor_estructura.get(estructura, 1.0)
    desplazamiento = base * estructura_factor * (espesor / 5.0) * random.uniform(0.9, 1.1)

    return {
        "Máximo asentamiento (m)": round(desplazamiento, 4),
        "Tipo de suelo": tipo_suelo,
        "Espesor de capa (m)": espesor,
        "Estructura": estructura
    }
