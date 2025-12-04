"""
Gestion de la connexion à la base de données PostgreSQL avec SQLAlchemy
"""
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import logging

logger = logging.getLogger("mobility-service")

# ============================================================================
# CONNEXION EN DUR (pas de settings.py pour éviter problèmes d'encodage)
# ============================================================================
DATABASE_URL = "postgresql://mobility_user:mobility_pass@localhost:5432/mobility_db"

# Création du moteur de base de données
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    echo=False,
    pool_pre_ping=True,
    connect_args={
        "client_encoding": "utf8",
        "options": "-c client_encoding=utf8"
    }
)

# Session locale
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base pour les modèles ORM
Base = declarative_base()

# Événements de logging
@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    logger.info("📊 Connexion PostgreSQL établie")

@event.listens_for(engine, "close")
def receive_close(dbapi_conn, connection_record):
    logger.info("📊 Connexion PostgreSQL fermée")

def get_db() -> Generator[Session, None, None]:
    """Générateur de session DB pour injection de dépendances FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialise la base de données (crée les tables)"""
    from database.models import LigneModel, HoraireModel, EtatTraficModel, DisponibiliteModel
    logger.info("🔧 Création des tables PostgreSQL...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tables créées avec succès")
    except Exception as e:
        logger.error(f"❌ Erreur création tables: {e}")
        raise

def seed_data():
    """Insère les données initiales (mock data)"""
    from database.models import LigneModel, HoraireModel, EtatTraficModel, DisponibiliteModel
    import uuid
    
    db = SessionLocal()
    try:
        # Vérifier si des données existent déjà
        if db.query(LigneModel).count() > 0:
            logger.info("ℹ️  Données déjà présentes, seed ignoré")
            return
        
        logger.info("🌱 Insertion des données initiales...")
        
        # Lignes
        lignes = [
            LigneModel(
                id=str(uuid.uuid4()),
                numero="L1",
                nom="Ligne 1 - Centre Nord",
                type_transport="metro",
                terminus_debut="Gare Centrale",
                terminus_fin="Banlieue Nord",
                actif=True
            ),
            LigneModel(
                id=str(uuid.uuid4()),
                numero="L2",
                nom="Ligne 2 - Est Ouest",
                type_transport="metro",
                terminus_debut="Gare Est",
                terminus_fin="Gare Ouest",
                actif=True
            ),
            LigneModel(
                id=str(uuid.uuid4()),
                numero="B15",
                nom="Bus 15 - Universite",
                type_transport="bus",
                terminus_debut="Centre-Ville",
                terminus_fin="Campus Universitaire",
                actif=True
            ),
            LigneModel(
                id=str(uuid.uuid4()),
                numero="T1",
                nom="Tramway 1 - Cotier",
                type_transport="tramway",
                terminus_debut="Port",
                terminus_fin="Plage Sud",
                actif=True
            ),
        ]
        
        db.add_all(lignes)
        db.commit()
        
        # Récupérer les IDs
        ligne_l1 = db.query(LigneModel).filter(LigneModel.numero == "L1").first()
        ligne_l2 = db.query(LigneModel).filter(LigneModel.numero == "L2").first()
        ligne_b15 = db.query(LigneModel).filter(LigneModel.numero == "B15").first()
        ligne_t1 = db.query(LigneModel).filter(LigneModel.numero == "T1").first()
        
        # Horaires
        horaires = [
            HoraireModel(id=str(uuid.uuid4()), ligne_id=ligne_l1.id, destination="Banlieue Nord", 
                        heure_depart="08:00", heure_arrivee="08:25", station="Gare Centrale", quai="A"),
            HoraireModel(id=str(uuid.uuid4()), ligne_id=ligne_l1.id, destination="Banlieue Nord", 
                        heure_depart="08:15", heure_arrivee="08:40", station="Gare Centrale", quai="A"),
            HoraireModel(id=str(uuid.uuid4()), ligne_id=ligne_l1.id, destination="Gare Centrale", 
                        heure_depart="08:30", heure_arrivee="08:55", station="Banlieue Nord", quai="B"),
            HoraireModel(id=str(uuid.uuid4()), ligne_id=ligne_l2.id, destination="Gare Ouest", 
                        heure_depart="07:50", heure_arrivee="08:15", station="Gare Est", quai="1"),
            HoraireModel(id=str(uuid.uuid4()), ligne_id=ligne_l2.id, destination="Gare Ouest", 
                        heure_depart="08:20", heure_arrivee="08:45", station="Gare Est", quai="1"),
            HoraireModel(id=str(uuid.uuid4()), ligne_id=ligne_b15.id, destination="Campus Universitaire", 
                        heure_depart="08:05", heure_arrivee="08:30", station="Centre-Ville", quai="C"),
            HoraireModel(id=str(uuid.uuid4()), ligne_id=ligne_b15.id, destination="Centre-Ville", 
                        heure_depart="08:35", heure_arrivee="09:00", station="Campus Universitaire", quai="D"),
        ]
        
        db.add_all(horaires)
        
        # États du trafic
        etats = [
            EtatTraficModel(id=str(uuid.uuid4()), ligne_id=ligne_l1.id, statut="normal", 
                           retard_minutes=0, message="Trafic fluide"),
            EtatTraficModel(id=str(uuid.uuid4()), ligne_id=ligne_l2.id, statut="retard", 
                           retard_minutes=5, message="Retard du a un incident technique"),
            EtatTraficModel(id=str(uuid.uuid4()), ligne_id=ligne_b15.id, statut="normal", 
                           retard_minutes=0, message="Circulation normale"),
            EtatTraficModel(id=str(uuid.uuid4()), ligne_id=ligne_t1.id, statut="perturbe", 
                           retard_minutes=10, message="Travaux sur la voie"),
        ]
        
        db.add_all(etats)
        
        # Disponibilités
        dispos = [
            DisponibiliteModel(id=str(uuid.uuid4()), ligne_id=ligne_l1.id, 
                              vehicules_total=20, vehicules_en_service=18, taux_disponibilite=90.0),
            DisponibiliteModel(id=str(uuid.uuid4()), ligne_id=ligne_l2.id, 
                              vehicules_total=15, vehicules_en_service=12, taux_disponibilite=80.0),
            DisponibiliteModel(id=str(uuid.uuid4()), ligne_id=ligne_b15.id, 
                              vehicules_total=10, vehicules_en_service=9, taux_disponibilite=90.0),
            DisponibiliteModel(id=str(uuid.uuid4()), ligne_id=ligne_t1.id, 
                              vehicules_total=8, vehicules_en_service=7, taux_disponibilite=87.5),
        ]
        
        db.add_all(dispos)
        db.commit()
        
        logger.info("✅ Données initiales insérées avec succès")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du seed: {e}")
        db.rollback()
    finally:
        db.close()