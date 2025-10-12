from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Хранение задач в памяти: словарь {id: {content, completed}}
tasks = {}
current_id = 1

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    global current_id
    content = request.form.get('content')
    if content:
        tasks[current_id] = {'content': content, 'completed': False}
        current_id += 1
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = tasks.get(task_id)
    if task:
        task['completed'] = not task['completed']
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if task_id in tasks:
        tasks.pop(task_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

