# City Views Finder - Cloud Run Deployment Guide

Este documento describe cómo desplegar el agente City Views Finder en Google Cloud Run con un frontend de Streamlit y monitorización completa.

## 📋 Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Arquitectura](#arquitectura)
- [Despliegue Rápido](#despliegue-rápido)
- [Configuración Detallada](#configuración-detallada)
- [Monitorización](#monitorización)
- [Solución de Problemas](#solución-de-problemas)
- [Costos](#costos)

## 🎯 Requisitos Previos

### 1. Google Cloud Setup

- Cuenta de Google Cloud activa
- Proyecto de Google Cloud creado
- Facturación habilitada en el proyecto
- Google Cloud SDK instalado ([Instrucciones](https://cloud.google.com/sdk/docs/install))

### 2. Agente Desplegado

Antes de desplegar el frontend en Cloud Run, debes tener tu agente desplegado en Vertex AI:

```bash
# 1. Despliega el agente primero
python deploy_agent.py

# 2. Verifica que se haya creado agent_resource_name.txt
cat agent_resource_name.txt
```

### 3. Autenticación

```bash
# Autenticarse con gcloud
gcloud auth login

# Configurar el proyecto
gcloud config set project gen-lang-client-0495395701

# Configurar credenciales para Docker
gcloud auth configure-docker
```

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                        Usuario                               │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              Cloud Run (Streamlit Frontend)                  │
│  ┌───────────────────────────────────────────────────┐      │
│  │  streamlit_app.py                                  │      │
│  │  - Interfaz de usuario                             │      │
│  │  - Gestión de sesiones                             │      │
│  │  - Logging estructurado                            │      │
│  └───────────────────────────────────────────────────┘      │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│          Vertex AI Agent Engine                              │
│  ┌───────────────────────────────────────────────────┐      │
│  │  City Views Finder Agent                           │      │
│  │  - Google Search Tool                              │      │
│  │  - URL Context Tool                                │      │
│  └───────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              Cloud Logging & Monitoring                      │
│  - Logs estructurados                                        │
│  - Métricas personalizadas                                   │
│  - Dashboards                                                │
│  - Alertas                                                   │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Despliegue Rápido

### Opción 1: Script Automático (Windows)

```bash
deploy_cloudrun.bat
```

### Opción 2: Script Automático (Linux/Mac)

```bash
chmod +x deploy_cloudrun.sh
./deploy_cloudrun.sh
```

### Opción 3: Paso a Paso Manual

```bash
# 1. Configurar proyecto
export PROJECT_ID="gen-lang-client-0495395701"
export REGION="us-central1"
export SERVICE_NAME="city-views-finder"

gcloud config set project $PROJECT_ID

# 2. Habilitar APIs necesarias
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable logging.googleapis.com
gcloud services enable monitoring.googleapis.com

# 3. Construir imagen Docker
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# 4. Desplegar en Cloud Run
AGENT_RESOURCE_NAME=$(cat agent_resource_name.txt)

gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300s \
  --max-instances 10 \
  --min-instances 0 \
  --allow-unauthenticated \
  --set-env-vars "PROJECT_ID=$PROJECT_ID,LOCATION=$REGION,AGENT_RESOURCE_NAME=$AGENT_RESOURCE_NAME"
```

## ⚙️ Configuración Detallada

### Variables de Entorno

El servicio de Cloud Run utiliza las siguientes variables de entorno:

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `PROJECT_ID` | ID del proyecto de Google Cloud | `gen-lang-client-0495395701` |
| `LOCATION` | Región de Vertex AI | `us-central1` |
| `AGENT_RESOURCE_NAME` | Nombre del recurso del agente desplegado | Leído de `agent_resource_name.txt` |
| `PORT` | Puerto del servidor (configurado por Cloud Run) | `8080` |

### Recursos de Cloud Run

Configuración recomendada:

```yaml
Memoria: 2Gi
CPU: 2
Timeout: 300s (5 minutos)
Concurrency: 80
Max instances: 10
Min instances: 0 (escala a cero)
```

### Personalización de Streamlit

Edita [streamlit_app.py](streamlit_app.py) para personalizar:

- Colores del tema
- Mensajes de bienvenida
- Estructura de la interfaz
- Métricas adicionales

## 📊 Monitorización

### Logs Estructurados

La aplicación genera logs estructurados en formato JSON que se pueden consultar en Cloud Logging:

```json
{
  "event": "user_query",
  "user_id": "user_20260111_143052",
  "message_length": 45,
  "timestamp": "2026-01-11T14:30:52.123456",
  "project_id": "gen-lang-client-0495395701"
}
```

### Tipos de Eventos Registrados

1. **user_query**: Consultas de usuario
2. **agent_response**: Respuestas del agente (incluye tiempo de respuesta)
3. **error**: Errores del sistema

### Ver Logs en Tiempo Real

```bash
# Ver logs recientes
gcloud run logs read city-views-finder --region us-central1 --limit 50

# Seguir logs en tiempo real
gcloud run logs tail city-views-finder --region us-central1
```

### Consultas de Logs Útiles

En la Consola de Cloud Logging, usa estas consultas:

**Todas las consultas de usuario:**
```
resource.type="cloud_run_revision"
jsonPayload.event="user_query"
```

**Errores:**
```
resource.type="cloud_run_revision"
jsonPayload.event="error"
```

**Tiempos de respuesta lentos (>10s):**
```
resource.type="cloud_run_revision"
jsonPayload.event="agent_response"
jsonPayload.response_time_seconds>10
```

### Métricas Personalizadas

El archivo [monitoring_config.yaml](monitoring_config.yaml) define métricas personalizadas:

1. **user_queries_total**: Total de consultas
2. **agent_responses_total**: Total de respuestas
3. **response_time_seconds**: Tiempo de respuesta
4. **errors_total**: Total de errores

### Dashboards

Accede a los dashboards en:
```
https://console.cloud.google.com/monitoring?project=gen-lang-client-0495395701
```

Métricas disponibles:
- Número de solicitudes
- Tiempo de respuesta promedio
- Tasa de errores
- Uso de memoria y CPU
- Instancias activas

### Alertas

Configura alertas para:
- Tasa de errores alta (>10 por minuto)
- Tiempo de respuesta alto (>30 segundos)
- Servicio inactivo (sin solicitudes por 10 minutos)

## 🔧 Solución de Problemas

### Error: "Agent not found"

**Causa**: El agente no está desplegado o el resource name es incorrecto.

**Solución**:
```bash
# Verificar que agent_resource_name.txt existe y tiene contenido válido
cat agent_resource_name.txt

# Re-desplegar el agente si es necesario
python deploy_agent.py
```

### Error: "Permission denied"

**Causa**: Falta de permisos en el proyecto.

**Solución**:
```bash
# Verificar permisos
gcloud projects get-iam-policy gen-lang-client-0495395701

# Otorgar permisos necesarios
gcloud projects add-iam-policy-binding gen-lang-client-0495395701 \
  --member="user:tu-email@gmail.com" \
  --role="roles/run.admin"
```

### Error: "Container failed to start"

**Causa**: Error en la construcción de la imagen o en el código.

**Solución**:
```bash
# Ver logs de Cloud Build
gcloud builds list --limit 5

# Ver logs del último build
gcloud builds log $(gcloud builds list --limit 1 --format="value(id)")

# Probar la imagen localmente
docker build -t city-views-finder .
docker run -p 8080:8080 -e PROJECT_ID=gen-lang-client-0495395701 city-views-finder
```

### Error: "Response timeout"

**Causa**: El agente tarda más de 5 minutos en responder.

**Solución**:
```bash
# Aumentar el timeout
gcloud run services update city-views-finder \
  --region us-central1 \
  --timeout 600s
```

### Problemas de Rendimiento

Si el servicio es lento:

1. **Aumentar recursos**:
```bash
gcloud run services update city-views-finder \
  --region us-central1 \
  --memory 4Gi \
  --cpu 4
```

2. **Configurar instancias mínimas** (evita cold starts):
```bash
gcloud run services update city-views-finder \
  --region us-central1 \
  --min-instances 1
```

## 💰 Costos

### Estimación de Costos Mensuales

**Cloud Run** (tráfico bajo-medio):
- Solicitudes: ~$0.40 por millón de solicitudes
- vCPU: ~$0.024 por vCPU-hora
- Memoria: ~$0.0025 por GB-hora
- **Estimado**: $10-50/mes

**Vertex AI Agent Engine**:
- Depende del uso del agente
- **Estimado**: $20-100/mes

**Cloud Logging**:
- Primeros 50GB/mes gratuitos
- **Estimado**: $0-10/mes

**Total estimado**: **$30-160/mes** (uso moderado)

### Optimizar Costos

1. **Escalar a cero**: Configurar `min-instances=0`
2. **Limitar instancias**: Configurar `max-instances` apropiado
3. **Optimizar logs**: Reducir logs verbosos en producción
4. **Usar budgets**: Configurar alertas de presupuesto

```bash
# Configurar alerta de presupuesto
gcloud billing budgets create \
  --billing-account=BILLING_ACCOUNT_ID \
  --display-name="City Views Finder Budget" \
  --budget-amount=100USD
```

## 🔄 Actualización del Servicio

Para actualizar la aplicación después de hacer cambios:

```bash
# Opción 1: Re-ejecutar el script de despliegue
./deploy_cloudrun.sh

# Opción 2: Despliegue manual rápido
gcloud builds submit --tag gcr.io/$PROJECT_ID/city-views-finder
gcloud run deploy city-views-finder --image gcr.io/$PROJECT_ID/city-views-finder --region us-central1
```

## 🗑️ Eliminar el Servicio

```bash
# Eliminar el servicio de Cloud Run
gcloud run services delete city-views-finder --region us-central1

# Eliminar la imagen de Container Registry
gcloud container images delete gcr.io/gen-lang-client-0495395701/city-views-finder
```

## 📚 Recursos Adicionales

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Vertex AI Agent Builder](https://cloud.google.com/vertex-ai/docs/agent-builder)
- [Cloud Monitoring](https://cloud.google.com/monitoring/docs)

## 🆘 Soporte

Para problemas o preguntas:

1. Revisar los logs: `gcloud run logs read city-views-finder --region us-central1`
2. Consultar la documentación de Google Cloud
3. Revisar el código en [streamlit_app.py](streamlit_app.py)

---

**Autor**: Adri
**Fecha**: 2026-01-11
**Versión**: 1.0
