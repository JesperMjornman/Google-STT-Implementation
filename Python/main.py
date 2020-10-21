import SpeechRecognition
import time
recognizer = SpeechRecognition.SpeechRecognition()

recognizer.start_record_microphone()
time.sleep(5)
recognizer.stop_record_microphone()
