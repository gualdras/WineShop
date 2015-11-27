#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

import json
from flask import Flask, jsonify, abort, make_response, request, url_for

app = Flask(__name__)
app.config['DEBUG'] = True

'''
wines

{''id'': automatic,
''grade'': float, (Opcional, 12 por defecto)
''size'': int, (Opcional, 75 por defecto)
''varietals'': [],
''do'': bool, // Denominacion de Origen La Mancha (False por defecto)
''price'': float, (Opcional)
''name'': string,
''photo'':path} (Opcional)

---------------------------------------------------
red

{''cask'': int, // Envejecimiento en barrica
''bottle'': int} // Envejecimiento en botella

----------------------------------------------------
client

{''email'': mail, // ID del cliente
''pass'': string,
''carts'': [],
''address'': string,
''phone'': int}

--------------------------------
cart

{''id'': auto,
''name'': string, (Opcional)
''items'': []}
'''

wines = []
clients = []
carts = []

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

@app.errorhandler(409)
def not_found(error):
    return make_response(jsonify({'error': 'Email already in use'}), 409)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad Request'}), 404)

@app.errorhandler(501)
def not_found(error):
    return make_response(jsonify({'error': 'Not Implemented'}), 501)

@app.route('/clients', methods = ['POST', 'GET'])
def manager_clients():
    if request.method == 'GET':
        return getClients()
    if request.method == 'POST':
        return newClient()

def getClients():
    return make_response(jsonify({'clients': clients}), 200)
        
def newClient():
    if not request.json or not all(x in request.json for x in {'email', 'pass', 'carts', 'address', 'phone'}):
        abort(400)
    if request.json in clients:
        abort(409)
    c = request.json
    clients.append(c)
    return make_response(jsonify({'created':c['email']}), 201)

@app.route('/clients/<path:id_client>', methods = ['GET', 'PUT', 'DELETE'])
def manager_client(id_client):
    if request.method == 'GET':
        return getClientDetails(id_client)
    if request.method == 'PUT':
        return updateClient(id_client)
    if request.method == 'DELETE':
        return deleteClient(id_client)

def getClientDetails(id_client):
    c = filter(lambda t:t['email'] == id_client, clients)
    if len(c) == 0:
        abort(404)
    return make_response(jsonify(c[0]), 200)

#TODO cambiar la eliminacion por mera actualizacion
def updateClient(id_client):
	if not request.json:
		abort(400)
        
	c = filter(lambda t:t['email'] == id_client, clients)
    if len(c) == 0:
        abort(404)
	c = c[0]
	clients.remove(c)
	for k in request.json:
		c[k] = request.json[k]
	clients.append(c)
	return make_response(jsonify({'updated':c}), 200)
	
def deleteClient(id_client):
    c = filter(lambda t:t['email'] == id_client, clients)
    if len(c) == 0:
        abort(404)
    clients.remove(c[0])
    return make_response(jsonify({'deleted':id_client}), 200)
        
@app.route('/clients/<path:id_client>/carts', methods = ['POST'])
def manager_clients_carts(id_client):
    if request.method == 'POST':
        return addCart(id_client)

def addCart(id_client):
    if not request.json or not 'items' in request.json:
        abort(400)
    c = filter(lambda t:t['email'] == id_client, clients)
    if len(c) == 0:
        abort(404)
    if(len(carts) > 0):
        id = carts[-1]['id'] + 1
    else:
        id = 0
        
    cart = request.json
    cart['id'] = id
    carts.append(cart)
    c[0]['carts'].append(cart)
    
    return make_response(jsonify({'created':id}), 201)
    
@app.route('/clients/<path:id_client>/carts/<path:id_cart>', methods = ['DELETE'])
def manager_client_cart(id_client, id_cart):
    if request.method == 'DELETE':
        return deleteCart(id_client, int(id_cart))
    
def deleteCart(id_client, id_cart):
    c = filter(lambda t:t['email'] == id_client, clients)
    if len(c) == 0:
        abort(404)
    cartsClientList = c[0]['carts']
    myCart = filter(lambda t:t['id'] == id_cart, cartsClientList)
    
    if len(myCart) == 0:
        abort(404)
        
    cartsClientList.remove(myCart[0])
    
    return make_response(jsonify({'deleted':myCart[0]['id']}), 200)
    

@app.route('/clients/<path:id_client>/carts/<path:id_cart>/items', methods = ['PUT', 'GET'])
def manager_client_cart_items(id_client, id_cart):
    if request.method == 'GET':
        return getItems(id_client, id_cart)
    
def getItems(id_client, id_cart):
    client = filter(lambda t:t['email'] == id_client, clients)
    if len(client) == 0:
        abort(404)


    cartsClientList = c[0]['carts']
    myCart = filter(lambda t:t['id'] == id_cart, cartsClientList)
    if len(myCart) == 0:
        abort(404)
    
    return make_response(jsonify({myCart['items']}), 200)
        
    
    

@app.route('/clients/<path:id_client>/carts/<path:id_cart>/items/<path:id_item>', methods = ['POST', 'PUT', 'DELETE'])
def manager_client_cart_item(id_item):
    if request.method == 'POST':
        return addItem(id_item)
    if request.method == 'PUT':
        return updateItem(id_cart)
    if request.method == 'DELETE':
        return deleteItem(id_item)

def addItem(id_client, id_cart, id_item):
    client = filter(lambda t:t['email'] == id_client, clients)
    if len(client) == 0:
        abort(404)


    cartsClientList = c[0]['carts']
    myCart = filter(lambda t:t['id'] == id_cart, cartsClientList)
    if len(myCart) == 0:
        abort(404)    
    
    if not id_item in wines:
        abort(404)
        
    myCart['items'].append(dict.copy(wines[id_item]))
    
    return make_response(jsonify({'updated': myCart['id']}))
    
def updateItem(id_client, id_cart, id_item):
    client = filter(lambda t:t['email'] == id_client, clients)
    if len(client) == 0:
        abort(404)


    cartsClientList = c[0]['carts']
    myCart = filter(lambda t:t['id'] == id_cart, cartsClientList)
    if len(myCart) == 0:
        abort(404)
        
    item = filter(lambda t:t['id'] == id_item, myCart[0])
    
    if len(item) == 0:
        abort(404)
        
    item = item[0]
    for k in request.json:
        item[k] = request.json[k]
    return make_response(jsonify({'updated':item}), 200)
    
    
def deleteItem(id_client, id_cart, id_item):
    client = filter(lambda t:t['email'] == id_client, clients)
    if len(client) == 0:
        abort(404)


    cartsClientList = c[0]['carts']
    myCart = filter(lambda t:t['id'] == id_cart, cartsClientList)
    if len(myCart) == 0:
        abort(404)
        
    item = filter(lambda t:t['id'] == id_item, myCart[0])
    
    if len(item) == 0:
        abort(404)
    
    myCart.remove(item[0])
    
    return make_response(jsonify({'deleted':item[0]['id']}), 200)
    
    
    
    
@app.route('/wines', methods = ['POST', 'GET', 'DELETE'])
def manager_wines():  
    if request.method == 'POST':
        return addWine()
    if request.method == 'GET':
        if 'type' in request.json:
            return wineByType()
        return getWines()
    if request.method == 'DELETE':
        return deleteWines()

def addWine():
    if not request.json or not all(x in request.json for x in {'varietals', 'name'}):
        abort(400)
    
    w = request.json
    if(not 'do' in request.json):
        w['do'] = False
        
    if(len(wines) > 0):
        id = wines[-1]['id'] + 1
    else:
        id = 0
    
    w['id'] = id
     
    wines.append(w)
    
    return make_response(jsonify({'created':w['id']}), 201)

def getWines():
    return make_response(jsonify({'wines': wines}), 200)

def wineByType():
    abort(501)
    
def deleteWines():
    wines = []
    return make_response(jsonify({'deleted':[]}), 200)

@app.route('/wines/<path:id_wine>', methods = ['PUT', 'GET', 'DELETE'])
def manager_whine(id_wine):  
    if request.method == 'PUT':
        return updateWine(int(id_wine))
    if request.method == 'GET':
        return getWineProperties(int(id_wine))
    if request.method == 'DELETE':
        return deleteWine(int(id_wine))
    
def updateWine(id_wine):
    if not request.json:
        abort(400)
        
    w = filter(lambda t:t['id'] == id_wine, wines)
    if len(w) == 0:
        abort(404)
        
    
    w = w[0]
    for k in request.json:
        w[k] = request.json[k]
    i
    return make_response(jsonify({'updated': w}), 200)
    
def getWineProperties(id_wine):
    if not request.json:
        abort(400)
        
    w = filter(lambda t:t['id'] == id_wine, wines)
    if len(w) == 0:
        abort(404)
        
    return make_response(jsonify({'wine': w[0]}), 200)

def deleteWine(id_wine):
    w = filter(lambda t:t['id'] == id_wine, wines)
    if len(w) == 0:
        abort(404)
        
    wines.remove(w[0])
    
    return make_response(jsonify({'deleted': w[0]['id']}))

class Client:
    def __init__(self, request):
        self.mail = request.json['email']
        self.password = request.json['pass']
        self.carts = request.json['carts']
        self.address = request.json['address']
        self.phone = request.json['phone']
    '''    
    def __init__(self, email, pass, carts, address, phone):
        self.mail = email
        self.password = pass
        self.carts = carts
        self.address = address
        self.phone = phone
    '''    
class Cart:
    def __init__(self, name = None, items = []):
        self.name = name
        self.items = items
        
class Wine:
    def __init__(self, id, name, grade = 12, size = 75, varietals = [], do = False, price = None, photo = None):
        self.id = id
        self.grade = grade
        self.size = size
        self.varietals = varietals
        self.do = do
        self.price = price
        self.name = name
        self.photo = photo

class redWine(Wine):
    def __init__(self, cask, bottle, id, name, grade = 12, size = 75, varietals = [], do = False, price = None, photo = None):
        Wine.__init__(self, id, name, grade, size, varietals, do, price, photo)
        self.cask = cask
        self.bottle = bottle
        
    
if __name__ == '__main__':
    app.run(debug=True)
