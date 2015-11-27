from wineFlask import app
from hamcrest import *

import os
import json
import unittest
import tempfile


class ClientsTestCase(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)
        app.config['TESTING'] =True

    def tearDown(self):
        del self.tester
        
    def addClient(self):
        response = self.tester.post('/clients', content_type='application/json', 
                                data = json.dumps({'email':'example@example.com', 'pass':'password', 'carts':[], 'address':'Pilar Square', 'phone':'654321098'}))
        return json.loads(response.data)['created']
    
    def deleteClient(self, id_client):
        self.tester.delete('/clients/' + id_client, content_type='application/json')
        
    def addCart(self, id_client):
        response = self.tester.post('/clients/' + id_client + '/carts', content_type='application/json', data=json.dumps({'items':[]}))
        return json.loads(response.data)['created']
    
    def deleteCart(self, id_client, id_cart):
        self.tester.delete('/clients/' + id_client + '/carts/' + str(id_cart), content_type='application/json')
        
    
    def test_POST_Client(self):
        response = self.tester.post('/clients', content_type='application/json', 
                                data = json.dumps({'email':'example@example.com', 'pass':'password', 'carts':[], 'address':'Pilar Square', 'phone':'654321098'}))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data), {'created':'example@example.com'})
        
        self.deleteClient(json.loads(response.data)['created'])

    
    def test_GET_Empty_Client(self):
        response = self.tester.get('/clients', content_type='application/json')
        self.assertEqual(json.loads(response.data), {'clients':[]})
        self.assertEqual(response.status_code, 200)
        
    def test_GET_Client(self):
        id_client = self.addClient()
        response = self.tester.get('/clients', content_type='application/json')
        
        assert_that(response.data, contains_string(id_client))
        self.assertEqual(response.status_code, 200)
        
        self.deleteClient(id_client)
            
    def test_GET_ClientDetails(self):
        id_client = self.addClient()
        response = self.tester.get('/clients/' + id_client, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'email':id_client, 'pass':'password', 'carts':[], 'address':'Pilar Square', 'phone':'654321098'})
        
        self.deleteClient(id_client)

    def test_deleteClient(self):
        id_client = self.addClient()
        response = self.tester.delete('/clients/' + id_client, content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'deleted':id_client})
        
    def test_updateClient(self):
        id_client = self.addClient()
        response = self.tester.put('/clients/' + id_client, content_type='application/json', data=json.dumps({'email':'example@example.com', 'pass':'newpass', 'carts':[], 'address':'Honolulu', 'phone':'123456789'}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'updated':{'email':'example@example.com', 'pass':'newpass', 'carts':[], 'address':'Honolulu', 'phone':'123456789'}})
        
        self.deleteClient(id_client)
        
    #TODO test with name value. 
    def test_addCart(self):
        id_client = self.addClient()
        response = self.tester.post('/clients/' + id_client + '/carts', content_type='application/json', data=json.dumps({'items':[]}))

        self.assertEqual(response.status_code, 201)
        
        self.deleteCart(id_client, json.loads(response.data)['created'])
        self.deleteClient(id_client)
      
    def test_deleteCart(self):
        id_client = self.addClient();
        
        id_cart = self.addCart(id_client)
        
        response = self.tester.delete('/clients/' + id_client + '/carts/' + str(id_cart), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        self.deleteClient(id_client)
        
    
    def test_getItems(self):
        id_client = self.addClient()
        id_cart = self.addCart(id_client)

        response = self.tester.getItems('/clients/' + id_client + '/carts/' + str(id_cart + '/items'), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        self.deleteCart(id_client, id_cart)
        self.deleteClient(id_client)
    
    '''
    def addItem(self):
        id_client = self.addClient()
        id_cart = self.addCart(id_client)

        response = self.tester.getItems('/clients/' + id_client + '/carts/' + str(id_cart + '/items/'), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        self.deleteCart(id_client, id_cart)
        self.deleteClient(id_client)
        
        
    def updateItem(self):
    
    def deleteItem(self);
    
    '''    
    
    
    
if __name__ == '__main__':
    unittest.main()