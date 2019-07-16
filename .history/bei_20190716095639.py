import tkinter as tk
# from backend import *
import random
import sys

words = []
isShown_R = False
isShown_F = False
regretWord = ''
badDict = {}


def parseTXT(txtName):

    fp = open(txtName, 'r')
    lines = fp.readlines()

    global words

    for line in lines:
        r = line.split()
        # print(line)
        # print(r[0])
        # print(r[1:])

        words.append((r[0], r[1:]))

    return words


def iRemember():
    global words
    print('remember')
    if len(words) == 0:
        # this list is complete
        print('remeber done')
        print(badDict)
        return '毕'
    elif len(words) == 1:
        word = words[0]
        words = []

        return word

    index = random.randint(0, len(words) - 1)
    word = words[index]
    print(word)
    words.pop(index)
    return word


class Application:
    def __init__(self, master):
        self.word_eg = tk.StringVar()
        self.word_ch = tk.StringVar()

        self.master = master
        self.frame_StatusBar = tk.Frame(self.master, bg='green')
        self. frame_WordWindow = tk.Frame(self.master, bg='blue')
        self.frame_OperationWindow = tk.Frame(self.master, bg='green')

        self.inner_frame_StatusBar = tk.Frame(self.frame_StatusBar)
        self. inner_frame_WordWindow = tk.Frame(self.frame_WordWindow)
        self.inner_frame_OperationWindow = tk.Frame(self.frame_OperationWindow)

        # pack the frame up
        self.frame_StatusBar.pack(side='top', fill='x')
        self.frame_WordWindow.pack(side='top', fill='x')
        self.frame_OperationWindow.pack(fill='both', expand='yes')
        self.inner_frame_StatusBar.pack(
            fill='both', expand='yes', padx=5, pady=5)
        self.inner_frame_WordWindow.pack(
            fill='both', expand='yes', padx=3, pady=3)
        self.inner_frame_OperationWindow.pack(
            fill='both', expand='yes', padx=3, pady=3)

        # create widgets
        self.label_title = tk.Label(
            self.inner_frame_StatusBar, text='GREat@背单词')
        self.ShowingWord = tk.Label(
            self.inner_frame_WordWindow, text='Wait for Load', font=('Arial', 20))
        self.line_between = tk.Canvas(
            self.inner_frame_WordWindow, height=2, bg='yellow')
        self.ShowingResult = tk.Label(
            self.inner_frame_WordWindow, text='Wait for Load', font=('Arial', 10))

        def nextWord_R():
            global isShown_R
            global isShown_F
            isShown_F = False

            if isShown_R == False:
                # need to show the Chinese
                self.ShowingResult.config(text=self.word_ch)
                print('remaining: %s ' % str(len(words)))
                isShown_R = True

            else:
                isShown_R = False
                r = iRemember()
                self.word_eg = r[0]
                ch = str(r[1:])

                self.word_ch = str(ch[3:-4])
                self.ShowingWord.config(text=self.word_eg)
                self.ShowingResult.config(text='')

            print('remaining: %s ' % str(len(words)))
            self.master.update()

        def nextWord_F():
            global regretWord
            global badDict
            global isShown_F
            global isShown_R

            print('exec nextWordF: ')
            print(isShown_F)
            print(isShown_R)
            print(regretWord)

            if regretWord != self.word_eg:
                if self.word_eg not in badDict:
                    badDict[self.word_eg] = 1

                else:
                    badDict[self.word_eg] = badDict[self.word_eg] + 1

            if (isShown_R == True) and (isShown_F == False) and (regretWord != self.word_eg):
                # regret option, first exec
                print('append')
                regretWord = self.word_eg
                temp = (self.word_eg, self.word_ch)
                words.append(temp)

            elif isShown_F == False:
                print('output')
                isShown_F = True
                print(isShown_F)
                self.ShowingResult.config(text=self.word_ch)

            else:
                print('next')
                isShown_F == False
                r = iRemember()
                self.word_eg = r[0]
                ch = str(r[1:])
                self.word_ch = str(ch[3:-4])
                self.ShowingWord.config(text=self.word_eg)
                self.ShowingResult.config(text='')

            print('remaining: %s ' % str(len(words)))
            self.master.update()

        def keyStroke(event):
            print(">>>>>>>>>>>>>>>>s")
            print(event.char)
            print(event.keycode)
            if event.char == 'a' or event.keycode == 113:
                nextWord_F()
            if event.char == 's' or event.keycode == 114:
                nextWord_R()

        self.master.bind("a", keyStroke)
        self.master.bind("s", keyStroke)
        self.master.bind("<Right>", keyStroke)
        self.master.bind("<Left>", keyStroke)

        self.button_forget = tk.Button(
            self.inner_frame_OperationWindow, text='我忘了', width=13, height=5, command=nextWord_F)
        self.button_remember = tk.Button(
            self.inner_frame_OperationWindow, text='我记得', width=13, height=5, command=nextWord_R)

        self.imageLoad = tk.Canvas(bg='red')

        self.button1 = tk.Button(
            self.master,  text='Setttings', width=25, command=self.StartSetttings)

        # pack them up
        self.label_title.pack(side='left')
        self.ShowingWord.pack(side='top', fill='x', expand='yes')
        self.line_between.pack(side='top', fill='x', expand='yes')
        self.ShowingResult.pack(side='top', fill='x', expand='yes')

        self.button_forget.pack(side='left', anchor='ne', fill='y')
        self.button_remember.pack(side='right', anchor='nw', fill='y')
        self.imageLoad.pack(fill='both')
        self.button1.pack()

    def StartSetttings(self):

        self.newWindow = tk.Toplevel(self.master)
        self.app = SubApplication(self.newWindow)


class SubApplication:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(
            self.frame, text='Quit', width=25, command=self.close_windows)
        self.setting_entry_indicator = tk.Label(
            self.master, text='输入读取文件地址(请放在当前目录下)')
        self.file_location = tk.Entry(self.master)

        self.setting_entry_indicator.pack()
        self.file_location.pack()
        self.quitButton.pack()
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()


def main(txtName):
    parseTXT(txtName)

    root = tk.Tk()
    root.title('GREat@背单词')
    root.geometry('280x550')
    app = Application(root)
    r = iRemember()
    app.word_eg = r[0]
    ch = str(r[1:])
    app.word_ch = str(ch[3:-4])
    app.ShowingWord.config(text=app.word_eg)
    app.ShowingResult.config(text='')

    print('remaining: %s ' % str(len(words)))
    print(len(words))

    root.mainloop()


if __name__ == '__main__':
    txtName = sys.argv[1]
    main(txtName)
