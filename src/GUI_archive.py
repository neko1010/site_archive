from tkinter import *
from archive_files import *
from tkinter import filedialog, messagebox
import os

def insert_files():
    """
    Function to insert files to archive into visible listbox widget
    """
    filenames = filedialog.askopenfilenames(multiple = True)
    for file in filenames:
        listbox.insert( 'end', file)

def process():
    """
    Function that runs archival program and destroys parent and error widgets
    """
    ## List of files in current window
    files = list(listbox.get(0, 'end'))
    
    ## Checking for site visit XML 
    if any(os.path.splitext(f)[1] == '.xml' and os.path.split(f)[1].startswith("SV") for f in files):
        ## Determine destination for files
        dest = final_dest(files)
        archive_files(files, dest)
        #root.destroy()
        
        ##Message to confirm archival completion
        msg_root = Tk()
        msg_root.withdraw()
        messagebox.showinfo("Processing complete", "Files archived to " + dest)
        msg_root.destroy()
        
    else:
        ## Message that communicates absence of site visit XML
        err_root = Tk()
        err_root.withdraw()
        messagebox.showerror("Invalid file entry", "Site visit XML file missing!")
        err_root.destroy()


root = Tk()
root.title("Site Visit File Archive Tool")

## Configuring columns and rows with weight other than the default(0)
## allows for dynamic resizing
root.columnconfigure(1, weight = 1)
#root.columnconfigure(2, weight = 1)
root.rowconfigure(1, weight =1 )

menu = Menu(root)
root.config(menu= menu) 

explanation = "Select site visit files and archive them with the click of a button! This version requires a 'master' site visit XML document that will guide ancillary files associated with the site visit to the proper location. Only one site visit and associated supporting documents are currently supported. If files need to be appended to an existing archived site vist, no problem. Insert files to be archived along with the site visit XML, and proceed as usual."

## Menu
filemenu = Menu(menu)
helpmenu = Menu(menu)

menu.add_cascade(label = "File", menu = filemenu)
menu.add_cascade(label = "Help", menu = helpmenu)

filemenu.add_command(label = "Exit", command = root.destroy)
helpmenu.add_command(label = "About", 
        command = lambda : messagebox.showinfo("About", explanation))

## Logo for GUI
logo = PhotoImage(file = '../img/logo/round.png')
insert_logo = Label(image = logo).grid(row = 1, rowspan = 3, column = 0)

label = Label(text = "Files to archive: ", justify = RIGHT)
label.grid(row = 0, column = 1)

## Listbox with weights for dynamic resizing
listbox = Listbox(root, width = 50, height = 13)
listbox.grid(row = 1, column = 1, columnspan = 3, sticky = NSEW)
listbox.columnconfigure(1, weight = 1)
listbox.rowconfigure(1, weight = 1)

## Scrollbar
xscroll = Scrollbar(root, orient = 'horizontal', command = listbox.xview)
xscroll.grid(row = 3, column = 1, columnspan = 3, sticky = EW)

## Clear list button
clearButton = Button( text = "Clear List", command = lambda : listbox.delete(0, 'end'), width = 20)
clearButton.grid(row = 4, column = 2, padx = 5, pady = 5)

## Button to insert files
addButton = Button( text = "Add Files", command = insert_files, width = 20)
addButton.grid(row = 4, column = 3)

## Remove button
remButton = Button( text = "Remove File", command = lambda : listbox.delete(listbox.curselection()), width = 20)
remButton.grid(row = 5, column = 2, padx = 5)

## Button to run archival tool
procButton = Button( text = "Archive", command = process, width = 20)
procButton.grid(row = 5, column = 3)

root.mainloop()
