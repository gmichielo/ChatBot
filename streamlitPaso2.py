# Codigo mejorado con personalización, avatares, indicador de escribiendo,
# descarga de chat, y diseño visual actualizado.

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage
import time
import base64
import json

# ======================================================
# CONFIGURACIÓN PRINCIPAL
# ======================================================
st.set_page_config(page_title="Drakonius AI", page_icon="🤖", layout="wide")

# ------------------------------------------------------
# ESTILOS PERSONALIZADOS (PALETA AZUL)
# ------------------------------------------------------
st.markdown(
    """
    <style>
    body {
        background-color: #E3F2FD;
    }

    /* Contenedor principal del chat */
    .main-container {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    /* Burbuja de usuario */
    .user-bubble {
        background: #BBDEFB;
        padding: 12px;
        border-radius: 12px;
        margin: 8px;
    }

    /* Burbuja del bot */
    .bot-bubble {
        background: #90CAF9;
        padding: 12px;
        border-radius: 12px;
        margin: 8px;
    }

    /* Indicador escribiendo */
    .typing {
        font-style: italic;
        color: #0277BD;
        margin-top: 4px;
    }

    /* Botones */
    .stButton button {
        background-color: #29B6F6 !important;
        color: white !important;
        border-radius: 8px !important;
        border: 1px solid #0288D1 !important;
    }
    .stButton button:hover {
        background-color: #0288D1 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------
# CABECERA
# ------------------------------------------------------
st.markdown(
    """
    <h1 style='text-align: center; color: #29B6F6;'>🤖 Drakonius AI 🐲</h1>
    <p style='text-align: center; font-size: 18px; color: #4FC3F7;'>Chat mejorado con funciones premium</p>
    """,
    unsafe_allow_html=True,
)

# ======================================================
# SIDEBAR
# ======================================================
with st.sidebar:

    st.markdown("### 🤖 Personalidad del Bot")
    personalidad = st.selectbox(
        "",
        [
            "Normal",
            "Amigable",
            "Serio",
            "Sarcástico",
            "Profesional",
        ],
    )

    st.markdown("### 🔥 Temperatura")
    temperatura = st.slider("", min_value=0.0, max_value=1.0, step=0.1, value=0.7)

    st.markdown("### 🤖 Modelo Utilizado")
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

    st.markdown("### 📄 Descargar conversación")

    if "mensajes" in st.session_state and st.session_state.mensajes:
        json_data = json.dumps([m.content for m in st.session_state.mensajes], indent=2)
        b64 = base64.b64encode(json_data.encode()).decode()
        href = f'<a href="data:text/plain;base64,{b64}" download="conversacion.txt">Descargar TXT</a>'
        st.markdown(href, unsafe_allow_html=True)


# ======================================================
# MODELO
# ======================================================
chat_model = ChatGoogleGenerativeAI(model=modelo, temperature=temperatura)

# Crear historial si no existe
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# ======================================================
# FUNCIÓN PARA APLICAR PERSONALIDAD
# ======================================================
def aplicar_personalidad(texto):
    estilos = {
        "Amigable": "😊 Hablo con calidez y cercanía: ",
        "Serio": "🧠 Respondo con formalidad y precisión: ",
        "Sarcástico": "😏 (un poco sarcástico): ",
        "Profesional": "📘 Respuesta técnica y concisa: ",
        "Normal": "",
    }
    return estilos.get(personalidad, "") + texto

# ======================================================
# MOSTRAR HISTORIAL DE CHAT
# ======================================================
for msg in st.session_state.mensajes:
    role = "assistant" if isinstance(msg, AIMessage) else "user"

    icon = "🤖" if role == "assistant" else "👤"
    bubble_class = "bot-bubble" if role == "assistant" else "user-bubble"

    st.markdown(f"<div class='{bubble_class}'><b>{icon}</b> {msg.content}</div>", unsafe_allow_html=True)

# ======================================================
# INPUT DEL USUARIO
# ======================================================
pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    # Mostrar usuario
    st.session_state.mensajes.append(HumanMessage(content=pregunta))
    st.markdown(f"<div class='user-bubble'><b>👤</b> {pregunta}</div>", unsafe_allow_html=True)

    # ----------- Indicador de "Escribiendo..." -----------
    placeholder = st.empty()
    placeholder.markdown("<p class='typing'>🤖 Drakonius está escribiendo...</p>", unsafe_allow_html=True)

    time.sleep(1.2)

    # Responder modelo
    respuesta = chat_model.invoke([
        HumanMessage(content=aplicar_personalidad(pregunta))
    ])

    placeholder.empty()  # Quitamos el "escribiendo"

    # Mostrar respuesta
    st.markdown(f"<div class='bot-bubble'><b>🤖</b> {respuesta.content}</div>", unsafe_allow_html=True)

    st.session_state.mensajes.append(respuesta)
