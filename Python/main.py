import SpeechRecognition
import time
import os
from threading import Thread

recognizer = SpeechRecognition.SpeechRecognition(
        API_KEY_LOCATION=os.path.join('../_key', 'GAPI.json'), 
        save_audio_files=True
)

#recognizer.start_record_microphone()
#time.sleep(5)
#recognizer.stop_record_microphone()
#active_thread = Thread(target=recognizer.recognize_async_audio_stream, args=(  ) )       
#active_thread.start()
recognizer.recognize_async_audio_stream()
time.sleep(5)
recognizer.stop_record_microphone()
print(recognizer.recognize_sync_audio_file(file='./audio/' + '2020-10-21_17-38-31.raw', language_code="en-US", return_options=None)) # + recognizer.current_session[0] + '.raw'))