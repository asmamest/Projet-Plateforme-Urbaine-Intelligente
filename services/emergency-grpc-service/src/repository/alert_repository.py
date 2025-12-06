"""
Repository pour la gestion des alertes (Pattern Repository)
"""
from typing import Dict, List, Optional
from datetime import datetime
from threading import Lock
from collections import defaultdict

from src.models.alert import Alert, AlertType, Priority, AlertStatus, Location


class AlertRepository:
    """
    Repository thread-safe pour la gestion des alertes
    Facilite la migration vers PostgreSQL/MongoDB
    """
    
    def __init__(self):
        self._alerts: Dict[str, Alert] = {}
        self._lock = Lock()
        # Indexes pour recherche rapide O(1)
        self._zone_index: Dict[str, set] = defaultdict(set)
        self._status_index: Dict[AlertStatus, set] = defaultdict(set)
        self._initialize_mock_data()
    
    def _initialize_mock_data(self):
        """Initialise des données mockées"""
        # Mock data pour tests
        mock_alerts = [
            Alert(
                alert_type=AlertType.FIRE,
                description="Incendie dans un immeuble résidentiel de 5 étages",
                location=Location(48.8566, 2.3522, "123 Rue de Rivoli", "Paris", "Zone Centre"),
                priority=Priority.CRITICAL,
                reporter_name="Jean Dupont",
                reporter_phone="+33612345678",
                affected_people=15,
                status=AlertStatus.IN_PROGRESS,
                assigned_team="Pompiers Caserne 5"
            ),
            Alert(
                alert_type=AlertType.ACCIDENT,
                description="Collision entre deux véhicules sur l'autoroute A1",
                location=Location(48.9200, 2.4200, "Autoroute A1 KM 45", "Saint-Denis", "Zone Nord"),
                priority=Priority.HIGH,
                reporter_name="Marie Martin",
                reporter_phone="+33623456789",
                affected_people=3,
                status=AlertStatus.PENDING
            ),
            Alert(
                alert_type=AlertType.MEDICAL_EMERGENCY,
                description="Patient en arrêt cardiaque, RCP en cours",
                location=Location(48.7800, 2.3300, "45 Avenue Victor Hugo", "Montrouge", "Zone Sud"),
                priority=Priority.CRITICAL,
                reporter_name="Pierre Durant",
                reporter_phone="+33634567890",
                affected_people=1,
                status=AlertStatus.IN_PROGRESS,
                assigned_team="SAMU 92"
            )
        ]
        
        for alert in mock_alerts:
            self.create(alert)
    
    def create(self, alert: Alert) -> Alert:
        """Crée une nouvelle alerte"""
        with self._lock:
            self._alerts[alert.alert_id] = alert
            # Mise à jour des indexes
            self._zone_index[alert.location.zone].add(alert.alert_id)
            self._status_index[alert.status].add(alert.alert_id)
            return alert
    
    def get_by_id(self, alert_id: str) -> Optional[Alert]:
        """Récupère une alerte par son ID"""
        return self._alerts.get(alert_id)
    
    def update(self, alert: Alert) -> Alert:
        """Met à jour une alerte"""
        with self._lock:
            old_alert = self._alerts.get(alert.alert_id)
            if old_alert and old_alert.status != alert.status:
                # Mettre à jour l'index de statut
                self._status_index[old_alert.status].discard(alert.alert_id)
                self._status_index[alert.status].add(alert.alert_id)
            
            self._alerts[alert.alert_id] = alert
            return alert
    
    def get_active_by_zone(
        self,
        zone: str,
        alert_type: Optional[AlertType] = None,
        min_priority: Optional[Priority] = None
    ) -> List[Alert]:
        """Récupère les alertes actives d'une zone avec filtres"""
        alert_ids = self._zone_index.get(zone, set())
        alerts = [self._alerts[aid] for aid in alert_ids if aid in self._alerts]
        
        # Filtrer par statut actif
        alerts = [a for a in alerts if a.status in [AlertStatus.PENDING, AlertStatus.IN_PROGRESS]]
        
        # Filtrer par type
        if alert_type:
            alerts = [a for a in alerts if a.alert_type == alert_type]
        
        # Filtrer par priorité minimale
        if min_priority:
            alerts = [a for a in alerts if a.priority.value >= min_priority.value]
        
        # Tri par priorité décroissante puis date décroissante
        alerts.sort(key=lambda a: (-a.priority.value, -a.created_at.timestamp()))
        
        return alerts
    
    def get_history(
        self,
        zone: Optional[str] = None,
        alert_type: Optional[AlertType] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Alert]:
        """Récupère l'historique des alertes avec filtres"""
        alerts = list(self._alerts.values())
        
        # Filtres
        if zone:
            alerts = [a for a in alerts if a.location.zone == zone]
        if alert_type:
            alerts = [a for a in alerts if a.alert_type == alert_type]
        if start_date:
            alerts = [a for a in alerts if a.created_at >= start_date]
        if end_date:
            alerts = [a for a in alerts if a.created_at <= end_date]
        
        # Tri chronologique décroissant
        alerts.sort(key=lambda a: a.created_at, reverse=True)
        
        return alerts[:limit]
    
    def get_statistics(
        self,
        zone: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, int]:
        """Génère des statistiques agrégées"""
        alerts = self.get_history(zone, None, start_date, end_date, limit=10000)
        
        stats = {
            "total": len(alerts),
            "pending": 0,
            "in_progress": 0,
            "resolved": 0,
            "cancelled": 0
        }
        
        # Compter par statut
        for alert in alerts:
            stats[alert.status.value.lower()] = stats.get(alert.status.value.lower(), 0) + 1
        
        # Compter par type
        for alert in alerts:
            key = f"type_{alert.alert_type.value.lower()}"
            stats[key] = stats.get(key, 0) + 1
        
        return stats
    
    def get_all(self) -> List[Alert]:
        """Récupère toutes les alertes"""
        return list(self._alerts.values())
    
    def delete(self, alert_id: str) -> bool:
        """Supprime une alerte"""
        with self._lock:
            alert = self._alerts.pop(alert_id, None)
            if alert:
                self._zone_index[alert.location.zone].discard(alert_id)
                self._status_index[alert.status].discard(alert_id)
                return True
            return False