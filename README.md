

# Introduction

The goal of this project is to provide a product Catalogue website in which a company can showcase their products

The project is written with django 4.0.1 and python 3.8 in mind.


### Main features

* Admin Panal

* Custom Login and Registraion

* ability to add products to an Order list which can be viewed by an Admin

      
    


# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone git@github.com/USERNAME/{{ project_name }}.git
    $ cd {{ project_name }}
    
First Install virtualenv 

    $ pip3 -m venv path/to/venv
    
Activate the virtualenv for your project.

    $ source venv/bin/activate
    
Install project dependencies:

    $ pip install -r requirements/local.txt
    
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver