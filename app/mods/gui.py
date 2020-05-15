import tkinter as tk

ft = ('Helvetica', 18, 'bold')

class DigiPyRo(tk.Tk()):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class CoverPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Info Page!", font=ft).pack()
        tk.Label(self, text=" Information about DigiPyRo").pack()

        tk.Button(self, text="Help",
                  command=lambda : master.switch_frame(HelpPage)).pack()

        tk.Button(self, text="Start",
                  command=lambda : master.switch_frame(StartPage)).pack()

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Start Page!", font=ft).pack()

        tk.Button(self, text="Help",
                  command=lambda : master.switch_frame(HelpPage)).pack()

        tk.Button(self, text="Start").pack()

class HelpPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Help Page!", font=ft).pack()



        self.master = master
        master.title('DigiPyRo')
        canvas = Canvas(master, height=480, width=480).pack()

        frame = Frame()
        frame.place(relx=0.3, rely=0.1, relwidth=0.8, relheight=0.8)

        label = Label(frame, text="Information about DigiPyRo!")
        label.grid(row=0, column=1)

        self.button1 = Button(frame,
                              text="Help",
                              cursor="hand1").grid(row=1, column=1)
        self.button2 = Button(frame,
                              text="Start",
                              cursor="hand1").grid(row=2, column=1)

def main():
    root = Tk()
    app = Main_Window(root)
    root.mainloop()

if __name__ == '__main__':
    main()
# startButton = Button(main_window,
                     # text="Start",
                     # cursor="hand1").pack()
