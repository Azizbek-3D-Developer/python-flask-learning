# imports
from flask import Flask, render_template, url_for, request, redirect # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore


# Main Variables
application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact_organizer.db' # database name 
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
contacts_database = SQLAlchemy(application)

# Model
class Contacts(contacts_database.Model):
    id = contacts_database.Column(contacts_database.Integer, primary_key = True)
    contact_name = contacts_database.Column(contacts_database.String(100), nullable = False )
    contact_number = contacts_database.Column(contacts_database.String(20), nullable = False)
    
    def __repr__(self):
        return 'Contacts %r' % self.id
    

# Finance calculator

# Routes
# local-server/
@application.route('/') # index page / Landing page
@application.route('/home')
@application.route('/index')
def LandingPage():
    return render_template("index.html")


# local-server/about
@application.route('/about') # About page 
def AboutPage():
    return render_template("about.html")


@application.route('/create-contact', methods=['POST', 'GET'])
def create_contact_page():
    if request.method == "POST":
        name = request.form['user-name']
        telephone = request.form['user-phone']
        
        error = validate_contact(name, telephone)
        if error:
            return render_template('create-contact.html', error=error)
        
        newContact = Contacts(contact_name = name, contact_number = telephone)
        try:
            contacts_database.session.add(newContact)
            contacts_database.session.commit()  
            return redirect('/contacts')
        except:
            return render_template('error-404.html')
    else:
        return render_template("create-contact.html")


@application.route('/contacts')
def get_all_contacts():
    
    contacts_list = Contacts.query.order_by(Contacts.contact_name.asc()).all()
    return render_template('get-all-contacts.html', contacts_list = contacts_list)


@application.route('/contacts/<int:user_id>/edit', methods=['POST', 'GET'])
def edit_contact(user_id):
    contact = Contacts.query.get_or_404(user_id)
    
    if request.method == "POST":
        contact.contact_name = request.form['user-name']
        contact.contact_number = request.form['user-phone']
        
        error = validate_contact(contact.contact_name, contact.contact_number)
        if error:
            return render_template('create-contact.html', error=error)

        
        try:
            contacts_database.session.commit()
            return redirect(url_for('get_all_contacts')) 
        except:
            return render_template('error-404.html')
    else:
        return render_template("update-contact.html", contact=contact)


@application.route('/contacts/<int:id>/delete')
def delete_contact(id):
    contact = Contacts.query.get_or_404(id)
    
    try:
        contacts_database.session.delete(contact)
        contacts_database.session.commit()
        return redirect(url_for('get_all_contacts'))
    except:
        return render_template('error-404.html')
    

# @application.route('/error-404')
# def Error_404_page():
#      return render_template('error-404.html')


def validate_contact(name, phone):
    if not name or not phone:
        return "All fields are required."
    if not phone.isdigit() or not (10 <= len(phone) <= 20):
        return "Phone number must be 10-20 digits."
    return None



@application.errorhandler(404)
def page_not_found(e):
    return render_template('error-404.html'), 404


# Runing the Project
if __name__ == "__main__":
    application.run(debug=True) # runing the local server for Development
    # application.run(debug=False) # After production
    
    
# Runing instruction
# cd Contact
# venv/Scripts/activate
# python main.py