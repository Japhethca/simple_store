import os
import dotenv

dotenv.load_dotenv()

if os.getenv("ENVIRON") == "production":
    from .prod import *
else:
    from .dev import *
