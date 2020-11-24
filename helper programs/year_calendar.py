from tkinter import *
from calendar import *

def showCal(y): 
  
    # Create a GUI window 
    new_gui = Tk()

    new_gui.geometry('540x600')
      
    # Set the background colour of GUI window 
    new_gui.config(background = "white") 
  
    # set the name of tkinter GUI window  
    new_gui.title("CALENDER") 
   
  
    # get method returns current text as string 
    fetch_year = 2020 
  
    cal_list = []
    for i in range(1,13):
        data = month(2020,i)[:-1]
        ind = data[::-1].index('\n')
        data = data+(7-data[-1*ind:].count(' ')-1)*' --'
        cal_list.append(data)

    k = 0
    for i in range(4):
        for j in range(3):
            Label(new_gui, text = cal_list[k], font = "Consolas 10 bold").grid(row = i, column = j, padx = 15, pady = 10)
            k+=1
  
      
    # start the GUI  
    new_gui.mainloop()


y = int(input('Enter year: '))
showCal(y)
