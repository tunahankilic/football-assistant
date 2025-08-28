from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker



Base = declarative_base()

# Define a simple User model
# This is a basic example; you can expand it with more fields as needed.
# The model represents a table in the database.
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)



engine = create_engine('sqlite:///:memory:') # Using SQLite for simplicity
Base.metadata.create_all(engine)  # Create the table in the database

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Create a new user instance
new_user = User(name='Alice')
session.add(new_user)  # Add the user to the session
session.commit()  # Commit the session to save the user to the database

# Query the user back from the database
queried_user = session.query(User).filter_by(name='Alice').first()
if queried_user:
    print(f"User ID: {queried_user.id}")
    print(f"User found: {queried_user.name}")