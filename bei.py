import tkinter as tk
# from backend import *
import random
import sys
import csv

list_CN = []
list_EN = []


def parseTXT(txtName):

    fp = open(txtName, 'r')
    lines = fp.readlines()

    global list_CN
    global list_EN

    for line in lines:
        r = line.split()

        list_EN.append(r[0])
        list_CN.append((str(r[1:])[2:-2]))

    return


class Application:
    def __init__(self, master):
        self.wordState = False  # False for unknown and True for known.
        self.level = 0          # 0 for not choose, 1 for first choice, 2 for more choice
        self.master = master    # storing the window var
        self.index = 0
        self.isShown_CN = False
        self.currentFile = ''
        self.currentFileFolder = ''
        self.badDict = {}
        self.word_eg = tk.StringVar()
        self.word_ch = tk.StringVar()
        self.ViewControl()
        self.keyboardSupoort()  # enable keyboard binding

    def NextNewWord(self):
        # todo: delete prev entry
        self.updateBothButtons('我忘了', '我记得')

        if self.wordState == False:
            # save this to badict
            print('saved to baddict')
            print(list_EN[self.index])
            if list_EN[self.index] not in self.badDict:
                self.badDict[list_EN[self.index]] = 1
            else:
                self.badDict[list_EN[self.index]] = self.badDict[list_EN[self.index]] + 1
            print(self.badDict)

        else:
            list_CN.pop(self.index)
            list_EN.pop(self.index)


        self.updateStatusBar('yellow')

        self.index = random.randint(0, len(list_EN)-1)
        self.level = 0
        self.wordState = False
        self.updateCHN('')
        self.updateENG(list_EN[self.index])
        # self.updateStatusBar()

    def control(self, isRemembered):
        if len(list_EN) == 0:
            # write baddict to file
            print(self.badDict)
            with open('result/10.csv', 'w') as f:
                for key in self.badDict.keys():
                    f.write('%s     %s\n' % (key, self.badDict[key]))

        # print('level is %d' % self.level)
        if self.level == 0:
            self.level = 1
            if isRemembered == True:
                self.wordState = True
            else:
                self.wordState = False

            self.updateCHN(list_CN[self.index])
            return

        if self.level == 1:

            self.level = 2
            if self.wordState == True and isRemembered == True:

                self.NextNewWord()
            if self.wordState == False and isRemembered == False:
                self.NextNewWord()

            else:
                self.wordState == False
                if isRemembered == False:
                    self.updateBothButtons('忘记了', '下一个')
                    self.updateStatusBar('red')
                    return

                self.NextNewWord()
            return

        if self.level == 2:
            # regret
            self.wordState == False
            if isRemembered == False:
                self.updateBothButtons('忘记了', '下一个')
                self.updateStatusBar('red')
                return

            self.NextNewWord()
            return

    def RemHelper(self):
        self.control(True)

    def FgtHelper(self):
        self.control(False)

    def updateENG(self, input):
            # remember to call master.update after it
        print('updating eng: %s' % input)
        self.ShowingWord.config(text=input)
        # self.button_remember.config(text='我记得')

    def updateCHN(self, input):
                # remember to call master.update after it
        print('updating chn: %s' % input)
        self.ShowingResult.config(text=input)
        # self.button_remember.config(text='下一个')

    def updateBothButtons(self, t1, t2):
        self.button_forget.config(text=t1)
        self.button_remember.config(text=t2)

    def keyStroke(self, event):
        # print(">>>>>>>>>>>>>>>>s")
        # print(event.char)
        # print(event.keycode)
        # print(event)
        # print('>>>>>>>>>>>>>>>>>>')
        if event.char == 'a'  or event.keycode == 100 or event.keycode == 113 or event.char == '\uf702':
            self.FgtHelper()
        if event.char == 's'  or event.keycode == 102 or event.keycode == 114 or event.char == '\uf703':
            self.RemHelper()

    def updateStatusBar(self, fgColor='MISS'):
        # self.label_title_right.config(text=self.currentFile)
        remain = '(剩余:' + str(len(list_EN)) + ')'
        if fgColor == 'MISS':
            self.label_title.config(text=remain)
        else:
            self.label_title.config(text=remain, fg=fgColor)

            # self.label_title_right.config()

    def ViewControl(self):
        self.frame_StatusBar = tk.Frame(self.master, bg='green')
        self. frame_WordWindow = tk.Frame(self.master, bg='grey')
        self.frame_OperationWindow = tk.Frame(self.master, bg='green')

        self.inner_frame_StatusBar = tk.Frame(
            self.frame_StatusBar, bg='green')
        self.inner_frame_WordWindow = tk.Frame(self.frame_WordWindow)
        self.inner_frame_OperationWindow = tk.Frame(self.frame_OperationWindow)

        # pack the frame up
        self.frame_StatusBar.pack(side='top', fill='x')
        self.frame_WordWindow.pack(side='top', fill='x')
        self.frame_OperationWindow.pack(fill='both', expand='yes')
        self.inner_frame_StatusBar.pack(
            fill='both', expand='yes', padx=5, pady=3)
        self.inner_frame_WordWindow.pack(
            fill='both', expand='yes', padx=3, pady=3)
        self.inner_frame_OperationWindow.pack(
            fill='both', expand='yes', padx=3, pady=3)

        # create widgets
        self.label_title_left = tk.Label(
            self.inner_frame_StatusBar, text='')
        self.label_title = tk.Label(
            self.inner_frame_StatusBar, text='', bg='green')
        self.label_title_right = tk.Label(
            self.inner_frame_StatusBar, text='')

        self.ShowingWord = tk.Label(
            self.inner_frame_WordWindow, text='Wait for Load', font=('Arial', 20))
        self.line_between = tk.Canvas(
            self.inner_frame_WordWindow, height=2, bg='grey')
        self.ShowingResult = tk.Label(
            self.inner_frame_WordWindow, text='Wait for Load', font=('Arial', 13))

        self.button_forget = tk.Button(
            self.inner_frame_OperationWindow, text='我忘了', width=13, height=5, command=self.FgtHelper)
        self.button_remember = tk.Button(
            self.inner_frame_OperationWindow, text='我记得', width=13, height=5, command=self.RemHelper)

        self.imageLoad = tk.Canvas(bg='red')

        self.button1 = tk.Button(
            self.master,  text='Setttings', width=25, command=self.StartSetttings)

        # pack them up
        # self.label_title_left.pack(side='left')
        self.label_title.pack(side='top', fill='both')
        # self.label_title_right.pack(side='left')
        self.ShowingWord.pack(side='top', fill='x', expand='yes')
        self.line_between.pack(side='top', fill='x', expand='yes')
        self.ShowingResult.pack(side='top', fill='x', expand='yes')

        self.button_forget.pack(side='left', anchor='ne', fill='y')
        self.button_remember.pack(side='right', anchor='nw', fill='y')
        # self.imageLoad.pack(fill='both')
        self.button1.pack()

    def StartSetttings(self):

        self.newWindow = tk.Toplevel(self.master)
        self.app = SubApplication(self.newWindow)

    def keyboardSupoort(self):
        self.master.bind("a", self.keyStroke)
        self.master.bind("s", self.keyStroke)
        self.master.bind("<Right>", self.keyStroke)
        self.master.bind("<Left>", self.keyStroke)


class SubApplication:
    def __init__(self, master):
        self.master = master
        self.ViewControl()


    def ViewControl(self):
        self.SettingFrame = tk.Frame(self.master)

        self.quitButton = tk.Button(
            self.SettingFrame, text='Quit', width=25, command=self.close_windows)
        self.setting_entry_indicator = tk.Label(
            self.SettingFrame, text='输入读取文件地址(请放在当前目录下)')
        self.file_location = tk.Entry(self.SettingFrame)

        self.entry1 = tk.Entry(self.SettingFrame)

        self.entry1Button = tk.Button(self.SettingFrame)
        self.entry1Label = tk.Label(self.SettingFrame, text='entry1')
        self.entry2 = tk.Entry(self.SettingFrame)
        self.entry2Button = tk.Button(self.SettingFrame)
        self.entry2Label = tk.Label(self.SettingFrame, text='entry2')

        self.entry3 = tk.Entry(self.SettingFrame)
        self.entry3Button = tk.Button(self.SettingFrame)
        self.entry3Label = tk.Label(self.SettingFrame, text='entry3')

        self.SettingFrame.pack()
        # self.entryFrame1.pack()
        # self.entryFrame2.pack()
        # self.entryFrame3.pack()

        self.entry1Label.pack()
        self.entry1.pack()

        self.entry2Label.pack()
        self.entry2.pack()

        self.entry3Label.pack()
        self.entry3.pack()

        self.setting_entry_indicator.pack()
        self.file_location.pack()

        self.quitButton.pack()

    def close_windows(self):
        self.master.destroy()


def main(txtName):
    parseTXT(txtName)

    root = tk.Tk()
    root.title('GREat@背单词')
    root.geometry('280x300')
    app = Application(root)
    app.NextNewWord()
    root.mainloop()


if __name__ == '__main__':
    print(len(sys.argv))
    if len(sys.argv) == 2:
        txtName = sys.argv[1]
    else:
        txtName = '08red/10.txt'
    main(txtName)
