class MatrixAI {
    constructor() {
        this.socket = io();
        this.isListening = false;
        this.isSpeaking = false;
        
        this.initElements();
        this.initSocketEvents();
        this.initEventListeners();
        this.startWelcomeMessage();
    }
    
    initElements() {
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.voiceBtn = document.getElementById('voiceBtn');
        this.avatar = document.getElementById('avatar');
        this.welcomeText = document.getElementById('welcomeText');
        this.statusIndicator = document.getElementById('statusIndicator');
        this.agentStatus = document.getElementById('agentStatus');
    }
    
    initSocketEvents() {
        this.socket.on('connect', () => {
            console.log('Connected to Matrix AI server');
        });
        
        this.socket.on('new_message', (data) => {
            this.addMessage(data.assistant_response, false);
        });
        
        this.socket.on('voice_status', (data) => {
            this.updateVoiceStatus(data.status);
        });
        
        this.socket.on('status', (data) => {
            console.log('Server status:', data);
        });
    }
    
    initEventListeners() {
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.voiceBtn.addEventListener('click', () => this.toggleVoice());
        this.avatar.addEventListener('click', () => this.avatarClick());
        
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === ' ' && e.ctrlKey) {
                e.preventDefault();
                this.toggleVoice();
            }
        });
    }
    
    startWelcomeMessage() {
        const welcomeMessage = "Greetings Neo, welcome to the Matrix. I am your digital assistant. How may I guide you through the code streams today?";
        this.typeText(this.welcomeText, welcomeMessage, 50);
    }
    
    typeText(element, text, speed = 30) {
        element.textContent = '';
        element.classList.add('typing-text');
        
        let index = 0;
        const typeInterval = setInterval(() => {
            if (index < text.length) {
                element.textContent += text.charAt(index);
                index++;
            } else {
                element.classList.remove('typing-text');
                clearInterval(typeInterval);
            }
        }, speed);
    }
    
    addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        if (!isUser) {
            // Typing effect for assistant messages
            this.typeText(contentDiv, content, 30);
        } else {
            contentDiv.textContent = content;
        }
        
        messageDiv.appendChild(contentDiv);
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;
        
        // Add user message immediately
        this.addMessage(message, true);
        this.messageInput.value = '';
        
        // Set speaking state
        this.setSpeakingState(true);
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                // Response will be handled by socket event
                setTimeout(() => this.setSpeakingState(false), 2000);
            } else {
                this.addMessage('Error processing request', false);
                this.setSpeakingState(false);
            }
        } catch (error) {
            console.error('Error sending message:', error);
            this.addMessage('Connection error', false);
            this.setSpeakingState(false);
        }
    }
    
    async toggleVoice() {
        if (this.isListening) {
            await this.stopVoice();
        } else {
            await this.startVoice();
        }
    }
    
    async startVoice() {
        try {
            const response = await fetch('/api/voice/start', {
                method: 'POST'
            });
            
            if (response.ok) {
                this.setListeningState(true);
                this.updateAgentStatus('Listening for your command...');
            }
        } catch (error) {
            console.error('Error starting voice:', error);
        }
    }
    
    async stopVoice() {
        try {
            const response = await fetch('/api/voice/stop', {
                method: 'POST'
            });
            
            if (response.ok) {
                this.setListeningState(false);
                this.updateAgentStatus('Processing your request...');
            }
        } catch (error) {
            console.error('Error stopping voice:', error);
        }
    }
    
    setListeningState(listening) {
        this.isListening = listening;
        
        if (listening) {
            this.avatar.classList.add('listening');
            this.voiceBtn.classList.add('active');
            this.voiceBtn.textContent = 'LISTENING';
            this.statusIndicator.classList.add('listening');
        } else {
            this.avatar.classList.remove('listening');
            this.voiceBtn.classList.remove('active');
            this.voiceBtn.textContent = 'VOICE';
            this.statusIndicator.classList.remove('listening');
        }
    }
    
    setSpeakingState(speaking) {
        this.isSpeaking = speaking;
        
        if (speaking) {
            this.avatar.classList.add('speaking');
            this.statusIndicator.classList.add('speaking');
            this.updateAgentStatus('Matrix AI is responding...');
        } else {
            this.avatar.classList.remove('speaking');
            this.statusIndicator.classList.remove('speaking');
            this.updateAgentStatus('Ready to assist you, Neo');
        }
    }
    
    updateVoiceStatus(status) {
        switch (status) {
            case 'listening':
                this.setListeningState(true);
                break;
            case 'processing':
                this.setListeningState(false);
                this.setSpeakingState(true);
                break;
            default:
                this.setListeningState(false);
                this.setSpeakingState(false);
        }
    }
    
    updateAgentStatus(message) {
        this.agentStatus.textContent = `Agent: ${message}`;
    }
    
    avatarClick() {
        if (!this.isListening && !this.isSpeaking) {
            this.addMessage("Matrix AI interface activated. How may I assist you, Neo?", false);
        }
    }
    
    // Utility method for API status checks
    async checkStatus() {
        try {
            const response = await fetch('/api/status');
            const status = await response.json();
            console.log('System status:', status);
            return status;
        } catch (error) {
            console.error('Error checking status:', error);
            return null;
        }
    }
}

// Initialize Matrix AI when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.matrixAI = new MatrixAI();
});