from tkinter import *
import speech_recognition as sr
from tkinter import messagebox
import os

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
            mresult = recog.recognize_google(audio, language='ne-NP')     
            #print(type(mresult))
            #mresult = mresult.encode("ascii","ignore") encoding to ascii
            #print(mresult)
            #for each_byte in mresult:
            #    print(each_byte)
            #    print(hex(ord(each_byte)))  prints the hex value of unicode character
            print('you said '+mresult)           
            owd = os.getcwd() # would be the MAIN folder
            nxtdir = owd + "//Cpp" # add the Cpp folder name
            os.chdir(nxtdir) #  go to the Cpp folder
            print(nxtdir)
            f = open("UniCodeOutput.txt",encoding='utf8',mode='w')
            f.write(mresult)
            f.close()
            os.system('python unicodeToPreeti.py UniCodeOutput.txt input.txt')
            os.chdir(owd)
            
            translated_label.config(text=mresult)
        except:
            print('Sorry !')
            translated_label.config(text='Error Occured !!')




def print_now():
    print('Text is now being printed...')
    translated_label.config(text='Text is now being printed...')
    owd = os.getcwd() # would be the MAIN folder
    nxtdir = owd + "//Cpp" # add the CPP folder name
    os.chdir(nxtdir) # change the current working directory
    os.system('TextToGcode.exe -font "PREETI.TTF" -filename gcodeOutput')
    os.chdir(owd)
    translated_label.config(text='Success !!')
    
    
def reset():
    os.system('cmd /c ""')

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

reset_btn = Button(app, text='Reset', width=12, command=reset)
reset_btn.grid(row=7, column=2)

# Look
app.title("Speech Translation")
app.geometry('500x400')

app.mainloop()