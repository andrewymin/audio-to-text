from transcribe import TranscribeAudio

MP3 = r"A:\New_python\speechToTextVosk\audio_files\Scribie--Transcription-Test-Practice-Louis-CK-(American-accent-low-difficulty).mp3"
# MP3 = r"A:\New_python\speechToTextVosk\audio_files\transcribing_2.mp3"

# try:
#     wav_file = TranscribeAudio(MP3)  # Creating object with src file passed in with mp3 file
#     wav_file.convertFile()  # Converting mp3 to stereo wav file
#     wav_file.SToM()
#     wav_file.monoToText()
# except Exception as e:
#     print(e)
# else:
#     print("Transcription complete")

try:
    audio_file = TranscribeAudio(MP3)
    if audio_file.audio_time() > 3.3:
        print("File will be too long, need to split")
        # create spliting of mp3 file method into two different files that end with 0, 1
        # later will divide by 3 to see how many times to split audio
        #    using that resulting number split the audio with that number of times with the index number placed at
        #    end of file path name.
except Exception as e:
    print(e)
else:
    print("Finished program")

