from main import db, User,app

# Delete all users  
with app.app_context():  #Create an application context
    db.session.query(User).delete()
    db.session.commit()

print("All users have been deleted.")   #Print message to the console