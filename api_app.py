from flask import Flask, jsonify, request
from datos_dummy import books

app = Flask(__name__)
# app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

# 1.Ruta para obtener todos los libros
@app.route('/api/v0/resources/books/all', methods=['GET']) # La ruta esta se llama "Endpoint"
def get_all():
    # Como hacer un json.dumps:
    return jsonify(books)

# 2.Ruta para obtener un libro concreto mediante su id como parámetro en la llamada
@app.route('/api/v0/resources/book', methods=['GET'])
def book_id():
    results = []
    if 'id' in request.args: # Contiene los argumentos que vienen después del ?
        id = int(request.args['id'])
        for book in books:
            if book['id']==id:
                results.append(book)
        if results == []:
            return "Book not found with the id requested"    
        else:
            return jsonify(results)
    else:
        return "No id field provided"
    


@app.route('/api/v0/resources/rangebooks', methods=['GET'])
def book_id_range():
    results = []
    if ('start' in request.args) & ('end' in request.args):
    
    
        start = int(request.args['start'])
        end = int(request.args['end'])
        
        rango = list(range(start-1, end+1))
        
        for book in books:
            if book['id'] in rango:
                results.append(book)
        if results == []:
            return "Book not found with the id requested"    
        else:
            return jsonify(results)
    else:
        return "No range provided"

# 3.Ruta para obtener un libro concreto mediante su título como parámetro en la llamada de otra forma
# @app.route('/api/v0/resources/book/<string:title>', methods=['GET'])

@app.route('/api/v0/resources/booktitle/<string:title>/', methods=['GET'])
def get_book_title(title):
    results = []

    for book in books:
        if book['title'] == title:
            results.append(book)
    if results == []:
        return "Book not found with the title requested"    
    else:
        return jsonify(results)


# 4.Ruta para obtener un libro concreto mediante su título dentro del cuerpo de la llamada
# @app.route('/api/v1/resources/book', methods=['GET'])



# 5.Ruta para añadir un libro mediante parámetros en la llamada
# @app.route('/api/v1/resources/book/add', methods=['POST'])


# 6.Ruta para añadir un libro de otra forma 1
# @app.route('/api/v1/resources/book/add_parameters', methods=['POST'])


# 7.Ruta para modificar un libro
# @app.route('/api/v1/resources/book/update', methods=['PUT'])


# 8.Ruta para eliminar un libro
# @app.route('/api/v1/resources/book/delete', methods=['DELETE'])


app.run()