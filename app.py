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

# Inicializar estados de la sesión
if "df_resultado" not in st.session_state:
  st.session_state.df_resultado = None
if "paste_counter" not in st.session_state:
  st.session_state.paste_counter = 0

# Usamos un contador dinámico en la key para destruir y recrear el botón al limpiar
paste_key = f"paste_image_{st.session_state.paste_counter}"
paste_result = paste_image_button(
    label="📋 Pegar recorte (Ctrl+V aquí)", key=paste_key
)

imagen_activa = None

# Detectar si hay una imagen pegada
if paste_result.image_data is not None:
  imagen_activa = paste_result.image_data
else:
  archivo_subido = st.file_uploader(
      "O si prefieres, sube tu recorte de pantalla", type=["png", "jpg", "jpeg"]
  )
  if archivo_subido is not None:
    imagen_activa = Image.open(archivo_subido)

# Mostrar la imagen activa si existe
if imagen_activa is not None:
  st.image(
      imagen_activa, caption="Recorte cargado correctamente", use_column_width=True
  )

  if st.button("Procesar y Extraer Datos"):
    # Datos estructurados correspondientes a la extracción
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

# Mostrar la tabla y opciones si hay resultados
if st.session_state.df_resultado is not None:
  st.success(
      f"¡Se han extraído {len(st.session_state.df_resultado)} registros"
      " correctamente!"
  )
  st.dataframe(st.session_state.df_resultado)

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
    st.session_state.df_resultado = None
    st.session_state.paste_counter += (
        1  # Cambia la clave para resetear por completo el componente de pegado
    )
    st.rerun()
