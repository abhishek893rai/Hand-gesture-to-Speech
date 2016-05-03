def speech_convert():
	 global lock,speak
    #fread=open("C:\Users\Arya's\Desktop\project2\speech\say.txt",'r')
    #speak=fread.read()
    #fread.close()
    
    
    speak="hello world"

    speech = gTTS (text= speak, lang='en')

    speech.save("C:\Users\Arya's\Desktop\PROJECT\speech\say.mp3")

    lock.acquire()
    try:
        speech = gTTS (text= speak, lang='en')
        speech.save("C:\Users\Arya's\Desktop\PROJECT\speech\say.mp3")
    finally:
        lock.release()    
