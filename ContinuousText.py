#!/usr/bin/env python
# -*- coding: utf-8 -*-s

import tkinter as tk
from tkinter.font import Font
from random import shuffle
import sys, os

# NON SALTA BENE SE PIGIO SPAZIO PRIMA DELLA FINE DELLA PAROLA

GENTIME = 60

wrong = 0
right = 0
spaces = 0
percent = 0
prevLen = 0
sec = GENTIME
goodW = 0
badW = 0
timeStarted = False
wIndex = 0
actIndex = 0
wrongLettersList = []
second_max = []
firstLettersStr = 'Lettere più sbagliate: '
secondLettersStr = ''

for i in range(27):
    wrongLettersList.append(0)

def fillText():
    for i in range(len(words)):
        T.insert('insert', words[i] + ' ')

def callback(sv):
    global wIndex, words, right, wrong, percent, prevLen, timeStarted, sec, actIndex
    if sv.get()!='' and timeStarted==False:
        timeF()
    
    if sv.get()[-1:] == ' ': changeWord()

    if len(sv.get())>prevLen and len(sv.get())<=len(words[wIndex]):
        actIndex += 1
        i = len(sv.get())-1
        if i>=0:
            if sv.get()[i] == words[wIndex][i]:
                make_colored('1.' + str(actIndex-1), '1.' + str(actIndex), 'green')
                right+=1
            else:
                make_colored('1.' + str(actIndex-1), '1.' + str(actIndex), 'red')
                wrong += 1
                wrongLettersList[ord(words[wIndex][i]) - 97] += 1         
    
    elif len(sv.get())>len(words[wIndex]) and len(sv.get())>prevLen:
        wrong += 1
    elif len(sv.get())<prevLen and not sv.get()=='':
        actIndex -= 1
    prevLen = len(sv.get())
    make_colored('1.' + str(actIndex), '1.' + str(actIndex + len(words[wIndex])), 'black')
    try: percent = right/(right+wrong) * 100
    except: pass
    

def changeWord():
    global wIndex, goodW, badW, wrong, actIndex, spaces
    if sv.get()[:-1]==words[wIndex]:
        goodW += 1
    else:
        badW += 1
        wrong += len(words[wIndex])-len(sv.get()[:-1])
    if len(sv.get())<len(words[wIndex]):
        make_colored('1.' + str(actIndex), '1.' + str(actIndex + len(words[wIndex]) - len(sv.get()) + 1), 'red')
        actIndex += len(words[wIndex]) - len(sv.get()) + 2
    else:
        actIndex += 1
    spaces += 1
    wIndex += 1
    sv.set('')

def scrollWords():
    global actIndex, wIndex
    sv.set('')
    T['state'] = 'normal'
    T.delete('1.0', '2.0')
    T.insert('1.0', words[wIndex])
    T['state'] = 'disabled'
    T['bg'] = '#f5f5f5'
    wIndex += 1
    actIndex = (actIndex + 1) % 3

def changeWordLabels():
    global wIndex
    sv.set('')
    T['state'] = 'normal'
    T.delete('1.0', '2.0')
    T.insert('1.0', words[wIndex])
    T.tag_configure('center', justify='center')
    T.tag_add('center', '1.0', 'end')
    T['state'] = 'disabled'

def make_colored(start, end, color):
    global T
    for cl in ('green', 'red', 'black'): T.tag_remove(cl, start, end) 
    T.tag_add(color, start, end)
    T.tag_config(color, foreground=color)

def timeF():
    global sec, timeStarted, tEntry
    if sec>1:
        timeStarted = True
        sec -= 1
        timeLabel.config(text = '0:' + str(sec)) 
        timeLabel.after(1000, timeF)
    else:
        timeEnded()

def timeEnded():
    global right, wrong, percent, goodW, badW
    global wrongLettersList, second_max, firstLettersStr, secondLettersStr
    timeLabel.config(text = '0:0')
    tEntry['state'] = 'disabled'
    sv.set('')
    restartB['state'] = 'normal'
    
    # print('Accuratezza ', '{:.2f}'.format(percent), '%')
    # print('Lettere giuste: ', right, 'Lettere sbagliate: ', wrong)
    # print('Parole giuste: ', goodW, 'Parole sbagliate: ', badW)
    
    if not all(v == 0 for v in wrongLettersList):
        for i, n in enumerate(wrongLettersList):
            if n == max(wrongLettersList) and n!=0:
                firstLettersStr += chr(i+97) + ':' + str(n) + ', '
                second_max.append(0)
            else:
                second_max.append(n)
    if not all(v == 0 for v in second_max):
        # print('Queste sono le seconde lettere che hai sbagliato di più')
        for i, n in enumerate(second_max):
            if n == max(second_max) and n != 0:
                secondLettersStr += chr(i+97) + ':' + str(n) + ', '
    showStats()

def showStats():
    global percent, right, wrong, goodW, badW, sec, spaces, GENTIME
    T.grid_forget()
    Stats = tk.Label(root, font=('Helvetica', 20), bd = 0, justify = 'l')
    Stats.grid(row = 1, column = 0, columnspan = 5, sticky = 'nw')

    accuracyStr = 'Accuratezza: ' + str('{:.2f}'.format(percent)) + '%\n'
    rLettersStr = 'Lettere giuste: ' + str(right) + ', sbagliate: ' + str(wrong) + '\n'
    rWordsStr = 'Parole giuste: ' + str(goodW) + ', sbagliate: ' + str(badW) + '\n'
    speedStr = 'Parole per minuto: ' + str('{:.2f}'.format(60/GENTIME * (right+wrong+spaces)/5))

    if firstLettersStr != 'Lettere più sbagliate: ':
        Stats['text'] = 'Risultati:\n' + accuracyStr + rLettersStr + rWordsStr + \
            firstLettersStr + '\n' + secondLettersStr + '\n' + speedStr
    else:
        Stats['text'] = 'Risultati:\n' + accuracyStr + rLettersStr + rWordsStr + \
            'Tutto Giusto!' + '\n' + speedStr

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

# ----------------------------------------------------------------------------
# MAIN

#   LETTURA FILE
words = []
with open('Words.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if len(line[:-1])<=13:
            words.append(line[:-1].lower().strip())
shuffle(words)

root = tk.Tk()
root.geometry('700x300+300+200')
root.wm_attributes('-topmost', 1)

root.columnconfigure((0,1,2,3,4), weight= 1)
root.rowconfigure((1), weight= 1)

#   TEXTVARIABLES IN TEXT
sv = tk.StringVar()
sv.trace('w', lambda name, index, mode, sv=sv: callback(sv))

#   WIDGETS
restartB = tk.Button(root, text='Restart', font=("Helvetica", 11), command= lambda: restart_program(), state = 'disabled')
restartB.grid(row = 0, column = 0, sticky = 'nw')

timeLabel = tk.Label(root, font=('Helvetica', 11), bd = 0, text = '1:00')
timeLabel.grid(row = 0, column = 4, sticky = 'ne')

T = tk.Text(root, font=('Helvetica', 50), bd = 0, bg = '#f5f5f5', wrap = 'word')
T.grid(row = 1, column = 0, columnspan = 5, sticky = 'ew')

fillText()

# changeWord()

# scrollWords()
# scrollWords()
# scrollWords()
# actIndex=0

tEntry = tk.Entry(root, text='', justify = 'center', font=('Helvetica', 32), textvariable=sv)
tEntry.grid(row = 2, column = 0, columnspan = 5, sticky = 'ew')

root.mainloop()