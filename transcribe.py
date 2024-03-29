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
import os


class TranscribeAudio:
    def __init__(self, recording, model):
        self.current_dir = os.getcwd()
        self.src = recording
        self.audio = MP3(recording)
        self.endingMp3 = 'notification_sound.mp3'
        self.languageModel = model
        self.stereoFile = rf"{self.current_dir}\audio_files\wav_files\transcribing_test.wav"
        self.monoFile = rf"{self.current_dir}\audio_files\mono_files\test_conversion_mono.wav"
        self.timeStamps = rf"{self.current_dir}\results\timestamp_results.json"
        self.transcription = rf"{self.current_dir}\results\results_text.json"
        self.cutOffTime = 3.4
        self.seconds = 60
        self.timeLimit = 3
        self.startTime = 0.0
        self.endTime = 180.0  # This is the start of one split at for 3 min
        self.splits = 0

    def convert(self, seconds):
        # seconds %= 3600
        mins = seconds // self.seconds
        seconds %= self.seconds
        return mins, seconds

    def audio_time(self):
        audio_info = self.audio.info
        length_in_secs = int(audio_info.length)
        mins, seconds = self.convert(length_in_secs)
        # print(f"Minutes: {mins}\nSeconds: {seconds}")
        t = float(f"{mins}.{seconds}")
        return t

    def convertFile(self):

        sound = AudioSegment.from_mp3(self.src)

        if self.audio_time() <= self.cutOffTime:
            sound.export(self.stereoFile, format="wav")
            return print("Successfully converted mp3 to wav")

        # print("File will be too long, need to split")
        num_of_splits = int(float(self.audio_time()) // self.timeLimit)
        self.splits = num_of_splits
        # print(num_of_splits)
        if num_of_splits == 1:  # This means if there's only one split
            startTime = self.startTime
            endTime = self.endTime
            # cut it to length (if needed)
            beginning_cut = sound[startTime * 1000:endTime * 1000]
            # export sound cut as wav file
            beginning_cut.export(rf"{self.current_dir}\audio_files\wav_files\transcribing_test{0}.wav", format="wav")
        else:
            for n in range(num_of_splits):
                startTime = self.startTime
                endTime = self.endTime
                # cut it to length (if needed)
                cut = sound[startTime * 1000:endTime * 1000]
                # export sound cut as wav file
                cut.export(rf"{self.current_dir}\audio_files\wav_files\transcribing_test{n}.wav", format="wav")

                self.startTime = endTime  # new start time is last end time
                if n != num_of_splits - 1:
                    self.endTime = endTime * 3

        startTime = self.endTime
        audio_info = self.audio.info
        total_sec = int(audio_info.length)
        # total_sec %= self.seconds
        # print(f"start: {startTime} total: {total_sec}")
        # remainingTime = (total_sec - self.endTime)
        # print(f"remaining: {total_sec}")
        remaining_cut = sound[startTime * 1000:total_sec * 1000]
        remaining_cut.export(rf"{self.current_dir}\audio_files\wav_files\transcribing_test{num_of_splits}.wav", format="wav")

    def endingSound(self):
        finished_sound = AudioSegment.from_mp3(self.endingMp3)
        play(finished_sound)

    def multi_spits(self):
        # create method to make SToM and monoToText DRY
        pass

    def SToM(self): # stereo to mono
        if self.splits != 0:
            # print(self.splits)
            for n in range(self.splits):
                try:
                    inFile = wave.open(rf"{self.current_dir}\audio_files\wav_files\transcribing_test{n}.wav", 'rb')
                    outFile = wave.open(rf"{self.current_dir}\audio_files\mono_files\test_conversion_mono{n}.wav", 'wb')

                    outFile.setnchannels(1)

                    outFile.setsampwidth(inFile.getsampwidth())
                    outFile.setframerate(inFile.getframerate())

                    soundBytes = inFile.readframes(inFile.getnframes())

                    monoSoundBytes = audioop.tomono(soundBytes, inFile.getsampwidth(), 1, 1)
                    outFile.writeframes(monoSoundBytes)
                except Exception as e:
                    print(f"Error from STom: {e}")
                finally:
                    inFile.close()
                    outFile.close()
            try:
                inFile = wave.open(rf"{self.current_dir}\audio_files\wav_files\transcribing_test{self.splits}.wav", 'rb')
                outFile = wave.open(rf"{self.current_dir}\audio_files\mono_files\test_conversion_mono{self.splits}.wav", 'wb')

                outFile.setnchannels(1)

                outFile.setsampwidth(inFile.getsampwidth())
                outFile.setframerate(inFile.getframerate())

                soundBytes = inFile.readframes(inFile.getnframes())

                monoSoundBytes = audioop.tomono(soundBytes, inFile.getsampwidth(), 1, 1)
                outFile.writeframes(monoSoundBytes)
            except Exception as e:
                print(f"Error from STom: {e}")
            finally:
                inFile.close()
                outFile.close()

        try:
            inFile = wave.open(self.stereoFile, 'rb')
            outFile = wave.open(self.monoFile, 'wb')

            outFile.setnchannels(1)

            outFile.setsampwidth(inFile.getsampwidth())
            outFile.setframerate(inFile.getframerate())

            soundBytes = inFile.readframes(inFile.getnframes())
            # print("frames read: {} length: {}".format(inFile.getnframes(), len(soundBytes)))

            monoSoundBytes = audioop.tomono(soundBytes, inFile.getsampwidth(), 1, 1)
            outFile.writeframes(monoSoundBytes)
        except Exception as e:
            print(f"Error from STom: {e}")
        finally:
            inFile.close()
            outFile.close()

    def monoToText(self):
        startTime = time.time()  # Get current time when run

        # initialize a str to hold results
        results = ""
        textResults = []

        if self.splits != 0:
            # print(self.splits)
            for n in range(self.splits):
                # Changed the open file to a wav file instead of mono due to pitch problems
                wf = wave.open(rf"{self.current_dir}\audio_files\wav_files\transcribing_test{n}.wav", "rb")

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

                # process "final" result
                # print(json.loads(recognizer.FinalResult())['text'])
                finalText = recognizer.FinalResult()
                # print(finalText)
                results = results + finalText
                resultDict = json.loads(finalText)
                # print(resultDict['text'])
                textResults.append(resultDict.get("text", ""))

                # write results to a file
                with open(rf"{self.current_dir}\results\timestamp_results{n}.json", 'w') as output:
                    print(results, file=output)

                # write text portion of results to a file
                with open(rf"{self.current_dir}\results\results_text{n}.json", 'w') as output:
                    text_string = " ".join(textResults)
                    text = text_string.replace(" i ", " I ").replace("i'", "I'")
                    json.dump(text, output, indent=4)

            wf = wave.open(rf"{self.current_dir}\audio_files\wav_files\transcribing_test{self.splits}.wav", "rb")
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

            # process "final" result
            # print(json.loads(recognizer.FinalResult())['text'])
            finalText = recognizer.FinalResult()
            # print(finalText)
            results = results + finalText
            resultDict = json.loads(finalText)
            # print(resultDict['text'])
            textResults.append(resultDict.get("text", ""))

            # write results to a file
            with open(rf"{self.current_dir}\results\timestamp_results{self.splits}.json", 'w') as output:
                print(results, file=output)

            # write text portion of results to a file
            with open(rf"{self.current_dir}\results\results_text{self.splits}.json", 'w') as output:
                text_string = " ".join(textResults)
                text = text_string.replace(" i ", " I ").replace("i'", "I'")
                json.dump(text, output, indent=4)

            self.endingSound()

            endTime = time.time()
            total_time = endTime - startTime
            minutes = int(total_time / self.seconds)
            seconds = int(total_time % self.seconds)

            return print(f'Total time it took to transcribe is {minutes}:{seconds}')

        wf = wave.open(self.stereoFile, "rb")

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
        minutes = int(total_time / self.seconds)
        seconds = int(total_time % self.seconds)
        print(f'Total time it took to transcribe is {minutes}min:{seconds}sec')

