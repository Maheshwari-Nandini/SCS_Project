import subprocess
from celery import Celery

app = Celery('tasks', broker='memory://localhost/')

@app.task
def run_program():
    result = subprocess.run(['python', 'static/Program.py'], capture_output=True, text=True)
    return result.stdout
