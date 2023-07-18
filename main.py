from transcribe import TranscribeAudio
from dotenv import load_dotenv
import os
load_dotenv()



MP3 = os.environ.get(r"audio_file")
# MP3 = r"A:\New_python\speechToTextVosk\audio_files\transcribing_2.mp3"

try:
    wav_file = TranscribeAudio(MP3)  # Creating object with src file passed in with mp3 file
    wav_file.convertFile()  # Converting mp3 to stereo wav file
    # wav_file.SToM()
    wav_file.monoToText()
except Exception as e:
    print(e)
else:
    print("Transcription complete")
