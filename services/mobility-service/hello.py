import os
import sys
import psycopg2

# ============================================================================
# FORCER ENVIRONNEMENT ASCII POUR ÉVITER LES PROBLÈMES
# ============================================================================

# Supprimer toutes les variables d'environnement problématiques
env_vars_to_clean = [
    'PGCLIENTENCODING', 'LANG', 'LC_ALL', 'LC_CTYPE',
    'PYTHONIOENCODING', 'PYTHONUTF8'
]

for var in env_vars_to_clean:
    if var in os.environ:
        del os.environ[var]

# Forcer l'encodage ASCII pour la session
os.environ['PYTHONIOENCODING'] = 'ascii'
os.environ['LANG'] = 'C'
os.environ['LC_ALL'] = 'C'

# ============================================================================
# CONNEXION AVEC PARAMÈTRES SIMPLES
# ============================================================================
try:
    print("Testing PostgreSQL connection...")
    
    # Version ultra-minimaliste sans aucun caractère spécial
    conn = psycopg2.connect(
        host="localhost",
        database="mobility_db",
        user="mobility_user",
        password="mobility_pass",
        port=5432
    )
    
    print("SUCCESS: Connected to PostgreSQL!")
    
    # Test simple
    cur = conn.cursor()
    cur.execute("SELECT version();")
    result = cur.fetchone()
    print(f"PostgreSQL version: {result[0]}")
    
    cur.close()
    conn.close()
    
    print("\nAll tests passed successfully!")
    
except Exception as e:
    print(f"ERROR: {str(e)[:200]}")
    
    # Debug supplémentaire
    print("\n=== DEBUG INFO ===")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python executable: {sys.executable}")