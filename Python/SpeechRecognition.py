
class SpeechRecognition:
    def __init__(self, preffered_audio_folder = None):
        self.current_session = []
        self.save_audio_file = False
        self.sample_rate = 44100
        self.channels = 1 # Mono
        self.f_extension = '.raw'

        if (preffered_audio_folder == None):
            self.audio_file_folder = './audio'
        else:
            self.audio_file_folder = preffered_audio_folder

   # def start_record_microphone(self):

   # def stop_record_microphone(self):

    def recognize_sync_audio_file(self, file):
        return ""
    
    #def __clear_audio_files(self):