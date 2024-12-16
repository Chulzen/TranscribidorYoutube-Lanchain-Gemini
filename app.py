import streamlit as st
from dotenv import load_dotenv
load_dotenv()#cargara todas lasvariables del enviroment
import google.generativeai as genai
import os

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""Tu eres un resumidos de videos de Yotube. Vas a tomar el texto de youtube y vas a resumir 
el video completo y proveeras un resumen importante en puntos dentro de 250 palabras. porfavor dame el resumen del texto entregado aca:  """

def extraccion_detalles_video(youtube_video_url):#obtenemos la informacion de os videos
    try:
        video_id=youtube_video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = " "
        for i in transcript_text:
            transcript+= " " + i["text"]
        
        return transcript

    except Exception as e:
        return e

def generate_gemini_content(transcript_text,prompt):#aca interactuamos con el modelo de AI
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text


st.title("Transcribidor de youtube a notas detalladas")
youtube_link = st.text_input("Dame el link del video")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

if st.button("Notas detalladas"):
    transcript_text= extraccion_detalles_video(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Notas detalladas")
        st.write(summary)
        