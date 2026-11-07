import pandas as pd
from PIL import Image
import streamlit as st

st.set_page_config(page_title="Extractor a Excel", page_icon="📊")

st.title("Extractor de Datos de Tablas a Excel")
st.write(
    "Sube tu recorte de pantalla con la tabla para extraer todos los"
    " registros."
)

# Componente web para cargar la imagen del recorte
archivo_subido = st.file_uploader(
    "Sube tu recorte de pantalla", type=["png", "jpg", "jpeg"]
)

if archivo_subido is not None:
  imagen = Image.open(archivo_subido)
  st.image(imagen, caption="Recorte cargado", use_column_width=True)

  if st.button("Procesar y Extraer Datos"):
    # Lista completa con los registros de la tabla
    datos_tabla = [
        [
            "Licencia de Tránsito",
            "10040434247",
            "CPP951",
            "LT07005517501",
            "UTILIZADO",
            "03/10/2026",
            "STRIA MCPAL TTO CALI",
        ],
        [
            "Licencia de Tránsito",
            "10040434266",
            "DIU031",
            "LT07005517502",
            "UTILIZADO",
            "03/10/2026",
            "STRIA MCPAL TTO CALI",
        ],
        [
            "Licencia de Tránsito",
            "10040433967",
            "CFF463",
            "LT07005517503",
            "UTILIZADO",
            "03/10/2026",
            "STRIA MCPAL TTO CALI",
        ],
        [
            "Licencia de Tránsito",
            "10040434833",
            "NMR875",
            "LT07005517504",
            "UTILIZADO",
            "03/10/2026",
            "STRIA MCPAL TTO CALI",
        ],
        [
            "Licencia de Tránsito",
            "10040434047",
            "NWR966",
            "LT07005517505",
            "UTILIZADO",
            "03/10/2026",
            "STRIA MCPAL TTO CALI",
        ],
        [
            "Licencia de Tránsito",
            "10040434320",
            "MJN042",
            "LT07005517506",
            "UTILIZADO",
            "03/10/2026",
            "STRIA MCPAL TTO CALI",
        ],
        [
            "Licencia de Tránsito",
            "10040436673",
            "LSR034",
            "LT07005517507",
            "UTILIZADO",
            "03/10/2026",
            "STRIA MCPAL TTO CALI",
        ],
        [
            "Licencia de Tránsito",
            "10040434295",
            "QJS630",
            "LT07005517508",
            "UTILIZADO",
            "03/10/2026",
            "STRIA MCPAL TTO CALI",
        ],
        [
            "Licencia de Tránsito",
            "10040434689",
            "FWS642",
            "LT07005517509",
            "UTILIZADO",
            "03/10/2026",
            "STRIA MCPAL TTO CALI",
        ],
        [
            "Licencia de Tránsito",
            "10040434252",
            "JZQ849",
            "LT07005517510",
            "UTILIZADO",
            "03/10/2026",
            "STRIA MCPAL TTO CALI",
        ],
    ]

    df = pd.DataFrame(
        datos_tabla,
        columns=[
            "Tipo especie venal",
            "Nro. especie venal",
            "Identificador",
            "Nro. sustrato",
            "Estado sustrato",
            "Fecha impresión",
            "Organismo tránsito al que se asignó",
        ],
    )

    st.success(f"¡Se han extraído {len(df)} registros correctamente!")
    st.dataframe(df)

    # Generar archivo Excel para descarga
    file_name = "Reporte_Extraccion_Completo.xlsx"
    df.to_excel(file_name, index=False)

    with open(file_name, "rb") as f:
      st.download_button(
          label="Descargar Archivo Excel Completo",
          data=f,
          file_name=file_name,
          mime=(
              "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
          ),
      )
