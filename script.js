document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chat-window');
    const messageInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    const micBtn = document.getElementById('mic-btn');
    const typingStatus = document.getElementById('typing-status');
    const lastMessagePreview = document.querySelector('.chat-last-message .message-text');
    
    // Knowledge base for the AI bot
    const botKnowledge = {
        'admissions': 'For admissions, you need a high school diploma and a minimum GPA of 3.0. Applications close on May 1st. You can apply online via our university portal.',
        'courses': 'We offer a wide range of courses including Computer Science Engineering, Electronics and Communication Engineering, Civil Engineering, MBA, and Pharmacy.',
        'campus': 'Our campus spans 200 acres and includes state-of-the-art labs, a massive library, 5 cafeterias, and 12 dormitories.',
        'hello': 'Hello there! I am your AI College Assistant. How can I guide you today?',
        'hi': 'Hi! How can I help you with your college inquiries?',
        'fee': 'The tuition fee for a Btech program is approximately 95,000 Rs per year. We also offer MBA and Pharmacy programs.',
        'scholarship': 'We offer merit-based and need-based scholarships. The deadline to apply for the Presidential Scholarship is March 15th.',
        'contact': 'You can reach the administration at nnrg.edu ',
        'bye' : 'Goodbye! Feel free to ask if you have more questions about our college.'
    };

    function getCurrentTime() {
        const now = new Date();
        let hours = now.getHours();
        let minutes = now.getMinutes();
        const ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12; 
        minutes = minutes < 10 ? '0' + minutes : minutes;
        return `${hours}:${minutes} ${ampm}`;
    }

    function scrollToBottom() {
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function addMessage(text, type) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${type}`;
        
        const textSpan = document.createElement('span');
        textSpan.className = 'message-text';
        textSpan.innerHTML = text.replace(/\n/g, "<br>");
        
        const timeSpan = document.createElement('span');
        timeSpan.className = 'message-time';
        timeSpan.textContent = getCurrentTime();
        
        msgDiv.appendChild(textSpan);
        msgDiv.appendChild(timeSpan);
        
        chatWindow.appendChild(msgDiv);
        scrollToBottom();
        
        if (type === 'received') {
            lastMessagePreview.textContent = text;
        } else {
            lastMessagePreview.textContent = "You: " + text;
        }
    }

    async function getBotResponse(userText) {
        const lowerText = userText.toLowerCase();
        let response = "I'm sorry, I don't have information on that.";

        for (const [key, val] of Object.entries(botKnowledge)) {
            if (lowerText.includes(key)) {
                return val;
            }
        }

        // Call Python backend if no match
        try {
            const res = await fetch("http://127.0.0.1:5000/get-response", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text: userText })
            });

            const data = await res.json();
            response = data.response;

        } catch (error) {
            response = "Error connecting to server. Please try again later.";
        }

        return response;
    }

    function simulateTyping() {
        typingStatus.textContent = 'typing...';
        typingStatus.classList.add('typing');
    }

    function stopTyping() {
        typingStatus.textContent = 'Online';
        typingStatus.classList.remove('typing');
    }

    function handleSend() {
        const text = messageInput.value.trim();
        if (text === '') return;
        
        // Add user message
        addMessage(text, 'sent');
        messageInput.value = '';
        
        // Toggle Mic to Send icon logic
        sendBtn.style.display = 'none';
        micBtn.style.display = 'inline-block';
        
        // Simulate bot reply
        simulateTyping();
        
        // Random delay between 1 to 2.5 seconds
        const delay = Math.floor(Math.random() * 1500) + 1000;
        
        setTimeout( async () => {
            stopTyping();
            const reply = await getBotResponse(text);
            addMessage(reply, 'received');
        }, delay);
    }

    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSend();
        }
    });

    sendBtn.addEventListener('click', handleSend);
    
    // Toggle send vs mic button based on input
    messageInput.addEventListener('input', () => {
        if (messageInput.value.trim().length > 0) {
            sendBtn.style.display = 'inline-block';
            micBtn.style.display = 'none';
        } else {
            sendBtn.style.display = 'none';
            micBtn.style.display = 'inline-block';
        }
    });
    
    // Initial state
    sendBtn.style.display = 'none';
});
