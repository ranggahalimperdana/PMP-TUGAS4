from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import re

app = Flask(__name__)

# Koneksi ke database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Ganti dengan password Anda jika ada
    database="video_link"  # Pastikan ini adalah nama database yang benar
)

def get_video_id(url):
    match = re.search(r'(?:v=|\/)([a-zA-Z0-9_-]{11})', url)
    if match:
        return match.group(1)
    return None

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM links")
    links = cursor.fetchall()
    cursor.close()
    return render_template('index.html', links=links)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        url = request.form['url']
        description = request.form['description']
        cursor = db.cursor()
        cursor.execute("INSERT INTO links (url, description) VALUES (%s, %s)", (url, description))
        db.commit()
        cursor.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cursor = db.cursor()
    if request.method == 'POST':
        url = request.form['url']
        description = request.form['description']
        cursor.execute("UPDATE links SET url = %s, description = %s WHERE id = %s", (url, description, id))
        db.commit()
        cursor.close()
        return redirect(url_for('index'))
    
    cursor.execute("SELECT * FROM links WHERE id = %s", (id,))
    link = cursor.fetchone()
    cursor.close()
    return render_template('edit.html', link=link)

@app.route('/delete/<int:id>')
def delete(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM links WHERE id = %s", (id,))
    db.commit()
    cursor.close()
    return redirect(url_for('index'))

@app.context_processor
def utility_processor():
    return dict(get_video_id=get_video_id)

if __name__ == '__main__':
    app.run(debug=True)
