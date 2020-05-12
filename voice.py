import speech_recognition as sr
recog=sr.Recognizer()
with sr.Microphone() as source:
    print("speak")
    audio=recog.listen(source)
    try:
        text=recog.recognize_google(audio,language='ne')
        print("You speak:"+text)
        f =open("E:\WorkSpace\Python Projects\text-to-gcode\text.txt",encoding='utf8',mode='w')
        f.write(text)
        f.close()
    except:
        print("Error occured..")