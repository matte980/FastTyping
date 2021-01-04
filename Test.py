import tkinter as tk
from tkinter.font import Font

# FARE SCORRIMENTO DIVERSO
# DICE LE LETTERE CHE SI SBAGLIANO PIù SPESSO

wrong = 0
right = 0
percent = 0
wIndex = -1
prevLen = 0
sec = 3
goodW = 0
badW = 0
timeStarted = False

def callback(sv):
    global wIndex, words, right, wrong, percent, prevLen, timeStarted, sec
    if sv.get()!='' and wIndex==0 and timeStarted==False:
        timeF()
    if sv.get()[-1:] == ' ': changeWord()
    make_colored('1.' + str(len(sv.get())), '1.' + str(len(words[wIndex])), 1, 'black')
    if len(sv.get())>prevLen and len(sv.get())<=len(words[wIndex]):
        i = len(sv.get())-1
        if i>=0:
            if sv.get()[i] == words[wIndex][i]:
                make_colored('1.' + str(i), '1.' + str(i+1), 1, 'green')
                right+=1
            else:
                make_colored('1.' + str(i), '1.' + str(i+1), 1, 'red')
                wrong += 1
    elif len(sv.get())>len(words[wIndex]):
        wrong += 1
    prevLen = len(sv.get())
    try:
        percent = right/(right+wrong) * 100
        # print('right ', '{:.2f}'.format(percent), '%')
        # print('r/w', right, wrong)
    except: pass

def changeWord():
    global wIndex, goodW, badW, wrong
    if sv.get()[:-1]==words[wIndex]:
        goodW += 1
    elif wIndex!=-1 and len(words[wIndex])>len(sv.get()[:-1]):
        badW += 1
        wrong += len(words[wIndex])-len(sv.get()[:-1])
    # print('good/ba: ', goodW, badW)
    wIndex += 1
    changeWordLabels()

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
    if n==1:
        for cl in ('green', 'red', 'black'): T1.tag_remove(cl, start, end) 
        T1.tag_add(color, start, end)
        T1.tag_config(color, foreground=color)
    elif n==2:
        for cl in ('green', 'red', 'black'): T2.tag_remove(cl, start, end)
        T2.tag_add(color, start, end)
        T2.tag_config(color, foreground=color)
    elif n==3:
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
    timeLabel.config(text = '0:0')
    tEntry['state']='disabled'
    
    print('right ', '{:.2f}'.format(percent), '%')
    print('r/w', right, wrong)
    print('good/ba: ', goodW, badW)


# ----------------------------------------------------------------------------
# MAIN

#   LETTURA FILE
words = []
with open('Words.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if len(line[:-1])<=13:
            words.append(line[:-1].lower())

root = tk.Tk()
root.geometry('700x300+300+200')
root.wm_attributes('-topmost', 1)

root.columnconfigure((0,1,2,3,4), weight= 1)
root.rowconfigure((1), weight= 1)

#   TEXTVARIABLES IN TEXT
sv = tk.StringVar()
sv.trace('w', lambda name, index, mode, sv=sv: callback(sv))

#   WIDGETS
timeLabel = tk.Label(root, font=('Helvetica', 11), bd = 0, text = '1:00')
timeLabel.grid(row = 0, column = 4, sticky = 'ne')

T1 = tk.Text(root, font=('Helvetica', 25), bd = 0, pady = 80)
T1.grid(row = 1, column = 0, sticky = 'ew')
# T1.tag_configure('center', justify='center')
# T1.insert('1.0', words[wIndex])
# T1.tag_add('center', '1.0', 'end')
# T1['state'] = 'disabled'

T2 = tk.Text(root, font=('Helvetica', 25), bd = 0, pady = 80)
T2.grid(row = 1, column = 2, sticky = 'ew')
# T2.tag_configure('center', justify='center')
# T2.insert('1.0', words[wIndex+1])
# T2.tag_add('center', '1.0', 'end')
# T2['state'] = 'disabled'

T3 = tk.Text(root, font=('Helvetica', 25), bd = 0, pady = 80)
T3.grid(row = 1, column = 4, sticky = 'ew')
# T3.tag_configure('center', justify='center')
# T3.insert('1.0', words[wIndex+2])
# T3.tag_add('center', '1.0', 'end')
# T3['state'] = 'disabled'

changeWord()

tEntry = tk.Entry(root, text='', justify = 'center', font=('Helvetica', 32), textvariable=sv)
tEntry.grid(row = 2, column = 0, columnspan = 5, sticky = 'ew')

root.mainloop()