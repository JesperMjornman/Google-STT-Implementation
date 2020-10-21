import MicrophoneHandler
import _thread
import shutil
import os
import io

from google.cloud import speech

class SpeechRecognition:
    """
    Represents a Speech Recognition handler. 
    This allows for recording microphone audio, stopping the recording and 
    sending a request to Google Cloud services for a Speech To Text action.

    Files will be saved in the preffered_audio_folder or in the default ./audio folder.
    If save_audio_files is False all recorded audio will be deleted on destruction of this object.

    The microphone recording is handled in its own thread by using the MicrophoneHandler.
    """
    def __init__(self, API_KEY_LOCATION, preffered_audio_folder = None, save_audio_files = False):
        # Set environment variable.
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = API_KEY_LOCATION
        
        self.current_session = []
        self.save_audio_file = save_audio_files
        self.client = speech.SpeechClient()

        if (preffered_audio_folder == None):
            self.audio_file_folder = './audio'
        else:
            self.audio_file_folder = preffered_audio_folder

        self.microphone_handler = MicrophoneHandler.MicrophoneHandler(self.audio_file_folder)

    def start_record_microphone(self):
        """
        Start recording from microphone.
        Will create a audio folder to save the recorded files.
        The files will be removed in the deconstructor if specified.
        """
        if not os.path.exists(self.audio_file_folder):
            os.makedirs(self.audio_file_folder)

        self.microphone_handler.start_recording()
        self.current_session.append(self.microphone_handler.current_session)

    def stop_record_microphone(self):
        """
        Stop recording.
        """
        self.microphone_handler.stop_recording()
                  
    def recognize_sync_audio_file(self, file, return_all_options = False):
        """
        Send audio to Google API for Speech To Text and
        return the string representation of the audio.
        
        file is the filepath to file for STT      
        """
        with io.open(file, "rb") as audio_file:
            content = audio_file.read()
            audio = speech.RecognitionAudio(content=content)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.microphone_handler.RATE,
            language_code="en-US",
        )

        response = self.client.recognize(config=config, audio=audio)
        
        if (len(response.results) == 0):
            return 'Failed to find any transcripts.'
        elif not return_all_options: 
            return response.results[0].alternatives[0].transcript
        else:
            return response.results
    
    def __clear_audio_files(self):
        """
        Clear all audio files from specified audio folder.
        """
        try:
            shutil.rmtree(self.audio_file_folder)
        except:
            print('Failure to clear audio files in {self.audio_file_folder}')

    def __del__(self):
        """
        Deconstructor.
        Remove all audio files if save_audio_file is False
        """
        if not self.save_audio_file:
            self.__clear_audio_files()