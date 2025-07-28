# 🤖 Autonomous Multi-Agent Task Bot

A comprehensive AI agent system designed to autonomously complete complex tasks using multiple specialized agents with distinct roles. Built with CrewAI, LangChain, OpenAI, and FastAPI.

## ✨ Features

- **Multi-Agent System**: 6 specialized agents (Research Analyst, Strategic Planner, Task Executor, Business Intelligence Analyst, Quality Assurance Specialist, Report Compiler)
- **Memory Management**: Persistent conversation memory and FAISS vector store for semantic search
- **Modern UI**: Beautiful, responsive dashboard with markdown rendering and syntax highlighting
- **API Integration**: RESTful API endpoints for programmatic access
- **n8n Integration**: Optional workflow automation via webhooks
- **Docker Support**: Containerized deployment
- **Vercel Ready**: Serverless deployment support

## 🏗️ Architecture

### Agents
1. **Research Analyst**: Conducts comprehensive research using multiple sources
2. **Strategic Planner**: Transforms research into actionable plans
3. **Task Executor**: Executes planned tasks with precision
4. **Business Intelligence Analyst**: Provides strategic insights and recommendations
5. **Quality Assurance Specialist**: Ensures deliverables meet high standards
6. **Report Compiler**: Synthesizes findings into comprehensive reports

### Technology Stack
- **CrewAI**: Multi-agent orchestration
- **LangChain**: Memory and tool integration
- **OpenAI GPT-4**: Language model processing
- **FastAPI**: Web framework and API
- **FAISS**: Vector database for semantic search
- **n8n**: Workflow automation (optional)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API key

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd autonomous-multi-agent-task-bot
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the dashboard**
   Open http://127.0.0.1:8000 in your browser

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Or build manually**
   ```bash
   docker build -t autonomous-agent-bot .
   docker run -p 8000:8000 -e OPENAI_API_KEY=your_key autonomous-agent-bot
   ```

### Vercel Deployment

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy to Vercel**
   ```bash
   vercel
   ```

3. **Set environment variables in Vercel dashboard**
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `N8N_WEBHOOK_URL`: Optional n8n webhook URL

## 🔗 n8n Integration

The autonomous task bot includes comprehensive n8n integration for workflow automation and notifications.

### Setup n8n Integration

1. **Run the setup script**
   ```bash
   python setup_n8n.py
   ```

2. **Or manually configure**
   ```bash
   # Add to your .env file
   N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/autonomous-task-bot
   ```

### n8n Workflow Setup

1. **Create a new n8n workflow**
2. **Add a Webhook trigger node**
3. **Configure the webhook URL**
4. **Add conditional nodes for different event types:**
   - `task_started`: When a task begins
   - `task_completed`: When a task finishes successfully
   - `task_failed`: When a task encounters an error
   - `agent_progress`: Real-time agent progress updates
   - `memory_update`: Memory system updates
   - `system_health`: System health checks

### Sample Workflow

Import the provided `n8n_workflow_example.json` file into your n8n instance for a complete setup with:
- Slack notifications
- Email alerts
- Notion database logging
- Conditional event handling

### API Endpoints

- `GET /api/n8n/status`: Check n8n integration status
- `POST /api/n8n/test`: Test n8n webhook connection
- `POST /api/n8n/event`: Send custom events to n8n

### Event Payload Structure

```json
{
  "event_type": "task_completed",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "source": "autonomous-task-bot",
  "version": "1.0.0",
  "data": {
    "task_id": "uuid",
    "task_type": "general",
    "status": "completed",
    "result": "Task result content",
    "execution_time": 120.5
  }
}
```

## 📋 API Endpoints

### Web Interface
- `GET /`: Main dashboard
- `POST /`: Submit new task

### REST API
- `GET /api/health`: Health check
- `GET /api/config`: Configuration info
- `GET /api/tasks`: Get task history
- `POST /api/tasks`: Create new task
- `GET /api/search`: Search similar tasks

### Example API Usage
```bash
# Create a new task
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{"task_prompt": "Research AI trends", "task_type": "research"}'

# Get task history
curl "http://localhost:8000/api/tasks?limit=10"

# Search similar tasks
curl "http://localhost:8000/api/search?query=AI&limit=5"
```

## 🔧 Configuration

### Environment Variables
```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
N8N_WEBHOOK_URL=your_n8n_webhook_url
DEBUG=True
HOST=127.0.0.1
PORT=8000
FAISS_INDEX_PATH=./data/faiss_index
MEMORY_PATH=./data/memory
```

### API Keys Setup
1. **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **n8n Webhook**: Optional for workflow automation

## 📊 Dashboard Features

- **Task Submission**: Submit tasks with custom descriptions and types
- **Markdown Rendering**: Beautiful formatting of AI-generated content
- **Syntax Highlighting**: Code blocks with syntax highlighting
- **Task History**: View recent tasks and their results
- **System Status**: Real-time status of integrations
- **Responsive Design**: Works on desktop and mobile

## 🐳 Docker Commands

```bash
# Build image
docker build -t autonomous-agent-bot .

# Run container
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key autonomous-agent-bot

# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🌐 Vercel Deployment

The application is configured for Vercel serverless deployment:

1. **Automatic Detection**: Vercel detects Python FastAPI app
2. **Environment Variables**: Set via Vercel dashboard
3. **Function Limits**: Configured for 5-minute execution time
4. **Static Files**: Automatically served from `/static` directory

## 📁 Project Structure

```
autonomous-multi-agent-task-bot/
├── main.py                 # FastAPI application
├── agents.py              # Agent definitions
├── crew_runner.py         # Task execution logic
├── memory_manager.py      # Memory management
├── config.py             # Configuration
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose
├── vercel.json          # Vercel configuration
├── templates/           # HTML templates
│   └── dashboard.html
├── static/             # Static files
│   └── styles.css
└── data/              # Data storage
    ├── memory/
    └── reports/
```

## 🔍 Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Ensure your API key is set in `.env` file
   - Check if the key has sufficient credits

2. **Memory Initialization Error**
   - The system will work without FAISS if OpenAI key is not configured
   - Check logs for specific error messages

3. **Docker Build Issues**
   - Ensure Docker is running
   - Clear Docker cache: `docker system prune`

4. **Vercel Deployment Issues**
   - Check function timeout limits
   - Ensure environment variables are set
   - Review Vercel logs for errors

### Logs and Debugging

```bash
# View application logs
docker-compose logs -f app

# Check health endpoint
curl http://localhost:8000/api/health

# Test API endpoints
curl http://localhost:8000/api/config
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) for multi-agent orchestration
- [LangChain](https://github.com/langchain-ai/langchain) for memory and tool integration
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [OpenAI](https://openai.com/) for the language model

---

**Made with ❤️ for autonomous AI task completion** 