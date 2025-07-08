from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# MySQL configuration (XAMPP defaults)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Mysql@root#1990',
    'database': 'notes_app'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
    notes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['POST'])
def add_note():
    content = request.form['content']
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notes (content, created_at) VALUES (%s, %s)",
        (content, now)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:note_id>')
def edit(note_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notes WHERE id = %s", (note_id,))
    note = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit.html', note=note)

@app.route('/update/<int:note_id>', methods=['POST'])
def update(note_id):
    content = request.form['content']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE notes SET content = %s WHERE id = %s",
        (content, note_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:note_id>')
def delete(note_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = %s", (note_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/print_notes')
def print_notes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT content FROM notes ORDER BY created_at DESC"
    )
    notes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('print.html', notes=notes)

if __name__ == '__main__':
    app.run(debug=True)
