from main import application, contacts_database

with application.app_context():
    contacts_database.create_all()
    print("✅ Database and tables created successfully.")
