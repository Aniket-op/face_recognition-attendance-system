# combined qr
import cv2  #for caputing Live video from camera
import numpy as np  
import face_recognition  # Main library for face recognition
import os #for read and write operations of files with OS
from datetime import datetime  # It is used to get current date and time 
from pyzbar.pyzbar import decode    #used for decoding QR codes from camera
import csv  #  read and write tabular data in CSV format

#In bellow code we are stored all the name of students from data.csv into students List
students =[]   
with open("data.csv","r") as file:
    reader= csv.reader(file)
    for row in reader:
        students.append((row[1]))
    print("QR :",students)



path = 'Training_images' #path of training Image is stored in path veriable
images = []        #this veriable is used to store the encoded data of the images
classNames = []  # to store the name of all the images Present in path dir
myList = os.listdir(path)   #we can print a list of names of all the files present in the specified path.
print("My List :",myList)   



# to find the no. unique images from directory
for i in myList:
    curImg = cv2.imread(f'{path}/{i}')
    images.append(curImg)
    classNames.append(os.path.splitext(i)[0])
print("Class Name :",classNames)


#to find the face encodings i.e features of the face.
def findEncodings(images):
    encodeList = []

    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

#If it finds a particular class, it will mark the attendence.
def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()

        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')


encodeListKnown = findEncodings(images)



cap = cv2.VideoCapture(0) ##




while True:
    success, img = cap.read()  # reading the captured image
    


    d=decode(img)
    try:
        for obj in d:
            name=d[0].data.decode()
            if name in students:
                students.remove(name)
                markAttendance(name)
                print(name+" is marked present !")
    except:
        print("error")





    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)  # resizing image acc to requirement & BGR image is converted to RGB.

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)  # matching and comparing the faces.
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)  # gets eucledian distance of faces.

        matchIndex = np.argmin(faceDis) # min values wrt matching actually getting.
#for pritning the name!
        if matches[matchIndex]:
            name = classNames[matchIndex]

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            
            if name in students:
                markAttendance(name)
                students.remove(name)
                print(name+" is marked present !")

    cv2.imshow('Attendance', img)
    key = cv2.waitKey(1)
    if key == ord("q"):
        print(students)
        break
    
