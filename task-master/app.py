from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Flashメッセージ用の秘密鍵

# SQLiteデータベースのセットアップ
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority INTEGER NOT NULL,
            completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)),
            due_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

# タスクの取得（並べ替え）
def get_sorted_tasks(sort_by):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if sort_by == 'date_desc':
        cursor.execute('SELECT * FROM tasks ORDER BY due_date DESC')
    elif sort_by == 'date_asc':
        cursor.execute('SELECT * FROM tasks ORDER BY due_date ASC')
    elif sort_by == 'priority_desc':
        cursor.execute('SELECT * FROM tasks ORDER BY priority DESC')
    elif sort_by == 'priority_asc':
        cursor.execute('SELECT * FROM tasks ORDER BY priority ASC')

    tasks = cursor.fetchall()
    conn.close()
    return tasks

# タスクの追加
def add_task(title, description, priority, due_date):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (title, description, priority, completed, due_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, description, priority, 0, due_date))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        flash("タスクの追加に失敗しました。")
    finally:
        conn.close()

# タスクの更新
def update_task(task_id, completed):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET completed = ? WHERE id = ?', (completed, task_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        flash("タスクの更新に失敗しました。")
    finally:
        conn.close()

# タスクの削除
def delete_task(task_id):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        flash("タスクの削除に失敗しました。")
    finally:
        conn.close()

# due_dateのバリデーション
def validate_due_date(due_date):
    try:
        datetime.strptime(due_date, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# 最初にデータベースを初期化
init_db()

@app.route('/')
def index():
    sort_by = request.args.get('sort_by', 'date_desc')  # デフォルトは「期限日降順」
    tasks = get_sorted_tasks(sort_by)
    return render_template('index.html', tasks=tasks, sort_by=sort_by)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    description = request.form['description']
    priority = request.form['priority']
    due_date = request.form['due_date']

    if not validate_due_date(due_date):
        flash("期限日の形式が正しくありません。YYYY-MM-DDの形式で入力してください。")
        return redirect(url_for('index'))

    add_task(title, description, priority, due_date)
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>', methods=['POST'])
def update(task_id):
    completed = request.form.get('completed') == 'on'
    update_task(task_id, completed)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    delete_task(task_id)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)