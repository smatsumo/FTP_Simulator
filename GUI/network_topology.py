from Tkinter import Tk, BOTH, Frame, RIGHT, RAISED
from ttk import Button, Style



class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")   
         
        self.parent = parent
        self.parent.title("Generic Network Simulator")
        self.pack(fill=BOTH, expand=1)
        self.centerWindow()
        self.initUI()

    def centerWindow(self):
      
        w = 290
        h = 150

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
    def initUI(self):
      
	frame = Frame(self, relief=RAISED, borderwidth=1, background="blue")
        frame.pack(fill=BOTH, expand=1)
	self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)
        self.columnconfigure(2, pad=3)
        self.columnconfigure(3, pad=3)
        
        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)
        closeButton = Button(self, text="Close")
        closeButton.pack(side=RIGHT, padx=5, pady=5)
        okButton = Button(self, text="OK")
        okButton.pack(side=RIGHT)

def main():
  
    root = Tk()
    ex = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
