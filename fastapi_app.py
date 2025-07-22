from fastapi import FastAPI, HTTPException
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext
from pydantic import BaseModel
import joblib
import numpy as np
import os
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Database setup
Base = declarative_base()
engine = create_engine("sqlite:///./users.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username):
    return db.query(User).filter(User.username == username).first()

from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

@app.post("/signup")
def signup(user: UserCreate):
    db = next(get_db())
    db_user = get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Registration successful"}


with open(os.path.join(os.path.dirname(__file__), 'amount_scaler_params.json'), 'r') as f:
    amount_scaler_params = json.load(f)
with open(os.path.join(os.path.dirname(__file__), 'mcc_freq_scaler_params.json'), 'r') as f:
    mcc_freq_scaler_params = json.load(f)

class TransactionFeatures(BaseModel):
    zip: float
    merchant_city: str
    merchant_state: str
    mcc: int
    use_chip_Online_Transaction: bool
    amount: float
    use_chip_Swipe_Transaction: bool
    use_chip_Chip_Transaction: bool

def encode_feature(value, mapping, default=0):
    return mapping.get(str(value), default)

def scale_amount(amount, scaler_params):
    return (amount - scaler_params['mean']) / scaler_params['scale']




def load_json(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), 'r') as f:
        return json.load(f)

zip_freq_map = load_json('zip_freq_map.json')
merchant_city_map = load_json('merchant_city_map.json')
merchant_state_map = load_json('merchant_state_map.json')
mcc_freq_map = load_json('mcc_freq_map.json')
with open(os.path.join(os.path.dirname(__file__), 'amount_scaler_params.json'), 'r') as f:
    amount_scaler_params = json.load(f)
with open(os.path.join(os.path.dirname(__file__), 'mcc_freq_scaler_params.json'), 'r') as f:
    mcc_freq_scaler_params = json.load(f)
model = joblib.load(r'c:\Users\amad.mateen\Documents\Python\banking_task\fraud_model.joblib')

@app.post('/predict')
def predict_fraud(features: TransactionFeatures):
    try:
        zip_encoded = encode_feature(str(int(features.zip)), zip_freq_map)
        merchant_city_encoded = encode_feature(features.merchant_city, merchant_city_map)
        merchant_state_encoded = encode_feature(features.merchant_state, merchant_state_map)
        mcc_freq_raw = encode_feature(str(features.mcc), mcc_freq_map)
        mcc_freq_scaled = scale_amount(mcc_freq_raw, mcc_freq_scaler_params)
        amount_scaled = scale_amount(features.amount, amount_scaler_params)

        X = np.array([
            [
                zip_encoded,
                merchant_city_encoded,
                merchant_state_encoded,
                mcc_freq_scaled,
                int(features.use_chip_Online_Transaction),
                amount_scaled,
                int(features.use_chip_Swipe_Transaction),
                int(features.use_chip_Chip_Transaction)
            ]
        ])
        prediction = model.predict(X)[0]
        return {'fraud_prediction': int(prediction), 'encoded_features': X.tolist()[0]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
