import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Cargamos variables desde .env cuando corres localmente
load_dotenv()

# Soportar varios nombres de variable para mayor flexibilidad
SUPABASE_URL = os.getenv('VITE_SUPABASE_URL') or os.getenv('SUPABASE_URL')
ANON_KEY = os.getenv('VITE_SUPABASE_SUPABASE_ANON_KEY') or os.getenv('SUPABASE_ANON_KEY')
# Key con permisos elevados (service role) — usar SOLO en entorno servidor
SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE') or os.getenv('SERVICE_ROLE_KEY')

# Preferir la service role key en el backend si está disponible
_KEY_TO_USE = SERVICE_ROLE_KEY if SERVICE_ROLE_KEY else ANON_KEY

if not SUPABASE_URL or not _KEY_TO_USE:
    raise RuntimeError(
        "Faltan credenciales de Supabase: define VITE_SUPABASE_URL y VITE_SUPABASE_SUPABASE_ANON_KEY, "
        "o define SUPABASE_SERVICE_ROLE para uso del backend."
    )

supabase: Client = create_client(SUPABASE_URL, _KEY_TO_USE)

def get_supabase_client():
    return supabase
