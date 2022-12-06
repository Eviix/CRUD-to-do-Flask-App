from flask import Flask, request, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
   # Luodaan uusi SQLite-tietokanta ja luodaan to-do lista table
    conn = sqlite3.connect('todolist.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, task TEXT, status TEXT)')
    c.close()

    return redirect(url_for('todos'))

@app.route('/todos', methods=['GET', 'POST'])
def todos():
   # Yhdistetään SQLite-tietokantaan   
    conn = sqlite3.connect('todolist.db')
    c = conn.cursor()

    if request.method == 'POST':
    
        task = request.form['task']
        status = request.form['status']

        c.execute('INSERT INTO todos (task, status) VALUES (?, ?)', (task, status))
        conn.commit()

    c.execute('SELECT * FROM todos')
    todos = c.fetchall()

    c.close()
    return render_template('todos.html', todos=todos)

@app.route('/todos/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
   # Yhdistetään SQLite-tietokantaan 
    conn = sqlite3.connect('todolist.db')
    c = conn.cursor()

    if request.method == 'POST':
        task = request.form['task']
        status = request.form['status']
        c.execute('UPDATE todos SET task = ?, status = ? WHERE id = ?', (task, status, id))
        conn.commit()

        return redirect(url_for('todos'))


    c.execute('SELECT * FROM todos WHERE id = ?', (id,))
    todo = c.fetchone()

    return render_template('edit.html', todo=todo)

@app.route('/todos/<int:id>/delete', methods=['POST'])
def delete(id):
   # Yhdistetään SQLite-tietokantaan 
    conn = sqlite3.connect('todolist.db')
    c = conn.cursor()

    c.execute('DELETE FROM todos WHERE id = ?', (id,))
    conn.commit()

    c.close()
    return redirect(url_for('todos'))

if __name__ == '__main__':
    app.run()
