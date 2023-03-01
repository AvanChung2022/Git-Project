from app import app
from flask import render_template, redirect, request, session
from app.models.book import Book
from app.models.user import User

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/user/logout')
        
    return render_template('dashboard.html', user=user, books=Book.get_all())

@app.route('/books/new')
def create_book():
    if 'user_id' not in session:
        return redirect('/user/login')

    return render_template('book_new.html')

@app.route('/books/new/process', methods=['POST'])
def process_book():
    if 'user_id' not in session:
        return redirect('/user/login')
    if not Book.validate_book(request.form):
        return redirect('/books/new')

    data = {
        'user_id': session['user_id'],
        'title': request.form['title'],
        'description': request.form['description'],
    }
    Book.save(data)
    return redirect('/dashboard')

@app.route('/books/<int:id>')
def view_book(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    return render_template('book_view.html',book=Book.get_by_id({'id': id}))

@app.route('/books/edit/<int:id>')
def edit_book(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    return render_template('book_edit.html',book=Book.get_by_id({'id': id}))

@app.route('/books/edit/process/<int:id>', methods=['POST'])
def process_edit_book(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    if not Book.validate_book(request.form):
        return redirect(f'/books/edit/{id}')

    data = {
        'id': id,
        'title': request.form['title'],
        'description': request.form['description'],
    }
    Book.update(data)
    return redirect('/dashboard')

@app.route('/books/destroy/<int:id>')
def destroy_book(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    Book.destroy({'id':id})
    return redirect('/dashboard')