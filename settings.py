import os
import dotenv

dotenv.load_dotenv()

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
redirect_url = os.getenv("redirect_url")
discord_id = os.getenv("discord_id")
secret_flask_key = os.getenv("secret_flask_key", os.urandom(24).hex())