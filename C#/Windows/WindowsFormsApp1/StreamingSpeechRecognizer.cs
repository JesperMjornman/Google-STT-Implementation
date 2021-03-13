using System;
using System.Collections.Generic;
using System.Threading.Tasks;

using NAudio.Wave;
using Google.Cloud.Speech.V1;
using System.IO;

namespace GoogleSpeechToText
{
    class StreamingSpeechRecognizer
    {
        static void Init(string pathToAPI)
        {
            Environment.SetEnvironmentVariable("GOOGLE_APPLICATION_CREDENTIALS", pathToAPI);
        }

        static async Task<object> StreamingMicrophoneRecognizeAsync(int seconds = 60, string languageCode = "en-US")
        {
            var speech = SpeechClient.Create();
            var streamingCall = speech.StreamingRecognize();
            await streamingCall.WriteAsync(
                new StreamingRecognizeRequest()
                {
                    StreamingConfig = new StreamingRecognitionConfig()
                    {
                        Config = new RecognitionConfig()
                        {
                            Encoding = RecognitionConfig.Types.AudioEncoding.Linear16,
                            SampleRateHertz = 44100,
                            LanguageCode = languageCode
                        },
                        InterimResults = true,
                    }
                });

            Task printResponses = Task.Run(async () =>
            {
                var responseStream = streamingCall.GetResponseStream();
                while (await responseStream.MoveNextAsync())
                {
                    StreamingRecognizeResponse response = responseStream.Current;
                    Console.WriteLine(response.Results[0].Alternatives[0].Transcript); // Print most probable result.
                }
            });

            object writeLock = new object();
            bool writeMore = true;
            var waveIn = new NAudio.Wave.WaveInEvent();
            waveIn.DeviceNumber = 0;
            waveIn.WaveFormat = new NAudio.Wave.WaveFormat(44100, 1); // 44100Hz Mono.
            waveIn.DataAvailable += (object sender, NAudio.Wave.WaveInEventArgs args) =>
            {
                lock(writeLock)
                {
                    if (!writeMore)
                        return;

                    streamingCall.WriteAsync(
                        new StreamingRecognizeRequest()
                        {
                            AudioContent = Google.Protobuf.ByteString.CopyFrom(args.Buffer, 0, args.BytesRecorded)
                        }).Wait();
                }
            };

            waveIn.StartRecording();
            Console.WriteLine("Speek now.");
            await Task.Delay(TimeSpan.FromSeconds(seconds));

            waveIn.StopRecording();
            lock(writeLock)
            {
                writeMore = false;
            }

            await streamingCall.WriteCompleteAsync();
            await printResponses;
            return 0;
        }
    }
}
