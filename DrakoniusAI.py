import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tempfile
import mimetypes

LOGO_MAIN = "images/logo_title.png"
LOGO_ICON = "images/logo_icon.png"

profiles_personalitys = [
            "Generalista",
            "Rigger",
            "Animador",
            "Programador",
            "Shaders",
            "Narrador",
            ]

models_IA = [
            "gemini-2.5-flash",
            "gemini-2.5-flash-preview-09-2025",
            "gemini-2.5-flash-lite",
            "gemini-2.5-pro",
            ]

emojis = {
    "Generalista": "🐲🐉",
    "Rigger": "🐲🚻",
    "Animador": "🐲🎦",
    "Programador": "🐲💻",
    "Shaders": "🐲🌈",
    "Narrador": "🐲📖"
}

def apply_personality(text):
    profiles = {
        "Generalista": (
            "Responde de forma equilibrada, versátil y clara, "
            "como una IA general capaz de explicar, analizar o proponer ideas cuando sea útil. "
            "Puedes responder cualquier tipo de pregunta: "
        ),

        "Rigger": (
            "Responde como un experto en rigging para videojuegos. "
            "Tu especialidad son articulaciones, pesos, controladores, constraints, deformadores y pipelines de animación. "
            "Si la pregunta NO está relacionada con rigging, indícalo explícitamente con una frase como "
            "'Esto no pertenece directamente al rigging, pero puedo ayudarte desde un punto de vista general:'. "
            "Luego responde de manera útil si es posible: "
        ),

        "Animador": (
            "Responde como un animador profesional de videojuegos. "
            "Tu dominio incluye curvas, timing, spacing, posing, acting, squash & stretch, ciclos y retargeting. "
            "Si la pregunta NO pertenece al ámbito de la animación, primero acláralo con una frase como "
            "'Esta pregunta no es propiamente de animación, pero puedo orientarte:'. "
            "Después ofrece la mejor respuesta posible: "
        ),

        "Programador": (
            "Responde como un programador experto en Unity y desarrollo de videojuegos. "
            "Manejas patrones, optimización, arquitectura, scripting y ejemplos de código. "
            "Si la pregunta NO corresponde a programación, indícalo de forma clara con "
            "'Este tema no entra dentro de programación, pero intentaré ayudarte:'. "
            "Luego responde de manera general si es posible: "
        ),

        "Shaders": (
            "Responde como un artista técnico especializado en shaders. "
            "Tu enfoque incluye Shader Graph, HLSL, iluminación, materiales, efectos visuales y optimización gráfica. "
            "Si la pregunta NO está relacionada con shaders o gráficos, advierte primero con "
            "'Esto no forma parte del área de shaders, pero puedo darte una orientación:'. "
            "Después responde lo mejor que puedas: "
        ),

        "Narrador": (
            "Responde como un escritor de narrativa para videojuegos. "
            "Tu dominio incluye construcción de mundo, personajes, diálogos, tono, ritmo y estructura narrativa. "
            "Si la pregunta NO pertenece a narrativa, aclara primero con una frase como "
            "'Este tema no pertenece a narrativa, pero puedo orientarte de manera general:'. "
            "Luego ofrece una respuesta útil: "
        )
    }

    return profiles.get(personality, "") + text

### Configuracion principal pagina
st.set_page_config(page_title="Drakonius AI", page_icon=LOGO_ICON, layout="wide")
st.logo(LOGO_MAIN, icon_image=LOGO_ICON)

### Estilo / apartado grafico
st.markdown(
    """
    <style>
    body {
        background-color: #E3F2FD;
    }

    /* Animacion burbujas */
    .bubble-animate {
        animation: fadeIn 0.2s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Slider */
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

    /* Selectbox */
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

    /* Burbujas mensajes */
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

###  Cabecera (logo y labels)
# Columnas / espacios
col1, col2, col3 = st.columns([2.5, 2, 1])
with col2:
    st.image(LOGO_ICON, width=130)

st.markdown(
    """
    <h1 style="
    /* Efecto de neon */
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

### Barra de configuraciones 
with st.sidebar:

    st.markdown("### Perfil de la IA")
    personality = st.selectbox(
        "",
        profiles_personalitys,
    )

    st.markdown("### temperatures")
    temperatures = st.slider("", min_value=0.0, max_value=1.0, step=0.1, value=0.5)

    st.markdown("### Modelo Utilizado")
    modelo = st.selectbox(
        "",
        models_IA,
        index=0,
    )

    st.markdown("---")
    if st.button("Resetear conversación"):
        st.session_state.mensajes = []
        st.rerun()

    # Descargar la conversacion
    st.markdown("### Descargar conversación")

    if "mensajes" in st.session_state and st.session_state.mensajes:

        if st.button("Descargar en PDF⬇️"):

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
                    label="Descargar PDF⬇️",
                    data=f.read(),
                    file_name="conversacion.pdf",
                    mime="application/pdf"
                )

### Modelo
chat_model = ChatGoogleGenerativeAI(model=modelo, temperature=temperatures)

### Estados de la sesion
if "chat_model" not in st.session_state:
    st.session_state.chat_model = ChatGoogleGenerativeAI(model=modelo, temperature=temperatures)
    st.session_state.chat_model_modelo = modelo
    st.session_state.chat_model_temp = temperatures
else:
    if st.session_state.chat_model_modelo != modelo or st.session_state.chat_model_temp != temperatures:
        st.session_state.chat_model = ChatGoogleGenerativeAI(model=modelo, temperature=temperatures)
        st.session_state.chat_model_modelo = modelo
        st.session_state.chat_model_temp = temperatures

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

if "archivo_procesado" not in st.session_state:
    st.session_state.processed_file = False

if "bloqueo_input" not in st.session_state:
    st.session_state.block_input = False


### Chat / Historial
chat_area = st.container()

### Comportamiento de las burbujas de dialogo
with chat_area:
    for msg in st.session_state.mensajes:
        role = "assistant" if isinstance(msg, AIMessage) else "user"

        if role == "assistant":
            personalidad_msg = msg.meta.get("personalidad", personality)
            icon = emojis.get(personalidad_msg, "🐲")
        else:
            icon = "👤"
        bubble_class = "bot-bubble" if role == "assistant" else "user-bubble"

        st.markdown(
            f"<div class='{bubble_class} bubble-animate'><b>{icon}</b> {msg.content}</div>",
            unsafe_allow_html=True
        )

st.markdown("---")

### Seccion del input
input_area = st.container()
with input_area:
    col_input, col_files = st.columns([4, 1])

    user_message = None
    archive = None

    ### Columna izquierda: chat input con adjuntar archivos
    with col_input:
        chat_data = st.chat_input(
            "Escribe tu mensaje:",
            disabled=st.session_state.block_input,
            accept_file=True,
            file_type=["txt", "pdf", "doc", "docx"]  # Solo documentos
        )

        if chat_data:
            # Texto
            if hasattr(chat_data, "text") and chat_data.text:
                user_message = chat_data.text

            # Archivo
            if hasattr(chat_data, "files") and chat_data.files:
                archive = chat_data.files[0]
                st.session_state.block_input = True

                tipo_mime, _ = mimetypes.guess_type(archive.name)
                if tipo_mime == "text/plain":
                    user_message = archive.read().decode("utf-8")
                else:
                    user_message = f"[Archivo cargado: {archive.name}]"

    # Columna derecha: expansor de archivos
    with col_files:
        with st.expander("📎 Subir documento"):
            archive_expander = st.file_uploader(
                "Selecciona un archivo",
                type=["txt", "pdf", "doc", "docx"],
                key=f"file_uploader_{st.session_state.uploader_key}_side_expander"
            )

            if archive_expander and not user_message:
                archivo = archive_expander
                st.session_state.block_input = True

                tipo_mime, _ = mimetypes.guess_type(archivo.name)
                if tipo_mime == "text/plain":
                    user_message = archivo.read().decode("utf-8")
                else:
                    user_message = f"[Archivo cargado: {archivo.name}]"

### Respuesta de la IA
if user_message:

    st.session_state.mensajes.append(
    HumanMessage(content=user_message, meta={"personalidad": personality}))

    with chat_area:
        placeholder = st.chat_message("assistant")
        placeholder.write("🐲 Drakonius está escribiendo...")

    respuesta = st.session_state.chat_model.invoke([
        HumanMessage(content=apply_personality(user_message))
    ])

    placeholder.empty()
    
    respuesta.meta = {"personalidad": personality}
    st.session_state.mensajes.append(respuesta)

    st.session_state.uploader_key += 1
    st.session_state.processed_file = False
    st.session_state.block_input = False

    st.rerun()
