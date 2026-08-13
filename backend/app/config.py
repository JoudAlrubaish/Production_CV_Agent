# import Pydantic configuration tools to read from .env
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings): #creating object that contains all application settings
    database_url: str

    model_path: str = "models/model.pt" #to be modify later when Student 1 finish the model 
    model_version: str = "1.0.0"

    cors_origins: str = "http://localhost:5173" #tells FastAPI that local React frontend can communicate with it

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings() # now every file can use settings. to read .env information speartly 