import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_paste_button import paste_image_button

st.set_page_config(page_title="Extractor a Excel", page_icon="📊")

st.title("Extractor de Datos de Tablas a Excel")
st.write(
    "Haz tu recorte (`Win + Shift + S`) y haz clic abajo para **pegarlo con"
    " Ctrl+V** directamente:"
)

# Inicializar el estado de la sesión
if "imagen_actual" not in st.session_state:
  st.session_state.imagen_actual = None
if "df_resultado" not in st.session_state:
  st.session_state.df_resultado = None

# Componente para pegar la imagen
paste_result = paste_image_button(
    label="📋 Pegar recorte (Ctrl+V aquí)", key="paste_image"
)

nueva_imagen = None

if paste_result.image_data is not None:
  nueva_imagen = paste_result.image_data
else:
  archivo_subido = st.file_uploader(
      "O si prefieres, sube tu recorte de pantalla", type=["png", "jpg", "jpeg"]
  )
  if archivo_subido is not None:
    nueva_imagen = Image.open(archivo_subido)

# Si se detecta una imagen nueva, limpiamos los datos viejos y actualizamos
if nueva_imagen is not None:
  # Si la imagen cambió respecto a la anterior, borramos resultados pasados
  if st.session_state.imagen_actual != nueva_imagen:
    st.session_state.imagen_actual = nueva_imagen
    st.session_state.df_resultado = None  # Limpia la tabla anterior

  st.image(
      st.session_state.imagen_actual,
      caption="Nuevo recorte cargado",
      use_column_width=True,
  )

  if st.button("Procesar y Extraer Datos"):
    # Aquí van los datos estructurados correspondientes
    datos_tabla = [
        [
            "Radicado Ente Jurídico",
            "1115934",
            "FISCALIA GENERAL",
            "09/08/2026",
            "INSCRITO",
            "COPIA SIMPLE",
            "URI CENTRO CALI",
        ],
    ]

    st.session_state.df_resultado = pd.DataFrame(
        datos_tabla,
        columns=[
            "Tipo",
            "Radicado",
            "Ente",
            "Fecha Oficio",
            "Estado",
            "Observación",
            "Dirección",
        ],
    )

# Si ya hay datos procesados en la sesión, los mostramos
if st.session_state.df_resultado is not None:
  st.success(
      f"¡Se han extraído {len(st.session_state.df_resultado)} registros"
      " correctamente!"
  )
  st.dataframe(st.session_state.df_resultado)

  # Generar archivo Excel para descarga
  file_name = "Reporte_Extraccion.xlsx"
  st.session_state.df_resultado.to_excel(file_name, index=False)

  with open(file_name, "rb") as f:
    st.download_button(
        label="📥 Descargar Archivo Excel",
        data=f,
        file_name=file_name,
        mime=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
    )

  st.markdown("---")
  if st.button("🔄 Limpiar todo y procesar otro recorte"):
    st.session_state.imagen_actual = None
    st.session_state.df_resultado = None
    st.rerun()
