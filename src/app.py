from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

#requerimos pymongo


app = Flask(__name__)
#Configuracion de mongodb
app.config['MONGO_URI']='mongodb://localhost/pythonreactdb'

mongo =PyMongo(app)

db = mongo.db.users



@app.route('/users', methods=['POST'])
def createUser():
  print(request.json)
  id = db.insert({
    'name': request.json['name'],
    'email': request.json['email'],
    'password': request.json['password']
  })
  #print(str(ObjectId(id)))
  #vamos a retornar el id atraves jsonify

  return jsonify(str(ObjectId(id)))

@app.route('/users', methods=['GET'])
def getUsers():
    #Creamos una lista vacia users
    users=[]
    #Por cada documento en la respuesta db.find
    for doc in db.find():
        #Vamos añadir los objetos a la lista 
        users.append({
            #La conversion del id a un string 
            #obtenemos el id en string
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'email': doc['email'],
            'password': doc['password']
        })

    return jsonify(users)

@app.route('/user/<id>', methods=['GET'])
def getUser(id):
    #vamos abuscar el dato y lo guardamos en la variable user
    user = db.find_one({'_id': ObjectId(id)})

    return jsonify({
        #Se va a convertir el id a string
        '_id': str(ObjectId(user['_id'])),
        'name': user['name'],
            'email': user['email'],
            'password': user['password']
            #Pendiente min 25:41

    })

@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    #Realizamos una consulta
    db.delete_one({'_id': ObjectId(id)})
    print(id)
    return jsonify({'msg': 'Usuario eliminado'})

@app.route('/users/<id>', methods=['PUT'])
def updateUser():
    return 'Hola bb'


if __name__ =='__main__':
    app.run(debug=True)
