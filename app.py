from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = {}
counter = 1

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    global counter
    task_content = request.form.get('content', '').strip()
    if task_content:
        tasks[counter] = {'content': task_content, 'completed': False}
        counter += 1
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    if task_id in tasks:
        tasks[task_id]['completed'] = not tasks[task_id]['completed']
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if task_id in tasks:
        del tasks[task_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
