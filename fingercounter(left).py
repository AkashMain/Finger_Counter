import cv2 as cv  
import mediapipe as mp
import os 
import time 

w,h=640,480 

cap=cv.VideoCapture(0)
cap.set(3,w)
cap.set(4,h)
ctime=0
ptime=0
lmlist=[]
tippoint=[4,8,12,16,20]


mpHands = mp.solutions.hands
hands = mpHands.Hands() 

mpDraw = mp.solutions.drawing_utils

while True:
    k,frame = cap.read()
    imgRGB = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:

        for handlandmarks in results.multi_hand_landmarks:

            for id,lm in enumerate(handlandmarks.landmark):
            
                h,w,c = frame.shape
                cx,cy = int(lm.x*w),int(lm.y*h)  
                #print(id,cx,cy)
                lmlist.append([id,cx,cy])

            #print(lmlist)   
            
            if len(lmlist)!=0:
                fingers=[]
                
                # Thumb
                if lmlist[tippoint[0]][1] < lmlist[tippoint[0]-1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)    

                # Fingers
                for id in range(1,5):
                    if lmlist[tippoint[id]][2] < lmlist[tippoint[id]-2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)    
            print(fingers)
            totalfingers=fingers.count(1)
            #print("Total Numbers of OPEN fingers: ",fingers.count(1))
            
            lmlist=[]
            
            cv.rectangle(frame,(480,50),(650,200),(255,0,0),-1)
            cv.putText(frame,str(totalfingers),(520,175),cv.FONT_HERSHEY_PLAIN,10,(255,0,255),15)

            mpDraw.draw_landmarks(frame, handlandmarks, mpHands.HAND_CONNECTIONS)


    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime=ctime

    cv.putText(frame,"FPS: "+str(int(fps)),(10,50),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)

    cv.imshow('Frame',frame)
    if cv.waitKey(1) & 0xff== ord('e'):
        break 

cap.release()
cv.destroyAllWindows()