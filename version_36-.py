# gesture and voice control

# importing directories
from   pynput.mouse       import Button                as MButton
from   pynput.mouse       import Controller            as mouse_controller
from   pynput.keyboard    import Key,       Controller as key_controller
from   playsound          import playsound
from   tkinter            import messagebox
from   PIL                import ImageTk,   Image
from   tkinter            import *
from   calendar           import *

import speech_recognition as     sr
import subprocess         as     sp
import cv2                as     cv
import numpy              as     np
import pygetwindow        as     gw
import tensorflow         as     tf

import time
import os
import threading
import win32api



# global variables
command                  = None                   #contains text of speech
mouse_x                  = 0                      #x value to set mouse
mouse_y                  = 0                      #y value to set mouse
yellow_coord             = []                     #coordinates of yellow token in last 2 seconds
blue_coord               = []                     #coordinates of blue token in last 2 seconds
current_window           = ''                     #name of foreground window
current_window_object    = ''                     #object of foreground window
mywindows                = []                     #list of objects of windows opened by program
status_text              = 'Loading program...'   #dictates state of the program
response_text            = ''                     #reaction of program
valid_mic_port           = 'null'                 #valid microphone port number
valid_webcam_port        = 'null'                 #valid webcam port number
numbering                = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9, 'ten':10, 'eleven':11, 'twelve':12,
                            'thirteen':13, 'fourteen':14, 'fifteen':15, 'sixteen':16, 'seventeen':17, 'eighteen':18, 'nineteen':19, 'twenty':20, 'thirty':30,
                            'fourty':40, 'fifty':50, 'sixty':60, 'seventy':70, 'eighty':80, 'ninety':90, 'hundred':100, 'hundreds':100, 'thousand':1000,
                            'thousands':1000, 'lakh':100000, 'lakhs':100000, 'crore':10000000, 'crores':10000000, 'arab':1000000000, 'arabs':1000000000}
factor                   = ['arab', 'crore', 'lakh', 'thousand', 'hundred']
valid_two                = {'twenty':20, 'thirty':30, 'fourty':40, 'fifty':50, 'sixty':60, 'seventy':70, 'eighty':80, 'ninety':90}
months_dic               = {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6, 'july':7, 'august':8, 'september':9, 'october':10,
                            'november':11, 'december':12}
extensions               = {'mp3':'vlc','mp4':'vlc','avi':'vlc','mkv':'vlc','py':'python','txt':'notepad','htm':'chrome','html':'chrome','jpg':'photos','jpeg':'photos'}
voice_activate_flag      = False                  #boolean activation of voice control
token_activate_flag      = False                  #boolean activation of token control
curser_locked_flag       = True                   #boolean whether to move curser with yellow token, if true then do not move
allopenwindows_flag      = False                  #weather alt+tab is on
my_window_active_flag    = False                  #boolean whether current window is created by program
desktop_flag             = False                  #boolean whether current window is desktop or not
media_flag               = False                  #boolean whether media is on
write_flag               = False                  #boolean whether writer is on
audio_flag               = True                   #boolean to say whether audio work for one loop is done
video_flag               = True                   #boolean to say whether video work for one loop is done
master_flag              = True                   #boolean to say whether work is done
terminate_flag           = False                  #boolean to say whether to terminate the program
awaiting_flag            = False                  #boolean to decide whether a function is waiting for something
webcam_image             = 0                      #current image taken by webcam          
enter_directory_flag     = False                  #boolean to say whether to enter a directory
pause_voice_control_flag = False                  #boolean to say whether voice control is paused



# global objects
mouse = mouse_controller()    #creating mouse oject
kb    = key_controller()      #creating keyboard object
    


# voice recognition function
def audio():
    global command, voice_activate_flag, terminate_flag, status_text, response_text, audio_flag, master_flag, audio_processed_flag, valid_mic_port
    global voice_terminate_flag, pause_voice_control_flag, token_activate_flag

    #creating microphone object
    mic = sr.Microphone(valid_mic_port)                                                   
    r = sr.Recognizer()

    while True:
        
        # checking whether to terminate the program
        if terminate_flag or (not voice_activate_flag):
            response_text = 'Deactivating voice control'
            status_text = 'Audio function thread killed'
            break

        # if master_flag is false then do not resume, reset the loop
        if not master_flag:
            status_text = 'Processing previous command...'
            continue
        
        with mic as source:
            status_text = 'Collecting audio...'
            
            print('listening')
            # adjusting mic with noise
            #r.adjust_for_ambient_noise(source, duration = 1)
            # listening microphone
            #r.energy_threshold = 500
            
            try:
                audio = r.listen(source, timeout = 3)

            except sr.WaitTimeoutError:
                status_text = 'Listening timed out'
                time.sleep(0.5)
                continue
            
            print('listened')
            
            try:
                    
                # setting audio_flag as false as audio is not processed but starting
                audio_flag = False
                    
                #print('Converting')

                status_text = 'Converting into text...'
                    
                # speech into text
                text = r.recognize_google(audio, language='en-IN').lower()
                command = text
                response_text = 'Command found'

                #print('converted')
                    
                #print(text)
                status_text = 'Running...'
                    
            

                # if voice control is paused then check for only one command
                if pause_voice_control_flag:
                    if text=="reactivate voice control":  #if true then then turn on voice control
                        response_text = 'Voice control reactivated'
                        pause_voice_control_flag = False
                        playsound('sounds/activation_voice.mp3')
                        status_text = 'Running...'

                else:                                        
                    if text=="pause voice control":
                        response_text = 'Voice control paused'
                        pause_voice_control_flag = True
                        playsound('sounds/pause_voice.mp3')
                        status_text = 'Voice Paused...'
                        
                    elif text=="deactivate voice control":  #if true then turn off voice control
                        response_text = 'Voice control deactivated'
                        status_text = 'Running...'
                        voice_activate_flag = False
                        playsound('sounds/deactivation_voice.mp3')
                        break

                    elif text=="activate token control":
                        token_activate_flag = True

                    elif text=="deactivate token control":
                        token_activate_flag = False
                        
                    else:  #if none of above commands matches the text then make command global to be checked by master function
                        command = text
                        response_text = 'Command found'

                        # setting audio_flag as true as audio has been processed e.g.text has arrived
                        audio_flag = True
        
            except sr.UnknownValueError:  #if no command found
                print('exception')
                response_text = 'No command found'


    
# image processing function
def video():
    global mouse_x, mouse_y, yellow_coord, blue_coord, terminate_flag, status_text, response_text, token_activate_flag, valid_webcam_port, webcam_image

    # loading saved model
    model = tf.keras.models.load_model('helper programs/model.h5')

    # function to find gesture
    def find_gesture():
        global blue_coord
        if len(blue_coord)<30:
            for i in range(30-len(blue_coord)):
                blue_coord.append([0.,0.])
        else:
            blue_coord = blue_coord[:30]
        data = np.array([blue_coord])
        #print(data)
        gesture = model.predict(data)
        gesture = np.argmax(gesture, axis = 1)
        gesture = gesture[0]
        if gesture==0:
            kb.press(Key.ctrl)
            kb.press(Key.right)
            kb.release(Key.ctrl)
            kb.release(Key.right)
        elif gesture==1:
            kb.press(Key.ctrl)
            kb.press(Key.left)
            kb.release(Key.ctrl)
            kb.release(Key.left)
        elif gesture==2:
            for i in range(5):
                kb.press(Key.media_volume_down)
                kb.release(Key.media_volume_down)
        elif gesture==3:
            for i in range(5):
                kb.press(Key.media_volume_up)
                kb.release(Key.media_volume_up)

    # function for detecting shape
    def detectshape(c):
        peri = cv.arcLength(c,True)
        approx = cv.approxPolyDP(c,0.1*peri,True)
        if len(approx)==4:
            return 1
        return 0
        
    # creating video object 
    cap = cv.VideoCapture(valid_webcam_port)#'files/video.mp4')

    # setting width and height of window
    width = int(1366/4)
    height = int(768/4)

    # creating kernel for dilation 
    kernel = np.ones((3,3),np.uint8)
    t = 2

    previous_blue = [-1,-1]

    t1 = time.time()
    # mainloop for iterating throught the frames of video
    while cap.isOpened():
        
        # checking whether to terminate program
        if terminate_flag or not token_activate_flag:
            status_text = 'Token function thread killed'
            response_text = 'Deactivating token control'
            break
        
        # measuring time
        if time.time()-t1>2:
            if len(blue_coord)>7:
                #print(blue_coord)
                find_gesture()
            yellow_coord.clear()
            blue_coord.clear()
            t1 = time.time()
            
        # reading a new frame
        ret, img = cap.read()
        #print(img)
        # flipping the frame
        img = cv.flip(img,1)

        # converting the frame from BGR to HSV
        hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)

        # setting lower bound and upper bound for yellow color
        lb_yellow = np.array([20,100,100],dtype=np.uint8)
        ub_yellow = np.array([30,255,255],dtype=np.uint8)

        # setting lower bound and upper bound for blue color
        lb_blue = np.array([110,50,50], dtype=np.uint8) #20,100,100 #110,50,50   #80,70,50
        ub_blue = np.array([130,255,255], dtype=np.uint8) #30,255,255 #130,255,255 #100,255,255

        # creating mask for both the colors in the specified range     
        mask_yellow = cv.inRange(hsv, lb_yellow, ub_yellow)
        mask_blue = cv.inRange(hsv, lb_blue, ub_blue)

        ##### dilating the colors masks
        #mask = cv.dilate(mask,kernel,iterations = 4)

        ##### blurring the colors masks
        #mask = cv.GaussianBlur(mask,(5,5),100)         

        # finding contours for bith the colors in the frame
        contours_yellow, hierarchy_yellow = cv.findContours(mask_yellow, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contours_blue, hierarchy_blue = cv.findContours(mask_blue, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
        #img = cv.drawContours(img,contours,-1,(0,255,0),3)
        #cv.imshow('img',img)

        maxarea_yellow = 0

        # finding the contour of yellow color with maximum area
        for cnt in contours_yellow:
            area = cv.contourArea(cnt)
            if area>maxarea_yellow and area>500:
                c_yellow = cnt
                maxarea_yellow = area

        maxarea_blue = 0

        # finding the contour of blue color with maximum area
        for cnt in contours_blue:
            area = cv.contourArea(cnt)
            if area>maxarea_blue and area>500:
                c_blue = cnt
                maxarea_blue = area
        #print(maxarea_blue)
            
        try:
            
            # finding center of yellow square
            m_yellow = cv.moments(c_yellow)
            cx_yellow = int(m_yellow['m10']/m_yellow['m00'])
            cy_yellow = int(m_yellow['m01']/m_yellow['m00'])

            # drawing rectangle over the yellow square
            img = cv.rectangle(img,(cx_yellow-50,cy_yellow-50),(cx_yellow+50,cy_yellow+50),(0,255,255),3)
            img = cv.circle(img,(cx_yellow,cy_yellow),3,(0,255,255),-1)
            

            # saving coordinates in global variable 
            yellow_coord.append([cx_yellow,cy_yellow])

            # setting mouse co-ordinates
            mouse_x = cx_yellow
            mouse_y = cy_yellow
            
        except: # catching exception
            #print('Yellow Square not found')
            pass

        try:
            
            # finding center of blue square
            m_blue = cv.moments(c_blue)
            cx_blue = int(m_blue['m10']/m_blue['m00'])
            cy_blue = int(m_blue['m01']/m_blue['m00'])

            #print(cx_blue, cy_blue)
            
            # drawing rectangle over the blue square
            img = cv.rectangle(img,(cx_blue-50,cy_blue-50),(cx_blue+50,cy_blue+50),(255,0,0),3)
            img = cv.circle(img,(cx_blue,cy_blue),3,(255,0,0),-1)
            
            if previous_blue==[cx_blue,cy_blue]:
                pass
            else:
                previous_blue = [cx_blue,cy_blue]
                # saving coordinates in global variable
                blue_coord.append([float(cx_blue),float(cy_blue)])
            
            ##### drawing contour over the blue square found
            #img = cv.drawContours(img,[c_blue],-1,(0,255,0),3)
        
        except: # catching exception
            #print('Blue Square not found')
            pass


        # resizing window with the width and height described above    
        img = cv.resize(img, (width, height), fx=0, fy=0, interpolation = cv.INTER_CUBIC)

        # moving window to the right corner
        cv.moveWindow('img', 1000, 500)

        # showing frame
        #cv.imshow('img',img)
        webcam_image = img
        cv.waitKey(1)

    # release video object
    cap.release()

    # destroying every wndow created
    cv.destroyAllWindows()



# function to show current time
def show_current_time():

    # function to return full name of day
    def day(d):
        d = d.lower()
        if d=='sun':
            return 'Sunday'
        elif d=='mon':
            return 'Monday'
        elif d=='tue':
            return 'Tuesday'
        elif d=='wed':
            return 'Wednesday'
        elif d=='thu':
            return 'Thursday'
        elif d=='fri':
            return 'Friday'
        elif d=='sat':
            return 'Saturday'

    # storing ticks till now
    t1 = time.time()
    
    while True:

        # if its more than 5 seconds then close window
        if time.time()-t1>5:
            break

        # taking time tuple which looks like this 'Sun Jun 28 23:29:16 2020'
        t = time.ctime(time.time())
        t = t.split()

        # reading image to set background
        img = cv.imread("files/sky.jpg")
        img = cv.resize(img,(400,300))

        # showing time
        img = cv.putText(img,str(t[3]),(50,150),cv.FONT_HERSHEY_SIMPLEX,2,(0,0,0),5,cv.LINE_AA)

        # showing month date year
        img = cv.putText(img,str(t[1])+"  "+str(t[2])+"  "+str(t[4]),(70,50),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,0),3,cv.LINE_AA)

        # showing day
        d = day(t[0])
        img = cv.putText(img,d,(135,200),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,0),3,cv.LINE_AA)

        # showing window
        cv.imshow('Current time',img)
        cv.waitKey(1)

    # destroying window after 5 seconds
    cv.destroyAllWindows()



def show_cal_month(y,m):
    from PIL import Image, ImageTk
    
    # Create a GUI window 
    new_gui = Tk() 
      
    # Set the background colour of GUI window 
    img = Image.open('files/sky.jpg')
    img = img.resize((240,180))
    img = ImageTk.PhotoImage(img)
    bg_img = Label(new_gui,image = img)
    bg_img.grid(row = 0,column = 0)
    # set the name of tkinter GUI window  
    new_gui.title(str(y)+' '+str(m)) 
  
    # Set the configuration of GUI window 
    new_gui.geometry("240x180") 
  
    # get method returns current text as string 
  
    # calendar method of calendar module return 
    # the calendar of the given year . 
    data = month(y,m)[:-1]
    ind = data[::-1].index('\n')
    data = data+(7-data[-1*ind:].count(' ')-1)*' --'
        
  
    # Create a label for showing the content of the calender 
    cal_year = Label(bg_img, text = data, font = "Consolas 10 bold") 
  
    # grid method is used for placing  
    # the widgets at respective positions  
    # in table like structure. 
    cal_year.grid(row = 1, column = 1, padx = 45,pady = 35) 
      
    # start the GUI  
    new_gui.mainloop()


# function to create a tkinter window to show calendar
def show_cal_year(y): 
    from PIL import Image, ImageTk
    
    # Create a GUI window 
    new_gui = Tk()

    new_gui.geometry('540x600')
          
    # Set the background colour of GUI window 
    img = Image.open('files/sky.jpg')
    img = img.resize((540,600))
    img = ImageTk.PhotoImage(img)
    bg_img = Label(new_gui,image = img)
    bg_img.grid(row = 0,column = 0)

      
    # set the name of tkinter GUI window  
    new_gui.title("CALENDER "+str(y)) 

    # storing calendar data for every month
    cal_list = []
    for i in range(1,13):
        data = month(y,i)[:-1]
        ind = data[::-1].index('\n')
        data = data+(7-data[-1*ind:].count(' ')-1)*' --'
        cal_list.append(data)

    # showing calendar data for every month on window
    k = 0
    for i in range(4):
        for j in range(3):
            Label(bg_img, text = cal_list[k], font = "Consolas 10 bold").grid(row = i, column = j, padx = 16, pady = 13)
            k+=1
                
    # start the GUI  
    new_gui.mainloop()


def show_calendar():
    global command, months_dic

    month_flag = False
    
    # splitting command
    command_split = command.split()

    # storing time tuple 
    t = time.ctime(time.time()).split()

    # storing current year
    y = int(t[-1])

    # storing current month
    m = t[1].lower()

    # taking month as a number
    for key, value in months_dic.items():
        if m in key:
            m = value
            break

    # checking whether a year and month is given in command
    for i in command_split:
        if i.isdigit() and len(i)==4 and int(i)>=1970:
            y = int(i)

        elif i.isdigit() and (len(i)==1 or len(i)==2) and 1<=int(i)<=12:
            month_flag = True
            m = int(i)
            
        elif i in months_dic.items():
            month_flag = True
            m = months_dic[i]

    if month_flag:
        show_cal_month(y,m)
    else:
        show_cal_year(y)


# mouse events handling function
def mouse_events(event):
    global mouse, response_text
    
    if event=='double':

        # pressing and releasing mouse left button two times
        mouse.press(MButton.left)
        mouse.release(MButton.left)
        mouse.press(MButton.left)
        mouse.release(MButton.left)
        
    elif event=='left':

        # pressing and releasing mouse left button
        mouse.press(MButton.left)
        mouse.release(MButton.left)
        
    elif event=='right':

        # pressing and releasing mouse right button
        mouse.press(MButton.right)
        mouse.release(MButton.right)



# functions to switch between opened windows
class all_open_windows():
    def __init__(self):

        # saving object data
        self.titles = gw.getAllTitles()
        self.win_objects = gw.getAllWindows()
        self.total_windows = 0
        for i,title in enumerate(self.titles):
            if len(title)!=0:
                self.total_windows+=1
                
    def start(self):
        global kb
        kb.press(Key.alt)
        kb.press(Key.tab)
        kb.release(Key.tab)
        
    def next(self):
        global kb, allopenwindows_flag, command, response_text
        window_name = command.split()

        # removing 'window' or 'windows' from command if exists
        if window_name[-1]=='window' or window_name[-1]=='windows':
            window_name = window_name[1:-1]
        else:
            window_name = window_name[1:]
            
        l = len(window_name)

        # find the selected window
        for i,title in enumerate(self.titles):
            c = 0
            for j in window_name:
                if j in title.lower():
                    c+=1
            if c==l:  #selected window found
                window_object = self.win_objects[i]
                for obj in self.win_objects:
                    if obj==window_object:  #maximize selected window
                        obj.maximize()
                    else:  #minimize other windows
                        obj.minimize()
                break
                    
        if c<l:
            response_text = 'No window found'
            playsound('sounds/no_window.mp3')
        kb.release(Key.alt)
        allopenwindows_flag = False


# class to store data of windows opened by the program
class my_window:
    def __init__(self, window_address, window_title, window_object):
        self.window_address = window_address
        self.window_title = window_title
        self.window_object = window_object



def my_window_manager():
    global command, mywindows, curent_window, current_window_object, numbering, extensions, status_text, response_text
    command_split = command.split()
    if command_split[1]=='file':  #if second word of command is file
        for i,obj in enumerate(mywindows):
            if obj.window_object==current_window_object:
                break

        # file_name is after keywords 'open file'
        file_name = command_split[2:]

        print(file_name)
        
        # modifying file name to a proper format
        file_name_mode = []
        for j in file_name:
            if j in numbering.keys():
                file_name_mode.append(numbering[j])
            else:
                file_name_mode.append(j)
                
        print(file_name)
        l = len(file_name_mode)
        flag1 = False  #flag to check whether file exist
                
        # making list of all the items in the current window
        items_list = os.listdir(obj.window_address)
        
        # searching item in the items_list
        for item in items_list:
            c = 0
            k = 0
            for key in file_name_mode:
                if key in item[k:].lower():  #if one of   
                    c+=1
                    k = item.lower().find(key)
            if c==l:
                file = item
                flag1 = True
                break
                
        if flag1: #means item is found
                    
            # creating new path by adding selected item
            current_address = obj.window_address+'/'+file
            
            # checking whether there is a extension in the file name
            dot = current_address[::-1].find('.')
            
            if dot>-1 and current_address[-1*dot:] in extensions.keys():  #extension exists

                # starting a subprocess while continuing execution of this thread
                sp.Popen(current_address, shell=True)
            
            else:  #extension does not exists

                # simply open the new selected window
                
                # del current window object from mywindows
                del mywindows[i]

                # closing current window
                current_window_object.close()

                # starting new window
                os.system('start '+current_address)
                
            time.sleep(2)
                    
            # getting current window name
            current_window = gw.getActiveWindowTitle()
    
            # finding object of current window
            current_window_object = gw.getActiveWindow()

            # saving new object of my_window in mywindows
            mywindows.append(my_window(current_address, current_window, current_window_object))

        else:
            response_text = 'No file found'
            playsound('sounds/invalid_file.mp3')



def application_manager(command_split):
    global command, response_text, status_text, awaiting_flag
    
    app_name_split = command_split[2:]
    app_name = ' '.join(app_name_split)

    if 'notepad' in app_name:
        response_text = 'Opening application notepad'
        sp.Popen('notepad')
            
    elif 'wordpad' in app_name:
        response_text = 'Opening application wordpad'
        sp.Popen('write')
            
    elif 'calculater' in app_name:
        response_text = 'Opening application calculater'
        sp.Popen('calc')

    elif 'cmd' in app_name or ('command' in app_name and 'prompt' in app_name):
        response_text = 'Opening application command prompt'
        sp.Popen('cmd')
        
    else:
        try:
            f = open('files/application_address_file.txt','r')
            addresses = f.readlines()
            f.close()
            l = len(app_name_split)
            for address in addresses:
                c = 0
                for name in app_name_split:
                    if name in address:
                        c+=1
                if c==l:
                    break

            if c==l:
                response_text = 'Opening application '+app_name
                sp.Popen(address[:-2])

            else:
                response_text = 'No application '+str(app_name)
                playsound('sounds/no_application.mp3')
                status_text = 'Waiting for yes or no...'
                while True:
                    if command=='yes' or command=='no':
                        status_text = 'Running...'
                        break
                    time.sleep(1)
                    
                if command=='yes':
                    response_text = 'Enter application path'

        except:
            response_text = 'No application '+str(app_name)
            playsound('sounds/no_application.mp3')
            status_text = 'Waiting for yes or no...'
            while True:
                if command=='yes' or command=='no':
                    status_text = 'Running...'
                    break
                time.sleep(1)
                    
            if command=='yes':
                response_text = 'Enter application path'
    
    
                    
def file_manager():
    global command, current_window, current_window_object, mywindows, my_window_active_flag, status_text
    command_split = command.split()

    # taking name of drives in a list
    drives = win32api.GetLogicalDriveStrings()

    # checking whether command says to open an application
    if command_split[1].find('app')>-1:
        status_text = 'Opening Application'
        application_manager(command_split)
    
    # checking whether command says to open a local disk
    elif 'local' in command_split[1] and 'disk' in command_split and command_split.index('disk')+1<len(command_split):
        status_text = 'Opening local disk'

        # name of drive entered
        drive = command_split[command_split.index('disk')+1]
        drive = drive.upper()
        flag = False     #flag to test whether drive exist or not
        for i in drives:
            if drive in i:
                current_address = i[0]+':'+'/'

                # starting window
                os.system("start "+current_address)
                time.sleep(2)

                # getting current window name
                current_window = gw.getActiveWindowTitle()

                # finding object of current window
                current_window_object = gw.getActiveWindow()

                # saving my_window object in mywindows list
                mywindows.append(my_window(current_address, current_window, current_window_object))
                flag = True
                break
        if not flag:
            status_text = 'No drive found'
            playsound('sounds/invalid_drive.mp3')
            
    elif 'file' in command and my_window_active_flag:
        status_text = 'Opening file'
        my_window_manager()
                


def volume_up():
    global command, numbering, response_text
    command_split = command.split()
    if len(command_split)==2:
        for i in range(5):
            kb.press(Key.media_volume_up)
            kb.release(Key.media_volume_up)

    elif len(command_split)>2:
        if any(list(map(lambda x:x.isdigit(),command_split[2:]))):
            for i in command_split[2:]:
                if i.isdigit():
                    factor = int(i)
            for i in range(int(factor)):
                kb.press(Key.media_volume_up)
                kb.release(Key.media_volume_up)

        elif factor in numbering.keys():
            factor = numbering[factor]
            for i in range(int(factor)):
                kb.press(Key.media_volume_up)
                kb.release(Key.media_volume_up)

        else:
            response_text = 'Wrong media factor'
            playsound('sounds/wrong_factor.mp3')
    else:
        response_text = 'Wrong media factor'
        playsound('sounds/wrong_factor.mp3')



def volume_down():
    global command, numbering, response_text
    command_split = command.split()
    if len(command_split)==2:
        for i in range(5):
            kb.press(Key.media_volume_down)
            kb.release(Key.media_volume_down)

    elif len(command_split)>2:
        if any(list(map(lambda x:x.isdigit(),command_split[2:]))):
            for i in command_split[2:]:
                if i.isdigit():
                    factor = int(i)
            for i in range(int(factor)):
                kb.press(Key.media_volume_down)
                kb.release(Key.media_volume_down)

        elif factor in numbering.keys():
            factor = numbering[factor]
            for i in range(int(factor)):
                kb.press(Key.media_volume_down)
                kb.release(Key.media_volume_down)

        else:
            response_text = 'Wrong media factor'
            playsound('sounds/wrong_factor.mp3')
    else:
        response_text = 'Wrong media factor'
        playsound('sounds/wrong_factor.mp3')



def volume_mute():
    kb.press(Key.media_volume_mute)
    kb.release(Key.media_volume_mute)


    
class media_manager:
    def next(self):
        kb.press(Key.right)
        kb.release(Key.right)

    def previous(self):
        kb.press(Key.left)
        kb.release(Key.left)

    def play_pause(self):
        kb.press(Key.media_play_pause)
        kb.release(Key.media_play_pause)

    def slow_forward(self):
        kb.press(Key.right)
        kb.release(Key.right)

    def fast_forward(self):
        kb.press(Key.ctrl)
        kb.press(Key.right)
        kb.release(Key.right)
        kb.release(Key.ctrl)

    def slow_backward(self):
        kb.press(Key.left)
        kb.release(Key.left)

    def fast_backward(self):
        kb.press(Key.ctrl)
        kb.press(Key.left)
        kb.release(Key.left)
        kb.release(Key.ctrl)
        
    
        
def writer():
    global command

    if command.split()[0]=='press':
        keyboard_events()

    else:
        for key in command:
            kb.press(key)
            kb.release(key)



# minimize the current window
def minimize_window():
    global current_window_object
    current_window_object.minimize()



# maximize the current window
def maximize_window():
    global current_window_object
    current_window_object.maximize()



# close the current window
def close_window():
    global current_window_object, mywindows

    # checking if the current window is created by program
    for i,obj in enumerate(mywindows):
        if obj.window_object==current_window_object:  #if yes then delete it's object from mywindow
            del mywindows[i]
            break

    # closing current window
    current_window_object.close()
    


def minimize_all():
    
    # getting object of all active windows
    all_windows_objects = gw.getAllWindows()

    # minimizing every window
    for obj in all_windows_objects:
        obj.minimize()
        


def close_all():

    # getting titles of all active windows
    all_windows_titles = gw.getAllTitles()
    
    # getting object of all active windows
    all_windows_objects = gw.getAllWindows()

    # minimizing every window
    for i,obj in enumerate(all_windows_objects):
        if all_windows_titles[i]=='AMD:CCC-AEMCapturingWindow' or all_windows_titles[i]=='Program Manager':
            pass
        else:
            obj.close()



def keyboard_events():
    global command, response_text
    command_split = command.split()
    
    if command_split[1]=='enter':
        response_text = "'Enter' key pressed"
        kb.press(Key.enter)
        kb.release(Key.enter)

    elif command_split[1]=='escape':
        response_text = "'Escape' key pressed"
        kb.press(Key.esc)
        kb.release(Key.esc)
                
    elif command_split[1]=='backspace':
        response_text = "'Backspace' key pressed"
        kb.press(Key.backspace)
        kb.release(Key.backspace)
                
    elif command_split[1]=='up':
        response_text = "'Up' key pressed"
        kb.press(Key.up)
        kb.release(Key.up)
                
    elif command_split[1]=='down':
        response_text = "'Down' key pressed"
        kb.press(Key.down)
        kb.release(Key.down)
                
    elif command_split[1]=='left':
        response_text = "'Left' key pressed"
        kb.press(Key.left)
        kb.release(Key.left)
                
    elif command_split[1]=='right':
        response_text = "'Right' key pressed"
        kb.press(Key.right)
        kb.release(Key.right)

    elif 'cap' in command and 'lock' in command:
        response_text = "'Caps lock' key pressed"
        kb.press(Key.caps_lock)
        kb.release(Key.caps_lock)
        
    else:
        response_text = 'No such Key'
        

    
# master function
def master():
    global command,voice_activate_flag, mouse_x, mouse_y, curser_locked_flag, yellow_coord, blue_coord, mouse, kb, allopenwindows_flag, current_window, current_window_object
    global mywindows, my_window_active_flag, desktop_flag, media_flag, write_flag, terminate_flag, status_text, response_text
    previous_command = ''

    # getting object of desktop window
    desktop_title = 'Program Manager'
    for i,name in enumerate(gw.getAllTitles()):
        if name==desktop_title:
            desktop_object = gw.getAllWindows()[i]
            break

    current_address = "C:/Users/Red/Desktop"
    
    # creating object of the desktop window and save it in 'mywindows'
    mywindows.append(my_window(current_address, desktop_title, desktop_object))
    
    while True:

        # checking whether to terminate the program
        if terminate_flag:
            break
        
        # getting current window name
        current_window = gw.getActiveWindowTitle()

        # finding object of current window
        current_window_object = gw.getActiveWindow()

        # checking whether current window is desktop
        if current_window=='Program Manager':  #if true
            desktop_flag = True  #turn desktop true
            
        else:  #if current window is not desktop
            desktop_flag = False  #turn desktop false

        # checking if the current window is created by program
        for object in mywindows:
            if object.window_object==current_window_object:
                my_window_active = True
            else:
                my_window_active = False

        # checking lock on curser
        if not curser_locked_flag:
            mouse.position = (5*mouse_x-800,4*mouse_y-500)

        # checking voice activation
        if voice_activate_flag:

            # if audio_flag is false then do not resume, reset the loop
            if not audio_flag:
                continue
            
            if command==None or command=='':
                # setting master_flag as False as command has not been processed
                master_flag = True
                continue

            else:
                master_flag = False
                
            if write_flag:
                writer()
                
            elif command.split()[0]=='press':
                keyboard_events()

            elif command.find('current time')>-1:
                show_current_time()

            elif command.find('calendar')>-1:
                show_calendar()

            elif command.find('exit')>-1 and command.find('program')>-1:
                status_text = 'Closing program...'
                response_text = 'Closing program'
                playsound('sounds/closing_program.mp3')
                terminate_flag = True

            elif command.find('system')>-1 and command.find('shut')>-1 and command.find('down')>-1:
                response_text = 'Shutting system down...'
                playsound('sounds/shut_down.mp3')
                os.system("shutdown /s /t 1")
            
            elif command.find('lock')>-1 and command.find('mouse')>-1:
                curser_locked_flag = True
                response_text = 'Mouse locked'
                playsound('sounds/mouse_locked.mp3')
                
            elif command.find('unlock')>-1 and command.find('mouse')>-1:
                curser_locked_flag = False
                response_text = 'Mouse unlocked'
                playsound('sounds/mouse_unlocked.mp3')
                
            elif command.find('double')>-1 and command.find('click')>-1:
                response_text = 'Double clicking mouse'
                mouse_events('double')
                
            elif command.find('left')>-1 and command.find('click')>-1:
                response_text = 'Left clicking mouse'
                mouse_events('left')
                
            elif command.find('right')>-1 and command.find('click')>-1:
                response_text = 'Right clicking mouse'
                mouse_events('right')

            elif command.find('all')>-1 and command.find('open')>-1 and command.find('window')>-1:
                response_text = 'Opening all opened windows'
                allopenwindows_flag = True
                allopenwindows_object = all_open_windows()
                allopenwindows_object.start()
            
            elif command.split()[0].find('select')>-1 and len(command.split())>1:
                if allopenwindows_flag:
                    allopenwindows_object.next()
                else:
                    file_manager()

            elif command.split()[0].find('open')>-1 and len(command.split())>1:
                if allopenwindows_flag:
                    obj.next()
                else:
                    file_manager()
                    
            elif command.find('minimise')>-1 and command.find('window')>-1:
                response_text = 'Minimizing current window'
                minimize_window()

            elif command.find('maximise')>-1 and command.find('window')>-1:
                response_text = 'Maximizing current window'
                maximize_window()
                
            elif command.find('close')>-1 and command.find('window')>-1:
                response_text = 'Closing current window'
                close_window()

            elif command.find('minimise all')>-1:
                response_text = 'Minimizing all windows'
                minimize_all()

            elif command.find('close all')>-1:
                response_text = 'Closing all windows'
                close_all()
                
            elif command.find('activate')>-1 and command.find('media')>-1:
                status_text = 'Media activated...'
                media_flag = True
                media_object = media_manager()

            elif command=='next':
                if media_flag:
                    response_text = 'Moving to next media'
                    media_object.next()

                else:
                    response_text = 'Invalid command'
                    playsound('sounds/invalid_command.mp3')

            elif command=='previous':
                if media_flag:
                    response_text = 'Moving to previous media'
                    media_object.previous()

                else:
                    response_text = 'Invalid command'
                    playsound('sounds/invalid_command.mp3')

            elif command=='slow forward':
                if media_flag:
                    response_text = 'Slow forwarding media'
                    media_object.slow_forward()

                else:
                    response_text = 'Invalid command'
                    playsound('sounds/invalid_command.mp3')

            elif command=='fast forward':
                if media_flag:
                    response_text = 'Fast forwarding media'
                    media_object.fast_forward()

                else:
                    response_text = 'Invalid command'
                    playsound('sounds/invalid_command.mp3')

            elif command=='slow backward':
                if media_flag:
                    response_text = 'Slow backwarding media'
                    media_object.slow_backward()

                else:
                    response_text = 'Invalid command'
                    playsound('sounds/invalid_command.mp3')

            elif command=='fast backward':
                if media_flag:
                    response_text = 'Fast backwarding media'
                    media_object.fast_backward()

                else:
                    response_text = 'Invalid command'
                    playsound('sounds/invalid_command.mp3')

            elif command=='play':
                if media_flag:
                    response_text = 'Media played'
                    media_object.play_pause()

                else:
                    response_text = 'Invalid command'
                    playsound('sounds/invalid_command.mp3')

            elif command=='pause':
                if media_flag:
                    response_text = 'Media paused'
                    media_object.play_pause()

                else:
                    response_text = 'Invalid command'
                    playsound('sounds/invalid_command.mp3')

            elif command.find('deactivate')>-1 and command.find('media')>-1:
                status_text = 'Media deactivated...'
                media_flag = False
                del media_object

            elif command.find('volume up')>-1:
                response_text = 'Increasing volume' 
                volume_up()

            elif command.find('volume down')>-1:
                response_text = 'Decreasing volume'
                volume_down()

            elif command.find('volume mute')>-1:
                response_text = 'Muting volume'
                volume_mute()

            elif command.find('volume unmute')>-1:
                response_text = 'Unmuting volume'
                volume_mute()

            elif command.find('activate')>-1 and command.find('write')>-1:
                status_text = 'Writer activated...'
                write_flag = True

            elif command.find('deactivate')>-1 and command.find('write')>-1:
                status_text = 'Writer deactivated...'
                write_flag = False
            
            else:
                if previous_command==command:
                    pass
                else:
                    previous_command = command
                    response_text = 'Invalid command...'
                    playsound('sounds/invalid_command.mp3')
            command = None
            
        # setting master_flag as True as command has been processed
        master_flag = True    


# function for interface
def GUI():
    from PIL import Image, ImageTk
    global terminate_flag, valid_mic_port, valid_webcam_port, status_text, response_text, command, webcam_image, voice_activate_flag, token_activate_flag
    global token_terminate_flag, voice_terminate_flag

    t3 = 0
    t4 = 0
    command_count = 0 # keeping track of number of commands so as to reset command display after it become full i.e. 16 commands
    webcam_port_error_flag = False # flag to say whether webcam port error has been shown
    mic_port_error_flag = False # flag to say whether mic port error has been shown
    previous_command = 'null' # not to repeat display commands

    # function for showing available mic ports on click on menubar option
    def microphone_ports():
        mic_list = sr.Microphone.list_microphone_names()
        for i in range(len(mic_list)):
            mic_list[i] = 'Microphone Port '+str(i)+' : '+mic_list[i]
        mic_list = '\n'.join(mic_list)
        messagebox.showinfo("Microphone Ports",mic_list)


    # function for showing available webcam portson click on menubar option
    def webcam_ports():
        webcam_list = []
        for i in range(5):
            cap = cv.VideoCapture(i)
            if cap.isOpened():
                webcam_list.append(True)
            else:
                webcam_list.append(False)
        for i in range(5):
            webcam_list[i] = 'Webcam Port '+str(i)+' : Enabled' if webcam_list[i] else 'Webcam Port '+str(i)+' : Disabled'
        webcam_list = '\n'.join(webcam_list)
        messagebox.showinfo("Webcam Ports",webcam_list)


    # function for handling events when mic port is entered and submit button is pressed
    def enter_mic_port():
        global valid_mic_port

        # getting data from mic port entry
        port = mic_port.get()
        mic_list = sr.Microphone.list_microphone_names()
        
        if port=='': # if nothing is entered 
            messagebox.showerror("Invalid Microphone Port","Microphone Port number can't be empty")
            
        elif port.isdigit(): # if entered data is digit
            
            if int(port)>=len(mic_list): # if entered digit is greater then available number of ports
                messagebox.showerror("Invalid Microphone Port","Microphone Port number exceeding ports")
                
            else: # if entered data is digit and is less then number of ports available
                valid_mic_port = int(port)
                
        else: # if entered data is not digit
            messagebox.showerror("Invalid Microphone Port","Enter valid Microphone Port number")


    # function for handling events when webcam port is entered and submit button is pressed
    def enter_webcam_port():
        global valid_webcam_port
        webcam_list = []

        # checking whether first five ports for webcam are opened or not and saving result as true or false in webcam_list
        for i in range(5):
            cap = cv.VideoCapture(i)
            if cap.isOpened():
                webcam_list.append(True)
                
            else:
                webcam_list.append(False)

        # getting data from webcam port entry
        port = webcam_port.get()
        
        if port=='': # if nothing is entered
            messagebox.showerror("Invalid Webcam Port","Webcam Port number can't be empty")
            
        elif port.isdigit(): # if entered data is digit
            
            if int(port)>=5: # if entered digit is greater than 5
                messagebox.showerror("Invalid Webcam Port","Webcam Port number exceeding ports")
                
            elif webcam_list[int(port)]: # if entered digit webcam port is available
                valid_webcam_port = int(port)
                
            else: # if entered digit webcam port is not available
                messagebox.showerror("Invalid Webcam Port","Webcam at this Port number is disabled")
                
        else: # if entered data is not digit
            messagebox.showerror("Invalid Webcam Port","Enter valid Webcam Port number")


    # function to save the path in the file
    def enter_directory():
        global response_text

        messagebox.showinfo("Address syntax","Enter address using forward slash '/'")

        # taking address entered
        path = address.get()

        try:
            if os.path.exists(path):        
                #open file in append mode
                f = open('files/application_address_file.txt','a')
                path = path + '\n'
                f.write(path)
                f.close()
                
                response_text = 'Directory path saved'
            else:
                messagebox.showerror("Invalid Address","Address does not exists")
                response_text = 'Failed to save address'
        except:
            messagebox.showerror("Invalid Address","Enter Valid Address")


    # function to update status, response, and command on the display every 200 microseconds
    def update():
        global status_text, response_text, voice_activate_flag, token_activate_flag, valid_mic_port, valid_webcam_port, voice_terminate_flag, token_terminate_flag
        global terminate_flag, webcam_image
        
        nonlocal webcam_port_error_flag, mic_port_error_flag, t3, t4, command_count, previous_command, root, web_frame

        if terminate_flag:
            root.destroy()

        
        # deleting available data on status
        status.delete(1.0,END)
        
        # inserting next status_text on status
        status.insert(INSERT,status_text)

        # deleting available data on response
        response.delete(1.0,END)
        
        # inserting next response_text on response
        response.insert(INSERT,response_text)

        # if command count has been 16 then reset the display
        if command_count==16 and voice_activate_flag:
            text.delete(1.0,END)
            if command != previous_command and command!=None:
                text.insert(INSERT,'\n'+command)
                previous_command = command
                command_count = 0

        # if command count has not been 16
        elif voice_activate_flag:
            if command != previous_command and command!=None:
                text.insert(INSERT,'\n'+command)
                previous_command = command
                command_count+=1

        # if webcam_image is available then show it on GUI
        if type(webcam_image)==np.ndarray:

            # copy the image
            image = webcam_image.copy()
            
            #converting opencv opened image to 'rgb' mode
            image[:,:,0] = webcam_image[:,:,2]
            image[:,:,2] = webcam_image[:,:,0]

            #converting opencv opened image into PIL.Image
            image = Image.fromarray(image)

            # resizing image to fit the display
            image = image.resize((320,240))

            #creating ImageTk object of PIL.Image
            image = ImageTk.PhotoImage(image)

            # creating an image label
            image_label = Label(web_frame, image = image)
            image_label.image = image
            image_label.grid(row = 5, column = 3, rowspan = 10, columnspan = 5)

        # if voice controlled is turned off then kill the thread
        if not voice_activate_flag:
            if t3!=0:
                #t3.join()
                t3 = 0

        # if voice control checkbox is activated then turn the flag on
        if activate_voice_state.get()==1:

            # if thread has not been created yet then create
            if t3==0:

                # if mic port number has not been entered then show error
                if valid_mic_port=='null':

                    if mic_port_error_flag: # if error has been shown once then pass
                        pass
                    
                    else: # if error has not been shown then show error and mark flag as True
                        messagebox.showerror("Invalid Microphone Port","Enter valid Microphone Port number")
                        mic_port_error_flag = True

                # if mic port number has been entered then create thread for audio function
                else:
                    voice_activate_flag = True
                    response_text = 'Voice Control activated'

                    # creating thread
                    t3 = threading.Thread(target = audio)

                    # starting thred4 for token control
                    t3.daemon = True
                    t3.start()
        elif activate_voice_state.get()==0:
            voice_activate_flag = False
            mic_port_error_flag = False
            
            # waiting untill thread 3 is completed or stopped
            if t3!=0:
                response_text = 'Voice Control Deactivated'
                status_text = 'Audio functin thread killed'
                #t3.join()
                t3 = 0

        # if token control is turned on using voice
        if token_activate_flag:
            
            # if thread has not been created yet then create
            if t4==0:

                # if webcam port number has not been entered then show error
                if valid_webcam_port=='null':

                    if webcam_port_error_flag: # if error has been shown once then pass
                        pass
                    
                    else: # if error has not been shown then show error and mark flag as True
                        messagebox.showerror("Invalid Webcam Port","Enter valid Webcam Port number")
                        webcam_port_error_flag = True

                # if webcam port number has been entered then create thread for video function
                else:
                    token_activate_flag = True
                    response_text = 'Token control activated'

                    # creating thread
                    t4 = threading.Thread(target = video)

                    # starting thred4 for token control
                    t4.daemon = True
                    t4.start()
                    
        # if token control is turned off using voice
        else:
            if t4 != 0:
                #t4.join()
                t4 = 0

        # if token control checkbox is activate then turn the flag on 
        if activate_token_state.get()==1:

            # if thread has not been created yet then create
            if t4==0:

                # if webcam port number has not been entered then show error
                if valid_webcam_port=='null':

                    if webcam_port_error_flag: # if error has been shown once then pass
                        pass
                    
                    else: # if error has not been shown then show error and mark flag as True
                        messagebox.showerror("Invalid Webcam Port","Enter valid Webcam Port number")
                        webcam_port_error_flag = True

                # if webcam port number has been entered then create thread for video function
                else:
                    token_activate_flag = True

                    # creating thread
                    t4 = threading.Thread(target = video)

                    # starting thred4 for token control
                    t4.daemon = True
                    t4.start()

        # if token control is deactivated then turn the flag off and kill the thread 4 for video
        elif activate_token_state.get()==0:
            token_activate_flag = False
            flag = False
            
            # waiting untill thread 4 is completed or stopped
            if t4!=0:
                response_text = 'Token Control Deactivated'
                status_text = 'Token function thread killed'
                #t4.join()
                t4 = 0

        # updating
        root.after(10,update)

    # function to display voice commands
    def voice_commands():
        root = Tk()
        root.geometry('330x435')
        root.title('Voice Commands')
        root.config(bg='gray')
        frame = LabelFrame(root, bd = 5, padx = 5, pady = 5)
        frame.grid(row = 0, column = 0)

        scroll = Scrollbar(root)
        scroll.grid(row = 0, column = 1, sticky = N+S)

        list_box = Listbox(frame, yscrollcommand = scroll.set, bd = 5, width = 35, height = 20)
        list_box.config(font=("Times New Roman", 12, 'italic'))
        list_box.grid(row = 0, column = 0)
        commands_list = ['Activate Voice Control', 'Deactivate Voice Control', 'Pause Voice Control', 'Reactivate Voice Control', 'Press [keyboard button]',
                         'Current Time', 'Calendar', 'Exit Program', 'System Shutdown', 'Lock Mouse', 'Unlock Mouse', 'Double Click', 'Left Click', 'Right Click',
                         'All Open Window', 'Select [window_name/file_name]', 'Open [window_name/file_name]', 'Minimize Window', 'Maximize Window', 'Close Window',
                         'Minimize All', 'Close All', 'Activate Media', 'Next', 'Previous', 'Slow Forward', 'Fast Forward', 'Slow Backward', 'Fast Backward', 'Play',
                         'Pause', 'Volume Down', 'Volume Up', 'Volume Mute', 'Volume Unmute', 'Activate Write', 'Deactivate Write']
        for data in commands_list:
            list_box.insert(END, data)
        scroll.config( command = list_box.yview )
        root.mainloop()

    # function to display gesture commands
    def gesture_commands():
        root = Tk()
        root.geometry('450x195')
        root.title('Gesture Commands')
        root.config(bg='gray')
        frame = LabelFrame(root, bd = 5, padx = 5, pady = 5)
        frame.grid(row = 0, column = 0)

        scroll = Scrollbar(root)
        scroll.grid(row = 0, column = 1, sticky = N+S)

        list_box = Listbox(frame, yscrollcommand = scroll.set, bd = 5, width = 50, height = 8)
        list_box.config(font=("Times New Roman", 12, 'italic'))
        list_box.grid(row = 0, column = 0)
        commands_list = ['Swiping from left to right : Fast forwarding media', 'Swiping from right to left : Fast backwarding media',
                         'Swiping from up to down : Reducing media volumn', 'Swiping from down to up : Increasing media volume']
        for data in commands_list:
            list_box.insert(END, data)
        scroll.config( command = list_box.yview )
        root.mainloop()


    # creating object of tkinter window
    root = Tk()

    # settting dimensions of window
    root.geometry('880x600')

    # setting title of window
    root.title('Gesture Control System - RedoneTech')

    # setting background of window
    root.config(bg='gray')

    # loading window icon
    p = PhotoImage(file = 'files/image2.png')

    # setting window icon
    root.iconphoto(False,p)

    # creating menu
    menubar = Menu(root)
    commands = Menu(menubar)
    commands.add_command(label="Voice Commands", command=voice_commands)
    commands.add_command(label="Gesture Commands", command=gesture_commands)

    ports = Menu(menubar)
    ports.add_command(label="Microphone Ports", command=microphone_ports)
    ports.add_command(label="Webcam Ports", command=webcam_ports)

    menubar.add_cascade(label="Commands",menu=commands)
    menubar.add_cascade(label="Ports",menu=ports)

    root.config(menu=menubar)
    
    # creating display frame by merging 15 rows and 3 columns and setting at position 0,0
    display_frame = LabelFrame(root, width = 335, height = 570, padx=5,pady = 5,bg = 'white', bd = 5).grid(row = 0, column = 0, rowspan = 15,columnspan = 3, padx = 5, pady = 5)

    # creating other frame by merging 15 rows and 4 columns and setting at position 0,3
    other_frame = LabelFrame(root, width = 525, height = 570, padx=5,pady = 5,bg = 'white', bd = 5).grid(row = 0, column = 3, rowspan = 15,columnspan = 5, padx = 5, pady = 5)

    # creating 'Status' label frame setting at positon 0,0 inside display frame
    status_label = LabelFrame(display_frame, text = 'Status', height = 200,width = 280, padx = 5, pady = 5, bg = 'white', bd = 5)
    status_label.grid(row = 0, column = 0, rowspan = 2, columnspan = 3, padx = 5, pady = 5)
    # setting font and size of text 'Status'
    status_label.config(font=("Times New Roman", 12))

    # creating text object to display status of program, setting it's position at 0,0 with 1 row and 3 columns
    status = Text(status_label, height = 2, width = 35, padx = 5, pady = 5, bg = 'white', bd = 3)
    status.grid(row = 0, column = 0, rowspan = 1, columnspan = 3)

    # creating 'Response' label frame setting at positon 2,0 inside display frame
    response_label = LabelFrame(display_frame, text = 'Response', height = 200,width = 280, padx = 5, pady = 5, bg = 'white', bd = 5)
    response_label.grid(row = 2, column = 0, rowspan = 2, columnspan = 3, padx = 5, pady = 5)
    # setting font and size of text 'Response'
    response_label.config(font=("Times New Roman", 12))

    # creating text object to display response of program, setting it's position at 2,0 with 1 row and 3 columns
    response = Text(response_label, height = 2, width = 35, padx = 5, pady = 5, bg = 'white', bd = 3)
    response.grid(row = 2, column = 0, rowspan = 1, columnspan = 3)
    
    # creating 'Command Display' label frame at position 2,0 with 13 rows and 3 columns
    text_label = LabelFrame(display_frame, text = 'Commands Display', height = 320, width = 280, padx = 5, pady = 5, bg = 'white', bd = 5)
    text_label.grid(row = 4, column = 0, rowspan = 11, columnspan = 3)
    # setting font and size of text 'Command Display'
    text_label.config(font=("Times New Roman", 12))

    # creating text object to display commands given by user at position 2,0 with 13 rows and 3 columns
    text = Text(text_label, height = 17, width = 35, padx = 5, pady = 5,  bg = 'white', bd = 3)
    text.grid(row = 4, column = 0, rowspan = 11, columnspan = 3)

    # creating label 'Enter Directory Path' at position 0,3 with 2 columns
    enter_address = Label(other_frame, text = 'Enter Directory Path     :', bg = 'white')
    enter_address.config(font=("Times New Roman", 12))
    enter_address.grid(row = 0, column = 3, columnspan = 2)

    # creating entry object and setting at position 0,5 with 2 columns
    address = Entry(other_frame,bd = 3, width = 30)
    address.grid(row = 0,column=5, columnspan = 2)

    # creating button for directory path
    directory_button = Button(other_frame, height = 1, width = 6, text = 'Submit', command = enter_directory)
    directory_button.config(font=("Ariel", 10))
    directory_button.grid(row = 0, column = 7)

    # creating label 'Enter Mic Port No' at position 1,3 with 2 columns
    mic_label = Label(other_frame, text = 'Enter Mic Port No        :', anchor = 'w', bg = 'white')
    mic_label.config(font=("Times New Roman", 12))
    mic_label.grid(row = 1, column = 3, columnspan = 2)

    # creating entry object and setting at position 1,5 with 2 columns 
    mic_port = Entry(other_frame,bd = 3, width = 30)
    mic_port.grid(row = 1,column=5, columnspan = 2)

    # creating button for mic port
    mic_button = Button(other_frame, height = 1, width = 6, text = 'Submit', command = enter_mic_port)
    mic_button.config(font=("Ariel", 10))
    mic_button.grid(row = 1, column = 7)

    # creating label 'Enter Webcam Port No' at position 2,3 with 2 columns
    webcam_label = Label(other_frame, text = 'Enter Webcam Port No :', anchor = 'w', bg = 'white')
    webcam_label.config(font=("Times New Roman", 12))
    webcam_label.grid(row = 2, column = 3, columnspan = 2)

    # creaing entry object and setting at position 2,5 with 2 columns
    webcam_port = Entry(other_frame,bd = 3, width = 30)
    webcam_port.grid(row = 2,column=5, columnspan = 2)

    # creating button for webcam port
    webcam_button = Button(other_frame, height = 1, width = 6, text = 'Submit', command=enter_webcam_port)
    webcam_button.config(font=("Ariel", 10))
    webcam_button.grid(row = 2, column = 7)

    # creating label 'Activate Voice\nControl' at position 3,3
    activate_voice = Label(other_frame, text = 'Activate Voice\nControl :', anchor = 'w', bg = 'white')
    activate_voice.config(font=("Times New Roman", 12))
    activate_voice.grid(row = 3, column = 3)

    # creating check button at position 3,4
    activate_voice_state = IntVar()
    voice = Checkbutton(other_frame, bg = 'white', variable = activate_voice_state, onvalue = 1, offvalue = 0).grid(row = 3, column = 4)

    # creating label ''Activate Token\nControl' at position 3,5
    activate_token = Label(other_frame, text = 'Activate Token\nControl :', anchor = 'w', bg = 'white')
    activate_token.config(font=("Times New Roman", 12))
    activate_token.grid(row = 3, column = 5)

    # creating check button at position 3,6
    activate_token_state = IntVar()
    token = Checkbutton(other_frame, bg = 'white', variable = activate_token_state, onvalue = 1, offvalue = 0).grid(row = 3, column = 6)

    # creating label 'Webcam projection' at position 4,3
    webcam = Label(other_frame, text = 'Webcam projection', bg = 'white')
    webcam.config(font=("Times New Roman", 15))
    webcam.grid(row = 4, column = 3, columnspan = 5)

    # creating labelframe for webcam projection at position 5,3
    web_frame = LabelFrame(other_frame, height = 250, width = 330, bg = 'white', bd = 5).grid(row = 5,column = 3, rowspan = 10, columnspan = 5)

    # showing message to enter port number in order to run program
    message_flag = True
    if message_flag:
        messagebox.showwarning("Required","Enter mic port number and webcam port number first")

    root.after(10,update)    
    root.mainloop()

    terminate_flag = True

        

# deriving function
if __name__ == "__main__":
    
    # creating thread
    t1 = threading.Thread(target = GUI)
    t2 = threading.Thread(target = master)
    
    ##### t2 is the master thread obtaining information from other thread and controlling the system 
    ##### t1 is the interface thread which will receive information from global variables and display it
    
    # starting thread 1
    t1.daemon = True
    t1.start()
    
    # starting thread 2
    t2.daemon = True
    t2.start()
        
    # wait until thread 1 is completely executed 
    t1.join()
    
    # wait until thread 2 is completely executed 
    t2.join()
    
    exit()
    
