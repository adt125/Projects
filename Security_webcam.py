import cv2
import numpy as np
import face_recognition
from datetime import datetime
import os
import time

def encode(images):
    enclist=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        enc=face_recognition.face_encodings(img)[0]
        enclist.append(enc)
    return enclist

def logins(name):
    with open('login_details.csv','r+') as f:
        data=f.readlines()
        if name=="Unknown":
            tstr=datetime.now().strftime('%H:%M:%S')
            dstr=datetime.now().strftime('%d/%m/%Y')
            f.writelines(f'\n{name}\t{tstr}\t{dstr}')
            return
        names=[]
        for line in data:
            item=line.split('\t')[0]
            names.append(item)
        if name not in names:
            tstr=datetime.now().strftime('%H:%M:%S')
            dstr=datetime.now().strftime('%d/%m/%Y')
            f.writelines(f'\n{name}\t{tstr}\t{dstr}')
        else:
            for line in data:
                if line.split('\t')[0] == name:
                    time_obj=datetime.strptime(line.split['t'][1],'%H:%M:%S')
                    curr_time=datetime.now()
                    if curr_time-time_obj >= 60000:
                        tstr=datetime.now().strftime('%H:%M:%S')
                        dstr=datetime.now().strftime('%d/%m/%Y')
                        f.writelines(f'\n{name}\t{tstr}\t{dstr}')

            


print("Initialising...please wait")
known_faces=[]
known_names=[]
path='Images'
imglist=os.listdir(path)
for img in imglist:
    curr_img=cv2.imread(f'{path}/{img}')
    known_faces.append(curr_img)
    known_names.append(os.path.splitext(img)[0])

encknown_faces=encode(known_faces)
cap=cv2.VideoCapture(0)
print("Please sit upright!!!")
t=time.time()
timer = 10
while timer>0:
    ret, frame=cap.read()
    orignal_frame=frame.copy()
    faces= cv2.resize(frame, (0,0), None, 0.25, 0.25)
    faces= cv2.cvtColor(faces,cv2.COLOR_RGB2BGR)
    flag=False
    curr_face=face_recognition.face_locations(faces)
    curr_enc=face_recognition.face_encodings(faces,curr_face)
    for encface,faceloc in zip(curr_enc,curr_face):
        matches=face_recognition.compare_faces(encknown_faces, encface)
        facedis=face_recognition.face_distance(encknown_faces, encface)

        match_idx=np.argmin(facedis)
        if matches[match_idx]:
            name=known_names[match_idx].upper()
            y1,x2,y2,x1=faceloc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0),2)
            cv2.rectangle(frame, (x1,y2-15), (x2,y2), (0,255,0), cv2.FILLED)
            cv2.putText(frame,"Welcome! "+name,(x1+10,y2-3),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
            logins(name)
        else:
            print("Unauthorized Access attempt!!!")
            
            y1,x2,y2,x1=faceloc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,0,255),2)
            cv2.rectangle(frame, (x1,y2-15), (x2,y2), (255,255,255), cv2.FILLED)
            cv2.putText(frame,"Unknown",(x1+10,y2-3),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)    
            time_stamp = datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
            file_name = f'photos\\img-{time_stamp}.jpg'
            path='photos'
            imglist=os.listdir(path)
            unknown=[]
            for img in imglist:
                curr_img=cv2.imread(f'{path}/{img}')
                unknown.append(curr_img)
            if len(unknown)==0:
                cv2.imwrite(file_name,orignal_frame)
                logins("Unknown")
                continue
            encuk=encode(unknown)
            matches=face_recognition.compare_faces(encuk, encface)
            facedis=face_recognition.face_distance(encuk, encface)
            match_idx=np.argmin(facedis)
            if matches[match_idx]:
                continue
            else:
                logins("Unknown")
                cv2.imwrite(file_name,orignal_frame)
    cv2.imshow("Camera",frame)  
    cur=time.time()
    if cur-t>=1:
        t=cur
        timer=timer-1
    if cv2.waitKey(10)==13:
        break
cap.release()
cv2.destroyAllWindows()
