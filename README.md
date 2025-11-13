# CORA Customer Agent 🤖

<div align="center">

**An intelligent AI-powered customer support agent for enhanced e-commerce experiences**

![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1E88E5?style=for-the-badge&logo=chainlink&logoColor=white)
![LangSmith](https://img.shields.io/badge/LangSmith-FFE766?style=for-the-badge&logo=chainlink&logoColor=black)
![Hugging Face](https://img.shields.io/badge/HuggingFace-FFCC00?style=for-the-badge&logo=huggingface&logoColor=black)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-FF6B6B?style=for-the-badge&logo=protocol&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-FF7C00?style=for-the-badge&logo=gradio&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6584?style=for-the-badge&logo=chromadb&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)


</div>

---

## 🎯 Project Overview

**CORA (Customer-Oriented Responsive Assistant)** is a prototype AI agent designed for **TechHive**, a simulated e-commerce company specializing in smart home devices, gaming hardware, and computer technology. This project demonstrates how modern AI technologies can revolutionize customer service by automating repetitive inquiries, providing instant product information, and delivering personalized support experiences.

The goal is to improve customer satisfaction while reducing support team workload by intelligently handling common questions.

---

## ✨ Key Features

### 🧠 Agentic AI with LangChain & Ollama
- **Tool-Calling Agents** - Autonomous decision-making to route queries to appropriate data sources
- **Local LLM Inference** - Privacy-focused, cost-effective inference using Ollama
- **Flexible Model Support** - Compatible with any Ollama model that supports tool calling
- **Configurable Parameters** - Fine-tune temperature, top-p, top-k, and context windows

### 📚 Retrieval-Augmented Generation (RAG)
- **Vector Database** - ChromaDB stores vectorized company FAQs and product catalogs
- **Semantic Search** - Retrieves relevant information based on query similarity
- **Dual Knowledge Bases** - Separate collections for FAQ and product information
- **Threshold-Based Filtering** - Only returns results exceeding configurable relevance scores

### 🔌 Model Context Protocol (MCP)
- **FastMCP Server** - Exposes two tools for FAQ and product information retrieval
- **Async Tool Execution** - Non-blocking operations for efficient query handling
- **Standardized Interface** - Clean separation between agent logic and data access

### 👤 Dynamic System Prompts
- **Personalized Greetings** - Addresses users by name for a more engaging experience
- **Context-Aware Responses** - Adapts tone and content based on user information
- **Company Branding** - Consistent TechHive identity across all interactions

### 🛡️ Agent Middleware
- **PII Protection** - Automatically redacts emails and masks credit card numbers
- **Input Sanitization** - Prevents sensitive data from being logged or cached
- **Dynamic Prompt Injection** - Contextualizes system prompts at runtime

### 💾 Conversational Memory
- **In-Memory State** - Maintains conversation history within sessions
- **Thread-Based Persistence** - Tracks multi-turn conversations with thread IDs
- **Stateful Interactions** - Agent remembers previous context for follow-up questions

### 🎨 Simple Gradio Frontend
- **Chat Interface** - Clean, intuitive UI for interacting with CORA
- **Streaming Responses** - Token-by-token output for responsive user experience
- **Easy Deployment** - Single command to launch the web interface

### 🗄️ Vector Database (ChromaDB)
- **Persistent Storage** - Documents remain available across restarts
- **Docker-Hosted** - Easy deployment with docker-compose
- **Configurable Collections** - Separate FAQ and product knowledge bases

### ⚡ Redis Semantic Cache
- **Query Caching** - Stores responses to semantically similar questions
- **Reduced Latency** - Instant responses for cached queries
- **Cost Optimization** - Minimizes LLM inference calls
- **TTL Management** - Automatic cache expiration after configurable time periods

### 🐳 Docker Deployment
- **One-Command Setup** - `docker-compose up -d` launches all services
- **Isolated Services** - ChromaDB and Redis run in separate containers
- **Persistent Volumes** - Data survives container restarts

---

## 🚀 Quick Start

### Prerequisites

Before starting, ensure you have the following installed:

1. **[UV Package Manager](https://docs.astral.sh/uv/)** - Modern Python package manager
2. **[Docker & Docker Compose](https://docs.docker.com/get-docker/)** - For ChromaDB and Redis services
3. **[Ollama](https://ollama.com/download)** - Local LLM inference engine

### Ollama Model Setup

⚠️ **Important:** CORA requires a model that supports **tool calling**. The default configuration uses `qwen3:14b`.

**Pull the model:**
```bash
# Pull the default model (recommended)
ollama pull qwen3:14b
```

Browse all tool-capable models: **[Ollama Tool-Capable Models](https://ollama.com/search?c=tools)**

**Changing the model:**
Edit `src/cora_customer_agent/cora_config.yaml`:
```yaml
ollama_config:
  model: "qwen3:14b"  # Change this when using a different model
```

⚠️ **Performance Note:** Models with fewer parameters (e.g., `llama3.2:1b`) may produce inconsistent or lower-quality responses.

---

### Installation Steps

#### 1. Clone the Repository
```bash
git clone git@github.com:niels-2005/cora_customer_agent.git
cd cora_customer_agent
```

#### 2. Create Virtual Environment
```bash
# Create virtual environment with uv
uv venv

# Activate the virtual environment
# On Linux/macOS:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate

# Install dependencies
uv sync
```

#### 3. Start Docker Services
```bash
# Start ChromaDB and Redis
docker-compose up -d
```

#### 4. Configure the Application (Optional)

📋 **Review the configuration file:**  
Most settings are pre-configured and work out of the box. However, it's recommended to review `src/cora_customer_agent/cora_config.yaml` to understand the customization options.

**Key configuration sections:**
- **MCP Server** - Port and host settings
- **Vector Database** - Collection names, paths, and initialization flags
- **Embedding Model** - HuggingFace model selection
- **Semantic Cache** - Redis connection and similarity thresholds
- **Ollama LLM** - Model selection and inference parameters

⚠️ **First-Time Setup:** If running for the first time, set `init_vector_store: true` (default) in the config to populate ChromaDB with documents. After the first run, set it back to `false` to avoid re-initialization.

---

### Running the Application

#### Start the MCP Server
```bash
# Start the MCP Server
run_mcp
```

#### Start the Gradio Frontend (in a new terminal)
```bash
# Start the Gradio interface
run_gradio
```

---

## 🌐 Access Points

| Service | URL | Description |
|---------|-----|--------------|
| **Gradio Chat UI** | http://127.0.0.1:7860 | Interactive chatbot interface |
| **MCP Server** | http://127.0.0.1:8080 | Tool server for agent (no UI) |
| **ChromaDB** | http://127.0.0.1:8000 | Vector database (no UI) |
| **Redis** | http://127.0.0.1:6379 | Semantic cache (no UI) |

---

## 🧪 Testing the Agent

You can find the simulated company data in `src/cora_customer_agent/company_docs`

Once both services are running, try these example queries in the Gradio interface:

**FAQ Questions:**
- "How long does delivery take?"
- "How secure are my payment details?"

**Product Questions:**
- "Tell me about the HiveSmart Light Bulb A60"
- "Show me details about the HiveCam 360 Pro"

**Conversational Memory:**
- "How long does delivery take?"
- "What was my first message?" (tests memory)

---

## 📊 Optional: LangSmith Integration

Enable distributed tracing and debugging with [LangSmith](https://docs.langchain.com/langsmith/home) for advanced observability.

**Features:**
- 📈 Trace agent decisions and tool calls
- 🐛 Debug chain execution step-by-step
- ⏱️ Measure latency for each component
- 💰 **Free tier:** 5,000 traces per month

### Setup Instructions

1. **Create LangSmith Account**  
   Sign up at https://smith.langchain.com

2. **Generate API Key**  
   Navigate to Settings → API Keys → Create New Key

3. **Configure Environment Variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your key
   ```

4. **Restart the Application**
   ```bash
   # Restart Gradio frontend to load environment variables
   run_gradio
   ```

Traces will now appear in your LangSmith dashboard at https://smith.langchain.com

---

## 🚧 Known Limitations & Future Improvements

### Known Limitations
- **In-Memory Conversations** - Session state lost on restart (no persistent database).  
  **Possible Solution:** Implement PostgreSQL integration for persistent conversation history and user accounts.

- **Single-User Frontend** - No authentication or multi-user support.  
  **Possible Solution:** Add authentication system with user login and personalized chat history.

- **Limited Reasoning Display** - Reasoning steps not shown in UI when reasoning is enabled

- **Manual Model Management** - Ollama models must be pulled separately

- **Semantic Cache Personalization Issue** - The cache stores responses with personalized greetings (e.g., "Hi Niels!"). When another user with a different name asks the same question, they receive the cached response with the wrong name. This occurs because the system prompt is dynamically injected with the user's name.  
  **Possible Solutions:** Remove `user_name` from the context, implement user-specific cache keys (expensive), or exclude personalized responses from caching. Semantic Cache was implemented for learning purposes.

- **Hardcoded RAG Parameters** - The number of retrieved documents (`k=1`) and similarity threshold (`0.4`) are fixed in the configuration. This one-size-fits-all approach may not be optimal for all queries—some questions might benefit from retrieving multiple documents for comprehensive answers.  
  **Possible Solution:** Allow the agent to dynamically determine the number of documents to retrieve based on query complexity. If the agent can dynamically set `k`, a mechanism is needed to prevent excessive retrieval (e.g., `k=100`), which introduces noise and degrades response quality.  
  **Possible Solution:** Implement bounded retrieval (e.g., `min=1, max=10`) and add an embedding-based reranker to filter and prioritize the most relevant documents beyond simple similarity scores.

### Future Improvements

#### Evaluation & Testing
- **AI-as-a-Judge Evaluation Framework** - Implement comprehensive evaluation system for model quality assessment:
  - **Input/Output Evaluation** - Compare agent responses against reference outputs
  - **RAG Retrieval Evaluation** - Assess relevance and quality of retrieved documents
  - **Edge Case Testing** - Test handling of non-existent products, ambiguous queries, etc.
  - **Implementation Resources:** Review [LangSmith Documentation](https://docs.smith.langchain.com), [openevals](https://github.com/langchain-ai/openevals), and [agentevals](https://github.com/langchain-ai/agentevals) repositories
  - Note: Not implemented due to hardware limitations
- **Model & Embedding Experimentation** - Conduct systematic testing with different embedding models and LLMs to optimize performance (hardware constraints prevented comprehensive testing)

#### Observability & Monitoring
- **Langfuse Integration** - For organizations requiring fully open-source observability, consider [Langfuse](https://langfuse.com) as an alternative to LangSmith (SaaS). Provides self-hosted tracing, evaluation, and prompt management.

#### Context Management
- **Context Window Handling** - Implement intelligent context management for production systems:
  - Monitor token usage approaching context limits (e.g., 128k tokens)
  - Add for example **Summarization Middleware** to condense conversation history at ~80-90% capacity
  - Preserve critical information while staying within model constraints
  - Note: Currently ignored due to hardware limitations

#### Feature Extensions
- **Enhanced MCP Tools** - Extend the MCP server with additional capabilities:
  - Product recommendation engine
  - Order tracking integration
  - Personalized product suggestions based on user history
  - Smart home device compatibility checker
- **User Profile Management MCP Server** - Separate MCP server (following separation of concerns) allowing users to update personal information (address, preferences, etc.) via the chatbot. Note: This requires careful evaluation and introduces security risks that must be thoroughly addressed.
- **Voice Interface** - Speech-to-text and text-to-speech capabilities for accessibility
- **Image Support** - Visual product catalogs with image embeddings for multimodal interactions
- **Feedback Loop** - User ratings to improve responses over time through reinforcement learning

#### Cloud & API Integration
- **API-Based Model Inference** - Consider using hosted APIs (OpenAI, Anthropic, etc.) for:
  - Improved performance and reliability
  - Access to frontier models
  - Reduced infrastructure overhead
  - ⚠️ **Critical Security Note:** Ensure no sensitive customer data (PII, payment info, personal details) is sent to external APIs in production. Implement strict data filtering and anonymization.

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

This README.md file was written by AI but strictly followed by human review and edits.

---

<div align="center">

**⭐ If you find this project useful, consider giving it a star on GitHub! ⭐**

</div>