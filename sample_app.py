"""
Simple app to show Flask functionality.
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Tiber!"

@app.route('/<square_me>')
def square(square_me):
    
    squared = int(square_me)**2
    
    return str(squared)

@app.route('/cube/<cube_me>')
def cube(cube_me):
    
    cubed = int(cube_me)**3
    
    return str(cubed)

if __name__ == '__main__':
    app.run(debug=True)
