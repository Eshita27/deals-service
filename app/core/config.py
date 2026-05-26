import hvac
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Polyglot Commerce - Deals API"
    PORT: int = 8082
    
    # These will be dynamically overwritten by Vault, but have safe local development defaults
    MONGO_URI: str = "mongodb://admin:supersecretpassword@localhost:27017"
    DATABASE_NAME: str = "deals_db"
    GLOBAL_OVERRIDE_SECRET: str = "local_development_fallback_secret"

    def load_secrets_from_vault(self):
        try:
            # Connect to the local HashiCorp Vault container we are spinning up
            client = hvac.Client(url='http://localhost:8200', token='master-vault-token-2026')
            
            if client.is_authenticated():
                # Read configuration from the secure Key-Value path
                vault_response = client.secrets.kv.v1.read_secret(
                    path='deals-api/config',
                    mount_point='secret'
                )
                
                secrets = vault_response['data']
                
                # Dynamically inject the credentials into our runtime memory
                self.MONGO_URI = secrets.get("MONGO_URI", self.MONGO_URI)
                self.DATABASE_NAME = secrets.get("DATABASE_NAME", self.DATABASE_NAME)
                self.GLOBAL_OVERRIDE_SECRET = secrets.get("GLOBAL_OVERRIDE_SECRET", self.GLOBAL_OVERRIDE_SECRET)
                print("🔒 [VAULT] Successfully bootstrapped environment configurations from HashiCorp Vault!")
            else:
                print("⚠️ [VAULT] Authentication failed. Using local fallback environment parameters.")
                
        except Exception as e:
            print(f"⚠️ [VAULT] Could not connect to Vault service ({e}). Operating with local sandbox fallback properties.")

settings = Settings()
# Execute the bootstrap logic immediately on application import
settings.load_secrets_from_vault()