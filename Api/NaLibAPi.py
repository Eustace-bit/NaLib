from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
# from peewee import BooleanField, DateTimeField
from psycopg2 import OperationalError
from pydantic import BaseModel, ValidationError
from typing import List, Optional
from pymongo import MongoClient
from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, create_engine, Column, String, func
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
import jwt
from datetime import date, datetime, timedelta
import uuid
from passlib.context import CryptContext
import uvicorn
import os
from fastapi.staticfiles import StaticFiles
from mongoengine import Document, StringField, connect, ReferenceField, DateTimeField, BooleanField, IntField, ListField
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.orm import relationship



app = FastAPI()

# Serve static files (frontend)
app.mount("/WebApplication", StaticFiles(directory="../WebApplication"), name="../WebApplication")
# Secret key and algorithm for JWT
# SECRET_KEY = str(uuid.uuid4())  # Replace with a strong, random secret key
SECRET_KEY = os.getenv("SECRET_KEY", "secret")  # Ensure this is consistent
ALGORITHM = "HS256"  # HMAC SHA-256 algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database setup
# SQLALCHEMY_DATABASE_URL = "sqlite:///./library.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
DATABASE_URL = "postgresql://angledimensions:NaLibrary1234@localhost:5432/nalibrarydatabase"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# mongodb connect
connect("angledimensions")

# client = MongoClient('mongodb://localhost:27017/')
# dbname = client['angledimensions']  # Replace 'library_db' with your database name
# collection = dbname['libraryresources'] 

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
# Drop the existing table
# MongoDB setup

# Define the User model
class User(Base):
    __tablename__ = "users"
    userId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    fullname = Column(String(225), nullable=True)
    password = Column(String)
    email = Column(String, nullable=True)
    role = Column(String, nullable=True)
    qualification = Column(String, nullable=True)
    experience = Column(String, nullable=True)
    skillSet = Column(String, nullable=True)
    grade = Column(String, nullable=True)
    contact = Column(String, nullable=True)
    responsibilities = Column(String, nullable=True)

class Member(Base):
    __tablename__ = "members"
    memberId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fullname = Column(String, nullable=False)
    membershipID = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    postCode = Column(String, nullable=False)
    memberstatus = Column(String, nullable=False, default="Active")
    dateEnrolled = Column(DateTime, default=datetime.utcnow)
    
    


class LendingBehavior(Base):
    __tablename__ = "lendingbehavior"
    behaviorID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    membershipID = Column(String, ForeignKey("members.membershipID"), nullable=False)
    overdueCount = Column(Integer, default=0)
    preference = Column(String)  # Store preferences as a comma-separated string or use JSON

    # Define a relationship to the Member model
    member = relationship("Member", back_populates="lending_behaviors")

# Add a relationship in the Member model
Member.lending_behaviors = relationship("LendingBehavior", back_populates="member")


class BorrowingHistory(Document):
    historyId = StringField(primary_key=True)  # Use `primary_key=True` for the `_id` field
    borrowId = ReferenceField('BorrowBookData', required=True)  # Use `ReferenceField` to reference another document
    borrowedDate = DateTimeField(required=True)
    returnDate = DateTimeField(required=True)
    actualReturnDate = DateTimeField()  # Optional field
    isOverdue = BooleanField(required=True, default=False)  # Default value set to False

    meta = {
        'collection': 'borrowing_history'  # Optional: Specify the collection name
    }


class Library(Document):
    resourceId = StringField(required=True, unique=True)  # Unique identifier
    title = StringField(required=True)
    author = StringField(required=True)
    genre = StringField(required=True)
    publishedDate = StringField(required=True)
    resourceType = StringField(required=True)
    catalogedBy = StringField(required=True)  # Fixed typo
    format = StringField(required=True)

    meta = {
        'collection': 'libraryresources',  # MongoDB collection name
        'indexes': [
            'resourceId',  # Index on resourceId for faster queries
            'title',       # Index on title for faster queries
        ]
    }

class BorrowBookData(Document):
    borrowId = StringField(unique=True, required=True)
    resource = StringField(required=True)
    member = StringField(required=True)
    issuedBy = StringField(required=True)
    borrowedDate = StringField()
    issuedDate = StringField()
    status = BooleanField(required=True)
    returnDate = StringField()
    actualReturnDate = StringField()
    status = BooleanField(default=True)

    meta = {
        'collection': 'borrowedbooks'  # MongoDB collection name
    }

class ReturnBookData(Document):
    returnId = StringField(primary_key=True, required=True)
    resource = StringField(required=True)
    member = StringField(required=True)
    returnedBy = StringField(required=True)
    status = StringField(required=True)
    returnedDate = StringField()
    actualReturnDate = StringField()
    isOverdue = BooleanField(required=True, default=False)

    meta = {
        'collection': 'returnedbooks'  # MongoDB collection name
    }

# Pydantic models
class UserBase(BaseModel):
    username: str
    role: str
    

class RegisterUser(BaseModel):
    username: str
    password: str
    role: str
    email: Optional[str] = None
    fullname: Optional[str] = None
    qualification: Optional[str] = None
    experience: Optional[str] = None
    skillSet: Optional[str] = None
    grade: Optional[str] = None
    contact: Optional[str] = None

    
class AddMember(BaseModel):
    fullname: str
    membershipID: str
    memberstatus: str
    phone: str
    address: str
    postCode: str

class LendingBehaviorBase(BaseModel):
    membershipID: int
    overdueCount: int
    preference: str

class BorrowingHistoryBase(BaseModel):
    membershipID: int
    resourceId: str
    borrowedDate: date
    returnDate: date
    actualReturnDate: date = None
    isOverdue: bool = False

# class ReturnedBook(BaseModel):
#     bookTitle: str
#     memberName: str
#     returnDate: date
#     dueDate: date
#     condition: str
#     resourceStatus: str

class UpdateMemberStatus(BaseModel):
    membershipID: str
    status: str
class EditMember(BaseModel):
    new_fullname: Optional[str] = None
    new_phone: Optional[str] = None
    new_address: Optional[str] = None
    new_postCode: Optional[str] = None

class EditUser(BaseModel):
    fullname: Optional[str] = None
    qualification: Optional[str] = None
    experience: Optional[str] = None
    skillSet: Optional[str] = None
    grade: Optional[str] = None
    contact: Optional[str] = None
    roles: Optional[List[str]] = None

class EditRole(BaseModel):
    username: str
    role: str

class LoginUser(BaseModel):
    username: str
    password: str

class AddBook(BaseModel):
    resourceId: str
    title: str
    author: str
    genre: str
    format: str
    publishedDate: str
    resourceType: str
    catelogedBy: str

class EditBook(BaseModel):
    new_title: Optional[str] = None
    new_author: Optional[str] = None
    new_genre: Optional[str] = None
    new_format: Optional[str] = None
    new_publishedDate: Optional[str] = None
    new_resourceType: Optional[str] = None
    new_catelogedBy: Optional[str] = None


class DeleteBook(BaseModel):
    resourceId: str
    
class ResourceInput(BaseModel):
    resourceId: str  # User only provides the resourceId

class MemberInput(BaseModel):
    membershipID: str  # User only provides the membershipID

class BorrowBook(BaseModel):
    borrowId: str
    resource: ResourceInput
    member: MemberInput
    issuedBy: str
    borrowedDate: str
    issuedDate: str
    returnDate: str
    preferences: List[str] = None  # List of preferences (e.g., ["software standards", "fiction"])

class LendBehavior(BaseModel):
    membershipID: str
    overdueCount: int
    preference: str

class BorrowingHistory(BaseModel):
    membershipID: str
    resourceId: str
    borrowedDate: str
    returnDate: str


# class ReturnBook(BaseModel):
#     borrowId: str
#     returnDate: str
#     comment: str

class ReturnBook(BaseModel):
    borrowId: str
    status: str
    bookstatus: str

class SearchBook(BaseModel):
    search_query: str
    
class Token(BaseModel):
    access_token: str
    token_type: str



# Base.metadata.drop_all(bind=engine)

# Recreate the table with the updated schema
Base.metadata.create_all(bind=engine)
# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_dbsession():
    # Replace this with your actual MongoDB connection logic
    client = AsyncIOMotorClient("mongodb://localhost:27017") # type: ignore
    db = client["angledimensions"]
    return db

@app.get("/")
async def read_root():
    return RedirectResponse(url="/WebApplication/auth/login.html")

# Password verification
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to get user from database
def get_user(db, username: str):
    user = db.query(User).filter(User.username == username).first()
    return user

# Function to authenticate user
def authenticate_user(db, data: LoginUser):
    user = get_user(db, data.username)
    if not user:
        return False
    if not verify_password(data.password, user.password):
        return False
    return user

# Function to create access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print("Generated Token:", encoded_jwt)  # Debugging: Print the generated token
    return encoded_jwt

# Dependency to get current user from JWT token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print("SECRET_KEY:", SECRET_KEY)  # Debugging: Print the SECRET_KEY
        print("Token to Decode:", token)  # Debugging: Print the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        print("JWTError:", e)  # Debugging: Print the JWT error
        raise credentials_exception
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise credentials_exception
    finally:
        db.close()
    return user

async def get_current_userss():
    # Replace this with your actual user authentication logic
    return UserBase(username="Linda2", role="admin")
# Dependency to check if user is admin
async def get_current_library_user(current_user: User = Depends(get_current_user)):
    if current_user.role not in ["admin", "librarian", "cataloger", "librarymanager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin, librarian, cataloger and librarymanager can perform this action"
        )
    return current_user


    if current_user.role not in ["cataloger", "librarymanager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only cataloger and librarymanager can perform this action"
        )
    return current_user
# Login endpoint to get JWT token
@app.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == form_data.username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    finally:
        db.close()

# List all users
@app.get("/listusers")
async def list_users(user: UserBase = Depends(get_current_user),):
    if user.role not in ["librarymanager"]:
        raise HTTPException(status_code=403, detail="Only admin, librarian, cataloger and librarymanager can list borrowed books")
    
    db = SessionLocal()
    try:
        # Query all users from the database
        users = db.query(User).all()

        # Return the list of users
        return [{key: value for key, value in user.__dict__.items() if key != 'password'} for user in users]
    finally:
        db.close()
# Register endpoint
@app.post("/register")
async def register(data: RegisterUser):
    db = SessionLocal()
    try:
        user = User(username=data.username, password=pwd_context.hash(data.password), role=data.role, email=data.email, fullname=data.fullname)
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"username": user.username}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

# get user info
@app.get("/userinfo")
async def get_user_info(current_user: User = Depends(get_current_user)):
    db= SessionLocal()
    try:
        user = db.query(User).filter(User.username == current_user.username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {key: value for key, value in user.__dict__.items() if key != 'password'}
    finally:
        db.close()  
# Edit user info 
@app.put("/edituser")
async def edit_user(data: EditUser, current_user: User = Depends(get_current_user)): 
    db = SessionLocal()
    try:
        # Query the user to be edited
        user = db.query(User).filter(User.username == current_user.username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update the user info (only if the field is provided in the request)
        if data.fullname is not None:
            user.fullname = data.fullname
        if data.qualification is not None:
            user.qualification = data.qualification
        if data.experience is not None:
            user.experience = data.experience
        if data.skillSet is not None:
            user.skillSet = data.skillSet
        if data.grade is not None:
            user.grade = data.grade
        if data.contact is not None:
            user.contact = data.contact
        if data.roles is not None:
            user.role = ",".join(data.roles)

        db.commit()
        return {"message": "User updated successfully", "username": user.username}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()


# Edit user role
@app.put("/editrole")
async def edit_role(data: EditRole, current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    try:
        # Query the user to be edited
        user = db.query(User).filter(User.username == data.username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update the user role (only if the field is provided in the request)
        if data.role is not None:
            user.role = data.role

        db.commit()
        return {"message": "User role updated successfully", "username": user.username}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

# Add member
@app.post("/addmember")
async def add_member(data: AddMember, db: Session = Depends(get_db)):
    # status = "Active"
            # memberStatus = data.memberStatus,
    try:
        member = Member(
            fullname=data.fullname,
            membershipID=data.membershipID,
            phone=data.phone,
            address=data.address,
            postCode=data.postCode,
            dateEnrolled=datetime.now()
        )
        db.add(member)
        db.commit()
        db.refresh(member)
        return {"Member added successfully": member.fullname}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# List members
@app.get("/listmembers")
async def list_members(db: Session = Depends(get_db)):
    try:
        members = db.query(Member).all()
        return [
            {
                "fullname": member.fullname,
                "membershipID": member.membershipID,
                "phone": member.phone,
                "address": member.address,
                "postCode": member.postCode,
                "dateEnrolled": member.dateEnrolled.isoformat(),
                "status": member.memberstatus
            } for member in members
        ]
    finally:
        db.close()
# Edit member
@app.put("/editmember/{membershipID}")
async def edit_member(membershipID: str, data: EditMember):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.membershipID == membershipID).first()
        if user:
            user.fullname = data.fullname
            user.membershipID = data.membershipID
            user.phone = data.phone
            user.address = data.address
            user.postCode = data.postCode
            user.behaviour = data.behaviour
            user.enrolledDate = data.enrolledDate
            db.commit()
            return {"Member updated successfully": user.fullname}
        raise HTTPException(status_code=400, detail="Member not found")
    finally:
        db.close()

# Update member status
@app.put("/updatestatus/{membershipID}")
async def update_member_status(membershipID: str, data: UpdateMemberStatus):
    db = SessionLocal()
    try:
        member = db.query(Member).filter(Member.membershipID == membershipID).first()
        if member:
            member.status = data.status
            db.commit()
            return {"Member status updated successfully": member.status}
        raise HTTPException(status_code=400, detail="Member not found")
    finally:
        db.close()

# Edit username and password
@app.put("/edit/{username}")
async def edit_user(data: EditUser, username: str):
    new_username = data.new_username
    new_password = data.new_password
    new_email = data.new_email
    new_fullname = data.new_fullname
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user:
            if new_username:
                user.username = new_username
            if new_password:
                user.password = new_password

            if new_email:
                user.email = new_email

            if new_fullname:
                user.fullname = new_fullname

            db.commit()
            return {"message": "User updated successfully", "username": user.username}
        raise HTTPException(status_code=400, detail="User not found")
    finally:
        db.close()


# LIBRARY MANAGEMENT
@app.post("/addbook")
async def add_book(
    data: AddBook,
    user: UserBase = Depends(get_current_user),
):
    # Check if the user is an admin
    if user.role not in ["cataloger", "librarymanager"]:
        raise HTTPException(status_code=403, detail="Only admin, librarian, cataloger and librarymanager can add books")
    

    # Generate a unique resourceId
    resourceId = str(uuid.uuid4())

    try:
        # Create a new Library document
        book_data = Library(
            resourceId=resourceId,
            title=data.title,
            author=data.author,
            genre=data.genre,
            format=data.format,
            publishedDate=data.publishedDate,
            resourceType=data.resourceType,
            catalogedBy=data.catelogedBy
        )

        # Save the document to MongoDB
        book_data.save()

        return {"message": "Book added successfully", "resourceId": resourceId}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/deletebook")
async def delete_book(data: DeleteBook, user: UserBase = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete books")
    db = SessionLocal()
    try:
        book = db.query(Library).filter(Library.resourceId == data.resourceId).first()
        if book:
            db.delete(book)
            db.commit()
            return {"message": "Book deleted successfully"}
        raise HTTPException(status_code=400, detail="Book not found")
    finally:
        db.close()


@app.get("/searchbook")
async def search_book(data: SearchBook):
    db = SessionLocal()
    try:
        books = db.query(Library).filter(Library.title.like(f"%{data.search_query}%")).all()
        if books:
            return [{"resourceId": book.resourceId, "title": book.title, "author": book.author, "genre": book.genre, "format": book.format} for book in books]
        raise HTTPException(status_code=400, detail="No books found")
    finally:
        db.close()

# List all books in the database

@app.get("/listbooks")
async def list_books(user: User = Depends(get_current_user)):
    # Check if the user is an admin
    if user.role not in ["admin", "librarian", "cataloger", "librarymanager"]:
        raise HTTPException(status_code=403, detail="Only admin can list books")

    try:
        # Query all books from MongoDB
        books = Library.objects.all()

        # Format the response
        return [
            {
                "resourceId": book.resourceId,
                "title": book.title,
                "author": book.author,
                "genre": book.genre,
                "format": book.format,
                "publishedDate": book.publishedDate,
                "resourceType": book.resourceType,
                "catalogedBy": book.catalogedBy
            }
            for book in books
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# BorrowBook
 # Assuming this is your SQLAlchemy session factory for PostgreSQL

# @app.post("/borrowbook")
@app.post("/borrowbook")
async def borrow_book(data: BorrowBook, user: User = Depends(get_current_user)):
    db = SessionLocal()
    if user.role not in ["librarian", "librarymanager"]:
        raise HTTPException(status_code=403, detail="Only librarian and librarymanager can borrowed books to members")
    
    try:

        # Fetch the resource (book) from the database using resourceId
        resource = Library.objects(resourceId=data.resource.resourceId).first()
        if not resource:
            raise HTTPException(status_code=404, detail="Resource (book) not found")

        # Fetch the member from the database using membershipID
        member = db.query(Member).filter(Member.membershipID == data.member.membershipID).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")

        # Check if the book is already borrowed by another member
        existing_borrowing = BorrowBookData.objects(resource=data.resource.resourceId, status=True).first()
        if existing_borrowing:
            raise HTTPException(status_code=400, detail="Book is already borrowed by another member")

        # Check if the member has already borrowed this book
        existing_borrowing = BorrowBookData.objects(resource=data.resource.resourceId, member=member.membershipID, status=True).first()
        if existing_borrowing:
            raise HTTPException(status_code=400, detail="Member has already borrowed this book")

        # Generate a unique borrowId
        borrowId = str(uuid.uuid4())
        # Create a BorrowBookData object with the fetched resource and member details
        borrowing_data = BorrowBookData(
            borrowId=borrowId,
            resource=data.resource.resourceId,  # Use the fetched resource's ID
            member=member.membershipID,   # Use the fetched member's ID
            issuedBy=data.issuedBy,
            borrowedDate=data.borrowedDate,
            issuedDate=data.issuedDate,
            returnDate=data.returnDate,
            status=True
        )

        # Save the borrowing details to MongoDB
        borrowing_data.save()

        # Update member's lending behavior with preferences
        update_lending_behavior(member.membershipID, preference=data.preferences)

        return {"message": "Book borrowed successfully", "borrowId": borrowId, "preferences": data.preferences or []}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

# update lending behaviour
@app.put("/lendingbehavior/{membershipID}")
def update_lending_behavior(membershipID: str, preference: List[str] = None):
    db = SessionLocal()
    try:
        # Find the member
        member = db.query(Member).filter(Member.membershipID == membershipID).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found.")

        # Find or create LendingBehavior for the member
        behavior = db.query(LendingBehavior).filter(LendingBehavior.membershipID == membershipID).first()
        if not behavior:
            behavior = LendingBehavior(membershipID=membershipID)
            db.add(behavior)

        # Add preferences if provided
        if preference:
            if behavior.preference:
                # Append new preferences to existing ones
                existing_preferences = behavior.preference.split(",")
                updated_preferences = list(set(existing_preferences + preference))  # Remove duplicates
                behavior.preference = ",".join(updated_preferences)
            else:
                # Set new preferences
                behavior.preference = ",".join(preference)

        db.commit()
        return {"message": f"Lending behavior updated for member {member.fullname}."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    finally:
        db.close()


# get lending behavior
@app.get("/get-lendingbehavior/{membershipID}")
def get_member_details(membershipID: str):
    db = SessionLocal()
    # Find the member
    member = db.query(Member).filter(Member.membershipID == membershipID).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found.")

    # Find the lending behavior for the member
    behavior = db.query(LendingBehavior).filter(LendingBehavior.membershipID == membershipID).first()
    if not behavior:
        raise HTTPException(status_code=404, detail="No lending behavior recorded for this member.")

    return {
        "message": f"Member Details: {member.fullname}, Status: {member.memberstatus}, Date Enrolled: {member.dateEnrolled}",
        "lendingBehavior": {
            "overdueCount": behavior.overdueCount,
            "preferences": behavior.preference.split(",") if behavior.preference else []
        }
    }


# List borrowed books
@app.get("/listborrowedbooks")
async def list_borrowed_books(user: UserBase = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role not in ["admin", "librarian", "cataloger", "librarymanager"]:
        raise HTTPException(status_code=403, detail="Only admin, librarian, cataloger and librarymanager can list borrowed books")
    
    try:
        # Fetch all borrowed books where status is True (not returned)
        borrowed_books = BorrowBookData.objects(status=True)
        
        result = []
        for borrowed_book in borrowed_books:
            # Fetch resource details from the Library collection
            resource = Library.objects(resourceId=borrowed_book.resource).first()
            
            # Fetch member details from the Member table
            member = db.query(Member).filter(Member.membershipID == borrowed_book.member).first()
            
            if resource and member:
                result.append({
                    "borrowId": borrowed_book.borrowId,
                    "resourceInfo": {
                        "resourceId": resource.resourceId,
                        "title": resource.title,
                        "author": resource.author,
                        "genre": resource.genre,
                        "format": resource.format,
                        "publishedDate": resource.publishedDate,
                        "resourceType": resource.resourceType,
                        "catalogedBy": resource.catalogedBy
                    },
                    "memberInfo": {
                        "membershipID": member.membershipID,
                        "fullname": member.fullname,
                        "phone": member.phone,
                        "address": member.address,
                        "postCode": member.postCode,
                        "dateEnrolled": member.dateEnrolled,
                    },
                    "issuedBy": borrowed_book.issuedBy,
                    "borrowedDate": borrowed_book.borrowedDate,
                    "returnDate": borrowed_book.returnDate
                })
            else:
                # Log or handle cases where resource or member is not found
                print(f"Resource or member not found for borrowId: {borrowed_book.borrowId}")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

# Return a book
@app.post("/returnbook")
async def return_book(data: ReturnBook, user: UserBase = Depends(get_current_user)):
    try:
        # Find the borrowing record
        borrowing = BorrowBookData.objects(borrowId=data.borrowId).first()
        if not borrowing:
            raise HTTPException(status_code=404, detail="Book not currently borrowed")

        # Update the return date and status
        borrowing.returnDate = datetime.now().isoformat()
        borrowing.status = False  # Mark as returned
        borrowing.save()

        # Record the returned book
        returned_book = ReturnBookData(
            returnId=data.borrowId,
            resource=borrowing.resource,
            member=borrowing.member,
            returnedBy=user.username,
            status=data.status,
            returnedDate=datetime.now().isoformat(),
            actualReturnDate=borrowing.returnDate,
            isOverdue=False  # Add logic to calculate overdue status if needed
        )
        returned_book.save()

        return {"message": "Book returned successfully", "borrowId": data.borrowId}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get returned books
@app.get("/getreturnedbooks")
async def get_returned_books(user: UserBase = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        # Fetch all returned books
        returned_books = ReturnBookData.objects()
        
        result = []
        for returned_book in returned_books:
            # Fetch resource details from the Library collection
            resource = Library.objects(resourceId=returned_book.resource).first()
            
            # Fetch member details from the Member table
            member = db.query(Member).filter(Member.membershipID == returned_book.member).first()
            
            if resource and member:
                result.append({
                    "borrowId": returned_book.returnId,
                    "resourceInfo": {
                        "resourceId": resource.resourceId,
                        "title": resource.title,
                        "author": resource.author,
                        "genre": resource.genre,
                        "format": resource.format,
                        "publishedDate": resource.publishedDate,
                        "resourceType": resource.resourceType,
                        "catalogedBy": resource.catalogedBy
                    },
                    "memberInfo": {
                        "membershipID": member.membershipID,
                        "fullname": member.fullname,
                        "phone": member.phone,
                        "address": member.address,
                        "postCode": member.postCode,
                        "dateEnrolled": member.dateEnrolled,
                    },
                    "issuedBy": returned_book.returnedBy,
                    "status": returned_book.status,
                    "borrowedDate": returned_book.returnedDate,
                    "returnDate": returned_book.actualReturnDate
                })
            else:
                # Log or handle cases where resource or member is not found
                print(f"Resource or member not found for returnId: {returned_book.returnId}")
        
        return {"returned_books": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
# Total number of library resources available based on the given categories



@app.get("/borrowpercentages")
async def borrow_percentages(
    year: int,
    month: int,
    user: UserBase = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user.role not in ["librarian", "cataloger", "librarymanager"]:
        raise HTTPException(status_code=403, detail="Only admin, librarian, cataloger and librarymanager can list borrowed books")
    
    try:
        total = db.query(Library).filter(
            func.extract('year', Library.publishedDate) == year,
            func.extract('month', Library.publishedDate) == month
        ).count()

        borrowed = db.query(BorrowBookData).filter(
            func.extract('year', BorrowBookData.borrowedDate) == year,
            func.extract('month', BorrowBookData.borrowedDate) == month
        ).count()

        percentage = (borrowed / total) * 100 if total > 0 else 0

        return {"percentage": percentage}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/totalresourcesbygenre")
async def total_resources_by_genre(genre: str):
    try:
        # Count documents with the specified genre
        total = Library.objects(genre=genre).count()
        return {"total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/totalresourcesbycategory")
async def total_resources_by_category(category: str):
    try:
        # Ensure the category is a valid field in the Library model
        if not hasattr(Library, category):
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")

        # Group by the specified category and count resources
        pipeline = [
            {"$group": {"_id": f"${category}", "count": {"$sum": 1}}}
        ]
        results = Library.objects.aggregate(pipeline)

        # Convert the results to a dictionary
        category_counts = {result["_id"]: result["count"] for result in results}
        return category_counts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/totalcataloguedinmonth")
async def total_catalogued_in_month(year: int, month: int):
    try:
        # Validate month input
        if month < 1 or month > 12:
            raise HTTPException(status_code=400, detail="Month must be between 1 and 12")

        # Convert year and month to a date range
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        # Query resources cataloged in the given month
        total = Library.objects(publishedDate__gte=start_date.isoformat(), publishedDate__lt=end_date.isoformat()).count()
        return {"total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/totalresources")
async def total_resources():
    try:
        # Count all documents in the Library collection
        total = Library.objects.count()
        return {"total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Total members
@app.get("/totalmembers")
async def total_members(
    user: UserBase = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user.role not in ["admin", "librarian", "cataloger", "librarymanager"]:
        raise HTTPException(status_code=403, detail="Only admin, librarian, cataloger and librarymanager can list borrowed books")
    
    try:
        total = db.query(Member).count()
        return {"total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Total borrowed books
@app.get("/totalborrowed")
async def total_borrowed(user: UserBase = Depends(get_current_user)):
    # Check if the user is an admin
    if user.role not in ["admin", "librarian", "cataloger", "librarymanager"]:
        raise HTTPException(status_code=403, detail="Only admin, librarian, cataloger and librarymanager can list borrowed books")
    
    try:
        # Count the total number of borrowed resources where status is True (active borrowings)
        total = BorrowBookData.objects(status=True).count()
        return {"total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")



@app.get("/borrowingpercentage")
async def borrowing_percentage(
    year: int,
    month: int,
    user: UserBase = Depends(get_current_user)
):
    # Check if the user is an admin
    if user.role not in ["admin", "librarian", "cataloger", "librarymanager"]:
        raise HTTPException(status_code=403, detail="Only admin, librarian, cataloger and librarymanager can list borrowed books")
    
    try:
        # Validate month input
        if month < 1 or month > 12:
            raise HTTPException(status_code=400, detail="Month must be between 1 and 12")

        # Calculate the start and end dates for the given month
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        # Fetch the total number of resources in the library
        total_resources = Library.objects.count()

        # Fetch the number of resources borrowed in the given month
        borrowed_in_month = BorrowBookData.objects(
            borrowedDate__gte=start_date.isoformat(),
            borrowedDate__lt=end_date.isoformat()
        ).count()

        # Calculate the borrowing percentage
        if total_resources == 0:
            borrowing_percentage = 0  # Avoid division by zero
        else:
            borrowing_percentage = (borrowed_in_month / total_resources) * 100

        return {
            "total_resources": total_resources,
            "borrowed_in_month": borrowed_in_month,
            "borrowing_percentage": round(borrowing_percentage, 2)  # Round to 2 decimal places
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")