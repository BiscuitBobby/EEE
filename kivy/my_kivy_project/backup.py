import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import pyaudio
import socket

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Set the audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Initialize the speech recognizer
recognizer = sr.Recognizer()
transcribe = True

def transcribe_audio():
    with sr.Microphone() as source:
        print("Listening...")
        audio_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

        audio_chunks = []
        silence_threshold = -40

        bd_addr = "B0:A7:32:F2:C2:22"  # itade address
        port = 1

        sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        sock.connect((bd_addr, port))

        print("Connected")
        sock.settimeout(1.0)
        sock.send(bytes('*', 'utf-8'))
        strt = 0
        while transcribe:
            data = audio_stream.read(CHUNK)
            audio_chunks.append(data)

            if len(audio_chunks) > 120:  # Process audio in chunks of 20 frames
                audio_segment = AudioSegment(data=b''.join(audio_chunks), sample_width=2, frame_rate=RATE, channels=1)
                audio_chunks = []

                # Split audio on silence
                chunks = split_on_silence(audio_segment, min_silence_len = 500, silence_thresh=silence_threshold)

                for chunk in chunks:
                    audio_data = sr.AudioData(chunk.raw_data, sample_rate=RATE, sample_width=chunk.sample_width)
                    try:
                        # Convert speech to text
                        text = recognizer.recognize_google(audio_data)
                        print(text)

                        if strt>=5:
                            sock.send(bytes("*", 'utf-8'))
                        sock.send(bytes(text, 'utf-8'))
                        sock.send(bytes('|', 'utf-8'))
                        strt+=1

                    except sr.UnknownValueError:
                        pass
                    except sr.RequestError as e:
                        print("Error requesting recognition:", str(e))
        sock.close()
        audio_stream.stop_stream()
        audio_stream.close()

#transcribe_audio()
# ----- #

def get_large_audio_transcription_on_silence(path):
    #Splitting the large audio file into chunks

    sound = AudioSegment.from_file(path)
    # split audio sound where silence is 500 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        min_silence_len = 500,
        silence_thresh = sound.dBFS-14,
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""

    for i, audio_chunk in enumerate(chunks, start=1):

        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")

        try:
            text = transcribe_audio(chunk_filename)
        except sr.UnknownValueError as e:
            print("Error:", str(e))
        else:
            text = f"{text.capitalize()}. "
            print(chunk_filename, ":", text)
            whole_text += text

    return whole_text
