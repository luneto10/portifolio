from supabase import create_client
from app.core.config import settings

try:
    if settings.ENVIRONMENT == "dev":
        supabase = create_client(settings.DEV_DB_URL, settings.DEV_DB_KEY)
    else:
        supabase = create_client(settings.PROD_DB_URL, settings.PROD_DB_KEY)
except Exception as e:
    print(f"Supabase initialization error: {e}")
    raise
