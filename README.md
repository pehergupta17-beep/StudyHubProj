# 🎓 StudyHub - High School Success Platform

A comprehensive web application designed to help high school students achieve academic success through smart study tools, AI-powered assistance, and productivity features.

![StudyHub Banner](https://via.placeholder.com/800x200/4F46E5/white?text=StudyHub+-+Your+Path+to+Academic+Success)

## ✨ Features

### 📅 **Academic Management**
- **Deadline Tracker**: Manage assignments with priority levels and urgency indicators
- **Interactive Calendar**: Schedule events, track deadlines, and view academic timeline
- **Smart To-Do Lists**: Organize tasks with categories, progress tracking, and completion stats

### ⏰ **Productivity Tools**
- **Pomodoro Timer**: 25-minute focused study sessions with customizable breaks
- **Time Management**: Built-in productivity techniques and scheduling tools
- **Progress Tracking**: Visual indicators for daily and weekly achievements

### 💪 **Motivation & Wellness**
- **Daily Quotes**: Inspirational messages categorized by themes
- **Positivity Challenges**: Interactive activities to build positive mindset
- **Favorite Quotes**: Save and organize meaningful quotes

### 🤖 **AI-Powered Study Assistant**
- **GEMINI Integration**: Advanced AI chatbot powered by Google's GEMINI Pro
- **Context-Aware Conversations**: Remembers your study patterns and preferences
- **Persistent Memory**: Vector database stores conversation history for personalized responses
- **Study Knowledge Base**: Pre-loaded with comprehensive academic guidance

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/studyhub.git
   cd studyhub
   ```

2. **Run the automated setup**
   ```bash
   python setup_gemini.py
   ```
   This will:
   - Install all required packages
   - Set up the vector database
   - Initialize the knowledge base
   - Test all integrations

3. **Configure GEMINI AI (Optional but Recommended)**
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Update the `.env` file:
     ```env
     GEMINI_API_KEY=your_actual_api_key_here
     ```

4. **Start the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   ```
   http://localhost:5000
   ```

## 🛠️ Manual Setup (Alternative)

If you prefer manual installation:

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Initialize the knowledge base**
   ```bash
   python init_knowledge_base.py
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

## 📁 Project Structure

```
StudyHub/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── routes/
│   │   ├── main.py              # Main page routes
│   │   └── chat_routes.py       # AI chat API endpoints
│   └── services/
│       ├── gemini_service.py    # GEMINI AI integration
│       └── vector_service.py    # Vector database management
├── static/
│   ├── css/
│   │   └── style.css            # Custom styling
│   ├── js/
│   │   └── main.js              # Frontend functionality
│   └── images/                  # Static images
├── templates/
│   ├── base.html                # Base template
│   ├── index.html               # Homepage
│   ├── deadlines.html           # Deadline management
│   ├── pomodoro.html            # Pomodoro timer
│   ├── quotes.html              # Motivational quotes
│   ├── todo.html                # To-do lists
│   ├── calendar.html            # Academic calendar
│   └── chat.html                # AI assistant
├── .env                         # Environment variables
├── requirements.txt             # Python dependencies
├── setup_gemini.py             # Automated setup script
├── init_knowledge_base.py      # Knowledge base initialization
├── app.py                      # Main application entry point
└── README.md                   # Project documentation
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///high_school.db

# GEMINI AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-pro

# Vector Database Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

### GEMINI API Setup

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new project or select existing one
3. Generate an API key
4. Add the key to your `.env` file
5. Restart the application

## 🎯 Usage Guide

### 📚 Study Assistant Features

**Getting Study Help:**
- Ask questions about any academic subject
- Get personalized study techniques
- Receive time management advice
- Find motivation during challenging times

**Quick Actions:**
- Use predefined question buttons for instant help
- Browse study knowledge base
- Get subject-specific guidance

### 📅 Academic Planning

**Deadline Management:**
- Add assignments with due dates and priority levels
- Filter deadlines by urgency and importance
- Get visual indicators for upcoming deadlines

**Calendar Integration:**
- Schedule study sessions and events
- View weekly and monthly academic overview
- Track progress and milestones

### ⏱️ Productivity Features

**Pomodoro Sessions:**
- Customize work and break intervals
- Track daily study sessions
- Build consistent study habits

**To-Do Organization:**
- Create tasks with categories and priorities
- Monitor completion rates and productivity scores
- Clear completed tasks and sort by importance

## 🔌 API Endpoints

### Chat API
- `POST /api/chat` - Send message to AI assistant
- `GET /api/chat/history` - Retrieve conversation history
- `POST /api/chat/quick-response` - Get quick topic responses
- `GET /api/chat/status` - Check AI service status
- `POST /api/chat/clear-history` - Clear session history

### Example API Usage

```javascript
// Send a message to the AI assistant
fetch('/api/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        message: 'How can I improve my study habits?'
    })
})
.then(response => response.json())
.then(data => console.log(data.response));
```

## 🧠 AI Knowledge Base

The AI assistant comes pre-loaded with comprehensive knowledge about:

- **Study Techniques**: Active recall, spaced repetition, Feynman technique, mind mapping
- **Time Management**: Pomodoro technique, time blocking, Eisenhower matrix
- **Subject-Specific Help**: Mathematics, science, history, language arts
- **Test Preparation**: Study strategies, anxiety management, test-taking skills
- **Motivation**: Growth mindset, goal setting, stress management

## 🛡️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Tailwind CSS with custom components
- **AI**: Google GEMINI Pro API
- **Vector Database**: ChromaDB with Sentence Transformers
- **Data Storage**: SQLite (development), PostgreSQL (production ready)
- **Session Management**: Flask sessions with secure cookies

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Areas for Contribution

- 🎨 **UI/UX Improvements**: Enhance the user interface and experience
- 🧠 **AI Features**: Expand the knowledge base or improve AI responses
- 📱 **Mobile Optimization**: Improve mobile responsiveness
- 🔧 **Performance**: Optimize loading times and efficiency
- 📚 **Documentation**: Improve guides and documentation
- 🧪 **Testing**: Add unit tests and integration tests

### Development Guidelines

- Follow PEP 8 for Python code
- Use meaningful commit messages
- Add comments for complex logic
- Test your changes before submitting
- Update documentation when needed

## 🐛 Troubleshooting

### Common Issues

**GEMINI API Not Working:**
- Verify your API key is correct in `.env`
- Check your internet connection
- Ensure you have API quota remaining

**Vector Database Issues:**
- Delete the `chroma_db` folder and run `python init_knowledge_base.py`
- Check disk space availability
- Verify write permissions in the project directory

**Frontend Not Loading:**
- Clear browser cache
- Check browser console for JavaScript errors
- Verify Flask server is running

**Package Installation Failures:**
- Update pip: `python -m pip install --upgrade pip`
- Use virtual environment: `python -m venv venv && source venv/bin/activate`
- Install packages individually if bulk install fails

### Getting Help

- Check the [Issues](https://github.com/yourusername/studyhub/issues) page
- Read through existing documentation
- Join our community discussions
- Contact the maintainers

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google GEMINI**: For providing advanced AI capabilities
- **ChromaDB**: For vector database functionality
- **Tailwind CSS**: For beautiful and responsive styling
- **Flask Community**: For the excellent web framework
- **Open Source Contributors**: For various libraries and tools used

## 🚀 Roadmap

### Upcoming Features

- [ ] **Mobile App**: Native iOS and Android applications
- [ ] **Study Groups**: Collaborative study spaces
- [ ] **Grade Tracking**: Academic performance monitoring
- [ ] **Parent Dashboard**: Progress sharing with parents/guardians
- [ ] **Integration APIs**: Connect with school learning management systems
- [ ] **Offline Mode**: Limited functionality without internet
- [ ] **Advanced Analytics**: Detailed study pattern analysis
- [ ] **Gamification**: Achievement badges and study streaks

### Long-term Vision

- Expand to support college students and lifelong learners
- Integration with major educational platforms
- Advanced AI tutoring capabilities
- Personalized learning path recommendations
- Community-driven study resources

## 📞 Support

Need help? We're here for you!

- 📧 **Email**: support@studyhub.com
- 💬 **Discord**: [Join our community](https://discord.gg/studyhub)
- 📖 **Documentation**: [Full documentation](https://docs.studyhub.com)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/studyhub/issues)

---

<div align="center">

**Made with ❤️ for students everywhere**

[Website](https://studyhub.com) • [Documentation](https://docs.studyhub.com) • [Community](https://discord.gg/studyhub) • [Twitter](https://twitter.com/studyhub)

</div>