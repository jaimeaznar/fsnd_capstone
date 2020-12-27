import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import  setup_db, Company, Product
from forms import *
jwt_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InQ3N2JJcTR6OUtwcVQ1QXYyaWlZdCJ9.eyJpc3MiOiJodHRwczovL2phaWF6bi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyMDZjMGM2ODAzM2YwMDNkNWRjMjdhIiwiYXVkIjoiY2Fwc3RvbmVfYXBpIiwiaWF0IjoxNjA5MDc1NzY1LCJleHAiOjE2MDkxNjIxNjUsImF6cCI6ImlLMVpXeG95SmlPTG1CdHlkNXU0WVhtdHR4S08yTGNSIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y29tcGFueSIsImRlbGV0ZTpwcm9kdWN0IiwiZ2V0OmNvbXBhbnkiLCJnZXQ6cHJvZHVjdCIsInBhdGNoOmNvbXBhbnkiLCJwYXRjaDpwcm9kdWN0IiwicG9zdDpjb21wYW55IiwicG9zdDpwcm9kdWN0Il19.pIQLSj2ceXD_2L9Jvg0KK7gq7kQOhK2gngQ63Bh-T74dRfJ3afhXfiXoHscEKuIzjnUlrCuKFhsUMj3s4xdi9pSWjCRe5bLHo_4727vPKUtxAD72TOUJGssSjg0G_xzmjEfecY5hAfhUJLHYZURfHql3jZFY9CYTEcg73oMiNaGlw4PpXgeKlLWXpLFpx2FiX2EGL71-O_Dvgz7hseF8TkdjCUQPdh09HRnhPckvlQLKppBh66iJMB8JTyRrcAe03D_4anX_y1eOAz8MSWZHg-JMoskdBx0Ab0F1omfBXY5YfjPvOGDPCBr9KBTFb9YfTyjxi-YLFQPQBI6yCLZnPQ'

class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client
        setup_db(self.app)
        
    
    def tearDown(self):
        pass
        
#----------------------------------------------------------------------------#
#  Tests
#----------------------------------------------------------------------------#
    
   
        
    
    
    
    # Test index page
    def test_index(self):
        response = self.client().get('/')
        self.assertEqual(response.status_code, 200)
    
    # Test products page
    def test_product(self):
        response = self.client().get('/api/products')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['products']))
    
    # Test search product by name
    def test_search_product(self):
        search_term = {
            'search_term': 'test name',
        }

        response = self.client().get('/api/products/search',
                            data=search_term)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    # Test search company by name
    def test_search_company_not_found(self):
        response = self.client().get('/api/company/search',
                            data=dict(search_term='facebook'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
            
     # Test search for company by id
    def test_search_company_by_id(self):
        response = self.client().get('/api/companies/37')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    ################
    # Create Company
    ################ 
    # Create company get form
    def test_form_create_company(self):
        response = self.client().get('/api/companies/create',
                                        headers={
                                            'Authorization': 'Bearer ' + jwt_token}
                                    )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # Create company post
    def test_create_company(self):
        response = self.client().post('/api/companies/create', 
                                        data=dict(
                                            name='test name', 
                                            city='test city',
                                            state='test state',
                                            address='test address',
                                            phone='phone'),
                                        headers={
                                            'Authorization': 'Bearer ' + jwt_token
                                            })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['company']))
   
   # Create company post incomplete info
    def test_create_company_with_incomplete_data(self):
        
        response = self.client().post('/api/companies/create', 
                                        data=dict(
                                            name='test name', 
                                            city='test city'
                                        ),
                                        headers={
                                            'Authorization': 'Bearer ' + jwt_token
                                            })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    # Create company post without token
    def test_create_company_without_token(self):
        response = self.client().post('/api/companies/create', 
                                        data=dict(
                                            name='test name', 
                                            city='test city',
                                            state='test state',
                                            address='test address',
                                            phone='phone')
                                    )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    ################
    # Patch Company
    ################ 
    # Patch company get form
    def test_form_patch_company(self):
        # Create company get form
        response = self.client().get('/api/companies/1/edit',
                                        headers={
                                            'Authorization': 'Bearer ' + jwt_token}
                                    )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # Patch company post
    def test_patch_company(self):
        response = self.client().patch('/api/companies/1/edit',
                                        data=dict(
                                            name='patch name', 
                                            city='patch city',
                                            state='patch state',
                                            address='patch address',
                                            phone='patch phone'),
                                        headers={
                                            'Authorization': 'Bearer ' + jwt_token
                                            })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # Patch company without token
    def test_patch_company_without_token(self):
        response = self.client().patch('/api/companies/1/edit',
                                        data=dict(
                                            name='patch name', 
                                            city='patch city',
                                            state='patch state',
                                            address='patch address',
                                            phone='patch phone')
                                        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)

    ################
    # Delete Company
    ################
    
    # Delete company 
    def test_delete_company(self):
        response = self.client().delete('/api/companies/1/delete',
                                        headers={
                                            'Authorization': 'Bearer ' + jwt_token
                                        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    # Delete with invalid id
    def test_delete_company_with_invalid_id(self):
        response = self.client().delete('/api/companies/100/delete',
                                        headers={
                                            'Authorization': 'Bearer ' + jwt_token
                                        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    # Delete without token
    def test_delete_company_without_token(self):
        response = self.client().delete('/api/companies/1/delete')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'],False)
    


if __name__ == "__main__":
    unittest.main()