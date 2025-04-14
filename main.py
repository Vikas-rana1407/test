#imports
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import IntegrityError 

#create database
engine = create_engine("postgresql://postgres:Apple%40123@localhost/test_db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Define the models
class User (Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name  = Column(String, nullable=False)
    email  = Column(String, unique=True)

    tasks = relationship("Task",back_populates="user", cascade="all, delete-orphan")

class Task (Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title  = Column(String, nullable=False)
    description  = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="tasks")

Base.metadata.create_all(engine)


#utility functions
def get_user_by_email(email):
    """Get user by email"""
    user = session.query(User).filter_by(email=email).first()
    return user

def confirm_action(prompt:str)->bool:
    """Confirm action"""
    return input(f"{prompt} (y/n): ").strip().lower() == "y"

#CRUD Ops

def add_user(): 
    """Add user"""
    name = input("Enter name: ")
    email = input("Enter email: ")

    if get_user_by_email(email):
        print("User already exists")
        return
    
    try:
        session.add(User(name=name, email=email))
        session.commit()
        print("User added successfully")
    except IntegrityError:
        session.rollback()
        print("User already exists")
   
def add_task():

    """Add task"""
    email = input("Enter user email: ")
    user = get_user_by_email(email)
    if not user:
        print("User not found")
        return
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    session.add(Task(title=title, description=description))
    session.commit()
    print(f"Task added successfully : {title}: {description}")

#Query 
    

#main ops
def main()->None:
    """Main function"""
    actions = {
        "1": add_user,
        "2": add_task,
    }
    while True:
        print("\nOptions:\n1. Add user\n2. Add task\n3. Query Usesr\n4. Query Task\n5. Update User\n6. Delete User\n7. Delete Task\n8. Exit")
        choice = input("Enter your choice: ")
        if choice == "8":
            print("Exiting...")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()

print(("hello"))