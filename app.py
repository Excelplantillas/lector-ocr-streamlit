import pandas as pd
from PIL import Image
import pytesseract
import streamlit as st
from streamlit_paste_button import paste_image_button

st.set_page_config(page_title="Extractor OCR a Excel", page_icon="📊")

st.title("Extractor Automático de Datos a Excel")
st.write(
    "Haz tu recorte (`Win + Shift + S`) y pégalo con **Ctrl+V** abajo para"
    " extraer los datos reales de la imagen:"
)

# Inicializar estados de la sesión
if "df_resultado" not in st.session_state:
  st.session_state.df_resultado = None
if "paste_counter" not in st.session_state:
  st.session_state.paste_counter = 0

# Botón dinámico de pegado web
paste_key = f"paste_image_{st.session_state.paste_counter}"
paste_result = paste_image_button(
    label="📋 Pegar recorte (Ctrl+V aquí)", key=paste_key
)

imagen_activa = None

if paste_result.image_data is not None:
  imagen_activa = paste_result.image_data
else:
  archivo_subido = st.file_uploader(
      "O si prefieres, sube tu recorte de pantalla", type=["png", "jpg", "jpeg"]
  )
  if archivo_subido is not None:
    imagen_activa = Image.open(archivo_subido)

# Si hay una imagen activa, la mostramos
if imagen_activa is not None:
  st.image(
      imagen_activa, caption="Recorte cargado para análisis", use_column_width=True
  )

  if st.button("🔍 Extraer Datos de la Imagen"):
    with st.spinner("Leyendo texto de la imagen..."):
      # Lectura OCR real del texto en la imagen (soporte en español)
      texto_leido = pytesseract.image_to_string(imagen_activa, lang="spa")

      # Convertimos el resultado detectado en un formato tabular limpio para Excel
      datos_extraidos = [
          [
              "Recorte Procesado",
              texto_leido.replace("\n", " ").strip()[:150]
              + "...",  # Muestra parte del texto detectado
              "Exitoso",
          ]
      ]

      st.session_state.df_resultado = pd.DataFrame(
          datos_extraidos,
          columns=[
              "Tipo de Documento / Registro",
              "Texto Detectado (OCR)",
              "Estado",
          ],
      )

# Mostrar la tabla y opciones de descarga si hay resultados vigentes
if st.session_state.df_resultado is not None:
  st.success("¡Datos extraídos correctamente de tu recorte!")
  st.dataframe(st.session_state.df_resultado)

  file_name = "Reporte_Extraccion_OCR.xlsx"
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
        1  # Resetea el componente de pegado y borra la imagen anterior
    )
    st.rerun()
