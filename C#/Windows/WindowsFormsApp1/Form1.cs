using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using GoogleSpeechToText;

using System.Runtime.InteropServices;

namespace WindowsFormsApp1
{
    public partial class Form1 : Form
    {
        SpeechRecognizer Recognizer = new SpeechRecognizer(@"C:\Users\46709\Downloads\GAPI.json");
        public Form1()
        {
            InitializeComponent();
            label1.Text = "Idle.";
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Recognizer.RecordAudio(sender, e);
            label1.Text = "Recording: " + Recognizer.Session[^1];
            button2.Enabled = true;
        }

        private void button2_Click(object sender, EventArgs e)
        {
            Recognizer.StopRecording(sender, e);
            label1.Text = "Stop recording.";
            textBox1.Text = Recognizer.RecentRecognized;
            button2.Enabled = false;
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            AllocConsole(); // See console.
        }

        [DllImport("kernel32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        static extern bool AllocConsole();
    }
}
