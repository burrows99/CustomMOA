import React, { useState } from 'react';
import ChatInput from './ChatInput';
import ChatMessage from './ChatMessage';
import './Chat.css';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async (userMessage) => {
    // Add user message
    setMessages(prev => [...prev, {
      content: userMessage.content,
      isBot: false,
      model: 'user'
    }]);

    // Add temporary bot message
    setMessages(prev => [...prev, {
      content: '',
      isBot: true,
      model: userMessage.model
    }]);

    setIsLoading(true);
    
    try {
      const response = await fetch(`${process.env.REACT_APP_OLLAMA_URL}/api/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: userMessage.model,
          prompt: userMessage.content,
          stream: true
        })
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let done = false;

      while (!done) {
        const { value, done: streamDone } = await reader.read();
        done = streamDone;
        
        if (value) {
          const chunk = decoder.decode(value);
          const parsed = JSON.parse(chunk);
          
          setMessages(prev => {
            const lastMessage = prev[prev.length - 1];
            return [
              ...prev.slice(0, -1),
              {
                ...lastMessage,
                content: lastMessage.content + (parsed.response || '')
              }
            ];
          });
        }
      }
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev.slice(0, -1), {
        content: 'Error generating response',
        isBot: true,
        model: userMessage.model
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((message, index) => (
          <ChatMessage key={index} message={message} />
        ))}
      </div>
      <ChatInput onSend={handleSend} disabled={isLoading} />
    </div>
  );
};

export default Chat; 