"""
Air Quality SOAP Service - Main Entry Point
Serveur SOAP pour la qualité de l'air urbain
"""
import os
import logging
from wsgiref.simple_server import make_server
from spyne import Application, rpc, ServiceBase
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

from models.air_quality_models import (
    AirQualityResult, PollutantList, ZoneComparison,
    HistoricalSeries, HealthStatus
)
from services.air_quality_service import AirQualityServiceImpl
from utils.logger import setup_logger, get_request_logger
from spyne.model.primitive import Unicode, DateTime, Float

logger = setup_logger('main', 'logs/service.log')
service_impl = AirQualityServiceImpl()


class AirQualitySOAPService(ServiceBase):
    """Service SOAP Qualité de l'Air"""
    
    @rpc(Unicode, _returns=AirQualityResult)
    def GetAQI(ctx, zone):
        req_logger = get_request_logger('GetAQI', {'zone': zone})
        req_logger.info(f"Requête GetAQI pour zone: {zone}")
        try:
            result = service_impl.get_aqi(zone)
            req_logger.info(f"Réponse GetAQI: AQI={result.aqi}")
            return result
        except Exception as e:
            req_logger.error(f"Erreur GetAQI: {str(e)}")
            raise
    
    @rpc(Unicode, _returns=PollutantList)
    def GetPollutants(ctx, zone):
        req_logger = get_request_logger('GetPollutants', {'zone': zone})
        req_logger.info(f"Requête GetPollutants pour zone: {zone}")
        try:
            result = service_impl.get_pollutants(zone)
            req_logger.info(f"Réponse GetPollutants: {len(result.pollutants)} polluants")
            return result
        except Exception as e:
            req_logger.error(f"Erreur GetPollutants: {str(e)}")
            raise
    
    @rpc(Unicode, Unicode, _returns=ZoneComparison)
    def CompareZones(ctx, zoneA, zoneB):
        req_logger = get_request_logger('CompareZones', {'zoneA': zoneA, 'zoneB': zoneB})
        req_logger.info(f"Requête CompareZones: {zoneA} vs {zoneB}")
        try:
            result = service_impl.compare_zones(zoneA, zoneB)
            req_logger.info(f"Réponse CompareZones: {result.cleanest_zone}")
            return result
        except Exception as e:
            req_logger.error(f"Erreur CompareZones: {str(e)}")
            raise
    
    @rpc(Unicode, DateTime, DateTime, Unicode, _returns=HistoricalSeries)
    def GetHistory(ctx, zone, startDate, endDate, granularity):
        req_logger = get_request_logger('GetHistory', {
            'zone': zone, 'startDate': str(startDate),
            'endDate': str(endDate), 'granularity': granularity
        })
        req_logger.info(f"Requête GetHistory: {zone}")
        try:
            result = service_impl.get_history(zone, startDate, endDate, granularity)
            req_logger.info(f"Réponse GetHistory: {len(result.data_points)} points")
            return result
        except Exception as e:
            req_logger.error(f"Erreur GetHistory: {str(e)}")
            raise
    
    @rpc(Unicode, Float, _returns=PollutantList)
    def FilterPollutants(ctx, zone, threshold):
        req_logger = get_request_logger('FilterPollutants', {'zone': zone, 'threshold': threshold})
        req_logger.info(f"Requête FilterPollutants: zone={zone}, seuil={threshold}")
        try:
            result = service_impl.filter_pollutants(zone, threshold)
            req_logger.info(f"Réponse FilterPollutants: {len(result.pollutants)} polluants")
            return result
        except Exception as e:
            req_logger.error(f"Erreur FilterPollutants: {str(e)}")
            raise
    
    @rpc(_returns=HealthStatus)
    def HealthCheck(ctx):
        req_logger = get_request_logger('HealthCheck', {})
        req_logger.info("Requête HealthCheck")
        try:
            result = service_impl.health_check()
            req_logger.info(f"Réponse HealthCheck: {result.status}")
            return result
        except Exception as e:
            req_logger.error(f"Erreur HealthCheck: {str(e)}")
            raise


def create_app():
    application = Application(
        [AirQualitySOAPService],
        tns='http://smartcity.air-quality.soap',
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11()
    )
    return WsgiApplication(application)


if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8000))
    
    logger.info(f"Démarrage serveur SOAP sur {host}:{port}")
    logger.info(f"WSDL: http://{host}:{port}/?wsdl")
    
    wsgi_app = create_app()
    server = make_server(host, port, wsgi_app)
    
    try:
        logger.info("Serveur SOAP démarré")
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Arrêt du serveur")
    except Exception as e:
        logger.error(f"Erreur fatale: {str(e)}", exc_info=True)
        raise