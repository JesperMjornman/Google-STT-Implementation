import pyaudio
import wave
import datetime
import time
import os
from threading import Thread

class MicrophoneHandler:
    """
    Represents a microphone handler for recording and saving audio recorded.
    Uses PyAudio to record audio and stores the recorded files in which will be saved
    in the format specified by the caller or a defaults to a timestamp. 
    All files will be saved in the specified "audio_folder".
    All audio will be recorded in MONO, if need be change the CHANNELS to any number to use.
    """
    def __init__(self, audio_folder):
        self.CHUNK     = 1024
        self.FORMAT    = pyaudio.paInt16  
        self.RATE      = 44100
        self.CHANNELS  = 1
        self.EXTENSION = '.raw'

        self.recording       = False
        self.current_session = None
        self.audio_folder    = audio_folder
        self.paudio          = pyaudio.PyAudio()
        
        self.__active_thread = None
        
    def start_recording(self, filename = None):
        """
        Starts recording the default microphone.
        Should be created as a separate thread to allow it to record for as long as needed.
        """
        if (self.paudio.get_device_count() < 1):
            print('Failed to identify any microphone!')
            return

        if (filename == None):
            filename = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')

        self.current_session = filename
        self.__active_thread = Thread(target=self.__active_recording, args=( filename, ) )
        self.__active_thread.start()
        
            

    def stop_recording(self):
        print('Stopping recording.')
        self.recording = False
        self.__active_thread.join() 

    def __active_recording(self, filename=None):
        print('Recording: {}'.format(filename))
        stream = self.paudio.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate = self.RATE,
                                  input=True,
                                  input_device_index=0,
                                  frames_per_buffer=self.CHUNK)
       
        self.recording = True       
        frames = []
        try:
            while(self.recording is True):
                data = stream.read(self.CHUNK)
                frames.append(data)
        except:
            print('Error when recording audio.')

        stream.stop_stream()
        stream.close()
        self.paudio.terminate()

        try:          
            file = wave.open(os.path.join(self.audio_folder, filename) + self.EXTENSION, 'wb')
            file.setnchannels(self.CHANNELS)
            file.setsampwidth(self.paudio.get_sample_size(self.FORMAT))
            file.setframerate(self.RATE)
            file.writeframesraw(b''.join(frames))
            file.close()
        except:
            print('Failure to write file {}{}'.format(filename, self.EXTENSION))