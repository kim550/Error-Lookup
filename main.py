from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sys
import ctypes

root = Tk()
root.attributes('-alpha', 0)
root.update()

window = Toplevel(root)
window.title('Error Lookup')
window.focus_set()
window.transient(root)

wwidth = window.winfo_screenwidth()
wheight = window.winfo_screenheight()
width = 300
height = 150
window.geometry('%sx%s+%s+%s' % (width, height, (wwidth-width) // 2 - 10, (wheight-height) // 2))
window.resizable(False, False)

def test(content):
    if content.isdigit() or content == '':
        return True
    window.bell()
    return False

def ondeletewindow():
    window.destroy()
    root.destroy()
    sys.exit()

def search():
    text = entry.get()
    if text:
        try:
            errtext = ctypes.FormatError(int(text))
        except OverflowError:
            messagebox.showerror('Error', 'Too large number.')
            window.focus_set()
            return
        except ValueError:
            messagebox.showerror('Error', 'Invalid input.')
            window.focus_set()
            return
        if errtext == '<no description>':
            messagebox.showerror('Error', 'Invalid error code.')
            window.focus_set()
            return
        err['state'] = 'normal'
        err.delete('0.0', 'end')
        err.insert('end', errtext)
        err['state'] = 'disabled'

def btnenter(event):
    global entered
    entered = True

def btnleave(event):
    global entered
    entered = False

ttk.Label(window, text='Error code: ').place(x=5, y=5)
test_cmd = window.register(test)
entry = ttk.Entry(window, validate='key', validatecommand=(test_cmd, '%P'))
entry.focus_set()
entry.place(x=80, y=5, width=210)
err = Text(window, state='disabled')
err.place(x=20, y=40, width=260, height=60)
ttk.Separator(window).place(x=0, y=110, width=300)

entered = False

lookupbtn = ttk.Button(window, text='Search', command=search)
lookupbtn.bind('<Button-1>', btnenter)
lookupbtn.bind('<ButtonRelease-1>', btnleave)
lookupbtn.place(x=110, y=115, width=80)

window.protocol('WM_DELETE_WINDOW', ondeletewindow)

while True:
    try:
        if entered:
            err.focus_set()
        window.update()
    except TclError:
        break
