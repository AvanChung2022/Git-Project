from app import app
from app.controllers import books, users

if __name__ == '__main__':
    app.run(debug=True)