import time
import random
import text as tt
from tkinter import *
from tkinter import ttk
import settings as st  # Make sure this file exists in the same directory or adjust the path
from threading import Thread
from PIL import Image, ImageTk
from pynput.keyboard import Listener
import json
import os

# Define the typing test class
class TypingTest:

    # Create the main application window
    def __init__(self, root):
        # Window Settings
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
        
        # Load user statistics
        self.loadStats()

        # Text for using as a paragraph
        self.textList = [tt.text1, tt.text2, tt.text3, tt.text4, tt.text5]

        # Tkinter Frame with gradient-like background
        self.frame = Frame(self.window, bg='#2c3e50', width=st.width, height=st.height)
        self.frame.place(x=0, y=0)

        # Calling the function, startWindow()
        self.startWindow()

    # The welcome window
    def startWindow(self):
        # Main title with modern styling
        titleLabel = Label(self.frame, text="Typing Speed Test Pro", 
                          bg='#2c3e50', fg='#ecf0f1', 
                          font=('Arial', 32, "bold"))
        titleLabel.place(x=150, y=60)
        
        # Subtitle
        subtitleLabel = Label(self.frame, text="Test and improve your typing speed", 
                             bg='#2c3e50', fg='#bdc3c7', 
                             font=('Arial', 12))
        subtitleLabel.place(x=280, y=110)
        
        # Display best WPM if available
        if hasattr(self, 'best_wpm') and self.best_wpm > 0:
            bestLabel = Label(self.frame, text=f"Your Best: {self.best_wpm} WPM", 
                             bg='#2c3e50', fg='#f39c12', 
                             font=('Arial', 14, 'bold'))
            bestLabel.place(x=320, y=140)

        # Modern start button
        startButton = Button(self.frame, text="Start Test", 
                           border=0, cursor='hand2', 
                           fg='white', bg='#3498db', 
                           font=('Arial', 16, 'bold'),
                           padx=30, pady=10,
                           relief='flat',
                           command=self.startTest)
        startButton.place(x=320, y=200)
        
        # Add hover effects
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

    # Typing test window
    def startTest(self):
        # Clearing the previous screen
        self.clearScreen()
        
        # Reset variables
        self.typingStarted = False
        self.currentCharIndex = 0
        self.correctChars = 0
        self.incorrectChars = 0
        self.startTime = 0

        # Getting the total time allocated for the test
        self.totalTime = st.totalTime

        # Choosing a random paragraph from the list of several choices
        self.paragraph = random.choice(self.textList)
        
        # Create header frame
        headerFrame = Frame(self.frame, bg='#34495e', height=50)
        headerFrame.pack(fill=X, padx=10, pady=(10, 0))
        
        # Time display with better styling
        self.timeLabel = Label(headerFrame, text="1:00", 
                              bg='#34495e', fg='#e74c3c', 
                              font=('Arial', 18, 'bold'))
        self.timeLabel.pack(side=LEFT, padx=20, pady=10)
        
        # Progress bar for time
        self.progressVar = DoubleVar()
        self.progressBar = ttk.Progressbar(headerFrame, variable=self.progressVar, 
                                          maximum=st.totalTime, length=200)
        self.progressBar.pack(side=LEFT, padx=20, pady=10)
        
        # Stats display
        self.statsLabel = Label(headerFrame, text="WPM: 0 | Accuracy: 100%", 
                               bg='#34495e', fg='#2ecc71', 
                               font=('Arial', 12, 'bold'))
        self.statsLabel.pack(side=RIGHT, padx=20, pady=10)

        # Text display area with better styling
        textFrame = Frame(self.frame, bg='#ecf0f1', relief='solid', bd=1)
        textFrame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Create a text widget with scroll
        self.textDisplay = Text(textFrame, width=70, height=8, 
                               bg='#ecf0f1', fg='#2c3e50',
                               font=('Courier New', 14),
                               wrap=WORD, relief='flat',
                               state='disabled',
                               cursor='arrow')
        self.textDisplay.pack(padx=10, pady=10)
        
        # Configure text tags for highlighting
        self.textDisplay.tag_configure('correct', background='#d5f4e6', foreground='#27ae60')
        self.textDisplay.tag_configure('incorrect', background='#fadbd8', foreground='#e74c3c')
        self.textDisplay.tag_configure('current', background='#fef9e7', foreground='#f39c12')
        self.textDisplay.tag_configure('untyped', background='#ecf0f1', foreground='#7f8c8d')
        
        # Insert and format the text
        self.textDisplay.config(state='normal')
        self.textDisplay.insert(END, self.paragraph)
        self.textDisplay.tag_add('untyped', '1.0', END)
        self.textDisplay.config(state='disabled')

        # Input area with better styling
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

        # Define the on press to capture key pressing
        self.listener = Listener(on_press=self.on_key_press)
        # Starting a different thread for this task
        self.listener.start()

    # Method to handle key press events
    def on_key_press(self, key):
        if not self.typingStarted:
            self.typingStarted = True
            self.startTime = time.time()
            self.multiThreading()
    
    # Real-time typing feedback
    def on_type(self, event):
        if not self.typingStarted:
            return
            
        typed_text = self.inputEntry.get()
        self.updateTextHighlight(typed_text)
        self.updateStats(typed_text)
    
    # Update text highlighting based on typing
    def updateTextHighlight(self, typed_text):
        self.textDisplay.config(state='normal')
        
        # Clear all tags
        self.textDisplay.tag_remove('correct', '1.0', END)
        self.textDisplay.tag_remove('incorrect', '1.0', END)
        self.textDisplay.tag_remove('current', '1.0', END)
        self.textDisplay.tag_remove('untyped', '1.0', END)
        
        # Apply highlighting based on typed text
        for i, char in enumerate(typed_text):
            pos = f"1.{i}"
            next_pos = f"1.{i+1}"
            
            if i < len(self.paragraph):
                if char == self.paragraph[i]:
                    self.textDisplay.tag_add('correct', pos, next_pos)
                else:
                    self.textDisplay.tag_add('incorrect', pos, next_pos)
        
        # Highlight current character
        if len(typed_text) < len(self.paragraph):
            current_pos = f"1.{len(typed_text)}"
            next_current_pos = f"1.{len(typed_text)+1}"
            self.textDisplay.tag_add('current', current_pos, next_current_pos)
        
        # Mark untyped text
        if len(typed_text) < len(self.paragraph):
            untyped_start = f"1.{len(typed_text)+1}"
            self.textDisplay.tag_add('untyped', untyped_start, END)
        
        self.textDisplay.config(state='disabled')
    
    # Update real-time statistics
    def updateStats(self, typed_text):
        if not typed_text or not self.typingStarted:
            return
            
        # Calculate correct and incorrect characters
        correct = sum(1 for i, char in enumerate(typed_text) 
                     if i < len(self.paragraph) and char == self.paragraph[i])
        
        # Calculate WPM
        elapsed_time = time.time() - self.startTime
        if elapsed_time > 0:
            wpm = (len(typed_text.split()) / elapsed_time) * 60
        else:
            wpm = 0
            
        # Calculate accuracy
        if len(typed_text) > 0:
            accuracy = (correct / len(typed_text)) * 100
        else:
            accuracy = 100
            
        # Update stats display
        self.statsLabel.config(text=f"WPM: {int(wpm)} | Accuracy: {int(accuracy)}%")

    # Multi-threading
    def multiThreading(self):
        x = Thread(target=self.countDown)
        x.start()

    # Display the remaining time
    def countDown(self):
        initial_time = self.totalTime
        while self.totalTime > 0:
            # Format time as MM:SS
            minutes = self.totalTime // 60
            seconds = self.totalTime % 60
            # Updating the Time Label
            self.timeLabel.config(text=f"{minutes}:{seconds:02d}")
            
            # Update progress bar
            progress = initial_time - self.totalTime
            self.progressVar.set(progress)
            
            time.sleep(1)
            self.totalTime -= 1

        self.timeLabel.config(text="0:00")
        self.progressVar.set(initial_time)
        
        # Stop the keyboard listener
        if hasattr(self, 'listener') and self.listener:
            self.listener.stop()
        # Calling the Function to Calculate the Final Result
        self.calculateResult()

    # Set an image
    def backgroundImage(self, img):
        # Opening the image
        image = Image.open(img)
        # Resize the image to fit to the screen
        resizedImg = image.resize((st.width, st.height))
        # Creating an instance of PhotoImage class of ImageTk module
        self.img = ImageTk.PhotoImage(resizedImg)

        label = Label(self.frame, image=self.img)
        label.pack()

    # Calculate the result with enhanced display
    def calculateResult(self):
        # Getting the text from the Tkinter Entry Widget
        typed_text = self.inputEntry.get()
        words_typed = typed_text.split()
        
        # Clearing the previous screen
        self.clearScreen()
        
        # Create results frame with modern styling
        resultsFrame = Frame(self.frame, bg='#2c3e50')
        resultsFrame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Title
        titleLabel = Label(resultsFrame, text="Test Results", 
                          bg='#2c3e50', fg='#ecf0f1', 
                          font=('Arial', 28, 'bold'))
        titleLabel.pack(pady=(0, 30))

        # Calculate comprehensive statistics
        if len(typed_text) > 0:
            # Character-level accuracy
            correct_chars = sum(1 for i, char in enumerate(typed_text) 
                               if i < len(self.paragraph) and char == self.paragraph[i])
            char_accuracy = (correct_chars / len(typed_text)) * 100
            
            # Word-level accuracy
            paragraph_words = self.paragraph.split()
            correct_words = 0
            for i, word in enumerate(words_typed):
                if i < len(paragraph_words) and word == paragraph_words[i]:
                    correct_words += 1
            
            word_accuracy = (correct_words / len(words_typed)) * 100 if words_typed else 0
            
            # WPM calculation
            wpm = len(words_typed)
            
            # Net WPM (accounting for errors)
            net_wpm = (correct_words / st.totalTime) * 60 if st.totalTime > 0 else 0
            
        else:
            char_accuracy = 0
            word_accuracy = 0
            wpm = 0
            net_wpm = 0
            correct_words = 0

        # Create stats grid
        statsFrame = Frame(resultsFrame, bg='#34495e', relief='solid', bd=1)
        statsFrame.pack(pady=20, padx=40, fill=X)
        
        # Row 1: WPM and Net WPM
        row1 = Frame(statsFrame, bg='#34495e')
        row1.pack(fill=X, pady=20)
        
        self.createStatBox(row1, "Gross WPM", str(wpm), '#3498db', LEFT)
        self.createStatBox(row1, "Net WPM", f"{net_wpm:.1f}", '#e74c3c', RIGHT)
        
        # Row 2: Accuracies
        row2 = Frame(statsFrame, bg='#34495e')
        row2.pack(fill=X, pady=(0, 20))
        
        self.createStatBox(row2, "Character Accuracy", f"{char_accuracy:.1f}%", '#2ecc71', LEFT)
        self.createStatBox(row2, "Word Accuracy", f"{word_accuracy:.1f}%", '#f39c12', RIGHT)
        
        # Additional stats
        additionalFrame = Frame(resultsFrame, bg='#2c3e50')
        additionalFrame.pack(pady=20)
        
        Label(additionalFrame, text=f"Words Typed: {len(words_typed)} | Correct Words: {correct_words}", 
              bg='#2c3e50', fg='#bdc3c7', font=('Arial', 12)).pack()
        
        Label(additionalFrame, text=f"Characters Typed: {len(typed_text)} | Correct Characters: {correct_chars if len(typed_text) > 0 else 0}", 
              bg='#2c3e50', fg='#bdc3c7', font=('Arial', 12)).pack()
        
        # Save and display personal best
        self.updatePersonalBest(net_wpm)
        
        if hasattr(self, 'best_wpm') and self.best_wpm > 0:
            if net_wpm > self.best_wpm:
                Label(additionalFrame, text="🎉 New Personal Best! 🎉", 
                      bg='#2c3e50', fg='#f1c40f', font=('Arial', 14, 'bold')).pack(pady=9)
            else:
                Label(additionalFrame, text=f"Personal Best: {self.best_wpm:.1f} WPM", 
                      bg='#2c3e50', fg='#95a5a6', font=('Arial', 12)).pack(pady=9)

        # Buttons frame
        buttonFrame = Frame(resultsFrame, bg='#2c3e50')
        buttonFrame.pack(pady=30)
        
        # Test again button
        testAgainButton = Button(buttonFrame, text="Test Again", 
                               border=0, cursor='hand2', 
                               fg='white', bg='#3498db', 
                               font=('Arial', 14, 'bold'),
                               padx=20, pady=8,
                               relief='flat',
                               command=self.startTest)
        testAgainButton.pack(side=LEFT, padx=10)
        
        # Back to menu button
        menuButton = Button(buttonFrame, text="Main Menu", 
                          border=0, cursor='hand2', 
                          fg='white', bg='#95a5a6', 
                          font=('Arial', 14, 'bold'),
                          padx=20, pady=8,
                          relief='flat',
                          command=self.startWindow)
        menuButton.pack(side=LEFT, padx=10)
        
        # Add hover effects
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
    
    # Create stat display box
    def createStatBox(self, parent, title, value, color, side):
        box = Frame(parent, bg=color, relief='flat', bd=0)
        box.pack(side=side, padx=20, pady=10, fill=X, expand=True)
        
        Label(box, text=title, bg=color, fg='white', 
              font=('Arial', 10, 'bold')).pack(pady=(10, 0))
        Label(box, text=value, bg=color, fg='white', 
              font=('Arial', 20, 'bold')).pack(pady=(0, 10))
    
    # Load user statistics
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
    
    # Update personal best
    def updatePersonalBest(self, current_wpm):
        try:
            self.total_tests += 1
            if current_wpm > self.best_wpm:
                self.best_wpm = current_wpm
            
            # Save to file
            stats = {
                'best_wpm': self.best_wpm,
                'total_tests': self.total_tests,
                'last_updated': time.time()
            }
            
            with open('typing_stats.json', 'w') as f:
                json.dump(stats, f)
        except:
            pass  # Silently fail if can't save stats

    # Clear the screen
    def clearScreen(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

# Initializing the application
if __name__ == "__main__":
    # Instance of Tk class
    root = Tk()
    # Object of TypingTest class
    obj = TypingTest(root)
    root.mainloop()