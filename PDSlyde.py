from pypdf import PdfReader,PdfWriter,Transformation,PaperSize,PageObject
from pypdf.generic import RectangleObject
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import os



     
def PrintCat():
    print(" _._     _,-'""`-._")
    print("(,-.`._,'(       |\\`-/|")
    print("    `-.-' \\ )-`( , o o)")
    print("          `-    \\`_`"'-')
    print("\nYou probably don't need the debug terminal so here's a kitty instead")


def filePath():
    #open file selector and assign path to readFile
    readFile = filedialog.askopenfilename(initialdir= "/",title= "Select File To Read",filetypes=[('PDF Files','*.pdf')])

    #check if a file was selected
    if readFile == '':
        print("Error No file Selected")
        return
    
    #Create ouput path for file
    outputName = os.path.dirname(readFile) + "/Converted_" + os.path.basename(readFile)

    #create reader and writer for pdf
    reader = PdfReader(readFile)
    writer = PdfWriter()
    
    #store number of pages in orig pdf
    numPages = len(reader.pages)

    #default page sizes
    defaultPageWidth = PaperSize.A4.width
    defaultPageHeight = PaperSize.A4.height

    #slides
    pageToMerge = reader.pages[0]
    pageToMerge2 = reader.pages[1]

    #page slides are drawn on
    basePage = PageObject.create_blank_page(width = defaultPageWidth,height =defaultPageHeight)

    #transforms of slides
    transform1 = Transformation().scale((defaultPageWidth/pageToMerge.mediabox.width),(defaultPageHeight/pageToMerge.mediabox.height/2) -.1).translate(0,defaultPageHeight - pageToMerge.mediabox.height)
    transform2 = Transformation().scale((defaultPageWidth/pageToMerge.mediabox.width),(defaultPageHeight/pageToMerge.mediabox.height/2) -.1).translate(0,defaultPageHeight - (pageToMerge.mediabox.height *2))

    #counter variable for pages in loop
    i = 0

    #loop all slides and write them to base pages
    for page in reader.pages:
        statusLabel.config(text="converting slide " + str(i + 1))
        statusLabel.update()
        
        if i % 2 == 0:
            
        #makes ptm1
            pageToMerge = reader.pages[i]
            pageToMerge.add_transformation(transform1)
            pageToMerge.cropbox = RectangleObject((0,0,defaultPageWidth,defaultPageHeight))
            basePage.merge_page(pageToMerge)
            if numPages % 2 != 0 and i == numPages -1:
                 writer.add_page(basePage)
        
        else: 
            
        #makes ptm2
            pageToMerge2 = reader.pages[i]
            pageToMerge2.add_transformation(transform2)
            pageToMerge2.cropbox = RectangleObject((0,0,defaultPageWidth,defaultPageHeight))
            basePage.merge_page(pageToMerge2)
        
        #creates a new base page
            writer.add_page(basePage)
        
            basePage = PageObject.create_blank_page(width= defaultPageWidth,height= defaultPageHeight)
       
    
        ##Increments Loop
        i+=1

    #write pages to output pdf
    with open(outputName,"wb") as fp:
            writer.write(fp)

    statusLabel.config(text="successfully converted " + str(i) + " slides")   




 #Print Debug Info   
PrintCat()
#Window Intitalization
window = Tk()
window.title("PDSlyde") 
window.geometry("300x100")
window.resizable(False,False)
window.config(background="gray15")

#Load Icon
ico = Image.open('PDSlyde.ico')
photo = ImageTk.PhotoImage(ico)
window.wm_iconphoto(False, photo)

#Create Buttons and Labels
statusLabel = Label(window,text="waiting for file...",background="gray15",foreground="white")
statusLabel.grid(column=0,row=1)
infoLabel = Label(window,text="For Jacks With 🎔",background="gray15",foreground="white",justify="center",anchor="w")
infoLabel.place(relx=.35,rely=1.0,anchor='sw')
openExplorer = Button(window, text= "Select PDF To Convert",command= filePath)
openExplorer.grid(column= 0, row= 0)

#GUI Loop
window.mainloop()