import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import  setup_db, Company, Product
from forms import *
jwt_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InQ3N2JJcTR6OUtwcVQ1QXYyaWlZdCJ9.eyJpc3MiOiJodHRwczovL2phaWF6bi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyMDZjMGM2ODAzM2YwMDNkNWRjMjdhIiwiYXVkIjoiY2Fwc3RvbmVfYXBpIiwiaWF0IjoxNjA4OTg1MDM5LCJleHAiOjE2MDkwNzE0MzksImF6cCI6ImlLMVpXeG95SmlPTG1CdHlkNXU0WVhtdHR4S08yTGNSIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y29tcGFueSIsImRlbGV0ZTpwcm9kdWN0IiwiZ2V0OmNvbXBhbnkiLCJnZXQ6cHJvZHVjdCIsInBhdGNoOmNvbXBhbnkiLCJwYXRjaDpwcm9kdWN0IiwicG9zdDpjb21wYW55IiwicG9zdDpwcm9kdWN0Il19.ShaA-FnFTYggYI1fFiUQOAlhJVKWBijbrGvtyN1V8DYstCFaquTj7TSWb_L4t82n-9k9DR0b_BIcq6ATBGpSr7J7_FoLafVjAhDX8w1SzY6aerG_L9l-DjihuneijnOJ2owr5Y7gBrTiNVU1DvCF5WXQ6LTutopgWHISx4B_Gq8-Isx_6OuoALP7yPOZjkgm49jiVEawq47rBAD3XMvXkfpQsInzlDZlaPqeQ8eelTt2fFe87MvOv9dC47KFxTpMjfVkRbs9e8oQVuxF0SerROLG3WPgOGfttwfVvcYPQIIqlXtYttkj7UUSmA_UBkFoQ15FLYZMh-NPiotkfByB5Q'

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

    ################
    # Create Company
    ################ 
    # Create company get form
    def test_form_create_company(self):
        response = self.client().get('/api/companies/create')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # Create company post
    def test_create_company(self):
        new_company={
            'name': 'Test name',
            'city': 'Test city',
            'state': 'Test state',
            'address': 'Test address',
            'phone': 'Test phone'
            }
        response = self.client().post('/api/companies/create', data=json.dumps(new_company), 
        headers={
            'Content-type': 'application/json',
            'Authorization': 'Bearer ' + jwt_token,
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['company']))
   

if __name__ == "__main__":
    unittest.main()