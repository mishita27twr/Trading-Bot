import os
from dotenv import load_dotenv

load_dotenv()

print("KEY =", os.getenv("BINANCE_API_KEY"))
print("SECRET =", os.getenv("BINANCE_API_SECRET"))