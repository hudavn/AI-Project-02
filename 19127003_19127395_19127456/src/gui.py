from os import system
from tkinter import *
from tkinter import messagebox
import tkinter
import time
from tkinter import filedialog
from tkinter import ttk
from threading import Thread
import threading
import backend as BE

Color = ['green', 'IndianRed1', 'black']
choices = ['Astar', 'Backtracking', 'Brute force', 'PySAT']
delay = ['0.5', '0.75', '1.0', '1.25', '1.5']


def readMatrix(strinput):
    f = open(strinput[:-1])
    Matrix = [[int(num) for num in line.split()] for line in f]
    return Matrix


def getConstraint(matrix):
    i = 0
    for x in matrix:
        for y in x:
            if y >= 0:
                i += 1
    return i


class colorPuzzle(Frame):

    def gridGUI(obj):
        obj.entAddr.grid(row=0, sticky=W, padx=8)
        obj.butBrowser.grid(row=0, column=1)
        obj.Delay.grid(row=1, sticky=W, padx=8)
        obj.Algorithm.grid(row=2, column=0, sticky=W, padx=8)
        obj.butStart.grid(column=1, row=1)
        obj.lbframe.grid(row=4, columnspan=2)
        obj.LbinfoFrame.grid(row=3, columnspan=2)

    def __init__(obj, master):
        super().__init__(master)
        obj.halt = False
        obj.stepHeur = Label(obj, font='Times 12')
        obj.entAddr = Text(obj, font='Times 12', height=1)
        obj.Delay = ttk.Combobox(obj, values=delay)
        obj.lbframe = LabelFrame(obj, text='Algorithm', font='Times 16')
        obj.Algorithm = ttk.Combobox(obj, values=choices)
        obj.butBrowser = Button(
            obj, text='Browse Files', font='Times 12', command=lambda: obj.browseFiles())
        obj.butStart = Button(
            obj, text='Start', font='Times 12', command=lambda: obj.start())
        obj.LbinfoFrame = LabelFrame(obj, bg='burlywood1')
        obj.gridGUI()

    def browseFiles(obj):
        filename = filedialog.askopenfilename(
            title="Select a File",
            filetypes=(("Text files",
                        "*.txt*"),
                       ("all files",
                        "*.*")))

        obj.entAddr.delete("1.0", tkinter.END)
        obj.entAddr.insert(tkinter.END, filename)
        InforMatix = readMatrix(obj.entAddr.get('1.0', tkinter.END))
        ColorMatrix = [[-1 for i in range(0, len(InforMatix))]
                       for j in range(0, len(InforMatix))]
        obj.createBoard(InforMatix, ColorMatrix)
        for x in obj.LbinfoFrame.winfo_children():
            x.destroy()
        Label(obj.LbinfoFrame, text=f'SIZE: {len(InforMatix)}x{len(InforMatix)}', font=(
            'Helvetica bold', 12), bg='burlywood1').grid(row=0, column=0, padx=10)
        Label(obj.LbinfoFrame, text=f'CONSTRAINTS: {getConstraint(InforMatix)}', font=(
            'Helvetica bold', 12), bg='burlywood1').grid(row=0, column=1, padx=10)
        Label(obj.LbinfoFrame, font=('Helvetica bold', 12),
              text='TIME LIMIT: 10 minutes', bg='burlywood1').grid(row=0, column=3)

    def createCell(obj, inf, clr):
        if inf < 0:
            inf = " "
        lb = tkinter.Label(obj.lbframe, text=inf, font='Times 12',
                           bg=Color[clr], fg='white', height=2, width=4, border=0.5, relief=RIDGE)
        return lb

    def createBoard(obj, MaInfo, MaColor):
        for x in obj.lbframe.winfo_children():
            x.destroy()

        for i in range(0, len(MaInfo)):
            for j in range(0, len(MaInfo)):
                obj.createCell(MaInfo[i][j], MaColor[i]
                               [j]).grid(column=j, row=i)

    def start(obj):
        InforMatix = readMatrix(obj.entAddr.get('1.0', tkinter.END))
        ColorMatrix = [[-1 for i in range(0, len(InforMatix))]
                       for j in range(0, len(InforMatix))]
        obj.createBoard(InforMatix, ColorMatrix)
        obj.lbframe['text'] = obj.Algorithm.get()
        fileAddr = obj.entAddr.get('1.0', tkinter.END)[:-1]
        algo = obj.Algorithm.get()
        if obj.Delay.get():
            delayTime = float(obj.Delay.get())
        else: delayTime = 0.5

        if fileAddr == '' or algo == '':
            # show messagebox
            messagebox.showinfo("ErrorMessage", "fill can not empty")
        else:
            time.sleep(0.5)
            threading.Thread(target=BE.Execute, args=(
                fileAddr, algo, delayTime)).start()
            while not BE.executeFinish:
                obj.Restart(-1, -1, BE.color)
                obj.Restart(-1, -1, BE.color)

            messagebox.showinfo("CONGRATULATIONS", "SUCCESS!")

    def Restart(obj, step, heur, maColor):
        obj.update()
        obj.UpdateColor(maColor)
        # print lai step va heuristic
        obj.stepHeur['text'] = f'step: {step} - heuristic: {heur}'
        if obj.Delay.get() == '':
            time.sleep(0.1)
        else:
            time.sleep(float(obj.Delay.get())-0.3)

    def getInfoStart(obj):
        return (obj.entAddr.get('1.0', tkinter.END), obj.Algorithm.get())

    def UpdateColor(obj, matrix):
        for i in range(0, len(matrix)):
            for j in range(0, len(matrix)):
                obj.lbframe.grid_slaves(row=i, column=j)[
                    0].config(bg=Color[matrix[i][j]])


window = Tk()
window.title("ColorPuzzle")
Main = colorPuzzle(window)
Main.pack()
Main.mainloop()
