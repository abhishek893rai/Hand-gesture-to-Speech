import cv2
import numpy as np
import math
import pyttsx
import win32com.client
import win32api
import time
import webbrowser
import threading
from gtts import gTTS


global extracted
def run():
    global lock
    lock.acquire()
    try:
        cap = cv2.VideoCapture(0)
        while(cap.isOpened()):
            ret, img1 = cap.read()
            img=cv2.flip(img1,1)
            cv2.rectangle(img,(300,300),(100,100),(0,255,0),0)
            crop_img = img[100:300, 100:300]
            grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
            value = (35, 35)
            blurred = cv2.GaussianBlur(grey, value, 0)
            _, thresh1 = cv2.threshold(blurred, 127, 255,
                                       cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            cv2.imshow('Thresholded', thresh1)
            contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
                    cv2.CHAIN_APPROX_NONE)
            max_area = -1
            for i in range(len(contours)):
                cnt=contours[i]
                area = cv2.contourArea(cnt)
                if(area>max_area):
                    max_area=area
                    ci=i
            cnt=contours[ci]
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(crop_img,(x,y),(x+w,y+h),(0,0,255),0)
            hull = cv2.convexHull(cnt)
            drawing = np.zeros(crop_img.shape,np.uint8)
            cv2.drawContours(drawing,[cnt],0,(0,255,0),0)
            cv2.drawContours(drawing,[hull],0,(0,0,255),0)
            hull = cv2.convexHull(cnt,returnPoints = False)
            defects = cv2.convexityDefects(cnt,hull)
            count_defects = 1
            cv2.drawContours(thresh1, contours, -1, (0,255,0), 3)
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
                if angle <= 90:
                    count_defects += 1
                    cv2.circle(crop_img,far,1,[0,0,255],-1)
                #dist = cv2.pointPolygonTest(cnt,far,True)
                cv2.line(crop_img,start,end,[0,255,0],2)
                #cv2.circle(crop_img,far,5,[0,0,255],-1)

            fob=open("C:\Users\Arya's\Desktop\project2\speech\say.txt",'a')
            

            if count_defects == 1:
                extracted="  1"
                fob.write(extracted)
                cv2.putText(img,"Hello", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)

            elif count_defects == 2:
                extracted="  2"
                fob.write(extracted)
                cv2.putText(img,"make gesture 4 to know about the gesture with speech", (15,15), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                
                
                
            elif count_defects == 3:
                extracted="  3"
                fob.write(extracted)
                cv2.putText(img,"Three",(50,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
                
               
                
            elif count_defects == 4:
                extracted="  4"
                fob.write(extracted)
                cv2.putText(img,"Fourth", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                
                
            else:
                extracted=" hello"
                cv2.putText(img,"Hello World!!!", (50,50),\
                            cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
                
               
            
            #cv2.imshow('drawing', drawing)
            #cv2.imshow('end', crop_img)
            cv2.imshow('Gesture', img)
            all_img = np.hstack((drawing, crop_img))
            cv2.imshow('Contours', all_img)
            k = cv2.waitKey(10)
            if k == 27:
                break
            
        cap.release()
        cv2.destroyAllWindows()
        fob.close()
    finally:
        lock.release()
            
            

                    

           

def play_it():
    global lock
    lock.acquire()
    try:
        webbrowser.open("C:\Users\Arya's\Desktop\PROJECT\speech\say.mp3")
    finally:
        lock.release()

def speech():
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

def main():
    global lock
    lock=threading.Lock()

    gestureit=threading.Thread( target = run)
    gestureit.start()

    speechit=threading.Thread( target = speech )
    speechit.start()

    playit=threading.Thread( target = play_it )
    playit.start()

    
if(__name__=='__main__'):
    main()
    # calling the function main()
