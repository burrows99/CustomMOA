download ollama from https://ollama.com/download
pip install -r requirements.txt 
python main.py
ollama run <model-name>  (for example llama3.2) to run the models

pip freeze > requirements.txt

uvicorn app.main:app --reload for dev server start
uvicorn app.main:app for prod server start


run container using this sudo /bin/bash ./start-container.sh