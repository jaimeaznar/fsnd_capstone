#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import os
import json
from flask import Flask, render_template, jsonify, request, abort, Response, flash, redirect, url_for
from flask import current_app
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from werkzeug.utils import secure_filename
from auth import AuthError, requires_auth
from models import *
from forms import *


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def create_app(test_config=None):
    # create and cofigure the app
    database_path = os.environ.get('DATABASE_URL')
    if not database_path:
        database_name = 'capstone'
        database_path = 'postgresql://jaimeaznar@{}/{}'.format('localhost:5432',database_name)
    
    app = Flask(__name__)
    setup_db(app, database_path)
    
    #CORS app
    cors = CORS(app)

    # CORS headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS'
        )

        return response


    #----------------------------------------------------------------------------#
    # Controllers.
    #----------------------------------------------------------------------------#

    @app.route('/')
    def index():
        return render_template('pages/home.html')

    #----------------------------------------------------------------------------#
    # Products.
    #----------------------------------------------------------------------------#

    @app.route('/products', methods=['GET'])
    @app.route('/api/products', methods=['GET'])
    def products():
        error = False
        # we create a product list which we will pass on to the html
        products = []
        # access the db
        try:
            for product in Product.query.all():
                product_dict = {'name':product.name,
                                'image':product.image,
                                'description': product.description
                                }
                products.append(product_dict)
            
        except:
            print('An error occurred. No products to display currently.')
            error = True
        
        if error:
            abort(404)

        else:
            if request.path == '/api/products':
                return jsonify({
                    'success': True,
                    'products': products
                }), 200
            return render_template('pages/products.html', products=products)

    @app.route('/products/search', methods=['GET'])
    @app.route('/api/products/search', methods=['GET'])
    def search_products():
        error = False
        # access database
        try:
            # get search term from request arguments
            search_term = request.args.get('search_term')
            # case insensitive --> ilike
            results = Product.query.filter(Product.name.ilike(f'%{search_term}')).all()

            # response object passed to the view
            response = {
                # get the count to display the number of results
                "count": len(results),
                # save info in a list of dict
                "data": [{
                    "id": p.id,
                    "name": p.name,
                    "description": p.description
                } for p in results]
            } 
            print(f'results:{results}')
            print(f'response:{response}')
            #return render_template('pages/search_products.html',response=response, search_term=search_term)
        
        except:
            print('An error occurred while searching, please try again')
            error = True
        
        if error:
            abort(404)

        else:
            if request.path == '/api/products/search':
                if response['count'] != 0:
                    return jsonify({
                        'success': True,
                        'search_term': search_term,
                        'products': response
                    }), 200
                else:
                    return jsonify({
                        'success': False,
                        'search_term': search_term,
                        'products': response
                    }), 404
            
            return render_template('pages/search_products.html',response=response, search_term=search_term)


    @app.route('/products/<int:product_id>', methods=['GET'])
    @app.route('/api/products/<int:product_id>', methods=['GET'])
    def show_product(product_id):
        error = False
        # access database
        try:
            # get product with product_id = id
            product = Product.query.filter_by(id=product_id).first_or_404()
            # save product infor into a variable to pass the view
            data = {
                'id': product.id,
                'name': product.name,
                'image': product.image,
                'description': product.description

            }
            # return render_template('pages/show_product.html',product=data)
        except:
            flash('Sorry, we couldn\'t show that product')
            error = True
            # return redirect(url_for('index'))
        if error:
            abort(404)

        else:
            if request.path == '/api/products/' + str(product_id):
                return jsonify({
                    'success': True,
                    'data': data,
                }), 200
            return render_template('pages/show_product.html',product=data)
        

    #----------------------------------------------------------------------------#
    # Create products.
    #----------------------------------------------------------------------------#

    @app.route('/products/create', methods=['GET'])
    @app.route('/api/products/create', methods=['GET'])
    @requires_auth('get:product')
    def create_product_form(jwt):
        # create a form object
        form = ProductForm()
        if request.path == '/api/products/create':
            return jsonify({
                'success': True,
            }), 200
        return render_template('forms/new_product.html', form=form)

    # function to check for allowed extensions
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/products/create', methods=['POST'])
    @app.route('/api/products/create', methods=['POST'])
    @requires_auth('post:product')
    def create_product_submission(jwt):
        error = False
        filename = request.files['image'].filename
        print(filename)
        # add to db
        try:
            #print(UPLOAD_FOLDER)
            # create product object with form data
            new_product = Product(
                name = request.form.get('name'),
               # image = app.config['UPLOAD_FOLDER'] + "/" + filename,
                description = request.form.get('description'),
                company_id = request.form.get('company')
            )
            # add to db
            new_product.insert()

        except:
            error = True
            db.session.rollback()
        finally:
            # close session
            db.session.close()
        
        if error:
            print('Product ' + request.form['name'] + 'with image' + request.files['image'].filename + ' was not listed.')
            abort(400)
        
        else:
            # check if the post request has the file part
            if 'image' in request.files:
                
                file = request.files['image']
                # if user does not select file, browser also
                # submit an empty part without filename
                if file.filename == '':
                    print('No selected file')
                    
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # if 'image' not in request.files:
                #     flash('No file part')
                #     return redirect(request.url)
                # file = request.files['image']
                # if file.filename == '':
                #     flash('No selected file')
                #     return redirect(request.url)
                # if file and allowed_file(file.filename):
                #     filename = secure_filename(file.filename)
                #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    

                # since it was successful we can use request.form
            flash('Product ' + request.form['name']  + ' was successfully added!')
            
            if request.path == '/api/products/create':
                
                return jsonify({
                    'success': True,
                    'new_product': {
                        'name': request.form['name'],
                        'image': request.files['image'].filename,
                        'description': request.form['description']
                    },
                }), 200

            return redirect(url_for('index'))
            

    #----------------------------------------------------------------------------#
    # Edit products.
    #----------------------------------------------------------------------------#
    @app.route('/products/<int:product_id>/edit', methods=['GET'])
    @app.route('/api/products/<int:product_id>/edit', methods=['GET'])
    @requires_auth('get:product')
    def edit_product_form(jwt,product_id):
        # get the product we want to modify
        product = Product.query.filter_by(id=product_id).first_or_404()
        # Show info on form
        form = ProductForm(
            name = product.name,
            description = product.description
        )
        if request.path == f'/api/products/{str(produc_id)}/edit':
            return jsonify({
                'success': True,
            }), 200
        return render_template('forms/edit_product.html',product=product,form=form)

    @app.route('/products/<int:product_id>/edit', methods=['PATCH'])
    @app.route('/api/products/<int:product_id>/edit', methods=['PATCH'])
    @requires_auth('patch:product')
    def edit_product_submission(jwt, product_id):
        error = False
        # get product we want to edit
        product = Product.query.filter_by(id=product_id).first_or_404()
        # get old image path
        old_img_path = product.image
        # access db
        try:
            # set the new values
            product.name = request.form.get('name')
            product.description = request.form.get('description')

            if 'image' in request.files:
                file = request.files['image']
                # if user does not select file, browser also
                # submit an empty part without filename
                if file.filename == '':
                    print('No selected file')
                    
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                    product.image = UPLOAD_FOLDER + "/" + request.files['image'].filename
                    os.remove(old_img_path)
                
            # commit changes
            product.update()
            
        except:
            error = True
            db.session.rollback()
            print('Error while editing product. Please try again later.')
        finally:
            db.session.close()
            # return redirect(url_for('show_product',product_id=product_id))

        if error:
            abort(404)
        else:
            if request.path == '/api/products/' + str(product_id) + '/edit':
                return jsonify({
                    'success': True,
                    'product': {
                        'name': product.name,
                        'image': product.image,
                        'description': product.description,
                        'company_id': product.company_id
                    },
                }), 200
            return render_template('pages/show_product.html',product_id=product_id)

    #----------------------------------------------------------------------------#
    # Delete products.
    #----------------------------------------------------------------------------#
    @app.route('/products/<int:product_id>/delete', methods=['DELETE'])
    @app.route('/api/products/<int:product_id>/delete', methods=['DELETE'])
    @requires_auth('delete:product')
    def delete_product(jwt, product_id):
        error = False
        product = Product.query.filter_by(id=product_id).first_or_404()
        
        # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
        try:
            product.delete()
        except:
            error = True
            db.session.rollback()
        finally:
            db.session.close()
        
        if error:
            print(f'An error ocurred when trying to delete the {product.name}. Please try again later.')
            abort(404)
        else:
            # delete image
            if product.image != '':
                os.remove(product.image)
            print(f'Successfully deleted product {product.name}')
            if request.path == '/api/products/' + str(product_id) + '/delete':
                return jsonify({
                    'success': True,
                    'product': {
                        'name': product.name,
                        'image': product.image,
                        'description': product.description,
                        'company_id': product.company_id
                    },
                }), 200

            return redirect(url_for('products'))



    #----------------------------------------------------------------------------#
    # Companies.
    #----------------------------------------------------------------------------#

    @app.route('/companies', methods=['GET'])
    @app.route('/api/companies', methods=['GET'])
    def companies():
        # access database
        companies = [{
            'name': company.name,
            'city': company.city,
            'state': company.state,
            'address': company.address,
            'phone': company.phone
        } for company in Company.query.all()]

        if request.path == '/api/companies':
            return jsonify({
                'success': True,
                'companies': companies,
            }), 200

        return render_template('pages/companies.html',companies=companies)

    @app.route('/companies/search', methods=['GET'])
    @app.route('/api/companies/search', methods=['GET'])
    def search_companies():
        error = False
        # access database
        try:
            # get search term from request arguments
            search_term = request.args.get('search_term')
            # case insensitive --> ilike
            results = Company.query.filter(Company.name.ilike(f'%{search_term}')).all()

            # response object passed to the view
            response = {
                # get the count to display the number of results
                "count": len(results),
                # save info in a list of dict
                "data": [{
                    "id": c.id,
                    "name": c.name,
                    "city": c.city,
                    "state": c.state,
                    "address": c.address,
                    "phone": c.phone
                } for c in results]
            } 
            
            # return render_template('pages/search_companies.html',response=response, search_term=search_term)
        except:
            print('An error occurred while searching, please try again')
            error = True
            # return redirect(url_for('companies'))
        if error:
            abort(404)
        else:
            if request.path == '/api/companies/search':
                if response['count'] != 0:
                    return jsonify({
                        'success': True,
                        'search_term': search_term,
                        'products': response
                    }), 200
                else:
                    return jsonify({
                        'success': False,
                        'search_term': search_term,
                        'products': response
                    }), 404
            return render_template('pages/search_companies.html',response=response, search_term=search_term)
        

    @app.route('/companies/<int:company_id>', methods=['GET'])
    @app.route('/api/companies/<int:company_id>', methods=['GET'])
    def show_company(company_id):
        error = False
        # access database
        try:
            # get product with product_id = id
            company = Company.query.filter_by(id=company_id).first_or_404()
            # save product infor into a variable to pass the view
            data = {
                'id': company.id,
                'name': company.name,
                'city': company.city,
                'state': company.state,
                'address': company.address,
                'phone': company.phone,
            }
            # return render_template('pages/show_company.html', data = data)
        except:
            error = True
            flash('Sorry, we couldn\'t show that product')
        
        if error:
            abort(404)
        else:
            if request.path == '/api/companies/' + str(company_id):
                return jsonify({
                    'success': True,
                    'company': data
                }), 200

            return render_template('pages/show_company.html', data = data)
        


    #----------------------------------------------------------------------------#
    # Create Companies.
    #----------------------------------------------------------------------------#
    @app.route('/companies/create', methods=['GET'])
    @app.route('/api/companies/create', methods=['GET'])
    @requires_auth('get:company')
    def create_company_from(jwt):
        form = CompanyForm()
        if request.path == '/api/companies/create':
            return jsonify({
                'success': True,
            }), 200
        return render_template('forms/new_company.html',form=form)


    @app.route('/companies/create', methods=['POST'])
    @app.route('/api/companies/create', methods=['POST'])
    @requires_auth('post:company')
    def create_company_submission(jwt):
        error = False
        # add to db
        try:
            # create product object with form data        
            new_company = Company(
                name = request.form.get('name'),
                city = request.form.get('city'),
                state = request.form.get('state'),
                address = request.form.get('address'),
                phone = request.form.get('phone')
            )
            # add to db
            new_company.insert()

        except:
            error = True
            db.session.rollback()
            print('Company ' + request.form['name'] + ' was not listed.')
        finally:
            # close session
            db.session.close()
            print('Company ' + request.form['name']  + ' was successfully added!')
        
        if error:
            abort(400)
        else:
            if request.path == '/api/companies/create':
                return jsonify({
                    'success': True,
                    'company':{
                        'name': request.form.get('name'),
                        'city': request.form.get('city'),
                        'state': request.form.get('state'),
                        'address': request.form.get('address'),
                        'phone': request.form.get('phone'),
                    },
                }), 200
            return redirect(url_for('index'))

    #----------------------------------------------------------------------------#
    # Edit Companies.
    #----------------------------------------------------------------------------#

    @app.route('/companies/<int:company_id>/edit', methods=['GET'])
    @app.route('/api/companies/<int:company_id>/edit', methods=['GET'])
    @requires_auth('get:company')
    def edit_company(jwt, company_id):
        # get company based on id
        company = Company.query.filter_by(id=company_id).first_or_404()
        form = CompanyForm(
            name = company.name,
            city = company.city,
            state = company.state,
            address = company.address,
            phone = company.phone
        )
        if request.path == f'/api/companies/{company_id}/edit':
            return jsonify({
                'success':True,
                'company': {
                        'name': company.name,
                        'city': company.city,
                        'state': company.state,
                        'address': company.address,
                        'phone': company.phone
                }
            }), 200
        return render_template('forms/edit_company.html',form=form, company=company)

    @app.route('/companies/<int:company_id>/edit', methods=['PATCH'])
    @app.route('/api/companies/<int:company_id>/edit', methods=['PATCH'])
    @requires_auth('patch:company')
    def edit_company_submission(jwt, company_id):
        error = False
        # get product we want to edit
        company = Company.query.filter_by(id=company_id).first_or_404()
        # access db
        try:
            # set the new values
            company.name = request.form.get('name')
            company.city = request.form.get('city')
            company.state = request.form.get('state')
            company.address = request.form.get('address')
            company.phone = request.form.get('phone')
                
            # commit changes
            company.update()
            
        except:
            error = True
            db.session.rollback()
            print('Error while editing company. Please try again later.')
        finally:
            db.session.close()
            #return redirect(url_for('show_company',company_id=company_id))
        if error:
            abort(400)
        else:
            if request.path == '/api/companies/' + str(company_id) + '/edit':
                return jsonify({
                    'success': True,
                    'company': {
                        'name': request.form.get('name'),
                        'city': request.form.get('city'),
                        'state': request.form.get('state'),
                        'address': request.form.get('address'),
                        'phone': request.form.get('phone')
                    }
                }), 200
            # return redirect(url_for('show_company',company_id=company_id))
            return redirect(url_for('show_company', company_id=company_id))


    #----------------------------------------------------------------------------#
    # Delete Companies.
    #----------------------------------------------------------------------------#
    @app.route('/companies/<int:company_id>/delete', methods=['DELETE'])
    @app.route('/api/companies/<int:company_id>/delete', methods=['DELETE'])
    @requires_auth('delete:company')
    def delete_company(jwt, company_id):
        error = False
        print('getting company')
        company = Company.query.filter_by(id=company_id).first_or_404()
        print(f'company: {company}')
        # get path to all images from company products
        img_paths = [product.image for product in Product.query.filter_by(company_id=company_id)]
        print(img_paths)
        # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
        try:
            print('in the try for delete')
            company.delete()
        except:
            error = True
            db.session.rollback()
        finally:
            db.session.close()
            print(f'Company {company_id} deleted.')
        
        #return redirect(url_for('index'))

        if error:
            print('aborting')
            abort(400)
        else:
            # delete images from the folder
            if img_paths:
                for path in img_paths:
                    if path != '':
                        os.remove(path)

            if request.path == '/api/companies/' + str(company_id) + '/delete':
                return jsonify({
                    'success': True,
                    'id': company_id,
                }), 200
            return redirect(url_for('companies'))   


    #----------------------------------------------------------------------------#
    # Error Handlers.
    #----------------------------------------------------------------------------#

    # @app.errorhandler(404)
    # def not_found_error(error):
    #     return render_template('errors/404.html'), 404

    # @app.errorhandler(500)
    # def server_error(error):
    #     return render_template('errors/500.html'), 500

    @app.errorhandler(400)
    def unauthorized(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "bad request"
        }), 400    

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False, 
            "error": 401,
            "message": "unauthorized"
        }), 401
    
    @app.errorhandler(AuthError)
    def authentification_failure(error):
        return jsonify({
            "success": False
        }), 401

    @app.errorhandler(403)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 403,
            "message": "forbidden"
        }), 403

    @app.errorhandler(404)
    def notfound(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def notfound(error):
        return jsonify({
            "success": False, 
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(500)
    def notfound(error):
        return jsonify({
            "success": False, 
            "error": 500,
            "message": "Internal Server error"
        }), 500


    #----------------------------------------------------------------------------#
    # Launch.
    #----------------------------------------------------------------------------#

    return app

app = create_app()