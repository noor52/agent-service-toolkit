# 🤖 Default Model Configuration Guide

This document explains the optimal model configuration for different use cases and provides step-by-step instructions for switching between models.

## 🎯 Recommended Default Model: FAKE MODEL

### Why Fake Model is Perfect for Development

```bash
# In .env file
USE_FAKE_MODEL=true
DEFAULT_MODEL=fake
```

**Benefits:**
- ✅ **Zero Cost**: No API charges during development
- ✅ **Instant Response**: No network latency
- ✅ **Consistent Output**: Predictable responses for testing
- ✅ **No Rate Limits**: Unlimited requests
- ✅ **Offline Development**: Works without internet
- ✅ **No API Keys Required**: Start coding immediately

**Perfect For:**
- Initial setup and testing
- Agent development and debugging
- UI/UX development
- Integration testing
- Learning the framework

## 🔄 Model Switching Guide

### 1. Development → Production Transition

#### Step 1: Add API Key
```bash
# Edit .env file
OPENAI_API_KEY=sk-your-actual-key-here
```

#### Step 2: Switch Model
```bash
# In .env file, change:
USE_FAKE_MODEL=false
DEFAULT_MODEL=gpt-4o-mini
```

#### Step 3: Restart Services
```bash
# Stop current services (Ctrl+C)
# Then restart:
python src/run_service.py
streamlit run src/streamlit_app.py
```

### 2. Model Provider Comparison

| Provider | Best Model | Cost | Speed | Quality | Use Case |
|----------|------------|------|-------|---------|----------|
| **OpenAI** | `gpt-4o-mini` | Low | Fast | High | General development |
| **OpenAI** | `gpt-4o` | High | Medium | Highest | Production apps |
| **Anthropic** | `claude-3-haiku` | Low | Fast | High | Cost-effective |
| **Anthropic** | `claude-3.5-sonnet` | Medium | Medium | Highest | Complex reasoning |
| **Google** | `gemini-2.0-flash` | Low | Very Fast | High | Speed-critical apps |
| **Groq** | `llama-3.1-8b` | Very Low | Very Fast | Good | High-throughput |
| **Fake** | `fake` | Free | Instant | N/A | Development only |

## 🛠️ Configuration Examples

### Example 1: Cost-Optimized Development
```bash
# .env configuration
USE_FAKE_MODEL=false
DEFAULT_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-your-key-here

# Features:
# - Real AI responses
# - Low cost (~$0.15/1M tokens)
# - Good for most development tasks
```

### Example 2: High-Quality Production
```bash
# .env configuration
USE_FAKE_MODEL=false
DEFAULT_MODEL=claude-3.5-sonnet
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Features:
# - Highest quality responses
# - Best reasoning capabilities
# - Ideal for production applications
```

### Example 3: Speed-Optimized
```bash
# .env configuration
USE_FAKE_MODEL=false
DEFAULT_MODEL=llama-3.1-8b
GROQ_API_KEY=gsk-your-key-here

# Features:
# - Ultra-fast responses
# - Very low cost
# - Great for high-throughput applications
```

### Example 4: Multi-Provider Setup
```bash
# .env configuration - All providers available
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
GOOGLE_API_KEY=your-google-key
GROQ_API_KEY=gsk-your-groq-key

DEFAULT_MODEL=gpt-4o-mini

# Users can switch models in the Streamlit UI
```

## 🎛️ Runtime Model Switching

### In Streamlit App
1. Open sidebar settings
2. Select different model from dropdown
3. Model applies to new conversations

### Via API
```bash
curl -X POST http://localhost:8080/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello",
    "model": "claude-3.5-sonnet"
  }'
```

### In Python Client
```python
from client import AgentClient

client = AgentClient()
response = client.invoke(
    "Hello, world!",
    model="gpt-4o"  # Override default model
)
```

## 🔧 Advanced Configuration

### Model-Specific Settings

#### OpenAI Configuration
```bash
# .env file
OPENAI_API_KEY=sk-your-key
DEFAULT_MODEL=gpt-4o-mini

# Optional: Azure OpenAI
AZURE_OPENAI_API_KEY=your-azure-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_DEPLOYMENT_MAP={"gpt-4o": "your-deployment-name"}
```

#### Anthropic Configuration
```bash
# .env file
ANTHROPIC_API_KEY=sk-ant-your-key
DEFAULT_MODEL=claude-3-haiku
```

#### Google Configuration
```bash
# .env file
# Option 1: Gemini API
GOOGLE_API_KEY=your-google-api-key
DEFAULT_MODEL=gemini-2.0-flash

# Option 2: Vertex AI
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
DEFAULT_MODEL=gemini-2.0-flash
```

#### Local Models (Ollama)
```bash
# .env file
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434  # if needed
DEFAULT_MODEL=ollama
```

### Custom Model Configuration

#### Add New Provider
1. **Update `schema/models.py`**:
```python
class NewProviderModelName(StrEnum):
    NEW_MODEL = "new-model-name"
```

2. **Update `core/llm.py`**:
```python
if model_name in NewProviderModelName:
    return NewProviderChatModel(
        model=api_model_name,
        temperature=0.5,
        streaming=True
    )
```

3. **Update `core/settings.py`**:
```python
case Provider.NEW_PROVIDER:
    if self.DEFAULT_MODEL is None:
        self.DEFAULT_MODEL = NewProviderModelName.NEW_MODEL
    self.AVAILABLE_MODELS.update(set(NewProviderModelName))
```

## 📊 Performance Comparison

### Response Time Benchmarks
```
Fake Model:     ~1ms    (instant)
Groq Llama:     ~50ms   (very fast)
OpenAI GPT-4o:  ~200ms  (fast)
Claude Sonnet:  ~300ms  (medium)
Gemini Flash:   ~150ms  (fast)
```

### Cost Comparison (per 1M tokens)
```
Fake Model:     $0.00   (free)
GPT-4o-mini:    $0.15   (very cheap)
Claude Haiku:   $0.25   (cheap)
Gemini Flash:   $0.075  (very cheap)
Groq Llama:     $0.05   (very cheap)
GPT-4o:         $2.50   (expensive)
Claude Sonnet:  $3.00   (expensive)
```

## 🚀 Production Recommendations

### For Different Use Cases

#### **Chatbots & Customer Service**
```bash
DEFAULT_MODEL=gpt-4o-mini
# Good balance of cost, speed, and quality
```

#### **Content Generation**
```bash
DEFAULT_MODEL=claude-3.5-sonnet
# Best for creative and long-form content
```

#### **Code Generation**
```bash
DEFAULT_MODEL=gpt-4o
# Excellent for programming tasks
```

#### **High-Volume Applications**
```bash
DEFAULT_MODEL=llama-3.1-8b  # via Groq
# Ultra-fast and cost-effective
```

#### **Research & Analysis**
```bash
DEFAULT_MODEL=claude-3.5-sonnet
# Best reasoning and analysis capabilities
```

## 🔍 Monitoring & Optimization

### Track Model Performance
```bash
# Enable tracing in .env
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-key
LANGCHAIN_PROJECT=model-comparison
```

### A/B Testing Models
```python
# In your application
models_to_test = ["gpt-4o-mini", "claude-3-haiku", "gemini-2.0-flash"]
for model in models_to_test:
    response = client.invoke("Test prompt", model=model)
    # Log performance metrics
```

## 🎯 Quick Decision Matrix

**Choose FAKE MODEL if:**
- ✅ Just starting development
- ✅ Testing UI/UX
- ✅ Learning the framework
- ✅ No budget for API calls

**Choose GPT-4O-MINI if:**
- ✅ Need real AI responses
- ✅ Budget-conscious
- ✅ General-purpose application
- ✅ Good balance of all factors

**Choose CLAUDE-3.5-SONNET if:**
- ✅ Need highest quality
- ✅ Complex reasoning tasks
- ✅ Content generation
- ✅ Budget allows premium model

**Choose GROQ LLAMA if:**
- ✅ Speed is critical
- ✅ High-volume application
- ✅ Cost optimization priority
- ✅ Simple tasks

---

**🎯 Recommendation**: Start with FAKE MODEL for development, then switch to GPT-4O-MINI for production testing, and finally choose the best model based on your specific needs and budget.