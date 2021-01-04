#!/usr/bin/env python

import tkinter as tk
from tkinter.font import Font
from random import shuffle
import sys, os

wrong = 0
right = 0
percent = 0
prevLen = 0
secForSpeed = 30
sec = 30
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

def callback(sv):
    global wIndex, words, right, wrong, percent, prevLen, timeStarted, sec, actIndex
    if sv.get()!='' and actIndex==0 and timeStarted==False:
        timeF()
    if sv.get()[-1:] == ' ': changeWord()
    make_colored('1.' + str(len(sv.get())), '1.' + str(len(words[wIndex-3])), actIndex, 'black')
    if len(sv.get())>prevLen and len(sv.get())<=len(words[wIndex-3]):
        i = len(sv.get())-1
        if i>=0:
            if sv.get()[i] == words[wIndex-3][i]:
                make_colored('1.' + str(i), '1.' + str(i+1), actIndex, 'green')
                right+=1
            else:
                make_colored('1.' + str(i), '1.' + str(i+1), actIndex, 'red')
                wrong += 1
                wrongLettersList[ord(words[wIndex-3][i]) - 97] += 1
    elif len(sv.get())>len(words[wIndex-3]):
        wrong += 1
    prevLen = len(sv.get())
    try:
        percent = right/(right+wrong) * 100
    except: pass

def changeWord():
    global wIndex, goodW, badW, wrong, actIndex
    if sv.get()[:-1]==words[wIndex-3]:
        goodW += 1
    elif len(words[wIndex-3])>len(sv.get()[:-1]):
    # wIndex!=-1 and 
        badW += 1
        wrong += len(words[wIndex-3])-len(sv.get()[:-1])
    scrollWords()
    # changeWordLabels()

def scrollWords():
    global actIndex, wIndex
    sv.set('')
    if actIndex == 0:
        T1['state'] = 'normal'
        T1.delete('1.0', '2.0')
        T1.insert('1.0', words[wIndex])
        T1.tag_configure('center', justify='center')
        T1.tag_add('center', '1.0', 'end')
        T1['state'] = 'disabled'
        T1['bg'] = '#f5f5f5'
        T2['bg'] = '#ffffff'
    elif actIndex == 1: 
        T2['state'] = 'normal'
        T2.delete('1.0', '2.0')
        T2.insert('1.0', words[wIndex])
        T2.tag_configure('center', justify='center')
        T2.tag_add('center', '1.0', 'end')
        T2['state'] = 'disabled'
        T2['bg'] = '#f5f5f5'
        T3['bg'] = '#ffffff'
    elif actIndex == 2: 
        T3['state'] = 'normal'
        T3.delete('1.0', '2.0')
        T3.insert('1.0', words[wIndex])
        T3.tag_configure('center', justify='center')
        T3.tag_add('center', '1.0', 'end')
        T3['state'] = 'disabled'
        T3['bg'] = '#f5f5f5'
        T1['bg'] = '#ffffff'
    wIndex += 1
    actIndex = (actIndex + 1) % 3

def changeWordLabels():
    global wIndex
    sv.set('')
    T1['state'] = 'normal'
    T2['state'] = 'normal'
    T3['state'] = 'normal'
    T1.delete('1.0', '2.0')
    T2.delete('1.0', '2.0')
    T3.delete('1.0', '2.0')
    T1.insert('1.0', words[wIndex])
    T2.insert('1.0', words[wIndex+1])
    T3.insert('1.0', words[wIndex+2])
    T1.tag_configure('center', justify='center')
    T1.tag_add('center', '1.0', 'end')
    T2.tag_configure('center', justify='center')
    T2.tag_add('center', '1.0', 'end')
    T3.tag_configure('center', justify='center')
    T3.tag_add('center', '1.0', 'end')
    T1['state'] = 'disabled'
    T2['state'] = 'disabled'
    T3['state'] = 'disabled'

def make_colored(start, end, n, color):
    global T1, T2, T3
    if n==0:
        for cl in ('green', 'red', 'black'): T1.tag_remove(cl, start, end) 
        T1.tag_add(color, start, end)
        T1.tag_config(color, foreground=color)
    elif n==1:
        for cl in ('green', 'red', 'black'): T2.tag_remove(cl, start, end)
        T2.tag_add(color, start, end)
        T2.tag_config(color, foreground=color)
    elif n==2:
        for cl in ('green', 'red', 'black'): T3.tag_remove(cl, start, end)
        T3.tag_add(color, start, end)
        T3.tag_config(color, foreground=color)

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
        print('Queste sono le seconde lettere che hai sbagliato di più')
        for i, n in enumerate(second_max):
            if n == max(second_max) and n != 0:
                secondLettersStr += chr(i+97) + ':' + str(n) + ', '
    showStats()

def showStats():
    global percent, right, wrong, goodW, badW, sec
    T1.grid_forget()
    T2.grid_forget()
    T3.grid_forget()
    Stats = tk.Label(root, font=('Helvetica', 20), bd = 0, justify = 'l')
    Stats.grid(row = 1, column = 0, columnspan = 5, sticky = 'nw')

    accuracyStr = 'Accuratezza: ' + str('{:.2f}'.format(percent)) + '%\n'
    rLettersStr = 'Lettere giuste: ' + str(right) + ', sbagliate: ' + str(wrong) + '\n'
    rWordsStr = 'Parole giuste: ' + str(goodW) + ', sbagliate: ' + str(badW) + '\n'
    speedStr = 'Parole per minuto: ' + str(60*goodW/secForSpeed)

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

restartB = tk.Button(root, text='Restart', font=("Helvetica", 11), command= lambda: restart_program(), state = 'disabled')
restartB.grid(row = 0, column = 0, sticky = 'nw')

timeLabel = tk.Label(root, font=('Helvetica', 11), bd = 0, text = '1:00')
timeLabel.grid(row = 0, column = 4, sticky = 'ne')

T1 = tk.Text(root, font=('Helvetica', 25), bd = 0, pady = 80, bg = '#f5f5f5')
T1.grid(row = 1, column = 0, sticky = 'ew')

T2 = tk.Text(root, font=('Helvetica', 25), bd = 0, pady = 80, bg = '#f5f5f5')
T2.grid(row = 1, column = 2, sticky = 'ew')

T3 = tk.Text(root, font=('Helvetica', 25), bd = 0, pady = 80, bg = '#f5f5f5')
T3.grid(row = 1, column = 4, sticky = 'ew')

# changeWord()

scrollWords()
scrollWords()
scrollWords()
actIndex=0

tEntry = tk.Entry(root, text='', justify = 'center', font=('Helvetica', 32), textvariable=sv)
tEntry.grid(row = 2, column = 0, columnspan = 5, sticky = 'ew')

root.mainloop()