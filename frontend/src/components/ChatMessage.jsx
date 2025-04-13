import React from 'react';

const ChatMessage = ({ message }) => {
  return (
    <div className={`chat-message ${message.isBot ? 'bot' : 'user'}`}>
      <div className="message-header">
        <span className="model-name">
          {message.isBot ? message.model : 'You'}
        </span>
      </div>
      <div className="message-content">
        {message.content}
      </div>
    </div>
  );
};

export default ChatMessage; 