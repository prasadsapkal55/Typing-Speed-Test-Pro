import time
import random
import text as tt
from tkinter import *
from tkinter import ttk
import settings as st  
from threading import Thread
from PIL import Image, ImageTk
from pynput.keyboard import Listener
import json
import os

class TypingTest:

    def __init__(self, root):
        self.window = root
        self.window.geometry(f"{st.width}x{st.height}")
        self.window.title('Typing Speed Test Pro')
        self.window.resizable(width=False, height=False)
        self.window.configure(bg='#2c3e50')  # Modern dark blue
        
        # Declaring some variables
        self.key = None
        self.typingStarted = False
        self.currentCharIndex = 0
        self.correctChars = 0
        self.incorrectChars = 0
        self.startTime = 0
        
        self.loadStats()

        self.textList = [tt.text1, tt.text2, tt.text3, tt.text4, tt.text5]

        self.frame = Frame(self.window, bg='#2c3e50', width=st.width, height=st.height)
        self.frame.place(x=0, y=0)

        self.startWindow()

    def startWindow(self):
        titleLabel = Label(self.frame, text="Typing Speed Test Pro", 
                          bg='#2c3e50', fg='#ecf0f1', 
                          font=('Arial', 32, "bold"))
        titleLabel.place(x=150, y=60)
        
        subtitleLabel = Label(self.frame, text="Test and improve your typing speed", 
                             bg='#2c3e50', fg='#bdc3c7', 
                             font=('Arial', 12))
        subtitleLabel.place(x=280, y=110)
        
        if hasattr(self, 'best_wpm') and self.best_wpm > 0:
            bestLabel = Label(self.frame, text=f"Your Best: {self.best_wpm} WPM", 
                             bg='#2c3e50', fg='#f39c12', 
                             font=('Arial', 14, 'bold'))
            bestLabel.place(x=320, y=140)

        startButton = Button(self.frame, text="Start Test", 
                           border=0, cursor='hand2', 
                           fg='white', bg='#3498db', 
                           font=('Arial', 16, 'bold'),
                           padx=30, pady=10,
                           relief='flat',
                           command=self.startTest)
        startButton.place(x=320, y=200)
        
        def on_enter(e):
            startButton.config(bg='#2980b9')
        def on_leave(e):
            startButton.config(bg='#3498db')
            
        startButton.bind("<Enter>", on_enter)
        startButton.bind("<Leave>", on_leave)
        
        # Instructions
        instructionLabel = Label(self.frame, 
                               text="Instructions: Click 'Start Test' and begin typing when you see the text.\nYour typing will automatically start the timer.",
                               bg='#2c3e50', fg='#95a5a6', 
                               font=('Arial', 10),
                               justify=CENTER)
        instructionLabel.place(x=200, y=280)

    def startTest(self):
        self.clearScreen()
        
        self.typingStarted = False
        self.currentCharIndex = 0
        self.correctChars = 0
        self.incorrectChars = 0
        self.startTime = 0

        self.totalTime = st.totalTime

        self.paragraph = random.choice(self.textList)
        
        headerFrame = Frame(self.frame, bg='#34495e', height=50)
        headerFrame.pack(fill=X, padx=10, pady=(10, 0))
        
        self.timeLabel = Label(headerFrame, text="1:00", 
                              bg='#34495e', fg='#e74c3c', 
                              font=('Arial', 18, 'bold'))
        self.timeLabel.pack(side=LEFT, padx=20, pady=10)
        
        self.progressVar = DoubleVar()
        self.progressBar = ttk.Progressbar(headerFrame, variable=self.progressVar, 
                                          maximum=st.totalTime, length=200)
        self.progressBar.pack(side=LEFT, padx=20, pady=10)
        
        self.statsLabel = Label(headerFrame, text="WPM: 0 | Accuracy: 100%", 
                               bg='#34495e', fg='#2ecc71', 
                               font=('Arial', 12, 'bold'))
        self.statsLabel.pack(side=RIGHT, padx=20, pady=10)

        textFrame = Frame(self.frame, bg='#ecf0f1', relief='solid', bd=1)
        textFrame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        self.textDisplay = Text(textFrame, width=70, height=8, 
                               bg='#ecf0f1', fg='#2c3e50',
                               font=('Courier New', 14),
                               wrap=WORD, relief='flat',
                               state='disabled',
                               cursor='arrow')
        self.textDisplay.pack(padx=10, pady=10)
        
        self.textDisplay.tag_configure('correct', background='#d5f4e6', foreground='#27ae60')
        self.textDisplay.tag_configure('incorrect', background='#fadbd8', foreground='#e74c3c')
        self.textDisplay.tag_configure('current', background='#fef9e7', foreground='#f39c12')
        self.textDisplay.tag_configure('untyped', background='#ecf0f1', foreground='#7f8c8d')
        
        self.textDisplay.config(state='normal')
        self.textDisplay.insert(END, self.paragraph)
        self.textDisplay.tag_add('untyped', '1.0', END)
        self.textDisplay.config(state='disabled')

        inputFrame = Frame(self.frame, bg='#2c3e50')
        inputFrame.pack(fill=X, padx=10, pady=(0, 10))
        
        inputLabel = Label(inputFrame, text="Type here:", 
                          bg='#2c3e50', fg='#ecf0f1', 
                          font=('Arial', 12))
        inputLabel.pack(anchor=W, padx=10, pady=(10, 5))
        
        self.inputEntry = Entry(inputFrame, fg='#2c3e50', bg='#ecf0f1', 
                               width=70, font=('Courier New', 14),
                               relief='flat', bd=5)
        self.inputEntry.pack(padx=10, pady=(0, 10))
        self.inputEntry.bind('<KeyRelease>', self.on_type)
        self.inputEntry.focus()

        self.listener = Listener(on_press=self.on_key_press)
        self.listener.start()

    def on_key_press(self, key):
        if not self.typingStarted:
            self.typingStarted = True
            self.startTime = time.time()
            self.multiThreading()
    
    def on_type(self, event):
        if not self.typingStarted:
            return
            
        typed_text = self.inputEntry.get()
        self.updateTextHighlight(typed_text)
        self.updateStats(typed_text)
    
    def updateTextHighlight(self, typed_text):
        self.textDisplay.config(state='normal')
        
        self.textDisplay.tag_remove('correct', '1.0', END)
        self.textDisplay.tag_remove('incorrect', '1.0', END)
        self.textDisplay.tag_remove('current', '1.0', END)
        self.textDisplay.tag_remove('untyped', '1.0', END)
        
        for i, char in enumerate(typed_text):
            pos = f"1.{i}"
            next_pos = f"1.{i+1}"
            
            if i < len(self.paragraph):
                if char == self.paragraph[i]:
                    self.textDisplay.tag_add('correct', pos, next_pos)
                else:
                    self.textDisplay.tag_add('incorrect', pos, next_pos)
        
        if len(typed_text) < len(self.paragraph):
            current_pos = f"1.{len(typed_text)}"
            next_current_pos = f"1.{len(typed_text)+1}"
            self.textDisplay.tag_add('current', current_pos, next_current_pos)
        
        if len(typed_text) < len(self.paragraph):
            untyped_start = f"1.{len(typed_text)+1}"
            self.textDisplay.tag_add('untyped', untyped_start, END)
        
        self.textDisplay.config(state='disabled')
    
    def updateStats(self, typed_text):
        if not typed_text or not self.typingStarted:
            return
            
        correct = sum(1 for i, char in enumerate(typed_text) 
                     if i < len(self.paragraph) and char == self.paragraph[i])
        
        elapsed_time = time.time() - self.startTime
        if elapsed_time > 0:
            wpm = (len(typed_text.split()) / elapsed_time) * 60
        else:
            wpm = 0
            
        if len(typed_text) > 0:
            accuracy = (correct / len(typed_text)) * 100
        else:
            accuracy = 100
            
        self.statsLabel.config(text=f"WPM: {int(wpm)} | Accuracy: {int(accuracy)}%")

    def multiThreading(self):
        x = Thread(target=self.countDown)
        x.start()

    def countDown(self):
        initial_time = self.totalTime
        while self.totalTime > 0:
            minutes = self.totalTime // 60
            seconds = self.totalTime % 60
            self.timeLabel.config(text=f"{minutes}:{seconds:02d}")
            
            progress = initial_time - self.totalTime
            self.progressVar.set(progress)
            
            time.sleep(1)
            self.totalTime -= 1

        self.timeLabel.config(text="0:00")
        self.progressVar.set(initial_time)
        
        if hasattr(self, 'listener') and self.listener:
            self.listener.stop()
        self.calculateResult()

    def backgroundImage(self, img):
        image = Image.open(img)
        resizedImg = image.resize((st.width, st.height))
        self.img = ImageTk.PhotoImage(resizedImg)

        label = Label(self.frame, image=self.img)
        label.pack()

    def calculateResult(self):
        typed_text = self.inputEntry.get()
        words_typed = typed_text.split()
        
        self.clearScreen()
        
        resultsFrame = Frame(self.frame, bg='#2c3e50')
        resultsFrame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        titleLabel = Label(resultsFrame, text="Test Results", 
                          bg='#2c3e50', fg='#ecf0f1', 
                          font=('Arial', 28, 'bold'))
        titleLabel.pack(pady=(0, 30))

        if len(typed_text) > 0:
            correct_chars = sum(1 for i, char in enumerate(typed_text) 
                               if i < len(self.paragraph) and char == self.paragraph[i])
            char_accuracy = (correct_chars / len(typed_text)) * 100
            
            paragraph_words = self.paragraph.split()
            correct_words = 0
            for i, word in enumerate(words_typed):
                if i < len(paragraph_words) and word == paragraph_words[i]:
                    correct_words += 1
            
            word_accuracy = (correct_words / len(words_typed)) * 100 if words_typed else 0
            
            wpm = len(words_typed)
            
            net_wpm = (correct_words / st.totalTime) * 60 if st.totalTime > 0 else 0
            
        else:
            char_accuracy = 0
            word_accuracy = 0
            wpm = 0
            net_wpm = 0
            correct_words = 0

        statsFrame = Frame(resultsFrame, bg='#34495e', relief='solid', bd=1)
        statsFrame.pack(pady=20, padx=40, fill=X)
        
        row1 = Frame(statsFrame, bg='#34495e')
        row1.pack(fill=X, pady=20)
        
        self.createStatBox(row1, "Gross WPM", str(wpm), '#3498db', LEFT)
        self.createStatBox(row1, "Net WPM", f"{net_wpm:.1f}", '#e74c3c', RIGHT)
        
        row2 = Frame(statsFrame, bg='#34495e')
        row2.pack(fill=X, pady=(0, 20))
        
        self.createStatBox(row2, "Character Accuracy", f"{char_accuracy:.1f}%", '#2ecc71', LEFT)
        self.createStatBox(row2, "Word Accuracy", f"{word_accuracy:.1f}%", '#f39c12', RIGHT)
        
        additionalFrame = Frame(resultsFrame, bg='#2c3e50')
        additionalFrame.pack(pady=20)
        
        Label(additionalFrame, text=f"Words Typed: {len(words_typed)} | Correct Words: {correct_words}", 
              bg='#2c3e50', fg='#bdc3c7', font=('Arial', 12)).pack()
        
        Label(additionalFrame, text=f"Characters Typed: {len(typed_text)} | Correct Characters: {correct_chars if len(typed_text) > 0 else 0}", 
              bg='#2c3e50', fg='#bdc3c7', font=('Arial', 12)).pack()
        
        self.updatePersonalBest(net_wpm)
        
        if hasattr(self, 'best_wpm') and self.best_wpm > 0:
            if net_wpm > self.best_wpm:
                Label(additionalFrame, text="🎉 New Personal Best! 🎉", 
                      bg='#2c3e50', fg='#f1c40f', font=('Arial', 14, 'bold')).pack(pady=9)
            else:
                Label(additionalFrame, text=f"Personal Best: {self.best_wpm:.1f} WPM", 
                      bg='#2c3e50', fg='#95a5a6', font=('Arial', 12)).pack(pady=9)

        buttonFrame = Frame(resultsFrame, bg='#2c3e50')
        buttonFrame.pack(pady=30)
        
        testAgainButton = Button(buttonFrame, text="Test Again", 
                               border=0, cursor='hand2', 
                               fg='white', bg='#3498db', 
                               font=('Arial', 14, 'bold'),
                               padx=20, pady=8,
                               relief='flat',
                               command=self.startTest)
        testAgainButton.pack(side=LEFT, padx=10)
        
        menuButton = Button(buttonFrame, text="Main Menu", 
                          border=0, cursor='hand2', 
                          fg='white', bg='#95a5a6', 
                          font=('Arial', 14, 'bold'),
                          padx=20, pady=8,
                          relief='flat',
                          command=self.startWindow)
        menuButton.pack(side=LEFT, padx=10)
        
        def on_enter_test(e):
            testAgainButton.config(bg='#2980b9')
        def on_leave_test(e):
            testAgainButton.config(bg='#3498db')
        def on_enter_menu(e):
            menuButton.config(bg='#7f8c8d')
        def on_leave_menu(e):
            menuButton.config(bg='#95a5a6')
            
        testAgainButton.bind("<Enter>", on_enter_test)
        testAgainButton.bind("<Leave>", on_leave_test)
        menuButton.bind("<Enter>", on_enter_menu)
        menuButton.bind("<Leave>", on_leave_menu)
    
    def createStatBox(self, parent, title, value, color, side):
        box = Frame(parent, bg=color, relief='flat', bd=0)
        box.pack(side=side, padx=20, pady=10, fill=X, expand=True)
        
        Label(box, text=title, bg=color, fg='white', 
              font=('Arial', 10, 'bold')).pack(pady=(10, 0))
        Label(box, text=value, bg=color, fg='white', 
              font=('Arial', 20, 'bold')).pack(pady=(0, 10))
    
    def loadStats(self):
        try:
            if os.path.exists('typing_stats.json'):
                with open('typing_stats.json', 'r') as f:
                    stats = json.load(f)
                    self.best_wpm = stats.get('best_wpm', 0)
                    self.total_tests = stats.get('total_tests', 0)
            else:
                self.best_wpm = 0
                self.total_tests = 0
        except:
            self.best_wpm = 0
            self.total_tests = 0
    
    def updatePersonalBest(self, current_wpm):
        try:
            self.total_tests += 1
            if current_wpm > self.best_wpm:
                self.best_wpm = current_wpm
            
            stats = {
                'best_wpm': self.best_wpm,
                'total_tests': self.total_tests,
                'last_updated': time.time()
            }
            
            with open('typing_stats.json', 'w') as f:
                json.dump(stats, f)
        except:
            pass  

    def clearScreen(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = Tk()
    obj = TypingTest(root)
    root.mainloop()
