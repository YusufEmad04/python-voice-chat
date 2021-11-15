import socket
import threading
import pyaudio

ip="127.0.0.1"
port = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
p = pyaudio.PyAudio()
audio_format = pyaudio.paInt16
chunk_size = 1024
rate = 20000
channels = 1

s.connect((ip,port))
print("connected")

playing_stream = p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                          frames_per_buffer=chunk_size)

recording_stream = p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                          frames_per_buffer=chunk_size)

def receive(socket):

    while True:
        try:
            data = socket.recv(1024)
            print(data)
            playing_stream.write(data)

        except:
            pass

def send(socket):
   while True:
       try:
           data = recording_stream.read(1024)
           socket.sendall(data)

       except:
           pass




threading.Thread(target=send,args=(s,)).start()
receive(s)
