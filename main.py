from transcribe import TranscribeAudio
import os

MP3 = rf"{os.getcwd()}\audio_files\transcribing_2.mp3"
Model = rf'{os.getcwd()}\vosk_lang\vosk-model-en-us-0.22'

try:
    wav_file = TranscribeAudio(MP3, Model)  # Creating object with src file passed in with mp3 file
    wav_file.convertFile()  # Converting mp3 to stereo wav file
    wav_file.SToM() # Convert stereo to mono
    wav_file.monoToText() # transcribe mono to text
except Exception as e:
    print(e)
else:
    print("Transcription complete")
