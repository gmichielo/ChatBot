# ==============================
# IMPORTS
# ==============================
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tempfile
import mimetypes


# ==============================
# CONSTANTES
# ==============================
LOGO_MAIN = "images/logo_title.png"
LOGO_ICON = "images/logo_icon.png"


# ==============================
# CONFIGURACIÓN PRINCIPAL
# ==============================
st.set_page_config(page_title="Drakonius AI", page_icon=LOGO_ICON, layout="wide")
st.logo(LOGO_MAIN, icon_image=LOGO_ICON)


# ==============================
# ESTILOS PERSONALIZADOS
# ==============================
st.markdown(
    """
    <style>
    body {
        background-color: #E3F2FD;
    }

    /* Animación burbujas */
    .bubble-animate {
        animation: fadeIn 0.35s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Slider azul (como versión original) */
    .stSlider > div[data-baseweb="slider"] > div > div > div {
        background-color: #90CAF9 !important;
    }
    .stSlider > div[data-baseweb="slider"] > div > div > div > div {
        background-color: #42A5F5 !important;
        border: 2px solid #42A5F5 !important;
    }
    .stSlider > div[data-baseweb="slider"] > div > div > div > div:hover {
        border: 2px solid #1E88E5 !important;
    }
    .stSlider > div[data-baseweb="slider"] > div > div > div > div > div {
        color: #1E88E5 !important;
    }

    /* Selectbox azul */
    .stSelectbox div[data-baseweb="select"] > div {
        border: 1px solid #29B6F6 !important;
        cursor: pointer !important;
    }
    .stSelectbox div[data-baseweb="select"] > div:hover {
        border-color: #0288D1 !important;
        box-shadow: 0 0 0 1px #0288D1 !important;
    }
    .stSelectbox div[data-baseweb="select"] > div:focus-within {
        border-color: #01579B !important;
        box-shadow: 0 0 0 2px #01579B !important;
    }
    

    /* Botones */
    .stButton button {
        background-color: #29B6F6 !important;
        color: white !important;
        border-radius: 6px !important;
        border: 1px solid #0288D1 !important;
        transition: 0.2s ease-in-out;
    }
    .stButton button:hover {
        background-color: #0288D1 !important;
        border-color: #01579B !important;
    }

    /* Burbujas */
    .user-bubble {
        background: #BBDEFB;
        padding: 12px;
        border-radius: 12px;
        margin: 8px;
        color: black;
    }
    .bot-bubble {
        background: #90CAF9;
        padding: 12px;
        border-radius: 12px;
        margin: 8px;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================
# CABECERA
# ==============================
col1, col2, col3 = st.columns([2.5, 2, 1])
with col2:
    st.image(LOGO_ICON, width=130)

st.markdown(
    """
    <h1 style="
        text-align: center;
        color: #29B6F6;
        font-size: 60px;
        font-weight: bold;
        text-shadow: 0px 0px 20px #7dcfff;
    ">
        Drakonius AI 🐲
    </h1>
    <p style='text-align: center; font-size: 18px; color: #4FC3F7;'>
        IA de Drakonius Studios para desarrollo de videojuegos
    </p>
    """,
    unsafe_allow_html=True
)


# ==============================
# SIDEBAR
# ==============================
with st.sidebar:

    st.markdown("### Perfil de IA")
    personalidad = st.selectbox(
        "",
        [
            "Generalista",
            "Rigger",
            "Animador",
            "Programador",
            "Shaders",
            "Narrador",
        ],
    )

    st.markdown("### Temperatura")
    temperatura = st.slider("", min_value=0.0, max_value=1.0, step=0.1, value=0.5)

    st.markdown("### Modelo Utilizado")
    modelo = st.selectbox(
        "",
        [
            "gemini-2.5-flash",
            "gemini-2.5-flash-preview-09-2025",
            "gemini-2.5-flash-lite",
            "gemini-2.5-pro",
        ],
        index=0,
    )

    st.markdown("---")
    if st.button("Resetear conversación"):
        st.session_state.mensajes = []
        st.rerun()

    # -------- DESCARGA DE CONVERSACIÓN (RESTAURADO) --------
    st.markdown("### Descargar conversación")

    if "mensajes" in st.session_state and st.session_state.mensajes:

        if st.button("Descargar en PDF"):

            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            file_path = temp_file.name

            c = canvas.Canvas(file_path, pagesize=letter)
            textobject = c.beginText(40, 750)
            textobject.setFont("Helvetica", 11)

            max_width = 90
            y_min = 40

            for m in st.session_state.mensajes:
                role = "USER: " if isinstance(m, HumanMessage) else "BOT: "
                line = role + m.content

                for subline in line.split("\n"):
                    wrapped = [subline[i:i+max_width] for i in range(0, len(subline), max_width)]

                    for w in wrapped:
                        if textobject.getY() <= y_min:
                            c.drawText(textobject)
                            c.showPage()
                            textobject = c.beginText(40, 750)
                            textobject.setFont("Helvetica", 11)

                        textobject.textLine(w)

                textobject.textLine("")

            c.drawText(textobject)
            c.save()

            with open(file_path, "rb") as f:
                st.download_button(
                    label="Descargar PDF",
                    data=f.read(),
                    file_name="conversacion.pdf",
                    mime="application/pdf"
                )

# MODELO IA
# ==============================
chat_model = ChatGoogleGenerativeAI(model=modelo, temperature=temperatura)


# ==============================
# SESSION STATE
# ==============================
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

if "archivo_procesado" not in st.session_state:
    st.session_state.archivo_procesado = False

if "bloqueo_input" not in st.session_state:
    st.session_state.bloqueo_input = False


# ==============================
# FUNCIÓN PERSONALIDAD
# ==============================
def aplicar_personalidad(texto):
    perfiles = {
        "Generalista": "Responde de forma equilibrada y versátil, como una IA general que puede explicar, ayudar o proponer ideas: ",
        "Rigger": "Responde como un experto en rigging para videojuegos. Habla de articulaciones, pesos, controladores, constraints, deformadores y pipelines de animación. Explica con detalle técnico: ",
        "Animador": "Responde como un animador profesional de videojuegos. Comenta temas como curvas, timing, spacing, posing, acting, squash & stretch, ciclos y retargeting. Explica con emoción y precisión: ",
        "Programador": "Responde como un programador experto en Unity y desarrollo de videojuegos. Usa términos técnicos claros, menciona patrones, optimización, arquitectura y ejemplos de código cuando sea útil: ",
        "Shaders": "Responde como un artista técnico especialista en shaders. Explica también nodos de Shader Graph, HLSL, iluminación, materiales, VFX y optimización gráfica: ",
        "Narrador": "Responde como un escritor de narrativa para videojuegos: enfócate en construcción de mundo, tono, personajes, diálogos, desarrollo emocional, ritmo y estructuras narrativas: "
    }
    return perfiles.get(personalidad, "") + texto


# ==============================
# CHAT HISTORIAL
# ==============================
chat_area = st.container()

with chat_area:
    for msg in st.session_state.mensajes:
        role = "assistant" if isinstance(msg, AIMessage) else "user"
        icon = "🐲" if role == "assistant" else "👤"
        bubble_class = "bot-bubble" if role == "assistant" else "user-bubble"

        st.markdown(
            f"<div class='{bubble_class} bubble-animate'><b>{icon}</b> {msg.content}</div>",
            unsafe_allow_html=True
        )

st.markdown("---")


# ==============================
# INPUT + UPLOAD
# ==============================
input_area = st.container()
with input_area:
    col_input, col_files = st.columns([4, 1])

    mensaje_usuario = None
    archivo = None

    # -------------------------
    # Columna izquierda: chat input mejorado
    # -------------------------
    with col_input:
        chat_data = st.chat_input(
            "Escribe tu mensaje o sube un archivo:",
            disabled=st.session_state.bloqueo_input,
            accept_file=True,
            file_type=["txt", "pdf", "doc", "docx"]  # Solo documentos
        )

        if chat_data:
            # Texto
            if hasattr(chat_data, "text") and chat_data.text:
                mensaje_usuario = chat_data.text

            # Archivo
            if hasattr(chat_data, "files") and chat_data.files:
                archivo = chat_data.files[0]
                st.session_state.bloqueo_input = True

                tipo_mime, _ = mimetypes.guess_type(archivo.name)
                if tipo_mime == "text/plain":
                    mensaje_usuario = archivo.read().decode("utf-8")
                else:
                    mensaje_usuario = f"[Archivo cargado: {archivo.name}]"

    # -------------------------
    # Columna derecha: expander para subir archivo
    # -------------------------
    with col_files:
        with st.expander("📎 Subir documento"):
            archivo_expander = st.file_uploader(
                "Selecciona un archivo",
                type=["txt", "pdf", "doc", "docx"],
                key=f"file_uploader_{st.session_state.uploader_key}_side_expander"
            )

            if archivo_expander and not mensaje_usuario:
                archivo = archivo_expander
                st.session_state.bloqueo_input = True

                tipo_mime, _ = mimetypes.guess_type(archivo.name)
                if tipo_mime == "text/plain":
                    mensaje_usuario = archivo.read().decode("utf-8")
                else:
                    mensaje_usuario = f"[Archivo cargado: {archivo.name}]"

# ==============================
# RESPUESTA IA
# ==============================
if mensaje_usuario:

    st.session_state.mensajes.append(HumanMessage(content=mensaje_usuario))

    with chat_area:
        placeholder = st.empty()
        placeholder.markdown(
            "<div class='bot-bubble'><b>🐲</b> Drakonius está escribiendo...</div>",
            unsafe_allow_html=True
        )

    respuesta = chat_model.invoke([
        HumanMessage(content=aplicar_personalidad(mensaje_usuario))
    ])

    placeholder.empty()
    st.session_state.mensajes.append(respuesta)

    st.session_state.uploader_key += 1
    st.session_state.archivo_procesado = False
    st.session_state.bloqueo_input = False

    st.rerun()


