import hvac
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Polyglot Commerce - Deals API"
    PORT: int = 8082
    
    # Injected securely from HashiCorp Vault on startup
    MONGO_URI: str = ""
    DATABASE_NAME: str = ""
    GLOBAL_OVERRIDE_SECRET: str = ""

    def load_secrets_from_vault(self):
        try:
            # Connect to local Vault container running via docker-compose
            client = hvac.Client(url='http://localhost:8200', token='master-vault-token-2026')
            
            if not client.is_authenticated():
                raise Exception("Vault authentication failed.")
            
            # Read secrets from the structural path we initialized
            vault_response = client.secrets.kv.v1.read_secret(
                path='deals-api/config',
                mount_point='secret'
            )
            
            secrets = vault_response['data']
            
            # Map values dynamically to variables
            self.MONGO_URI = secrets.get("MONGO_URI", "mongodb://localhost:27017")
            self.DATABASE_NAME = secrets.get("DATABASE_NAME", "deals_db")
            self.GLOBAL_OVERRIDE_SECRET = secrets.get("GLOBAL_OVERRIDE_SECRET", "default_fallback")
            print("Successfully bootstrapped environment settings from HashiCorp Vault!")
            
        except Exception as e:
            print(f"CRITICAL FAULT: Could not fetch properties from Vault: {e}")
            # Local fallback for safe resilience during localized testing
            self.MONGO_URI = "mongodb://admin:supersecretpassword@localhost:27017"
            self.DATABASE_NAME = "deals_db"
            self.GLOBAL_OVERRIDE_SECRET = "local_dev_fallback_secret"

settings = Settings()
settings.load_secrets_from_vault()