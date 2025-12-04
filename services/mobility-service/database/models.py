
"""
Modèles SQLAlchemy (ORM) - Représentation des tables PostgreSQL
"""
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.connection import Base

# ============================================================================
# Table: lignes
# ============================================================================
class LigneModel(Base):
    __tablename__ = "lignes"
    
    id = Column(String(36), primary_key=True)
    numero = Column(String(10), unique=True, nullable=False, index=True)
    nom = Column(String(255), nullable=False)
    type_transport = Column(String(20), nullable=False)
    terminus_debut = Column(String(255), nullable=False)
    terminus_fin = Column(String(255), nullable=False)
    actif = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relations
    horaires = relationship("HoraireModel", back_populates="ligne", cascade="all, delete-orphan")
    etats_trafic = relationship("EtatTraficModel", back_populates="ligne", cascade="all, delete-orphan")
    disponibilites = relationship("DisponibiliteModel", back_populates="ligne", cascade="all, delete-orphan")

# ============================================================================
# Table: horaires
# ============================================================================
class HoraireModel(Base):
    __tablename__ = "horaires"
    
    id = Column(String(36), primary_key=True)
    ligne_id = Column(String(36), ForeignKey("lignes.id", ondelete="CASCADE"), nullable=False, index=True)
    destination = Column(String(255), nullable=False)
    heure_depart = Column(String(5), nullable=False)
    heure_arrivee = Column(String(5), nullable=False)
    station = Column(String(255), nullable=False)
    quai = Column(String(10), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relation
    ligne = relationship("LigneModel", back_populates="horaires")

# ============================================================================
# Table: etats_trafic
# ============================================================================
class EtatTraficModel(Base):
    __tablename__ = "etats_trafic"
    
    id = Column(String(36), primary_key=True)
    ligne_id = Column(String(36), ForeignKey("lignes.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    statut = Column(String(20), nullable=False)
    retard_minutes = Column(Integer, default=0, nullable=False)
    message = Column(Text, default="")
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relation
    ligne = relationship("LigneModel", back_populates="etats_trafic")

# ============================================================================
# Table: disponibilites
# ============================================================================
class DisponibiliteModel(Base):
    __tablename__ = "disponibilites"
    
    id = Column(String(36), primary_key=True)
    ligne_id = Column(String(36), ForeignKey("lignes.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    vehicules_total = Column(Integer, nullable=False)
    vehicules_en_service = Column(Integer, nullable=False)
    taux_disponibilite = Column(Float, nullable=False)
    
    derniere_maj = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relation
    ligne = relationship("LigneModel", back_populates="disponibilites")