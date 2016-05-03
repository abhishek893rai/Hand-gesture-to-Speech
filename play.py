
def play():
	global lock
    lock.acquire()
    try:
        webbrowser.open("C:\Users\Arya's\Desktop\PROJECT\speech\say.mp3")
    finally:
        lock.release()
    
