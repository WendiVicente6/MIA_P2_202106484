from flask import Flask, jsonify, request
from flask_cors import CORS
import time
from readData import readData
from Analyzer.Analyzer import Commands

app = Flask(__name__)
CORS(app)

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json()
    entry_value = data.get('command','')
    response = readData(entry_value)
    words = entry_value.split()
    if words:
        entry_value = f'[Success] => comando {words[0]} ejecutado exitosamente'
    else:
        entry_value = "No se encontraron palabras en el mensaje."

    respuesta = {
        'estado': 'OK',
        'mensaje': entry_value,
    }
    return jsonify( respuesta)

if __name__ == '__main__':
    app.run(debug=True)
