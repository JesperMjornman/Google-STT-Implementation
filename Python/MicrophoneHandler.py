import pyaudio
import wave
import datetime
import time
import os
from threading import Thread

class MicrophoneHandler:
    """
    Represents a microphone handler for recording and saving audio recorded.
    Uses PyAudio to record audio and stores the recorded files which will be saved
    and named in the format specified by the caller. 
    If no specification is made it will default to a timestamp. 
    
    All files will be saved in the specified "audio_folder".   
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
        Creates a new thread for recording audio.
        Currently only supports one thread, any more may cause issues.

        filename -- filename of current recording, if None it will default to a timestamp.
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
        """
        Stops recording, waits for thread to finish.
        Returns the filename of the new audio file.
        """
        print('Stopping recording.')
        self.recording = False
        self.__active_thread.join()
        return self.current_session

    def __active_recording(self, filename=None):
        print('Recording: {}'.format(filename))
        stream = self.paudio.open(
            format             = self.FORMAT,
            channels           = self.CHANNELS,
            rate               = self.RATE,
            input              = True,
            input_device_index = 0,
            frames_per_buffer  = self.CHUNK
        )
       
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
    
    #def __active_streaming(self, filename=None):
