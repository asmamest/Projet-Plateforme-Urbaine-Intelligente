#!/usr/bin/env python3
"""
SCRIPT COMPLET DE CONFIGURATION PROPRE
Élimine tous les problèmes d'encodage
"""
import os
import sys
import subprocess
import tempfile

print("=" * 70)
print("CONFIGURATION COMPLÈTE PostgreSQL + Python")
print("=" * 70)

# ============================================================================
# 1. CONFIGURER L'ENVIRONNEMENT
# ============================================================================
print("\n1. 🛠️  Configuration de l'environnement...")

# Supprimer toutes les variables problématiques
for key in list(os.environ.keys()):
    if any(x in key.lower() for x in ['pg', 'encod', 'lang', 'lc_']):
        del os.environ[key]

# Forcer ASCII pur
os.environ['LANG'] = 'C'
os.environ['LC_ALL'] = 'C'
os.environ['PYTHONIOENCODING'] = 'ascii'
os.environ['PGCLIENTENCODING'] = 'SQL_ASCII'

print("   ✅ Environnement forcé en ASCII")

# ============================================================================
# 2. CRÉER UN FICHIER DE CONFIGURATION PROPRE
# ============================================================================
print("\n2. 📁 Création de la configuration...")

config_content = """# Configuration PostgreSQL - SANS ACCENTS
[postgresql]
host = localhost
port = 5432
database = mobility_db_clean
user = mobility_app
password = app_password_123
encoding = UTF8

[application]
name = Mobility Service
version = 1.0.0
"""

config_file = os.path.join(tempfile.gettempdir(), 'mobility_config.ini')
with open(config_file, 'w', encoding='ascii') as f:
    f.write(config_content)

print(f"   ✅ Fichier de configuration créé: {config_file}")

# ============================================================================
# 3. EXÉCUTER LES COMMANDES SQL POUR TOUT CRÉER
# ============================================================================
print("\n3. 🗄️  Création de la base de données via psql...")

sql_commands = """
-- 1. Supprimer l'ancien si existe
DROP DATABASE IF EXISTS mobility_db_clean;
DROP USER IF EXISTS mobility_app;

-- 2. Créer un nouvel utilisateur (ASCII PUR)
CREATE USER mobility_app WITH PASSWORD 'app_password_123';

-- 3. Créer une nouvelle base (avec encodage explicite)
CREATE DATABASE mobility_db_clean
    WITH 
    OWNER = mobility_app
    ENCODING = 'UTF8'
    LC_COLLATE = 'C'
    LC_CTYPE = 'C'
    TEMPLATE = template0;

-- 4. Message de confirmation
SELECT '✅ Base de données créée avec succès' as message;
"""

# Écrire les commandes SQL dans un fichier temporaire
sql_file = os.path.join(tempfile.gettempdir(), 'setup_mobility.sql')
with open(sql_file, 'w', encoding='ascii') as f:
    f.write(sql_commands)

# Exécuter via psql
print("\n   Exécution des commandes SQL...")
try:
    # Essayer avec le mot de passe postgres (commun)
    result = subprocess.run(
        ['psql', '-U', 'postgres', '-h', 'localhost', '-p', '5432', '-f', sql_file],
        input='postgres\n',  # Mot de passe
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode == 0:
        print("   ✅ Base de données créée avec succès!")
        print(result.stdout)
    else:
        print("   ❌ Erreur lors de la création:")
        print(result.stderr)
        
except Exception as e:
    print(f"   ⚠️  Exception: {e}")

# ============================================================================
# 4. TESTER LA NOUVELLE CONFIGURATION
# ============================================================================
print("\n4. 🔬 Test de la nouvelle configuration...")

test_code = '''
import psycopg2
import sys

# Forcer ASCII
sys.stdout.reconfigure(encoding='ascii') if hasattr(sys.stdout, 'reconfigure') else None

try:
    print("   Tentative de connexion...")
    
    # Connexion SIMPLE avec nouveaux paramètres
    conn = psycopg2.connect(
        host="localhost",
        dbname="mobility_db_clean",  # NOUVELLE BASE
        user="mobility_app",          # NOUVEL UTILISATEUR
        password="app_password_123",  # NOUVEAU MOT DE PASSE
        port=5432,
        connect_timeout=10
    )
    
    print("   ✅ CONNEXION RÉUSSIE!")
    
    # Créer une table de test
    cursor = conn.cursor()
    
    # Table simple
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_info (
            id SERIAL PRIMARY KEY,
            component VARCHAR(100),
            status VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Insérer des données de test
    cursor.execute("""
        INSERT INTO system_info (component, status) 
        VALUES ('Database', 'Online'),
               ('API Service', 'Ready'),
               ('Authentication', 'Active');
    """)
    
    # Lire les données
    cursor.execute("SELECT * FROM system_info ORDER BY id;")
    rows = cursor.fetchall()
    
    print("   📊 Données de test insérées:")
    for row in rows:
        print(f"      - {row[1]}: {row[2]}")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("   🎉 TOUT FONCTIONNE CORRECTEMENT!")
    
except Exception as e:
    print(f"   ❌ ÉCHEC: {str(e)}")
    
    # Afficher l'erreur en hex pour débogage
    error_str = str(e)
    if '0xe9' in error_str:
        print("   🔍 Problème détecté: caractère 'é' (0xe9) présent")
        print("   💡 Solution: Vérifiez les fichiers de configuration")
'''

# Exécuter le test
print("\n" + "=" * 50)
exec(test_code)
print("=" * 50)

# ============================================================================
# 5. CRÉER UN FICHIER DE CONNEXION POUR VOTRE APPLICATION
# ============================================================================
print("\n5. 📄 Création du fichier de connexion pour votre app...")

connection_code = '''"""
FICHIER DE CONNEXION PostgreSQL - VERSION PROPRE
À utiliser dans votre application mobility-service
"""
import psycopg2
from psycopg2 import pool
import logging

logger = logging.getLogger(__name__)

# Configuration PROPRE (ASCII seulement)
DB_CONFIG = {
    "host": "localhost",
    "database": "mobility_db_clean",
    "user": "mobility_app",
    "password": "app_password_123",
    "port": 5432,
    "client_encoding": "UTF8"
}

# Pool de connexions
connection_pool = None

def init_db_pool():
    """Initialiser le pool de connexions"""
    global connection_pool
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 20, **DB_CONFIG
        )
        logger.info("✅ Pool de connexions PostgreSQL initialisé")
        return True
    except Exception as e:
        logger.error(f"❌ Erreur d'initialisation du pool: {e}")
        return False

def get_connection():
    """Obtenir une connexion depuis le pool"""
    if connection_pool:
        return connection_pool.getconn()
    
    # Fallback: connexion directe
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        logger.error(f"❌ Impossible d'obtenir une connexion: {e}")
        raise

def return_connection(connection):
    """Retourner une connexion au pool"""
    if connection_pool:
        connection_pool.putconn(connection)

def test_connection():
    """Tester la connexion à la base de données"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT version(), current_database(), current_user;")
        result = cursor.fetchone()
        
        logger.info(f"📊 PostgreSQL {result[0]}")
        logger.info(f"📊 Base: {result[1]}, Utilisateur: {result[2]}")
        
        cursor.close()
        return True
    except Exception as e:
        logger.error(f"❌ Test de connexion échoué: {e}")
        return False
    finally:
        if conn:
            return_connection(conn)

# Initialiser au chargement du module
if init_db_pool():
    test_connection()
'''

# Écrire le fichier
connection_file = os.path.join(os.getcwd(), 'database_connection.py')
with open(connection_file, 'w', encoding='ascii') as f:
    f.write(connection_code)

print(f"   ✅ Fichier créé: {connection_file}")

# ============================================================================
# 6. FICHIER DE TEST FINAL
# ============================================================================
print("\n6. 🧪 Création d'un fichier de test final...")

final_test = '''"""
TEST FINAL - Vérification complète
Exécutez ce fichier pour valider que tout fonctionne
"""
import sys
import os

# Forcer l'encodage ASCII
os.environ['LANG'] = 'C'
os.environ['LC_ALL'] = 'C'

print("=" * 60)
print("TEST DE VALIDATION COMPLET")
print("=" * 60)

# Test 1: Import psycopg2
print("\n1. Test d'import de psycopg2...")
try:
    import psycopg2
    print("   ✅ psycopg2 importé avec succès")
except ImportError as e:
    print(f"   ❌ Impossible d'importer psycopg2: {e}")
    sys.exit(1)

# Test 2: Connexion simple
print("\n2. Test de connexion basique...")
try:
    conn = psycopg2.connect(
        host="localhost",
        database="mobility_db_clean",
        user="mobility_app",
        password="app_password_123",
        port=5432
    )
    print("   ✅ Connexion PostgreSQL établie")
    
    # Test 3: Requête simple
    print("\n3. Test de requête SQL...")
    cur = conn.cursor()
    cur.execute("SELECT version(), current_database(), current_user;")
    version, db, user = cur.fetchone()
    
    print(f"   ✅ Version: {version.split(',')[0]}")
    print(f"   ✅ Base: {db}")
    print(f"   ✅ Utilisateur: {user}")
    
    # Test 4: Création de table
    print("\n4. Test de création de table...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS test_validation (
            id SERIAL PRIMARY KEY,
            test_name VARCHAR(100),
            result VARCHAR(50),
            test_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        INSERT INTO test_validation (test_name, result) 
        VALUES ('Database Connection', 'PASSED'),
               ('Query Execution', 'PASSED'),
               ('Table Creation', 'PASSED');
    """)
    conn.commit()
    print("   ✅ Table créée et données insérées")
    
    # Test 5: Lecture des données
    print("\n5. Test de lecture des données...")
    cur.execute("SELECT test_name, result FROM test_validation ORDER BY id;")
    tests = cur.fetchall()
    
    print("   ✅ Résultats des tests:")
    for test_name, result in tests:
        print(f"      - {test_name}: {result}")
    
    cur.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS!")
    print("=" * 60)
    print("\nVotre environnement PostgreSQL est maintenant configuré.")
    print("Vous pouvez utiliser ces paramètres dans votre application:")
    print("  - Host: localhost")
    print("  - Database: mobility_db_clean")
    print("  - User: mobility_app")
    print("  - Password: app_password_123")
    print("  - Port: 5432")
    
except Exception as e:
    print(f"\n❌ ERREUR: {e}")
    print("\n💡 Solutions possibles:")
    print("   1. Vérifiez que PostgreSQL est démarré")
    print("   2. Exécutez le script setup_fresh.py d'abord")
    print("   3. Vérifiez les logs PostgreSQL")
    
    sys.exit(1)
'''

# Écrire le fichier de test
test_file = os.path.join(os.getcwd(), 'validate_connection.py')
with open(test_file, 'w', encoding='ascii') as f:
    f.write(final_test)

print(f"   ✅ Fichier de test créé: {test_file}")

# ============================================================================
# FIN
# ============================================================================
print("\n" + "=" * 70)
print("CONFIGURATION TERMINÉE!")
print("=" * 70)
print("\n📋 Prochaines étapes:")
print("   1. Exécutez: python validate_connection.py")
print("   2. Si tout passe, utilisez 'database_connection.py' dans votre app")
print("   3. Mettez à jour vos autres fichiers avec les nouveaux paramètres")
print("\n🔧 Nouveaux paramètres de connexion:")
print("   - Database: mobility_db_clean")
print("   - User: mobility_app")
print("   - Password: app_password_123")
print("\n⚠️  IMPORTANT: N'utilisez plus 'mobility_db' ni 'mobility_user'")
print("   Ces anciens noms semblent corrompus avec des problèmes d'encodage.")
print("=" * 70)