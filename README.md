# 🚀 Typing Speed Test Pro

A modern, feature-rich typing speed test application built with Python and Tkinter.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- **Real-time Typing Feedback**: Live character-by-character highlighting
- **Word-by-word Analysis**: Accurate word-level error detection
- **Comprehensive Statistics**: 
  - Gross WPM (Words Per Minute)
  - Net WPM (accuracy-adjusted)
  - Character accuracy
  - Word accuracy
- **Personal Best Tracking**: Saves and displays your best performance
- **Modern UI Design**: Clean, professional interface with hover effects
- **Multiple Text Samples**: 5 different paragraphs for variety
- **Progress Visualization**: Real-time timer and progress bar

## 🎨 User Interface

The application features a modern, clean design with:
- **Dark Theme**: Easy on the eyes with professional color scheme
- **Real-time Visual Feedback**: Instant color-coded text highlighting
- **Responsive Layout**: Clean, organized interface elements
- **Hover Effects**: Interactive buttons with smooth transitions
- **Progress Indicators**: Visual timer and completion tracking
- **Statistics Dashboard**: Professional results display with colored stat boxes

## 🎯 How It Works

1. **Start**: Click "Start Test" to begin
2. **Type**: Begin typing the displayed text
3. **Real-time Feedback**: See your progress with color-coded highlighting:
   - 🟢 Green: Correct characters
   - 🔴 Red: Incorrect characters
   - 🟡 Yellow: Current character
   - ⚪ Gray: Untyped text
4. **Results**: View detailed statistics after 60 seconds

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- Required packages (install via pip):

```bash
pip install pillow pynput
```

### Quick Start
1. Clone this repository:
```bash
git clone https://github.com/prasadsapkal55/Typing-Speed-Test-Pro.git
cd Typing-Speed-Test-Pro
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

> **📸 Note**: The screenshots in this README show the actual application interface. If you're forking this project, you can replace the images in the `Screenshots/` folder with your own captures.

## 📁 Project Structure

```
typing-speed-test-pro/
├── main.py              # Main application file
├── settings.py          # Configuration settings
├── text.py             # Sample text paragraphs
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
├── LICENSE             # MIT License file
├── .gitignore          # Git ignore rules
├── Screenshots/        # Application screenshots
│   ├── Main Screen.png   # Start screen screenshot
│   ├── Typing Screen.png # Typing interface screenshot
│   └── Result Screen.png # Results display screenshot
└── typing_stats.json   # User statistics (created automatically)
```

## 🎮 Usage

### Starting a Test
- Launch the application
- Your personal best will be displayed if available
- Click "Start Test" to begin

### During the Test
- Type the displayed text as accurately as possible
- Watch real-time statistics in the header
- The timer shows remaining time
- Progress bar indicates completion

### After the Test
- View comprehensive results including:
  - Gross and Net WPM
  - Character and Word accuracy
  - Detailed typing statistics
- See if you've achieved a new personal best!
- Choose to test again or return to main menu

## 🎨 Screenshots

### 🏠 Main Menu
The clean and modern start screen with your personal best display.

![Main Menu](Screenshots/Main%20Screen.png)

### ⌨️ Typing Test in Action
Real-time feedback with color-coded highlighting and live statistics.

![Typing Test](Screenshots/Typing%20Screen.png)

### 📊 Results Screen
Comprehensive statistics with modern design and visual appeal.

![Results Screen](Screenshots/Result%20Screen.png)

### 🎯 Features Overview
Visual demonstration of key features:

| Feature | Description |
|---------|-------------|
| 🟢 **Correct Text** | Green highlighting for correctly typed characters |
| 🔴 **Incorrect Text** | Red highlighting for mistakes |
| 🟡 **Current Position** | Yellow highlighting for the next character |
| ⚪ **Untyped Text** | Gray text for remaining content |
| 📈 **Real-time Stats** | Live WPM and accuracy tracking |
| ⏱️ **Progress Timer** | Visual countdown and progress bar |

## ⚙️ Configuration

Edit `settings.py` to customize:
- Window dimensions
- Test duration
- Colors and fonts
- Background image path

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

1. **Bug Reports**: Found a bug? Open an issue
2. **Feature Requests**: Have an idea? Suggest it
3. **Code Contributions**: 
   - Fork the repository
   - Create a feature branch
   - Make your changes
   - Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python's Tkinter for cross-platform compatibility
- Uses PIL (Pillow) for image processing
- Keyboard event handling with pynput
- JSON for persistent statistics storage

## 📊 Statistics Tracking

The application automatically tracks:
- Personal best WPM
- Total tests taken
- Performance history (stored in `typing_stats.json`)

## 🔧 Technical Details

- **Framework**: Python Tkinter
- **Real-time Processing**: Character-by-character analysis
- **Threading**: Background timer using Python threading
- **Data Persistence**: JSON-based statistics storage
- **Event Handling**: Keyboard and mouse event management

---

**Made with ❤️ for typing enthusiasts**

Want to improve your typing speed? Start practicing with Typing Speed Test Pro!
