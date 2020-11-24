from tkinter import *
from calendar import *
from PIL import ImageTk, Image

def showCal(y): 
  
    # Create a GUI window 
    new_gui = Tk()

    new_gui.geometry('540x600')
      
    # Set the background colour of GUI window 
    img = Image.open('sky.jpg')
    img = img.resize((540,600))
    img = ImageTk.PhotoImage(img)
    bg_img = Label(new_gui,image = img)
    bg_img.grid(row = 0,column = 0)

  
    # set the name of tkinter GUI window  
    new_gui.title("CALENDER "+str(y)) 
   
  
    # get method returns current text as string 
  
    cal_list = []
    for i in range(1,13):
        data = month(y,i)[:-1]
        ind = data[::-1].index('\n')
        data = data+(7-data[-1*ind:].count(' ')-1)*' --'
        cal_list.append(data)

    k = 0
    for i in range(4):
        for j in range(3):
            Label(bg_img, text = cal_list[k], font = "Consolas 10 bold").grid(row = i, column = j, padx = 16, pady = 13)
            k+=1
  
      
    # start the GUI  
    new_gui.mainloop()


#y = int(input('Enter year: '))
showCal(2100)
