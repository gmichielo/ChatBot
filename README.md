# 🐲 Drakonius AI — Chatbot para Desarrollo de Videojuegos

**Drakonius AI** es un chatbot interno de **Drakonius Studios** diseñado para asistir en tareas relacionadas al desarrollo de videojuegos: programación, animación, rigging, narrativa, shaders y más.
Está construido con **Streamlit**, **LangChain**, **Gemini** y **ReportLab**.

---

## Características
### Multi-personalidad
El chatbot permite seleccionar distintos perfiles, cada uno adaptando el estilo de respuesta:
- 🐉 Generalista
- 🚻 Rigger
- 🎦 Animador
- 💻 Programador
- 🌈 Shaders / Technical Artist
- 📖 Narrador  
Cada personalidad añade contexto único gracias al sistema interno de "prompting".

### Exportación de conversaciones a PDF
Usando ReportLab, el usuario puede descargar el chat completo formateado y ordenado.

### Soporte de archivos
Puedes subir archivos de tipo:
- .txt
- .pdf
- .doc
- .docx    
El bot detecta el tipo y procesa el contenido en caso de ser texto plano.

### Modelos de IA usados
El bot dado que esta hecho con Gemini comko base pues puede utilizar esto modelos a fecha de este README
- gemini-2.5-flash
- gemini-2.5-flash-preview-09-2025
- gemini-2.5-flash-lite
- gemini-2.5-pro

---

## Tecnologías usadas
- Python
- Streamlit
- JavaScript  
- HTML / CSS
  
---

## Dependencias a Instalar

- pip install streamlit
- pip install langchain_google_genai
- pip install langchain 
- pip install reportlab 
  
---

## 📁 Estructura del proyecto
.     
├── images/              
├── DrakoniusAI.py              
├── streamlitPaso2.py              
├── requirements.txt                   
└── README.md              
