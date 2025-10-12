// Main JavaScript functionality for StudyHub

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Initialize components based on page
    const currentPage = window.location.pathname;

    if (currentPage === '/pomodoro') {
        initializePomodoro();
    } else if (currentPage === '/todo') {
        initializeTodo();
    } else if (currentPage === '/quotes') {
        initializeQuotes();
    } else if (currentPage === '/deadlines') {
        initializeDeadlines();
    } else if (currentPage === '/calendar') {
        initializeCalendar();
    } else if (currentPage === '/chat') {
        initializeChat();
    }
});

// Pomodoro Timer Functions
function initializePomodoro() {
    let timer = null;
    let timeLeft = 25 * 60; // 25 minutes in seconds
    let isRunning = false;
    let isBreak = false;

    const display = document.getElementById('timer-display');
    const startBtn = document.getElementById('start-timer');
    const pauseBtn = document.getElementById('pause-timer');
    const resetBtn = document.getElementById('reset-timer');

    function updateDisplay() {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        if (display) {
            display.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }
    }

    function startTimer() {
        if (!isRunning) {
            isRunning = true;
            timer = setInterval(() => {
                timeLeft--;
                updateDisplay();

                if (timeLeft <= 0) {
                    clearInterval(timer);
                    isRunning = false;

                    // Play notification sound (if audio element exists)
                    const audio = document.getElementById('timer-sound');
                    if (audio) audio.play();

                    // Switch between work and break
                    if (isBreak) {
                        timeLeft = 25 * 60; // Back to work
                        isBreak = false;
                        showNotification('Break time over! Ready to work?');
                    } else {
                        timeLeft = 5 * 60; // 5 minute break
                        isBreak = true;
                        showNotification('Work session complete! Take a break!');
                    }
                    updateDisplay();
                }
            }, 1000);
        }
    }

    function pauseTimer() {
        if (isRunning) {
            clearInterval(timer);
            isRunning = false;
        }
    }

    function resetTimer() {
        clearInterval(timer);
        isRunning = false;
        timeLeft = 25 * 60;
        isBreak = false;
        updateDisplay();
    }

    if (startBtn) startBtn.addEventListener('click', startTimer);
    if (pauseBtn) pauseBtn.addEventListener('click', pauseTimer);
    if (resetBtn) resetBtn.addEventListener('click', resetTimer);

    updateDisplay();
}

// Todo List Functions
function initializeTodo() {
    const todoForm = document.getElementById('todo-form');
    const todoList = document.getElementById('todo-list');

    function addTodo(text) {
        const todoItem = document.createElement('div');
        todoItem.className = 'todo-item p-4 rounded-lg shadow mb-3 flex items-center justify-between';
        todoItem.innerHTML = `
            <div class="flex items-center">
                <input type="checkbox" class="mr-3 w-4 h-4 text-primary">
                <span class="todo-text">${text}</span>
            </div>
            <button class="delete-todo text-red-500 hover:text-red-700">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                </svg>
            </button>
        `;

        const checkbox = todoItem.querySelector('input[type="checkbox"]');
        const todoText = todoItem.querySelector('.todo-text');
        const deleteBtn = todoItem.querySelector('.delete-todo');

        checkbox.addEventListener('change', () => {
            if (checkbox.checked) {
                todoText.classList.add('line-through', 'text-gray-500');
            } else {
                todoText.classList.remove('line-through', 'text-gray-500');
            }
        });

        deleteBtn.addEventListener('click', () => {
            todoItem.remove();
        });

        if (todoList) {
            todoList.appendChild(todoItem);
        }
    }

    if (todoForm) {
        todoForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const input = todoForm.querySelector('input[type="text"]');
            if (input && input.value.trim()) {
                addTodo(input.value.trim());
                input.value = '';
            }
        });
    }
}

// Quotes Functions
function initializeQuotes() {
    const quotes = [
        "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt"
    ];

    const quoteDisplay = document.getElementById('quote-display');
    const newQuoteBtn = document.getElementById('new-quote');

    function displayRandomQuote() {
        const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
        if (quoteDisplay) {
            quoteDisplay.textContent = randomQuote;
        }
    }

    if (newQuoteBtn) {
        newQuoteBtn.addEventListener('click', displayRandomQuote);
    }

    // Display initial quote
    displayRandomQuote();
}

// Deadlines Functions
function initializeDeadlines() {
    const deadlineForm = document.getElementById('deadline-form');
    const deadlinesList = document.getElementById('deadlines-list');

    function addDeadline(title, date, priority) {
        const deadlineItem = document.createElement('div');
        const isUrgent = new Date(date) - new Date() < 7 * 24 * 60 * 60 * 1000; // Less than 7 days
        const cardClass = isUrgent ? 'deadline-urgent' : 'deadline-normal';

        deadlineItem.className = `${cardClass} p-4 rounded-lg shadow mb-3`;
        deadlineItem.innerHTML = `
            <div class="flex justify-between items-center">
                <div>
                    <h3 class="font-semibold text-lg">${title}</h3>
                    <p class="text-gray-600">Due: ${new Date(date).toLocaleDateString()}</p>
                    <span class="text-sm px-2 py-1 rounded ${priority === 'high' ? 'bg-red-100 text-red-800' : priority === 'medium' ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'}">${priority} priority</span>
                </div>
                <button class="delete-deadline text-red-500 hover:text-red-700">
                    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                    </svg>
                </button>
            </div>
        `;

        const deleteBtn = deadlineItem.querySelector('.delete-deadline');
        deleteBtn.addEventListener('click', () => {
            deadlineItem.remove();
        });

        if (deadlinesList) {
            deadlinesList.appendChild(deadlineItem);
        }
    }

    if (deadlineForm) {
        deadlineForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const title = deadlineForm.querySelector('#deadline-title').value;
            const date = deadlineForm.querySelector('#deadline-date').value;
            const priority = deadlineForm.querySelector('#deadline-priority').value;

            if (title && date && priority) {
                addDeadline(title, date, priority);
                deadlineForm.reset();
            }
        });
    }
}

// Calendar Functions
function initializeCalendar() {
    const currentDate = new Date();
    let currentMonth = currentDate.getMonth();
    let currentYear = currentDate.getFullYear();

    const monthNames = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];

    function generateCalendar(month, year) {
        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        const calendarGrid = document.getElementById('calendar-grid');
        const monthYear = document.getElementById('month-year');

        if (monthYear) {
            monthYear.textContent = `${monthNames[month]} ${year}`;
        }

        if (calendarGrid) {
            calendarGrid.innerHTML = '';

            // Add empty cells for days before month starts
            for (let i = 0; i < firstDay; i++) {
                const emptyDay = document.createElement('div');
                emptyDay.className = 'calendar-day p-2 text-center';
                calendarGrid.appendChild(emptyDay);
            }

            // Add days of the month
            for (let day = 1; day <= daysInMonth; day++) {
                const dayElement = document.createElement('div');
                dayElement.className = 'calendar-day p-2 text-center cursor-pointer rounded';
                dayElement.textContent = day;

                // Highlight today
                if (day === currentDate.getDate() && month === currentDate.getMonth() && year === currentDate.getFullYear()) {
                    dayElement.classList.add('calendar-today');
                }

                calendarGrid.appendChild(dayElement);
            }
        }
    }

    const prevBtn = document.getElementById('prev-month');
    const nextBtn = document.getElementById('next-month');

    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            currentMonth--;
            if (currentMonth < 0) {
                currentMonth = 11;
                currentYear--;
            }
            generateCalendar(currentMonth, currentYear);
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            currentMonth++;
            if (currentMonth > 11) {
                currentMonth = 0;
                currentYear++;
            }
            generateCalendar(currentMonth, currentYear);
        });
    }

    generateCalendar(currentMonth, currentYear);
}

// Chat Functions
function initializeChat() {
    const chatForm = document.getElementById('chat-form');
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');

    function addMessage(message, isUser = false) {
        const messageElement = document.createElement('div');
        messageElement.className = `chat-message mb-4 ${isUser ? 'text-right' : 'text-left'}`;

        const messageContent = document.createElement('div');
        messageContent.className = `inline-block max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
            isUser
                ? 'bg-primary text-white'
                : 'bg-white text-gray-800 shadow'
        }`;
        messageContent.textContent = message;

        messageElement.appendChild(messageContent);

        if (chatMessages) {
            chatMessages.appendChild(messageElement);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    function simulateAIResponse(userMessage) {
        // Simulate thinking time
        setTimeout(() => {
            const responses = [
                "That's a great question! Let me help you with that.",
                "I understand what you're asking. Here's what I think...",
                "Based on your question, I'd suggest...",
                "That's an interesting point. Consider this perspective...",
                "I'm here to help! Let me break that down for you."
            ];

            const randomResponse = responses[Math.floor(Math.random() * responses.length)];
            addMessage(randomResponse, false);
        }, 1000);
    }

    if (chatForm) {
        chatForm.addEventListener('submit', (e) => {
            e.preventDefault();

            if (chatInput && chatInput.value.trim()) {
                const message = chatInput.value.trim();
                addMessage(message, true);
                chatInput.value = '';

                // Simulate AI response
                simulateAIResponse(message);
            }
        });
    }

    // Add welcome message
    addMessage("Hello! I'm your AI study assistant. How can I help you today?", false);
}

// Utility Functions
function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'fixed top-4 right-4 bg-primary text-white px-6 py-3 rounded-lg shadow-lg z-50';
    notification.textContent = message;

    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Local Storage Functions
function saveToLocalStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
    } catch (e) {
        console.error('Error saving to localStorage:', e);
    }
}

function loadFromLocalStorage(key) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    } catch (e) {
        console.error('Error loading from localStorage:', e);
        return null;
    }
}