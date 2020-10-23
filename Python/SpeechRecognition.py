import MicrophoneHandler
import _thread
import shutil
import os
import io

from google.cloud import speech
from google.protobuf.json_format import MessageToDict, MessageToJson

class SpeechRecognition:
    """
    Represents a Speech Recognition handler. 
    This allows for recording microphone audio, stopping the recording and 
    sending a request to Google Cloud services for a Speech To Text action.

    Files will be saved in the preffered_audio_folder or in the default ./audio folder.
    If save_audio_files is False all recorded audio will be deleted on destruction of this object.
    The microphone recording is handled in its own thread by using the MicrophoneHandler.
   
    ---

    API_KEY_LOCATION -- path to the API KEY json file

    preffered_audio_folder -- preffered folder for recorded audio files (defaults to ./audio)

    save_audio_files -- save audio files after program is finished if True else remove all recorded files.
    """
    def __init__(self, API_KEY_LOCATION, preffered_audio_folder = None, save_audio_files = False):
        # Set environment variable.
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = API_KEY_LOCATION
        
        self.current_session = []
        self.save_audio_file = save_audio_files
        self.client = speech.SpeechClient()
        self.record_length = 0

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
        Stop recording, saves audio file.

        Returns the filename of the audio file.
        """
        return self.microphone_handler.stop_recording()
                  
    def recognize_sync_audio_file(self, file, return_dict_object = False, is_long_recording = False, return_all_options = False):
        """
        Send audio through Google API for Speech To Text and
        return the string representation of the audio.
        
        If return_all_options is set it will return a str object of the results message.
        
        Args:
            file -- the filepath to file for STT     
            return_all_options -- option to return .json array of found alternatives or the only the most likely. 
            return_dict_object -- return the full dictionary object of the most probable alternative.
        """
        with io.open(file, "rb") as audio_file:
            content = audio_file.read()
            audio = speech.RecognitionAudio(content=content)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.microphone_handler.RATE,
            language_code="en-US",
        )

        try:
            response = self.client.long_running_recognize(config=config, audio=audio, timeout=500).result()   
            if return_dict_object:
                return self.__get_message_from_proto(response) 
            elif not return_all_options: 
                return self.__get_message_from_proto(response)['transcript']
            else:
                return str(response)
        except:
            return ''
    
    def __clear_audio_files(self):
        """
        Clear all audio files from set audio folder.
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

    def __get_message_from_proto(self, message) -> dict: 
        """
        Return the most confident transcript from google.protobuf

        Args:
            message -- the protobuf message received when translating.
        """     
        result = { 'transcript' : '' , 'confidence' : 0.0 }
        try:
            alt = str(message).split('alternatives {')[1].split('}')[0]     
            
            if (alt.find('transcript:') != -1):
                alt = alt.split('\"')
                result['transcript'] = alt[1]
                result['confidence'] = alt[2].split(':')[1]
        except:
            result['transcript'] = ''
            result['confidence'] = 0.0

        return result
