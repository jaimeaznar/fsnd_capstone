import os
from werkzeug.datastructures import FileStorage
from io import BytesIO
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import db, setup_db, Company, Product
from forms import *
JWT_TOKEN = os.environ["JWT_TOKEN"]


class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        database_name = 'capstone_test'
        database_path = 'postgresql://jaimeaznar@{}/{}'.format(
            'localhost:5432', database_name)
        self.app = create_app()
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client
        setup_db(self.app, database_path)

        db.session.close()
        db.drop_all()
        db.create_all()

        # mock company
        self.company = Company(
            name='test company',
            city='test city',
            state='test state',
            address='test address',
            phone='12345'
        )
        self.company.insert()

        # mock product
        self.product = Product(
            name='test product',
            image='static/img/tomahawk.jpg',
            description='test description',
            company_id=1
        )
        self.product.insert()

    def tearDown(self):
        pass


#----------------------------------------------------------------------------#
#  Tests
#----------------------------------------------------------------------------#
    # Test index page

    def test_index(self):

        response = self.client().get('/')
        self.assertEqual(response.status_code, 200)

    ################
    # Product
    ################
    # Test products page
    def test_product(self):
        response = self.client().get('/api/products')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test search product by name
    def test_search_product(self):
        print('test_search_product')
        response = self.client().get(
            '/api/products/search',
            query_string=dict(
                search_term='test product'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    # Test search product by name not found

    def test_search_product_not_found(self):
        print('test_search_product_not_found')
        response = self.client().get('/api/products/search',
                                     query_string=dict(search_term='facebook'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    # Test search product by id
    def test_search_products_by_id(self):
        response = self.client().get('/api/products/1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    ################
    # Company
    ################
    # Test products page
    def test_company(self):
        response = self.client().get('/api/companies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test search product by name
    def test_search_company(self):

        response = self.client().get(
            '/api/companies/search',
            query_string=dict(
                search_term='test company'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # Test search company by name not found
    def test_search_company_not_found(self):
        response = self.client().get('/api/company/search',
                                     query_string=dict(search_term='facebook'))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    # Test search company by id
    def test_search_company_by_id(self):
        response = self.client().get('/api/companies/1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    ################
    # Create Company
    ################

    # Create company get form

    def test_form_create_company(self):
        response = self.client().get('/api/companies/create',
                                     headers={'Authorization': 'Bearer ' + JWT_TOKEN})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # Create company post
    def test_create_company(self):
        response = self.client().post(
            '/api/companies/create',
            data=dict(
                name='test name',
                city='test city',
                state='test state',
                address='test address',
                phone='phone'),
            headers={
                'Authorization': 'Bearer ' + JWT_TOKEN})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['company']))

   # Create company post incomplete info
    def test_create_company_with_incomplete_data(self):

        response = self.client().post(
            '/api/companies/create',
            data=dict(
                name='test name',
                city='test city'),
            headers={
                'Authorization': 'Bearer ' + JWT_TOKEN})
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


#     ################
#     # Create Product
#     ################

    # Create product form

    def test_form_create_product(self):
        response = self.client().get('/api/products/create',
                                     headers={'Authorization': 'Bearer ' + JWT_TOKEN})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # Create product post
    def test_create_product(self):
        path_img = 'static/img/tomahawk.jpg'
        with open(path_img, 'rb') as img:

            response = self.client().post(
                '/api/products/create',
                data=dict(
                    name='test name',
                    image=img,
                    description='test description',
                    company=self.company.id,
                ),
                headers={
                    'Authorization': 'Bearer ' + JWT_TOKEN})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['new_product']))

    # ################
    # # Patch Company
    # ################
    #  Patch company get form
    def test_form_patch_company(self):
        # Create company get form
        response = self.client().get('/api/companies/1/edit',
                                     headers={'Authorization': 'Bearer ' + JWT_TOKEN})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # Patch company post
    def test_patch_company(self):
        response = self.client().patch(
            '/api/companies/1/edit',
            data=dict(
                name='patch name',
                city='patch city',
                state='patch state',
                address='patch address',
                phone='patch phone'),
            headers={
                'Authorization': 'Bearer ' + JWT_TOKEN})
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

    # ################
    # # Delete Company
    # ################

    # Delete company
    def test_delete_company(self):
        response = self.client().delete(
            '/api/companies/1/delete',
            headers={
                'Authorization': 'Bearer ' + JWT_TOKEN})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # Delete with invalid id
    def test_delete_company_with_invalid_id(self):
        response = self.client().delete(
            '/api/companies/100/delete',
            headers={
                'Authorization': 'Bearer ' + JWT_TOKEN})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    # Delete without token
    def test_delete_company_without_token(self):
        response = self.client().delete('/api/companies/1/delete')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)


if __name__ == "__main__":
    unittest.main()
