import os
import dotenv

dotenv.load_dotenv()

if os.getenv("ENV") == "production":
    from .prod import *
else:
    from .dev import *
