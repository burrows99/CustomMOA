import React, { useState, useEffect } from 'react';
import { fetchInstalledModels, installModel, KNOWN_MODELS } from '../utils/ollama';

const ChatInput = ({ onSend, disabled }) => {
  const [input, setInput] = useState('');
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState('');
  const [isInstalling, setIsInstalling] = useState(false);

  useEffect(() => {
    const initializeModels = async () => {
      const installedModels = await fetchInstalledModels();
      const allModels = KNOWN_MODELS.map(name => ({
        name,
        installed: installedModels.some(m => m.name === name)
      }));
      
      setModels(allModels);
      if (allModels.length > 0) {
        setSelectedModel(allModels.find(m => m.installed)?.name || '');
      }
    };
    initializeModels();
  }, []);

  const handleInstall = async (modelName) => {
    setIsInstalling(true);
    const success = await installModel(modelName);
    if (success) {
      const installedModels = await fetchInstalledModels();
      setModels(prev => prev.map(m => 
        m.name === modelName ? { ...m, installed: true } : m
      ));
      setSelectedModel(modelName);
    }
    setIsInstalling(false);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || !selectedModel) return;
    
    onSend({
      content: input,
      model: selectedModel
    });
    setInput('');
  };

  return (
    <div className="chat-input">
      <div className="model-selector">
        <select
          value={selectedModel}
          onChange={(e) => setSelectedModel(e.target.value)}
          disabled={isInstalling || disabled}
        >
          <option value="">Select Model</option>
          {models.map(model => (
            <option
              key={model.name}
              value={model.name}
              disabled={!model.installed}
            >
              {model.name} {model.installed ? '' : '(Click to install)'}
            </option>
          ))}
        </select>
        
        {selectedModel && !models.find(m => m.name === selectedModel)?.installed && (
          <button
            onClick={() => handleInstall(selectedModel)}
            disabled={isInstalling}
          >
            {isInstalling ? 'Installing...' : 'Install Model'}
          </button>
        )}
      </div>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={!selectedModel || disabled}
        />
        <button
          type="submit"
          disabled={!input.trim() || !selectedModel || disabled}
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatInput; 