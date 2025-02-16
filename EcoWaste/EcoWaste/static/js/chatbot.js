document.addEventListener('DOMContentLoaded', () => {
    const chatbot = {
        isOpen: false,
        init() {
            this.icon = document.querySelector('.chatbot-icon');
            this.window = document.querySelector('.chatbot-window');
            this.closeBtn = document.querySelector('.chatbot-close');
            this.input = document.querySelector('.chatbot-input input');
            this.sendBtn = document.querySelector('.chatbot-input button');
            this.messagesContainer = document.querySelector('.chatbot-messages');
            this.typingIndicator = document.querySelector('.typing-indicator');

            this.bindEvents();
            this.addMessage('Hello! I'm your EcoWaste Assistant. How can I help you today?', 'bot');
        },
        bindEvents() {
            this.icon.addEventListener('click', () => this.toggleWindow());
            this.closeBtn.addEventListener('click', () => this.toggleWindow());
            this.sendBtn.addEventListener('click', () => this.sendMessage());
            this.input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') this.sendMessage();
            });
        },
        toggleWindow() {
            this.isOpen = !this.isOpen;
            this.window.style.display = this.isOpen ? 'flex' : 'none';
            if (this.isOpen) this.input.focus();
        },
        addMessage(text, sender) {
            const message = document.createElement('div');
            message.className = `message ${sender}`;
            message.innerHTML = `<div class="message-content">${text}</div>`;
            this.messagesContainer.appendChild(message);
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        },
        async processUserMessage(text) {
            this.typingIndicator.style.display = 'block';
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ message: text })
                });

                const data = await response.json();
                
                if (response.ok) {
                    this.addMessage(data.response, 'bot');
                } else {
                    this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
                }
            } catch (error) {
                this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            } finally {
                this.typingIndicator.style.display = 'none';
            }
        },
        sendMessage() {
            const text = this.input.value.trim();
            if (text) {
                this.addMessage(text, 'user');
                this.input.value = '';
                this.processUserMessage(text);
            }
        }
    };

    chatbot.init();

    // Function to trigger shake animation
    function shakeIcon() {
        const chatbotIcon = document.querySelector('.chatbot-icon');
        chatbotIcon.classList.add('animate');
        
        // Remove the animate class after animation completes
        setTimeout(() => {
            chatbotIcon.classList.remove('animate');
        }, 4000); // 4 seconds = 3 iterations of 1-second animation + delay
    }

    // Shake icon periodically if chat window is not open
    function startPeriodicShake() {
        if (!document.querySelector('.chatbot-window').classList.contains('active')) {
            shakeIcon();
        }
    }

    // Initial delay before starting periodic shake
    setTimeout(() => {
        // Shake every 30 seconds if window is not open
        setInterval(startPeriodicShake, 30000);
    }, 3000);

    // Shake icon when page loads
    shakeIcon();
});
