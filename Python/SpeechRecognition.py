import MicrophoneHandler
import _thread
import shutil
import os

class SpeechRecognition:
    """
    Represents a Speech Recognition handler. 
    This allows for recording microphone audio, stopping the recording and 
    sending a request to Google Cloud services for a Speech To Text action.

    Files will be saved in the preffered_audio_folder or in the default ./audio folder.
    If save_audio_files is False all recorded audio will be deleted on destruction of this object.

    The microphone recording is handled in its own thread by using the MicrophoneHandler.
    """
    def __init__(self, preffered_audio_folder = None, save_audio_files = False):
        self.current_session = []
        self.save_audio_file = save_audio_files
        self.f_extension = '.raw'

        if (preffered_audio_folder == None):
            self.audio_file_folder = './audio'
        else:
            self.audio_file_folder = preffered_audio_folder

        self.microphone_handler = MicrophoneHandler.MicrophoneHandler(self.audio_file_folder)

    def start_record_microphone(self):
        if not os.path.exists(self.audio_file_folder):
            os.makedirs(self.audio_file_folder)

        self.microphone_handler.start_recording()
    
    def stop_record_microphone(self):
        self.microphone_handler.stop_recording()
                  
    def recognize_sync_audio_file(self, file):
        return ""
    
    def __clear_audio_files(self):
        try:
            shutil.rmtree(self.audio_file_folder)
        except:
            print('Failure to clear audio files in {self.audio_file_folder}')

    def __del__(self):
        if not self.save_audio_file:
            self.__clear_audio_files()