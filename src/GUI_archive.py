from tkinter import *
from archive_files import *
from tkinter import filedialog, messagebox

def insert_files():
    
    filenames = filedialog.askopenfilenames(multiple = True)
    for file in filenames:
        listbox.insert( 'end', file)

def process():
    archive_files(list(listbox.get(0,'end')))
    root.destroy()

root = Tk()
root.title("Site Visit File Archive Tool")

root.columnconfigure(1, weight = 1)
root.columnconfigure(2, weight = 2)
root.rowconfigure(1, weight =1 )

menu = Menu(root)
root.config(menu= menu) 

explanation = "Select site visit files and archive them with the click of a button!"
helpmenu = Menu(menu)
menu.add_cascade(label = "Help", menu = helpmenu)

helpmenu.add_command(label = "About", 
        command = lambda : messagebox.showinfo("About", explanation))

logo = PhotoImage(file = '../img/logo/round.png')
insert_logo = Label(image = logo).grid(row = 1, rowspan = 3, column = 0)

label = Label(text = "Files to archive: ", justify = RIGHT)
label.grid(row = 0, column = 1)

listbox = Listbox(root, width = 50, height = 13)
listbox.grid(row = 1, column = 1, columnspan = 2, sticky = NSEW)
listbox.columnconfigure(1, weight = 1)
listbox.columnconfigure(2, weight = 1)
listbox.rowconfigure(1, weight = 1)

#yscroll = Scrollbar(root, orient = 'vertical', command = listbox.yview)
#yscroll.grid(row = 1, column = 2, sticky = NS)
xscroll = Scrollbar(root, orient = 'horizontal', command = listbox.xview)
xscroll.grid(row = 3, column = 1, columnspan = 2, sticky = EW)

addButton = Button( text = "Add Files", command = insert_files, width = 20)
addButton.grid(row = 4, column = 2)

procButton = Button( text = "Archive", command = process, width = 20)
procButton.grid(row = 5, column = 2)

root.mainloop()
