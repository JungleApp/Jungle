#     __             _
#  __|  |_ _ ___ ___| |___
# |  |  | | |   | . | | -_|
# |_____|___|_|_|_  |_|___|
#              |___|
#
# App-Backend
# Last Revision: 11/26/16

# ip: 138.197.4.56

from flask import Flask, request, session, g, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# The following URI is incorrect-- the password has been omitted for security reasons
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/jungle'
db = SQLAlchemy(app)

# Setup our error logging
if app.debug is not True:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('errors.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

@app.route('/')
def index():
    return '''
    <h1>Jungle</h1>
    <br/>
    <h4>Wow. What an exciting application!</h4>
    '''

@app.errorhandler(404)
def four_oh_four(url):
    return '''
    <h1 style="color:red;">
    Whoops! Looks like you've entered an invalid url.
    </h1>
    '''

if __name__ == '__main__':
    app.run(debug=True)