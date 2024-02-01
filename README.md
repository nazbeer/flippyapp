# FlippyApp API
Flippy App is a simple web application that demonstrates the use of Django, Django Rest Framework, and MongoDB to manage products, addresses, order items, and orders. The application provides a set of APIs to interact with the data and a user interface to display the available APIs.

# Prerequisites
-------------

1.  Python 3.x
2.  Django 4.x
3.  Django Rest Framework 3.x
4.  MongoDB
5.  pymongo 3.x

# Setup
-----

1.  Clone the repository: git clone <https://github.com/your_username/flippy_app.git> cd flippy_app
2.  Create a virtual environment and activate it:

`python -m venv venv 2source venv/bin/activate` 
On Windows, use `venv\Scripts\activate`

1.  Install the dependencies:

`pip install -r requirements.txt`

1.  Create a `.env` file in the project root directory and add the following:

`MONGO_URL=mongodb://username:password@localhost:27017/flippy_db`
`SECRET_KEY=your_secret_key`

Replace `username`, `password`, and `your_secret_key` with your own values.

1.  Run the migrations:

`python manage.py migrate`

1.  Start the development server:

`python manage.py runserver`

1.  Access the application at <http://127.0.0.1:8000/>

# APIs
----

The following APIs are available:

1.  Home

    -   URL: <http://127.0.0.1:8000/>
    -   Method: GET
    -   Description: Displays the list of available APIs
2.  List Products

    -   URL: <http://127.0.0.1:8000/list-products/>
    -   Method: GET
    -   Description: Retrieves the list of products
3.  Create Order

    -   URL: <http://127.0.0.1:8000/order-create/>
    -   Method: POST
    -   Description: Displays the order creation form
4.  Create Address

    -   URL: <http://127.0.0.1:8000/address-list-create/>
    -   Method: GET
    -   Description: Displays the address list and creation form
5.  Create Order Item

    -   URL: <http://127.0.0.1:8000/order-item-list-create/>
    -   Method: GET
    -   Description: Displays the order item list and creation form
6.  Create Order with Address

    -   URL: <http://127.0.0.1:8000/order-with-address-list/>
    -   Method: GET
    -   Description: Displays the order with address list
7.  Add New Product

    -   URL: <http://127.0.0.1:8000/add-new-product/>
    -   Method: POST
    -   Description: Displays the form to add a new product

# Technologies Used
-----------------

1.  Django
2.  Django Rest Framework
3.  MongoDB
4.  pymongo
5.  Bootstrap 4

# License
-------

This project is licensed under the MIT License - see the LICENSE.md file for details.

# Acknowledgments
---------------

-   Django: <https://www.djangoproject.com/>
-   Django Rest Framework: <https://www.django-rest-framework.org/>
-   MongoDB: <https://www.mongodb.com/>
-   pymongo: <https://pymongo.readthedocs.io/en/stable/>
-   Bootstrap: <https://getbootstrap.com/>
  
