import pyaudio
import threading
import socket

chunk_size = 1024
audio_format = pyaudio.paInt16
channels = 1
rate = 20000

s = socket.socket()
s.bind(("0.0.0.0",12345))

p = pyaudio.PyAudio()

playing_stream = p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                         frames_per_buffer=chunk_size)

recording_stream = p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                           frames_per_buffer=chunk_size)

s.listen(1)

def receive(socket):
   while True:
      try:
       data = socket.recv(1024)
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

while True:
   c,addr = s.accept()
   print("got connection from {}".format(addr))
   threading.Thread(target=receive,args=(s,)).start()
   send(s)
