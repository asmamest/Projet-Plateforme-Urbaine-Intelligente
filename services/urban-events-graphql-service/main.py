"""
Point d'entrée principal du microservice GraphQL
SOLUTION FINALE - Interface GraphQL sans dépendances externes
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import graphene
import json

from repositories.data_repository import DataRepository
from services.event_service import EventService
from graphql_schemas.queries import Query
from graphql_schemas.mutations import Mutation
from utils.logger import setup_logger
from utils.middleware import GraphQLLoggingMiddleware

# Configuration du logger
logger = setup_logger()

# Initialisation de l'application FastAPI
app = FastAPI(
    title="Urban Events GraphQL Service",
    description="Microservice GraphQL pour la gestion des événements urbains",
    version="1.0.0"
)

# Middleware de logging
app.add_middleware(GraphQLLoggingMiddleware)

# Initialisation repository + service
repository = DataRepository()
event_service = EventService(repository)

# Définition du schéma GraphQL
schema = graphene.Schema(query=Query, mutation=Mutation)


@app.get("/graphql", response_class=HTMLResponse)
async def graphql_ui():
    """Interface GraphQL - 100% fonctionnelle sans CDN externe"""
    return """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GraphQL UI - Urban Events Service</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
            animation: slideIn 0.5s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            min-height: 600px;
        }
        
        .panel {
            padding: 30px;
        }
        
        .left-panel {
            border-right: 3px solid #f0f0f0;
        }
        
        h2 {
            color: #333;
            margin-bottom: 20px;
            font-size: 1.5em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .query-input {
            width: 100%;
            min-height: 350px;
            padding: 20px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-family: 'Courier New', Consolas, monospace;
            font-size: 14px;
            resize: vertical;
            transition: border-color 0.3s;
            background: #f9f9f9;
        }
        
        .query-input:focus {
            outline: none;
            border-color: #667eea;
            background: white;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 35px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            margin-top: 20px;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        }
        
        .btn:active {
            transform: translateY(-1px);
        }
        
        .btn-example {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            padding: 10px 20px;
            font-size: 13px;
            margin: 5px 5px 5px 0;
            display: inline-block;
        }
        
        .examples-section {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #f0f0f0;
        }
        
        .response-container {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 20px;
            border-radius: 10px;
            font-family: 'Courier New', Consolas, monospace;
            font-size: 13px;
            white-space: pre-wrap;
            word-wrap: break-word;
            overflow: auto;
            max-height: 500px;
            min-height: 350px;
            line-height: 1.6;
        }
        
        .status-bar {
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 8px;
            display: none;
            animation: fadeIn 0.3s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .status-success {
            background: #d4edda;
            color: #155724;
            border-left: 5px solid #28a745;
        }
        
        .status-error {
            background: #f8d7da;
            color: #721c24;
            border-left: 5px solid #dc3545;
        }
        
        .status-loading {
            background: #d1ecf1;
            color: #0c5460;
            border-left: 5px solid #17a2b8;
        }
        
        .info-box {
            background: #e7f3ff;
            border-left: 5px solid #2196F3;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }
        
        .info-box strong {
            color: #1976D2;
        }
        
        .json-key { color: #9cdcfe; }
        .json-string { color: #ce9178; }
        .json-number { color: #b5cea8; }
        .json-boolean { color: #569cd6; }
        .json-null { color: #569cd6; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏙️ Urban Events GraphQL Service</h1>
            <p>Interface GraphQL Interactive - API de gestion des événements urbains</p>
        </div>
        
        <div class="main-content">
            <!-- Panneau gauche : Requête -->
            <div class="panel left-panel">
                <h2>📝 Requête GraphQL</h2>
                <textarea id="queryInput" class="query-input" placeholder="Entrez votre requête GraphQL ici...">{
  events {
    id
    name
    priority
    status
    zone {
      name
    }
    eventType {
      name
    }
  }
}</textarea>
                
                <button class="btn" onclick="executeQuery()">
                    ▶️ Exécuter la Requête
                </button>
                
                <div class="examples-section">
                    <h2>💡 Exemples Rapides</h2>
                    <button class="btn btn-example" onclick="loadExample(1)">📋 Tous les événements</button>
                    <button class="btn btn-example" onclick="loadExample(2)">🔴 Événements critiques</button>
                    <button class="btn btn-example" onclick="loadExample(3)">🏘️ Par zone</button>
                    <button class="btn btn-example" onclick="loadExample(4)">➕ Créer événement</button>
                    <button class="btn btn-example" onclick="loadExample(5)">✏️ Mettre à jour</button>
                    <button class="btn btn-example" onclick="loadExample(6)">📍 Toutes les zones</button>
                </div>
                
                <div class="info-box">
                    <strong>💡 Astuce :</strong> Utilisez <code>Ctrl + Enter</code> pour exécuter rapidement votre requête
                </div>
            </div>
            
            <!-- Panneau droit : Résultat -->
            <div class="panel">
                <h2>📊 Résultat</h2>
                <div id="statusBar" class="status-bar"></div>
                <div id="response" class="response-container">Les résultats de votre requête s'afficheront ici...</div>
            </div>
        </div>
    </div>

    <script>
        // Exemples de requêtes
        const examples = {
            1: `query GetAllEvents {
  events {
    id
    name
    description
    priority
    status
    date
    zone {
      id
      name
      description
    }
    eventType {
      id
      name
      description
    }
  }
}`,
            2: `query CriticalEvents {
  events(priority: "CRITICAL", status: "IN_PROGRESS") {
    id
    name
    description
    date
    priority
    status
    zone {
      name
    }
    eventType {
      name
    }
  }
}`,
            3: `query EventsByZone {
  events(zoneId: "zone-1") {
    id
    name
    priority
    status
    date
    zone {
      name
      description
    }
  }
}`,
            4: `mutation CreateEvent {
  createEvent(
    name: "Nouvel accident grave"
    description: "Collision multiple sur l autoroute A1"
    eventTypeId: "type-1"
    zoneId: "zone-1"
    date: "2025-12-06T15:30:00"
    priority: "HIGH"
    status: "IN_PROGRESS"
  ) {
    success
    message
    event {
      id
      name
      priority
      status
      zone {
        name
      }
      eventType {
        name
      }
    }
  }
}`,
            5: `mutation UpdateEvent {
  updateEvent(
    eventId: "event-1"
    status: "RESOLVED"
    priority: "LOW"
  ) {
    success
    message
    event {
      id
      name
      status
      priority
      updatedAt
    }
  }
}`,
            6: `query GetAllZones {
  zones {
    id
    name
    description
  }
}`
        };

        // Charger un exemple
        function loadExample(num) {
            document.getElementById('queryInput').value = examples[num];
            showStatus('Exemple charge ! Cliquez sur Executer pour tester', 'success');
        }

        // Afficher un message de statut
        function showStatus(message, type) {
            const statusBar = document.getElementById('statusBar');
            statusBar.textContent = message;
            statusBar.className = 'status-bar status-' + type;
            statusBar.style.display = 'block';
            
            if (type !== 'loading') {
                setTimeout(function() {
                    statusBar.style.display = 'none';
                }, 4000);
            }
        }

        // Coloration JSON simple
        function formatJSON(json) {
            let formatted = JSON.stringify(json, null, 2);
            formatted = formatted
                .replace(/"([^"]+)":/g, '<span class="json-key">"$1"</span>:')
                .replace(/: "([^"]+)"/g, ': <span class="json-string">"$1"</span>')
                .replace(/: (\d+)/g, ': <span class="json-number">$1</span>')
                .replace(/: (true|false)/g, ': <span class="json-boolean">$1</span>')
                .replace(/: null/g, ': <span class="json-null">null</span>');
            return formatted;
        }

        // Exécuter la requête GraphQL
        async function executeQuery() {
            console.log('Execute query called');
            
            const query = document.getElementById('queryInput').value.trim();
            const responseDiv = document.getElementById('response');
            
            console.log('Query:', query);
            
            if (!query) {
                showStatus('Veuillez entrer une requete GraphQL', 'error');
                return;
            }

            showStatus('Execution en cours...', 'loading');
            responseDiv.textContent = 'Envoi de la requete au serveur...';
            
            try {
                const startTime = Date.now();
                
                console.log('Sending POST request to /graphql');
                
                const response = await fetch('/graphql', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({ query: query })
                });

                console.log('Response received:', response.status);

                const duration = Date.now() - startTime;
                
                if (!response.ok) {
                    throw new Error('HTTP ' + response.status + ': ' + response.statusText);
                }
                
                const result = await response.json();
                console.log('Result:', result);
                
                if (result.errors) {
                    showStatus('Erreur dans la requete (' + duration + 'ms)', 'error');
                    responseDiv.innerHTML = formatJSON(result);
                } else {
                    showStatus('Requete executee avec succes (' + duration + 'ms)', 'success');
                    responseDiv.innerHTML = formatJSON(result);
                }
            } catch (error) {
                console.error('Error:', error);
                showStatus('Erreur de connexion au serveur', 'error');
                responseDiv.textContent = 'Erreur: ' + error.message;
            }
        }

        // Raccourci clavier Ctrl+Enter
        document.getElementById('queryInput').addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                e.preventDefault();
                executeQuery();
            }
        });

        // Message de bienvenue
        console.log('Urban Events GraphQL Service');
        console.log('Interface GraphQL Interactive');
        console.log('Utilisez Ctrl+Enter pour executer vos requetes');
    </script>
</body>
</html>
    """


@app.post("/graphql")
async def graphql_endpoint(request: Request):
    """Endpoint POST pour les requêtes GraphQL"""
    try:
        body = await request.json()
        query = body.get("query")
        variables = body.get("variables")
        operation_name = body.get("operationName")
        
        logger.info(f"GraphQL Query received: {query[:100]}...")
        
        # Exécution de la requête GraphQL
        result = schema.execute(
            query,
            variable_values=variables,
            operation_name=operation_name,
            context_value={"event_service": event_service}
        )
        
        # Préparation de la réponse
        response_data = {"data": result.data}
        if result.errors:
            response_data["errors"] = [
                {"message": str(error), "locations": getattr(error, 'locations', None)}
                for error in result.errors
            ]
            logger.error(f"GraphQL Errors: {result.errors}")
        
        return JSONResponse(response_data)
        
    except Exception as e:
        logger.error(f"GraphQL Error: {str(e)}", exc_info=True)
        return JSONResponse(
            {"errors": [{"message": f"Erreur serveur: {str(e)}"}]},
            status_code=400
        )


@app.get("/health")
async def health_check():
    """Endpoint de healthcheck"""
    return {
        "status": "healthy",
        "service": "urban-events-graphql-service",
        "version": "1.0.0",
        "endpoints": {
            "graphql_ui": "http://localhost:8004/graphql (GET)",
            "graphql_api": "http://localhost:8004/graphql (POST)",
            "health": "http://localhost:8004/health"
        }
    }


@app.get("/")
async def root():
    """Page d'accueil"""
    return {
        "message": "🏙️ Urban Events GraphQL Service",
        "version": "1.0.0",
        "status": "operational",
        "graphql_interface": "http://localhost:8004/graphql",
        "documentation": "Accédez à /graphql pour l'interface interactive"
    }


if __name__ == "__main__":
    import uvicorn
    logger.info("=" * 70)
    logger.info("🚀 Démarrage du service Urban Events GraphQL")
    logger.info("=" * 70)
    logger.info("📍 Interface GraphQL: http://localhost:8004/graphql")
    logger.info("💚 Health Check:      http://localhost:8004/health")
    logger.info("📚 API Docs:          http://localhost:8004/docs")
    logger.info("=" * 70)
    uvicorn.run(app, host="0.0.0.0", port=8004)