from tkinter import *
from calendar import *
from PIL import Image, ImageTk

def showCal(y,m) : 
  
    # Create a GUI window 
    new_gui = Tk() 
      
    # Set the background colour of GUI window 
    img = Image.open('sky.jpg')
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

#y,m = list(map(int,input("Enter year and month: ").split()))
showCal(2020,12)
