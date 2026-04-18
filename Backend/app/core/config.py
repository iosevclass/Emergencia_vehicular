from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):

    SECRET_KEY: str
    ALGORITHM: str="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int=30
    DEBUG: bool = False
    #configuración para cargar variables de entorno desde un archivo .env
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")   
settings = Settings()
print(f"DEBUG MODE: {settings.SECRET_KEY[:5]}...") # Solo para ver que cargó algo
print(f"DEBUG MODE: {settings.DEBUG}")  #verifico si esta sacando de env