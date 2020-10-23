import SpeechRecognition
import time
import os

recognizer = SpeechRecognition.SpeechRecognition(API_KEY_LOCATION=os.path.join('../_key', 'GAPI.json'), save_audio_files=False)

#recognizer.start_record_microphone()
#time.sleep(5)
#recognizer.stop_record_microphone()
print(recognizer.recognize_sync_audio_file(file='./audio/' + '2020-10-21_17-38-31.raw', return_all_options=False))# + recognizer.current_session[0] + '.raw'))