import tkinter as tk
from tkinter.font import Font

wrong = 0
right = 0

def callback(sv):
    if sv.get()[-1:] == ' ': changeWord()
    global visWords, right, wrong
    reset()
    imax=0
    for i in range(1,len(sv.get())+1):
        if sv.get()[:i] == visWords[0].get()[:i]:
            make_green(0, i, 1)
            if i>imax:
                imax=i
    if len(sv.get())>imax:
        make_red(imax, len(sv.get()), 1)
        wrong += 1
        
    print('right, wrong: ', right, wrong)

def changeWord():
    sv.set('')
    T1['state'] = 'normal'
    T2['state'] = 'normal'
    T3['state'] = 'normal'
    print(visWords[0].get(), visWords[1].get(), visWords[2].get())
    print(words[:5])
    visWords[0].set(visWords[1].get())
    visWords[1].set(visWords[2].get())
    visWords[2].set(words[3])
    T1.delete('1.0', '2.0')
    T2.delete('1.0', '2.0')
    T3.delete('1.0', '2.0')
    T1.insert('1.0', visWords[0].get())
    T2.insert('1.0', visWords[1].get())
    T3.insert('1.0', visWords[2].get())
    
    T1.tag_configure('center', justify='center')
    T1.tag_add('center', '1.0', 'end')
    T2.tag_configure('center', justify='center')
    T2.tag_add('center', '1.0', 'end')
    T3.tag_configure('center', justify='center')
    T3.tag_add('center', '1.0', 'end')

    T1['state'] = 'disabled'
    T2['state'] = 'disabled'
    T3['state'] = 'disabled'

def reset():
    global T1, T2, T3
    T1.tag_delete('green', 'red')
    T2.tag_delete('green', 'red')
    T3.tag_delete('green', 'red')

def make_green(a, b, n):
    global T1, T2, T3
    start = '1.' + str(a)
    end = '1.' + str(b)
    # green_font = Font(family='Helvetica', size=30, weight='bold')
    if n==1: 
        T1.tag_add('green', start, end)
        T1.tag_config('green', foreground='green')
    elif n==2:        
        T2.tag_add('green', start, end)
        T2.tag_config('green', foreground='green')
    elif n==3:
        T3.tag_add('green', start, end)
        T3.tag_config('green', foreground='green')

def make_red(a, b, n):
    global T1, T2, T3
    start = '1.' + str(a)
    end = '1.' + str(b)
    # green_font = Font(family='Helvetica', size=30, weight='bold')
    if n==1: 
        T1.tag_add('red', start, end)
        T1.tag_config('red', foreground='red')
    elif n==2:        
        T2.tag_add('red', start, end)
        T2.tag_config('red', foreground='red')
    elif n==3:
        T3.tag_add('red', start, end)
        T3.tag_config('red', foreground='red')


#   LETTURA FILE
words = []
with open('Words.txt', 'r', encoding='utf-8') as f:
    for line in f: words.append(line[:-1].lower())
wordIndex = 0

#print(words)

root = tk.Tk()
root.geometry('600x300+300+200')
root.wm_attributes('-topmost', 1)

root.columnconfigure((0,1,2,3,4), weight= 1)
root.rowconfigure((0), weight= 1)



#   TEXTVARIABLES
sv = tk.StringVar()
sv.trace('w', lambda name, index, mode, sv=sv: callback(sv))

# index = 0

visWords = [tk.StringVar(), tk.StringVar(), tk.StringVar()]
for i in range(3): visWords[i].set(words[i])


#   WIDGETS

T1 = tk.Text(root, font=('Helvetica', 30), bd = 0, pady = 80)
T1.grid(row = 0, column = 0, sticky = 'ew')
T1.tag_configure('center', justify='center')
T1.insert('1.0', visWords[0].get())
T1.tag_add('center', '1.0', 'end')
T1['state'] = 'disabled'

T2 = tk.Text(root, font=('Helvetica', 30), bd = 0, pady = 80)
T2.grid(row = 0, column = 2, sticky = 'ew')
T2.tag_configure('center', justify='center')
T2.insert('1.0', visWords[1].get())
T2.tag_add('center', '1.0', 'end')
T2['state'] = 'disabled'

T3 = tk.Text(root, font=('Helvetica', 30), bd = 0, pady = 80)
T3.grid(row = 0, column = 4, sticky = 'ew')
T3.tag_configure('center', justify='center')
T3.insert('1.0', visWords[2].get())
T3.tag_add('center', '1.0', 'end')
T3['state'] = 'disabled'
# wordLbl.grid(row = 0, column = 0)

tEntry = tk.Entry(root, text='', justify = 'center', font=('Helvetica', 32), textvariable=sv)
# textE.pack()
# textE.place(relx=.5, rely=.5, anchor='c')
tEntry.grid(row = 1, column = 0, columnspan = 5, sticky = 'ew')

root.mainloop()