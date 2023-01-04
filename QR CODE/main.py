from pyzbar.pyzbar import decode
from PIL import Image
import cv2 ,time
import csv
import xlwt
from xlwt import Workbook
from  datetime import datetime

video = cv2.VideoCapture(0)    # this is used for capturing video 
students = []     #this list will store all the data of absent students 

wb = Workbook()   #workbook is created for storing the attendance in xls
ws = wb.add_sheet('Sheet 1') # this is used to create sheet
ws.write(0,0,'Names')
ws.write(0,1,"Date&Time")

#coordinates for rows and columns
x=1
y=0

#current time is taken from datetime.now()
Curr_time= datetime.now()
Date_time= (Curr_time.strftime('%Y-%m-%d %H:%M:%S'))


with open("data.csv","r") as file:
    reader= csv.reader(file)
    for row in reader:
        students.append((row[1]))
    print(students)
    
    
while True:
    check,frame=video.read()
    d=decode(frame)
    try:
        for obj in d:
            name=d[0].data.decode()
            if name in students:
                students.remove(name)
                ws.write(x,y,name) #entering name into xlm Sheet_1
                ws.write(x,y+1,Date_time) # entering time into xlm Sheet_1
                x=x+1   
                print(name+" is marked present !")
                

    except:
        print("error")

    cv2.imshow("Attendence",frame)
    key=cv2.waitKey(1)
    if key == ord("q"):
        wb.save('Attendace.xls')  #this is file where attendance is saved
        print(students)
        break

video.release()
cv2.destroyAllWindows()

        
