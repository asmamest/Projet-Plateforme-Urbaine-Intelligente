"""
Gestion de la connexion PostgreSQL
"""
import os
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import logging

logger = logging.getLogger("air-quality-soap")

# URL de la base de données
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://smart_city_user:smart_city_pass@localhost:5432/smart_city_db"
)

# Création du moteur
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    echo=False,
    pool_pre_ping=True,
    connect_args={
        "client_encoding": "utf8",
        "application_name": "air_quality_soap_service"
    }
)

# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles ORM
Base = declarative_base()

@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    logger.info("📊 Connexion PostgreSQL établie")
    dbapi_conn.set_client_encoding('UTF8')

def get_db() -> Generator[Session, None, None]:
    """Générateur de session DB"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialise les tables de la base de données"""
    from database.models import ZoneModel, AirQualityMeasurementModel, PollutantModel
    logger.info("🔧 Création des tables PostgreSQL...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tables créées avec succès")
    except Exception as e:
        logger.error(f"❌ Erreur création tables: {e}")
        raise

def seed_data():
    """Insère les données initiales"""
    from database.models import ZoneModel, AirQualityMeasurementModel, PollutantModel
    import uuid
    from datetime import datetime, timedelta
    
    db = SessionLocal()
    try:
        # Vérifier si des données existent
        if db.query(ZoneModel).count() > 0:
            logger.info("ℹ️  Données déjà présentes, seed ignoré")
            return
        
        logger.info("🌱 Insertion des données initiales...")
        
        # Zones géographiques (partagées avec REST)
        zones = [
            ZoneModel(
                id=str(uuid.uuid4()),
                code="CENTRE",
                nom="Centre-Ville",
                latitude=36.8065,
                longitude=10.1815,
                type_zone="urbain"
            ),
            ZoneModel(
                id=str(uuid.uuid4()),
                code="NORD",
                nom="Quartier Nord",
                latitude=36.8500,
                longitude=10.1900,
                type_zone="residentiel"
            ),
            ZoneModel(
                id=str(uuid.uuid4()),
                code="SUD",
                nom="Zone Industrielle Sud",
                latitude=36.7500,
                longitude=10.1700,
                type_zone="industriel"
            ),
            ZoneModel(
                id=str(uuid.uuid4()),
                code="EST",
                nom="Banlieue Est",
                latitude=36.8100,
                longitude=10.2500,
                type_zone="residentiel"
            ),
        ]
        
        db.add_all(zones)
        db.commit()
        
        # Récupérer les zones
        zone_centre = db.query(ZoneModel).filter(ZoneModel.code == "CENTRE").first()
        zone_nord = db.query(ZoneModel).filter(ZoneModel.code == "NORD").first()
        zone_sud = db.query(ZoneModel).filter(ZoneModel.code == "SUD").first()
        zone_est = db.query(ZoneModel).filter(ZoneModel.code == "EST").first()
        
        # Mesures de qualité de l'air actuelles
        now = datetime.now()
        measurements = [
            # Centre-Ville (qualité moyenne)
            AirQualityMeasurementModel(
                id=str(uuid.uuid4()),
                zone_id=zone_centre.id,
                aqi=75,
                status="MODERATE",
                timestamp=now
            ),
            # Nord (bonne qualité)
            AirQualityMeasurementModel(
                id=str(uuid.uuid4()),
                zone_id=zone_nord.id,
                aqi=45,
                status="GOOD",
                timestamp=now
            ),
            # Sud (mauvaise qualité - zone industrielle)
            AirQualityMeasurementModel(
                id=str(uuid.uuid4()),
                zone_id=zone_sud.id,
                aqi=125,
                status="UNHEALTHY",
                timestamp=now
            ),
            # Est (qualité correcte)
            AirQualityMeasurementModel(
                id=str(uuid.uuid4()),
                zone_id=zone_est.id,
                aqi=60,
                status="MODERATE",
                timestamp=now
            ),
        ]
        
        db.add_all(measurements)
        db.commit()
        
        # Polluants pour chaque zone
        pollutants = []
        
        # Centre-Ville
        pollutants.extend([
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[0].id,
                          nom="PM2.5", valeur=35.5, unite="µg/m³", status="MODERATE"),
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[0].id,
                          nom="PM10", valeur=55.2, unite="µg/m³", status="MODERATE"),
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[0].id,
                          nom="NO2", valeur=42.1, unite="µg/m³", status="OK"),
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[0].id,
                          nom="CO2", valeur=420.0, unite="ppm", status="OK"),
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[0].id,
                          nom="O3", valeur=68.3, unite="µg/m³", status="MODERATE"),
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[0].id,
                          nom="SO2", valeur=12.5, unite="µg/m³", status="OK"),
        ])
        
        # Nord (bonnes valeurs)
        pollutants.extend([
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[1].id,
                          nom="PM2.5", valeur=18.2, unite="µg/m³", status="OK"),
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[1].id,
                          nom="PM10", valeur=28.5, unite="µg/m³", status="OK"),
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[1].id,
                          nom="NO2", valeur=25.3, unite="µg/m³", status="OK"),
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[1].id,
                          nom="CO2", valeur=405.0, unite="ppm", status="OK"),
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[1].id,
                          nom="O3", valeur=45.1, unite="µg/m³", status="OK"),
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[1].id,
                          nom="SO2", valeur=5.2, unite="µg/m³", status="OK"),
        ])
        
        # Sud (valeurs élevées - zone industrielle)
        pollutants.extend([
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[2].id,
                          nom="PM2.5", valeur=85.7, unite="µg/m³", status="ALERT"),
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[2].id,
                          nom="PM10", valeur=125.3, unite="µg/m³", status="ALERT"),
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[2].id,
                          nom="NO2", valeur=95.8, unite="µg/m³", status="ALERT"),
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[2].id,
                          nom="CO2", valeur=550.0, unite="ppm", status="ALERT"),
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[2].id,
                          nom="O3", valeur=125.5, unite="µg/m³", status="ALERT"),
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[2].id,
                          nom="SO2", valeur=45.3, unite="µg/m³", status="ALERT"),
        ])
        
        # Est
        pollutants.extend([
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[3].id,
                          nom="PM2.5", valeur=28.3, unite="µg/m³", status="OK"),
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[3].id,
                          nom="PM10", valeur=42.1, unite="µg/m³", status="OK"),
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[3].id,
                          nom="NO2", valeur=35.7, unite="µg/m³", status="OK"),
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[3].id,
                          nom="CO2", valeur=415.0, unite="ppm", status="OK"),
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[3].id,
                          nom="O3", valeur=55.2, unite="µg/m³", status="MODERATE"),
            PollutantModel(id=str(uuid.uuid4()), measurement_id=measurements[3].id,
                          nom="SO2", valeur=8.5, unite="µg/m³", status="OK"),
        ])
        
        db.add_all(pollutants)
        
        # Données historiques (7 derniers jours)
        for days_ago in range(7):
            date = now - timedelta(days=days_ago)
            
            # Centre-Ville historique
            hist_centre = AirQualityMeasurementModel(
                id=str(uuid.uuid4()),
                zone_id=zone_centre.id,
                aqi=70 + (days_ago * 2),
                status="MODERATE",
                timestamp=date
            )
            db.add(hist_centre)
            
            # Nord historique
            hist_nord = AirQualityMeasurementModel(
                id=str(uuid.uuid4()),
                zone_id=zone_nord.id,
                aqi=40 + days_ago,
                status="GOOD",
                timestamp=date
            )
            db.add(hist_nord)
        
        db.commit()
        logger.info("✅ Données initiales insérées avec succès")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du seed: {e}")
        db.rollback()
        raise
    finally:
        db.close()