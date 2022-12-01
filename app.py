from tkinter import *
from chat import get_response, bot_name
import pyttsx3 as pp
import speech_recognition as sr
import threading
import time

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOUR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

class ChatApplication:
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        self.engine = pp.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice',self.voices[1].id)

    def speak(self,word):
        self.engine.say(word)
        self.engine.runAndWait()
    
    def takeQuery(self):
        self.speech=sr.Recognizer()
        self.speech.pause_threshold =1
        print("your bot is listening try to speak")
        with sr.Microphone() as m:
            try:
                audio = self.speech.listen(m)
                query = self.speech.recognize_google(audio, language='eng-in')
                self.msg_entry.delete(0, END)
                self.msg_entry.insert(0,query)
                self._insert_user_message(query, "You")
                self._insert_bot_message(query)
            except Exception as e:
                print(e)
                print("Not Recognised")


    def run(self):
        self.stop_threads = False
        t = threading.Thread(target=self.repeatL, args = (lambda : self.stop_threads,))
        t.start()
        self.window.mainloop()
        self.stop_threads = True
        t.join()
        

    def repeatL(self,stop):
            while True:
                self.takeQuery()
                if stop():
                    break

    def _setup_main_window(self):
        self.window.title("Chat")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=600, height=750, bg=BG_COLOR)

        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOUR,
                            text="Welcome", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        #tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        #text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOUR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        #bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        #message entry box
        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOUR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        #send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command= lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
        
    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_user_message(msg, "You")
        self._insert_bot_message(msg)

    def _insert_user_message(self, msg, sender):
        if not msg:
            return
        
        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)

    def _insert_bot_message(self,msg):
        self.message = get_response(msg)
        msg2 = f"{bot_name}: {self.message}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)

        # self.speak(self.message)
        time.sleep(0)
        t1 = threading.Thread(target=self.speak, args=(self.message,))
        t1.start()



if __name__ == "__main__":
    app = ChatApplication()
    app.run()