import requests
import wave
import sys
import time
import alsaaudio

SERVER_URL = "https://samsambackend.replit.app/getaudio"

import subprocess


def play_audio_file_non_blocking(audio_file):
    filename = audio_file
    subprocess.Popen(
        ["ffplay", filename, "-autoexit", "-nodisp"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )

def record_audio(filename="//home//elniko//Downloads//user_audio.wav"):
    f = wave.open(filename, 'wb')
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, channels=2, rate=44100, format=alsaaudio.PCM_FORMAT_S16_LE, periodsize=160, device='default')

    f.setnchannels(2)
    f.setsampwidth(2)
    f.setframerate(44100)

    inp.setperiodsize(160)
    
    loops = 1000000
    while loops > 0:
        loops -= 1
        # Read data from device
        l, data = inp.read()
        
        if l:
            f.writeframes(data)
            time.sleep(.001)
    f.close()
     

def save_audio_to_file(audio_data, filename="user_audio.wav"):
     with wave.open(filename, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(audio_data)

# NON-STREAMING 
import os
import time
import requests

def send_audio_to_server(filename):
    """Sends the audio file to the server and streams the response audio."""
    files = {'audioFile': open(filename, 'rb')}
    response = requests.post(SERVER_URL, files=files, stream=True)

    if response.status_code == 200:
        audio_buffer = bytearray()
        initial_path = "//home//elniko//Downloads//user_audio.wav"
        audio_filename = initial_path + "response_audio.wav"
        sentence_size_threshold = 102400 * 1 / 5 * 3  # Adjust this threshold based on your needs

        for chunk in response.iter_content(chunk_size=102400):
            if chunk:
                audio_buffer.extend(chunk)
                if len(audio_buffer) >= sentence_size_threshold:
                    with open(audio_filename, "wb") as f:
                        f.write(audio_buffer)
                    #os.system(f"mpg123 {audio_filename}")
                    play_audio_file_non_blocking(audio_filename)
                    time.sleep(len(audio_buffer) / 16000 - 1)  # Adjust the sleep time based on the audio sample rate
                    audio_buffer.clear()

        # Handle any remaining audio data
        if audio_buffer:
            with open(audio_filename, "wb") as f:
                f.write(audio_buffer)
            #os.system(f"mpg123 {audio_filename}")
            play_audio_file_non_blocking(audio_filename)
            time.sleep(len(audio_buffer) / 16000 - 1)

        print("Response audio processed.")
    else:
        print(f"Error: Server responded with status code {response.status_code}")




def main():

	play_audio_file_non_blocking("//home//elniko//Downloads//start_2.wav")
	time.sleep(2)
	while True:
		# audio_data = record_audio()
		# Save the recorded audio to a file
		# save_audio_to_file(audio_data, filename="//home//elniko//Samsam_Flask//user_audio.wav")
        
		record_audio(filename="//home//elniko//Downloads//user_audio.wav")
		# Send the audio file to the server and stream the response audio
		send_audio_to_server("//home//elniko//Downloads//user_audio.wav")


if __name__ == "__main__":
    main()

