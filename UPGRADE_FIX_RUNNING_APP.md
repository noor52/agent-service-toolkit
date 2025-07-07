# 🔧 Upgrade, Fix & Running App Guide

This comprehensive guide covers upgrading dependencies, fixing common issues, and maintaining a running AI Agent Service Toolkit application.

## 📋 Table of Contents

1. [Quick Health Check](#-quick-health-check)
2. [Upgrade Procedures](#-upgrade-procedures)
3. [Common Issues & Fixes](#-common-issues--fixes)
4. [Performance Optimization](#-performance-optimization)
5. [Monitoring & Maintenance](#-monitoring--maintenance)
6. [Emergency Procedures](#-emergency-procedures)

---

## 🩺 Quick Health Check

### **System Status Check**
```bash
# Run comprehensive health check
python -c "
import sys
print(f'Python: {sys.version}')
try:
    import langchain_core
    print(f'✅ LangChain Core: {langchain_core.__version__}')
except ImportError:
    print('❌ LangChain Core: Missing')

try:
    import fastapi
    print(f'✅ FastAPI: {fastapi.__version__}')
except ImportError:
    print('❌ FastAPI: Missing')

try:
    import streamlit
    print(f'✅ Streamlit: {streamlit.__version__}')
except ImportError:
    print('❌ Streamlit: Missing')
"
```

### **Service Health Check**
```bash
# Check if services are running
curl -f http://localhost:8080/health || echo "❌ FastAPI service down"
curl -f http://localhost:8501/healthz || echo "❌ Streamlit app down"

# Check database connectivity
python -c "
from memory import initialize_database
import asyncio
async def test_db():
    try:
        async with initialize_database() as db:
            print('✅ Database connection successful')
    except Exception as e:
        print(f'❌ Database error: {e}')
asyncio.run(test_db())
"
```

---

## 🚀 Upgrade Procedures

### **1. Dependency Upgrades**

#### **Safe Upgrade (Recommended)**
```bash
# 1. Backup current environment
cp uv.lock uv.lock.backup
cp pyproject.toml pyproject.toml.backup

# 2. Update UV package manager
pip install --upgrade uv

# 3. Update dependencies (respects version constraints)
uv sync --upgrade

# 4. Test the upgrade
python -m pytest tests/ -v

# 5. If tests pass, commit changes
git add uv.lock pyproject.toml
git commit -m "chore: upgrade dependencies"
```

#### **Major Version Upgrade**
```bash
# 1. Check for breaking changes
uv tree | grep -E "(langchain|langgraph|fastapi|streamlit)"

# 2. Update pyproject.toml manually for major versions
# Edit version constraints in pyproject.toml

# 3. Regenerate lock file
rm uv.lock
uv sync

# 4. Run comprehensive tests
python -m pytest tests/ -v --cov=src/

# 5. Test manually with different agents
python src/run_client.py
```

### **2. LangChain/LangGraph Upgrades**

#### **LangGraph Version Migration**
```bash
# Check current LangGraph version
python -c "import langgraph; print(langgraph.__version__)"

# Upgrade to latest compatible version
uv add "langgraph>=0.3.5,<0.4.0"

# Update agent code for new features
# Check: https://langchain-ai.github.io/langgraph/concepts/
```

#### **Breaking Changes Checklist**
- [ ] Check agent state schema changes
- [ ] Verify streaming API compatibility
- [ ] Test interrupt functionality
- [ ] Validate memory/store integration
- [ ] Update tool calling patterns

### **3. Model Provider Updates**

#### **Add New Model Provider**
```bash
# 1. Install provider package
uv add langchain-newprovider

# 2. Update models.py
# Add new provider enum and model names

# 3. Update llm.py
# Add model initialization logic

# 4. Update settings.py
# Add provider configuration

# 5. Test new provider
python -c "
from core.llm import get_model
from schema.models import NewProviderModelName
model = get_model(NewProviderModelName.MODEL_NAME)
print('✅ New provider working')
"
```

#### **Update Existing Provider Models**
```bash
# 1. Check provider documentation for new models
# 2. Update schema/models.py with new model names
# 3. Test new models
python src/run_client.py
# Try: "Use model: new-model-name"
```

---

## 🔧 Common Issues & Fixes

### **1. Dependency Conflicts**

#### **Issue**: `uv sync` fails with dependency conflicts
```bash
# Solution 1: Clear cache and retry
uv cache clean
uv sync --frozen

# Solution 2: Resolve conflicts manually
uv tree --show-conflicts
# Edit pyproject.toml to resolve version conflicts

# Solution 3: Fresh environment
rm -rf .venv
uv sync
```

#### **Issue**: Import errors after upgrade
```bash
# Solution: Reinstall problematic packages
uv remove langchain-anthropic
uv add langchain-anthropic

# Or reinstall all
rm -rf .venv uv.lock
uv sync
```

### **2. Database Issues**

#### **Issue**: Database connection failures
```bash
# PostgreSQL fix
# 1. Check connection string
echo $POSTGRES_HOST $POSTGRES_PORT $POSTGRES_DB

# 2. Test connection
psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT 1;"

# 3. Reset database
docker compose down postgres
docker volume rm agent-service-toolkit_postgres_data
docker compose up postgres -d
```

#### **Issue**: SQLite corruption
```bash
# Fix corrupted SQLite database
rm checkpoints.db
# Database will be recreated automatically
```

#### **Issue**: MongoDB connection problems
```bash
# Check MongoDB status
docker compose logs mongo

# Reset MongoDB
docker compose down mongo
docker volume rm agent-service-toolkit_mongo_data
docker compose up mongo -d
```

### **3. Performance Issues**

#### **Issue**: Slow response times
```bash
# 1. Check system resources
htop  # or top on macOS
docker stats  # if using Docker

# 2. Enable performance monitoring
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_PROJECT=performance-debug

# 3. Profile slow endpoints
python -m cProfile -o profile.stats src/run_service.py
```

#### **Issue**: Memory leaks
```bash
# 1. Monitor memory usage
python -c "
import psutil
import time
process = psutil.Process()
for i in range(10):
    print(f'Memory: {process.memory_info().rss / 1024 / 1024:.1f} MB')
    time.sleep(1)
"

# 2. Check for unclosed resources
# Look for database connections, HTTP clients not properly closed

# 3. Restart services periodically
# Add health checks and auto-restart logic
```

### **4. Streaming Issues**

#### **Issue**: Streaming stops working
```bash
# 1. Check client connection
curl -N http://localhost:8080/research-assistant/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "test", "stream_tokens": true}'

# 2. Verify SSE format
# Look for proper "data: " prefix and "\n\n" endings

# 3. Check for blocking operations
# Ensure all agent operations are async
```

#### **Issue**: Token streaming delays
```bash
# 1. Check model provider settings
# Ensure streaming=True in model configuration

# 2. Verify network latency
ping api.openai.com  # or relevant provider

# 3. Check buffer settings
# Some providers buffer tokens before sending
```

---

## ⚡ Performance Optimization

### **1. Application Performance**

#### **FastAPI Optimizations**
```python
# Add to service/service.py
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Enable async database operations
# Ensure all database calls use async methods
```

#### **Memory Optimization**
```bash
# 1. Limit conversation history
# Set max_messages in agent configuration

# 2. Use connection pooling
# Configure database connection pools

# 3. Enable garbage collection
export PYTHONOPTIMIZE=1
```

#### **Caching Strategies**
```python
# Add model caching
from functools import lru_cache

@lru_cache(maxsize=10)
def get_cached_model(model_name):
    return get_model(model_name)
```

### **2. Database Performance**

#### **PostgreSQL Optimization**
```sql
-- Add indexes for common queries
CREATE INDEX idx_checkpoints_thread_id ON checkpoints(thread_id);
CREATE INDEX idx_checkpoints_created_at ON checkpoints(created_at);

-- Optimize connection pool
-- In .env file:
POSTGRES_POOL_SIZE=20
POSTGRES_MAX_OVERFLOW=30
```

#### **SQLite Optimization**
```bash
# Use WAL mode for better concurrency
sqlite3 checkpoints.db "PRAGMA journal_mode=WAL;"
sqlite3 checkpoints.db "PRAGMA synchronous=NORMAL;"
sqlite3 checkpoints.db "PRAGMA cache_size=10000;"
```

### **3. Docker Performance**

#### **Optimize Docker Images**
```dockerfile
# Use multi-stage builds
FROM python:3.12-slim as builder
# ... build stage

FROM python:3.12-slim as runtime
# ... runtime stage with minimal dependencies
```

#### **Resource Limits**
```yaml
# In compose.yaml
services:
  agent_service:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
        reservations:
          memory: 512M
          cpus: '0.25'
```

---

## 📊 Monitoring & Maintenance

### **1. Health Monitoring**

#### **Automated Health Checks**
```bash
#!/bin/bash
# health_check.sh
set -e

echo "🔍 Checking service health..."

# Check FastAPI
if curl -f -s http://localhost:8080/health > /dev/null; then
    echo "✅ FastAPI service healthy"
else
    echo "❌ FastAPI service unhealthy"
    exit 1
fi

# Check Streamlit
if curl -f -s http://localhost:8501/healthz > /dev/null; then
    echo "✅ Streamlit app healthy"
else
    echo "❌ Streamlit app unhealthy"
    exit 1
fi

# Check database
python -c "
from memory import initialize_database
import asyncio
async def check():
    async with initialize_database() as db:
        pass
asyncio.run(check())
print('✅ Database healthy')
"

echo "🎉 All services healthy!"
```

#### **Performance Monitoring**
```python
# Add to service/service.py
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### **2. Log Management**

#### **Structured Logging**
```python
# Add to core/settings.py
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        return json.dumps(log_entry)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```

#### **Log Rotation**
```bash
# Setup logrotate (Linux/macOS)
sudo tee /etc/logrotate.d/agent-service << EOF
/var/log/agent-service/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 www-data www-data
}
EOF
```

### **3. Backup Procedures**

#### **Database Backup**
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)

# PostgreSQL backup
pg_dump -h $POSTGRES_HOST -U $POSTGRES_USER $POSTGRES_DB > backup_${DATE}.sql

# SQLite backup
cp checkpoints.db backup_checkpoints_${DATE}.db

# Compress and store
tar -czf backup_${DATE}.tar.gz backup_${DATE}.sql backup_checkpoints_${DATE}.db
rm backup_${DATE}.sql backup_checkpoints_${DATE}.db

echo "✅ Backup completed: backup_${DATE}.tar.gz"
```

#### **Configuration Backup**
```bash
# Backup configuration files
tar -czf config_backup_$(date +%Y%m%d).tar.gz \
    .env \
    pyproject.toml \
    uv.lock \
    compose.yaml \
    docker/
```

---

## 🚨 Emergency Procedures

### **1. Service Recovery**

#### **Quick Restart**
```bash
# Docker environment
docker compose restart

# Local environment
pkill -f "python src/run_service.py"
pkill -f "streamlit run"
python src/run_service.py &
streamlit run src/streamlit_app.py &
```

#### **Full Reset**
```bash
# 1. Stop all services
docker compose down
pkill -f python

# 2. Clean environment
rm -rf .venv
docker system prune -f

# 3. Rebuild from scratch
uv sync
docker compose up --build
```

### **2. Data Recovery**

#### **Restore from Backup**
```bash
# PostgreSQL restore
psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB < backup_20250101_120000.sql

# SQLite restore
cp backup_checkpoints_20250101_120000.db checkpoints.db
```

#### **Partial Data Recovery**
```bash
# Export specific thread data
python -c "
from memory import initialize_database
import asyncio
async def export_thread(thread_id):
    async with initialize_database() as db:
        # Export specific thread data
        pass
asyncio.run(export_thread('thread-id-here'))
"
```

### **3. Rollback Procedures**

#### **Dependency Rollback**
```bash
# Restore previous lock file
cp uv.lock.backup uv.lock
uv sync --frozen

# Or rollback to specific commit
git checkout HEAD~1 -- uv.lock pyproject.toml
uv sync --frozen
```

#### **Database Schema Rollback**
```bash
# If using migrations, rollback to previous version
# This depends on your migration system
```

---

## 🔄 Maintenance Schedule

### **Daily Tasks**
- [ ] Check service health
- [ ] Monitor error logs
- [ ] Verify backup completion

### **Weekly Tasks**
- [ ] Update dependencies (patch versions)
- [ ] Review performance metrics
- [ ] Clean up old logs
- [ ] Test backup restoration

### **Monthly Tasks**
- [ ] Security updates
- [ ] Performance optimization review
- [ ] Capacity planning
- [ ] Documentation updates

### **Quarterly Tasks**
- [ ] Major dependency upgrades
- [ ] Security audit
- [ ] Disaster recovery testing
- [ ] Performance benchmarking

---

## 📞 Support & Troubleshooting

### **Getting Help**
1. **Check logs**: Always start with application logs
2. **GitHub Issues**: https://github.com/JoshuaC215/agent-service-toolkit/issues
3. **Documentation**: Review README and troubleshooting guides
4. **Community**: Join discussions and ask questions

### **Reporting Issues**
When reporting issues, include:
- [ ] Python version
- [ ] Operating system
- [ ] Error messages (full traceback)
- [ ] Steps to reproduce
- [ ] Configuration (sanitized)
- [ ] Recent changes made

---

**Last Updated**: January 2025  
**Version**: 0.1.0  
**Maintainer**: AI Agent Service Toolkit Team