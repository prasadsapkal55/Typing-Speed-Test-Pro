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
git clone https://github.com/yourusername/typing-speed-test-pro.git
cd typing-speed-test-pro
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## 📁 Project Structure

```
typing-speed-test-pro/
├── main.py           # Main application file
├── settings.py       # Configuration settings
├── text.py          # Sample text paragraphs
├── requirements.txt  # Python dependencies
├── README.md        # Project documentation
└── typing_stats.json # User statistics (created automatically)
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

### Main Menu
![Main Menu](screenshot-menu.png)

### Typing Test
![Typing Test](screenshot-test.png)

### Results Screen
![Results](screenshot-results.png)

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
