#parking space picker

import cv2
import numpy as np

import cvzone


def space(x1,y1,x2,y2):
    with open('spaces.txt','a+') as f:
        
        f.write(f"{str(x1)} {str(y1)} {str(x2)} {str(y2)}\n")


def a(img):
    x1,y1,x2,y2=213,610,265,680
    cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,0),2)
   

def block(img):
    b_x1,b_y1,b_x2,b_y2=910,610,1000,680
    cv2.rectangle(img,(b_x1,b_y1),(b_x2,b_y2),(255,0,255),2)
    
    i=0
    w=146-120+1
    
    x1,y1,x2,y2=b_x1,b_y1,b_x1+w,b_y2
    while(x2<=b_x2 ):
        cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,0),2)
       
        x2=x2+w
    

# to check if the given space is avaliable or not



def check_space(img,frame,l):
    
    x1,y1,x2,y2=l[0],l[1],l[2],l[3]
    w=146-120+1
    img_crop=img[y1:y2,x1:x1+w]
    count=cv2.countNonZero(img_crop)
    return count
        
    

def working_function():
    
    cap=cv2.VideoCapture('parkingspace.mp4')
    while cap.isOpened():
        ret,frame=cap.read()
        try:
            frame = cv2.resize(frame, (1000, 700))
        except:
            pass
     
     

        if cap.get(cv2.CAP_PROP_POS_FRAMES)==cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)
        img___=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        img___=cv2.GaussianBlur(img___,(3,3),1)
        img___=cv2.adaptiveThreshold(img___,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
        img___=cv2.medianBlur(img___,5)
        kernel=np.ones((3,3),np.uint8)
        img___=cv2.dilate(img___,kernel,iterations=1)
        counting_spaces=0
        with open('spaces.txt','r') as f:
            for line in f:
                
                rec_list=[]
                b=0
                for i in range(0,len(line)):
                    if(line[i]==' '):
                        s=line[b:i]
                        rec_list.append(int(s))
                        b=i+1
                    elif(i==len(line)-1):
                        s=line[b:len(line)]
                        rec_list.append(int(s))
                a=check_space(img___,frame,rec_list)
                if a<350:
                    a=(255,0,0)
                    cv2.rectangle(frame,(rec_list[0],rec_list[1]),(rec_list[2],rec_list[3]),a,5)
                    counting_spaces=counting_spaces+1
                    
                    
                else:
                    a=(0,0,255)
                    cv2.rectangle(frame,(rec_list[0],rec_list[1]),(rec_list[2],rec_list[3]),a,2)
                    
                s="count are "
                cvzone.putTextRect(frame,s+str(counting_spaces),(50,50),scale=2.1,thickness=1,offset=3)        
                
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        
        cv2.imshow('frame', frame)
        
        if cv2.waitKey(100) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


working_function()

