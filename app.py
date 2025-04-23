from flask import Flask, render_template, request, send_file
from moviepy import VideoFileClip
from transformers import pipeline
from gtts import gTTS
from moviepy.video.io.VideoFileClip import VideoFileClip as mpVideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
#from moviepy.audio.AudioClip import CompositeAudioClip
import os
import torch
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

app = Flask(__name__)

# Load environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Helper functions
def get_audio_from_video(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

def get_text_from_audio(audio_path):
    whisper = pipeline("automatic-speech-recognition", "openai/whisper-large-v3", torch_dtype=torch.float16, device="cuda:0")
    transcription = whisper(audio_path)
    return transcription

def text_translation(google_api_key, transcription, desired_lang):
    summary_prompt = """
    You are a translator where you have given an input: {input_text}
    And you need to translate this input text into {desired_language} language.
    """
    prompt_template = PromptTemplate(input_variables=["input_text", "desired_language"], template=summary_prompt)
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=google_api_key)
    chain = prompt_template | llm | StrOutputParser()
    res = chain.invoke({"input_text": transcription["text"], "desired_language": desired_lang})
    return res

def text_to_speech(res):
    audio = gTTS(text=res, lang='hi', slow=False)
    return audio

# Removed adjust_audio_speed function, directly using the translated audio with the video

def adding_audio_to_video(original_video_path, translated_audio, new_video_path):
    videoclip = mpVideoFileClip(original_video_path)
    
    # Convert the gTTS object to a temporary audio file
    temp_audio_path = "static/temp_translated_audio.mp3"
    translated_audio.save(temp_audio_path)
    
    # Create an AudioFileClip object for the translated audio
    audioclip = AudioFileClip(temp_audio_path)
    videoclip.audio = audioclip
    videoclip.write_videofile(new_video_path)

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'video_file' not in request.files:
        return "No video file uploaded."

    video_file = request.files['video_file']
    video_path = os.path.join('static', 'uploads', video_file.filename)
    video_file.save(video_path)

    return render_template('language_selection.html', video_path=video_path)

@app.route('/translate', methods=['POST'])
def translate():
    video_path = request.form['video_path']
    desired_lang = request.form['language']

    # Extract audio from video
    audio_path = "static/temp_audio.mp3"
    get_audio_from_video(video_path, audio_path)

    # Transcribe audio to text
    transcription = get_text_from_audio(audio_path)
    
    # Translate the text
    res = text_translation(google_api_key, transcription, desired_lang)

    # Convert translated text to speech
    translated_audio = text_to_speech(res)

    # Combine translated audio with the original video
    output_video_path = "static/output_video.mp4"
    adding_audio_to_video(video_path, translated_audio, output_video_path)

    return render_template('result.html', original_video=video_path, translated_video=output_video_path)



@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
