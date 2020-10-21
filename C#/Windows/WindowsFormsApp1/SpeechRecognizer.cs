using System;
using System.Collections.Generic;

using NAudio.Wave;
using Google.Cloud.Speech.V1;
using System.IO;

namespace GoogleSpeechToText
{
    /// <summary>
    /// Represents a handler for recording audio and parsing it to the Google API to get STT.
    /// Needs to be in a WinForms project, i.e. buttons to record and stop recording.
    /// </summary>
    class SpeechRecognizer
    {
        private const string audioFilesFolder = @"./tmp/";
        private const int sampleRate = 44100;
        private WaveIn waveIn;
        private WaveFileWriter waveWriter;

        /// <summary>
        /// Constructor.
        /// </summary>
        /// <param name="pathToAPI">Path to the API key used for speech recognition cloud.</param>
        public SpeechRecognizer(string pathToAPI)
        {
			/*
			 * Some problems with setting the Environment variable led to this implementation.
			 * Make sure that the pathToAPI ends with .json (i.e. the full filepath). 
			 */
            Environment.SetEnvironmentVariable("GOOGLE_APPLICATION_CREDENTIALS", pathToAPI);
            Session = new List<string>();
        }

        /// <summary>
        /// If set to true, all recorded audio files will be removed when recognition is received.
        /// This includes Audio files from earlier sessions which are still in the "audioFilesFolder".
        /// </summary>
        public bool SaveAudioFiles { get; set; } = false;

        /// <summary>
        /// List containing timestamps of this session's recordings
        /// </summary>
        public List<string> Session { get; }

        /// <summary>
        /// Most recently recognized Speech to Text. (latest recording sent through google API).
        /// </summary>
        public string RecentRecognized { get; set; }

        /// <summary>
        /// Record the microphone's audio.
        /// The microphone is recorded in 44100 samplerate and uses mono channel.
        /// </summary>
        /// <returns>Name of the recorded file. (yyyy-MM-dd_HH-mm-ss)</returns>
        public string RecordAudio(object sender, EventArgs e)
        {
            if (NAudio.Wave.WaveIn.DeviceCount < 1)
            {
                Console.WriteLine("No microphone detected!");
                return null;
            }

            // Set wave format.
            waveIn = new WaveIn();
            waveIn.DeviceNumber = 0;
            waveIn.WaveFormat = new WaveFormat(sampleRate, 1); //Use mono for google.  // WaveIn.GetCapabilities(waveIn.DeviceNumber).Channels);

            string timestamp = DateTime.Now.ToString("yyyy-MM-dd_HH-mm-ss");
            Directory.CreateDirectory("./tmp");
            waveIn.DataAvailable += new EventHandler<WaveInEventArgs>(WaveInDataAvailable);
            waveWriter = new WaveFileWriter(audioFilesFolder + timestamp + ".raw", waveIn.WaveFormat);

            Console.WriteLine("Recording to /tmp/" + timestamp + ".raw");
            Session.Add(timestamp);

            waveIn.StartRecording();
            return timestamp;
        }

        /// <summary>
        /// Stops the recording of selected microphone.
        /// Writes a .raw audio file named after the timestamp of the start of recording.
        /// If saveAudioFiles is false the /tmp/ folder and all its children will be deleted.
        /// </summary>
        /// <returns>string representation of recorded audio (via Google API).</returns>
        public string StopRecording(object sender, EventArgs e)
        {
            if (waveIn != null)
            {
                waveIn.StopRecording();
                waveIn.Dispose();
                waveIn = null;
            }

            if (waveWriter != null)
            {
                waveWriter.Dispose();
                waveWriter = null;
            }

            try
            {
                byte[] bFAudio = File.ReadAllBytes(Path.Combine(audioFilesFolder, Session[^1] + ".raw"));
                RecentRecognized = RecognizeSpeech(bFAudio);
                Console.WriteLine("result: {0}", RecentRecognized);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Failed to read audio file: " + Session[^1] + ".raw" + "\n\n" + ex);
                return null;
            }

            if (!SaveAudioFiles)
            {
                try
                {
                    foreach (FileInfo f in (new DirectoryInfo(audioFilesFolder)).GetFiles())
                    {
                        f.Delete();
                    }
                    Directory.Delete(audioFilesFolder);
                }
                catch (Exception ex)
                {
                    Console.WriteLine("No recordings found.\n=====\n" + ex.Message + "\n=====");
                }
            }
            return RecentRecognized;
        }

        public string RecognizeSpeech(byte[] file)
        {
            var speech = SpeechClient.Create();
            var response = speech.Recognize(new RecognitionConfig()
            {
                Encoding = RecognitionConfig.Types.AudioEncoding.Linear16,
                SampleRateHertz = 44100,
                LanguageCode = "en",
            }, RecognitionAudio.FromBytes(file));

            return response.Results[0].Alternatives[0].Transcript;
        }

        private void WaveInDataAvailable(object sender, WaveInEventArgs e)
        {
            if (waveWriter == null) return;

            waveWriter.Write(e.Buffer, 0, e.BytesRecorded);
            waveWriter.Flush();
        }
    }
}
