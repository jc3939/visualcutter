from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Request
from pydantic import BaseModel, EmailStr
from passlib.hash import bcrypt
#from autocut.type import WhisperModel
import argparse
#from autocut.transcribe import Transcribe
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

app = FastAPI()

# Replace this with your actual secret key for JWT
SECRET_KEY = "mysecretekeyjjchennewryland"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserCreate(BaseModel):
    username: str
    email:str
    password: str

class User(BaseModel):
    username: str
    email: str

def get_user(username: str):
    for user in users_db:
        if user.username == username:
            return user
    return None

class PasswordResetRequest(BaseModel):
    email: str

class PasswordReset(BaseModel):
    token: str
    new_password: str

async def __uploadfile(_file: UploadFile):
    save_path = temp_file_path
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    out_file = os.path.join(save_path, _file.filename)
    with open(out_file, "wb") as f:
        data= await _file.read()
        f.write(data)
    print("audio_out_file", out_file)
    return out_file

# Simulated user database (replace with PostgreSQL)
users_db = []

@app.post("/signup")
async def signup(user: UserCreate):
    # Check if the user already exists
    if any(existing_user.email == user.email for existing_user in users_db):
        raise HTTPException(status_code=400, detail="User already registered")

    # Hash the password before storing it
    hashed_password = bcrypt.hash(user.password)

    # Store the user in the database (in-memory for this example)
    newUser = UserCreate(username=user.username,email = user.email,password = hashed_password)
    users_db.append(newUser)
    return {"message": "User registered successfully"}

@app.post("/login")
async def login(user: UserCreate):
    # Find the user by username
    existing_user = get_user(user.username)

    if existing_user is None:
        raise HTTPException(status_code=401, detail="User not found")

    print(existing_user.password)
    # Verify the password hash
    if not bcrypt.verify(user.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    # Generate a JWT token for authentication
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = {
        "sub": existing_user.username,
        "exp": datetime.utcnow() + access_token_expires,
    }
    access_token = jwt.encode(access_token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer"}
'''
@app.post("/transcribe/")
async def transcribe(request: Request, file: UploadFile = File(...)):
    video_file = await __uploadfile(file) 
    inputArgs = await request.json()
    myArgs = argparse.Namespace()
    setattr(myArgs, 'inputs', [video_file])
    setattr(myArgs, 's', False)
    setattr(myArgs, 'to_md', False)
    setattr(myArgs, 'lang', myArgs.get("lang", "en"))
    setattr(myArgs, 'prompt', myArgs.get("prompt", ""))
    setattr(myArgs, 'whisper_mode', "openai")
    setattr(myArgs, 'openai_rpm', 50)
    setattr(myArgs, 'whisper_model', WhisperModel.SMALL.value)
    setattr(myArgs, 'bitrate', "10m")
    setattr(myArgs, 'vad', "1")
    setattr(myArgs, 'force', True)
    setattr(myArgs, 'encoding', "utf-8")
    setattr(myArgs, 'device', "cpu")
    Transcribe(myArgs).run()
'''

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)