import unittest
import os, sys, inspect

sys.path.append(".")

import SpeechRecognition

class TestRecognition(unittest.TestCase):
    
    def test_speech_to_text(self):
        r = SpeechRecognition.SpeechRecognition(API_KEY_LOCATION=os.path.join('C:', 'Users', '46709', 'Downloads', 'GAPI.json'), save_audio_files=True)
        self.assertEqual(r.recognize_sync_audio_file('./audio/2020-10-21_17-38-31.raw'), 'hello hello hello hello hello hello')

if __name__ == '__main__':
    unittest.main()