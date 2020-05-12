from tkinter import *
import speech_recognition as sr
from tkinter import messagebox

# recognizer objecr
recog = sr.Recognizer()



def speak_now():
    if lang_from.get() == '':
        messagebox.showerror('Required Fields', 'Please include Source Language')
        return
    with sr.Microphone() as source:
        print('Speak Now')
        translated_label.config(text="Speak Now....")
        audio = recog.listen(source, 5)
        print('Connecting to server...')
        translated_label.config(text='Connecting to Server....')
        try:
            mresult = recog.recognize_google(audio, language=lang_from.get())
            print('you said '+mresult)
            translated_label.config(text=mresult)
        except:
            print('Sorry !')
            translated_label.config(text='Error Occured !!')




def print_now():
    print('Text Printed')
    translated_label.config(text='Printing Text')


# window
app = Tk()



# language from
lang_from = StringVar()
from_label = Label(app, text='From', font=('bold', 14), pady=30, padx=70)
from_label.grid(row=0, column=0)
from_entry = Entry(app, textvariable=lang_from,)
from_entry.grid(row=1, column=0)

# language to
lang_to = StringVar()
to_label = Label(app, text='Translate to', font=('bold', 14), pady=30, padx=20)
to_label.grid(row=0, column=3)
to_entry = Entry(app, textvariable=lang_to)
to_entry.grid(row=1, column=3)

# speak now button
speak_btn = Button(app, text='Speak Now', width=12, command=speak_now)
speak_btn.grid(row=2, column=2, pady=30)

# Print now button
print_btn = Button(app, text='Print Now', width=12, command=print_now)
print_btn.grid(row=3, column=3)

# result notation 
result_label = Label(app, text='Result', font=('bold', 15), pady=20)
result_label.grid(row=3, column=0)

result = 'some text'
translated_label = Label(app, text=result)
translated_label.grid(row=4,column=2,  padx=10)

# Look
app.title("Speech Translation")
app.geometry('500x400')

app.mainloop()