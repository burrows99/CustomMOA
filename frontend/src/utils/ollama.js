export const fetchInstalledModels = async () => {
  try {
    const response = await fetch(`${process.env.REACT_APP_OLLAMA_URL}/api/tags`);
    const data = await response.json();
    console.log('data for installed models', data);
    return data.models.map(model => ({
      name: model.name,
      installed: true
    }));
  } catch (error) {
    console.error('Error fetching models:', error);
    return [];
  }
};

export const installModel = async (modelName) => {
  try {
    const response = await fetch(`${process.env.REACT_APP_OLLAMA_URL}/api/pull`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name: modelName, stream: true })
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      console.log(decoder.decode(value));
    }
    return true;
  } catch (error) {
    console.error('Installation failed:', error);
    return false;
  }
};

export const KNOWN_MODELS = [
  'llama2', 'mistral', 'codellama', 'tinyllama:latest', 'phi3:latest', 'llava', 'gemma',
  'llama2-uncensored', 'dolphin-mistral', 'starling-lm'
]; 