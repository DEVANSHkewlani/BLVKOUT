import os

from dotenv import load_dotenv

from supabase import create_client


load_dotenv()


SUPABASE_URL = os.getenv(
    "SUPABASE_URL"
)

SUPABASE_ANON_KEY = os.getenv(
    "SUPABASE_ANON_KEY"
)

ADMIN_EMAIL = os.getenv(
    "ADMIN_EMAIL"
)


supabase = create_client(
    SUPABASE_URL,
    SUPABASE_ANON_KEY
)