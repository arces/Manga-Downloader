import threading
from subprocess import Popen, PIPE
from time import sleep
import tkinter as tk
from tkinter import *
 
  
 
PROCESS = ['netstat','1']
class Console(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.text = tk.Text(self, undo=False)
        self.text.pack(expand=True, fill="both")
        # run process in a thread to avoid blocking gui
        t = threading.Thread(target=self.execute)
        t.start()
  
  
    def display_text(self, p):
        display = ''
        lines_iterator = iter(p.stdout.readline, b"")
        for line in lines_iterator:
            if 'Active' in line:
                self.text.delete('1.0', END)
                self.text.insert(INSERT, display)
                display = ''
            display = display + line           
 
 
    def display_text2(self, p):
        while p.poll() is None:
            line = p.stdout.readline()
            if line != '':
                if 'Active' in line:
                    self.text.delete('1.0', END)
                self.text.insert(END, line)
                p.stdout.flush()       
 
 
    def execute(self):
            p = Popen(PROCESS,  universal_newlines=True,
                   stdout=PIPE, stderr=PIPE)
            print('process created with pid: {}'.format(p.pid))
            self.display_text(p)
 
   
if __name__ == "__main__":
    root = tk.Tk()
    root.title("netstat 1")
    Console(root).pack(expand=True, fill="both")
    root.mainloop()