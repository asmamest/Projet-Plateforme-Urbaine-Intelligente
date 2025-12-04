"""
Client de test SOAP utilisant zeep
"""
from zeep import Client
from zeep.transports import Transport
from requests import Session
from datetime import datetime, timedelta


def test_soap_service():
    """
    Tester toutes les méthodes du service SOAP
    """
    # Configuration
    wsdl_url = 'http://localhost:8000/?wsdl'
    
    session = Session()
    session.verify = False
    transport = Transport(session=session)
    
    try:
        client = Client(wsdl_url, transport=transport)
        print("✓ Connexion au service SOAP réussie")
        print(f"  WSDL: {wsdl_url}\n")
        
        # Test 1: GetAQI
        print("=" * 60)
        print("Test 1: GetAQI")
        print("=" * 60)
        result = client.service.GetAQI(zone='downtown')
        print(f"Zone: {result.zone}")
        print(f"AQI: {result.aqi}")
        print(f"Catégorie: {result.category}")
        print(f"Description: {result.description}")
        print(f"Timestamp: {result.timestamp}\n")
        
        # Test 2: GetPollutants
        print("=" * 60)
        print("Test 2: GetPollutants")
        print("=" * 60)
        result = client.service.GetPollutants(zone='industrial')
        print(f"Zone: {result.zone}")
        print(f"Nombre de polluants: {len(result.pollutants)}")
        for pollutant in result.pollutants:
            print(f"  - {pollutant.name}: {pollutant.value} {pollutant.unit} ({pollutant.status})")
        print()
        
        # Test 3: CompareZones
        print("=" * 60)
        print("Test 3: CompareZones")
        print("=" * 60)
        result = client.service.CompareZones(zoneA='park', zoneB='industrial')
        print(f"Zone A: {result.zoneA} (AQI: {result.aqiA})")
        print(f"Zone B: {result.zoneB} (AQI: {result.aqiB})")
        print(f"Zone la plus propre: {result.cleanest_zone}")
        print(f"Différence: {result.difference}")
        print(f"Recommandations: {result.recommendations}\n")
        
        # Test 4: GetHistory
        print("=" * 60)
        print("Test 4: GetHistory")
        print("=" * 60)
        start_date = datetime.now() - timedelta(days=3)
        end_date = datetime.now()
        result = client.service.GetHistory(
            zone='downtown',
            startDate=start_date,
            endDate=end_date,
            granularity='daily'
        )
        print(f"Zone: {result.zone}")
        print(f"Période: {result.start_date} à {result.end_date}")
        print(f"Granularité: {result.granularity}")
        print(f"Nombre de points: {len(result.data_points)}")
        if result.data_points:
            print(f"Premier point: AQI={result.data_points[0].aqi}, PM2.5={result.data_points[0].pm25}")
        print()
        
        # Test 5: FilterPollutants
        print("=" * 60)
        print("Test 5: FilterPollutants")
        print("=" * 60)
        result = client.service.FilterPollutants(zone='industrial', threshold=50.0)
        print(f"Zone: {result.zone}")
        print(f"Seuil: 50.0")
        print(f"Polluants au-dessus du seuil: {len(result.pollutants)}")
        for pollutant in result.pollutants:
            print(f"  - {pollutant.name}: {pollutant.value} {pollutant.unit}")
        print()
        
        # Test 6: HealthCheck
        print("=" * 60)
        print("Test 6: HealthCheck")
        print("=" * 60)
        result = client.service.HealthCheck()
        print(f"Status: {result.status}")
        print(f"Version: {result.version}")
        print(f"Uptime: {result.uptime_seconds} secondes")
        print(f"Database: {result.database_status}")
        print(f"Last check: {result.last_check}\n")
        
        print("=" * 60)
        print("✓ Tous les tests passés avec succès!")
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    test_soap_service()