from os import path
from pydub import AudioSegment
from pydub.playback import play
# from playsound import playsound
import wave
import audioop
from vosk import Model, KaldiRecognizer
import json
import time
from mutagen.mp3 import MP3


class TranscribeAudio:
    def __init__(self, recording):
        self.src = recording
        self.audio = MP3(recording)
        self.endingMp3 = 'audio_files/notification_sound.mp3'
        self.languageModel = r'A:\New_python\speechToTextVosk\vosk_lang\vosk-model-small-en-us-0.15'
        # self.languageModel = r'A:\New_python\speechToTextVosk\vosk_lang\vosk-model-en-us-0.22'
        # self.languageModel = r'A:\New_python\speechToTextVosk\vosk_lang\vosk-model-en-us-0.42-gigaspeech'
        self.stereoFile = r"A:\New_python\speechToTextVosk\audio_files\transcribing_test.wav"
        self.monoFile = r"A:\New_python\speechToTextVosk\audio_files\test_conversion_mono.wav"
        self.timeStamps = "timestamp_results.json"
        self.transcription = "results_text.json"

    def convert(self, seconds):
        # seconds %= 3600
        mins = seconds // 60
        seconds %= 60
        return mins, seconds

    def audio_time(self):
        audio_info = self.audio.info
        length_in_secs = int(audio_info.length)
        mins, seconds = self.convert(length_in_secs)
        print(f"Minutes: {mins}\nSeconds: {seconds}")
        t = float(f"{mins}.{seconds}")
        return t

    def convertFile(self):
        sound = AudioSegment.from_mp3(self.src)
        sound.export(self.stereoFile, format="wav")
        print("Successfully converted mp3 to wav")

    def endingSound(self):
        finished_sound = AudioSegment.from_mp3(self.endingMp3)
        play(finished_sound)

    def SToM(self):
        try:
            inFile = wave.open(self.stereoFile, 'rb')
            outFile = wave.open(self.monoFile, 'wb')

            outFile.setnchannels(1)

            outFile.setsampwidth(inFile.getsampwidth())
            outFile.setframerate(inFile.getframerate())

            soundBytes = inFile.readframes(inFile.getnframes())
            print("frames read: {} length: {}".format(inFile.getnframes(), len(soundBytes)))

            monoSoundBytes = audioop.tomono(soundBytes, inFile.getsampwidth(), 1, 1)
            outFile.writeframes(monoSoundBytes)

        except Exception as e:
            print(f"Error from STom: {e}")

        finally:
            inFile.close()
            outFile.close()

    def monoToText(self):
        startTime = time.time()  # Get current time when run
        wf = wave.open(self.monoFile, "rb")

        # initialize a str to hold results
        results = ""
        textResults = []

        # build the model and recognizer objects.
        model = Model(self.languageModel)
        recognizer = KaldiRecognizer(model, wf.getframerate())
        recognizer.SetWords(True)

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                recognizerResult = recognizer.Result()
                results = results + recognizerResult
                # convert the recognizerResult string into a dictionary
                resultDict = json.loads(recognizerResult)
                # save the 'text' value from the dictionary into a list
                textResults.append(resultDict.get("text", ""))

           # else:
           #     print(recognizer.PartialResult())

        # process "final" result
        # print(json.loads(recognizer.FinalResult())['text'])
        finalText = recognizer.FinalResult()
        # print(finalText)
        results = results + finalText
        resultDict = json.loads(finalText)
        # print(resultDict['text'])
        textResults.append(resultDict.get("text", ""))

        # write results to a file
        with open(self.timeStamps, 'w') as output:
            print(results, file=output)

        # write text portion of results to a file
        with open(self.transcription, 'w') as output:
            text_string = " ".join(textResults)
            text = text_string.replace(" i ", " I ").replace("i'", "I'")

            json.dump(text, output, indent=4)

        self.endingSound()

        endTime = time.time()
        total_time = endTime - startTime
        minutes = int(total_time / 60)
        seconds = int(total_time % 60)
        print(f'Total time it took to transcribe is {minutes}:{seconds}')

