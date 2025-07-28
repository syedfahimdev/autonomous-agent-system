from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from crew_runner import run_task, get_task_history, search_tasks
from n8n_integration import n8n, get_n8n_status, test_n8n_connection
import uvicorn
import os
import config
from datetime import datetime
from typing import Optional

app = FastAPI(
    title="Autonomous Multi-Agent Task Bot",
    description="A comprehensive AI agent system for autonomous task completion",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    """Main dashboard page"""
    try:
        # Get recent task history
        history = get_task_history(5)
        return templates.TemplateResponse(
            "dashboard.html", 
            {
                "request": request, 
                "result": "",
                "history": history,
                "timestamp": datetime.now().isoformat()
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "dashboard.html", 
            {
                "request": request, 
                "result": f"Error loading dashboard: {str(e)}",
                "history": [],
                "timestamp": datetime.now().isoformat()
            }
        )

@app.post("/", response_class=HTMLResponse)
async def process_task(request: Request, task_prompt: str = Form(...), task_type: str = Form("general")):
    """Process a task with the multi-agent system"""
    try:
        if not task_prompt.strip():
            raise HTTPException(status_code=400, detail="Task prompt cannot be empty")
        
        # Run the task
        result = run_task(task_prompt, task_type)
        
        # Get updated history
        history = get_task_history(5)
        
        if result["status"] == "completed":
            return templates.TemplateResponse(
                "dashboard.html", 
                {
                    "request": request, 
                    "result": result["result"],
                    "task_id": result["task_id"],
                    "history": history,
                    "timestamp": result["timestamp"]
                }
            )
        else:
            return templates.TemplateResponse(
                "dashboard.html", 
                {
                    "request": request, 
                    "result": f"Task failed: {result.get('error', 'Unknown error')}",
                    "history": history,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
    except Exception as e:
        return templates.TemplateResponse(
            "dashboard.html", 
            {
                "request": request, 
                "result": f"Error processing task: {str(e)}",
                "history": get_task_history(5),
                "timestamp": datetime.now().isoformat()
            }
        )

@app.get("/api/tasks", response_class=JSONResponse)
async def get_tasks(limit: int = 10):
    """Get task history via API"""
    try:
        history = get_task_history(limit)
        return {"tasks": history, "count": len(history)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search", response_class=JSONResponse)
async def search_tasks_api(query: str, limit: int = 5):
    """Search for similar tasks via API"""
    try:
        if not query.strip():
            raise HTTPException(status_code=400, detail="Search query cannot be empty")
        
        results = search_tasks(query, limit)
        return {"results": results, "query": query, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tasks", response_class=JSONResponse)
async def create_task(task_prompt: str, task_type: str = "general"):
    """Create a new task via API"""
    try:
        if not task_prompt.strip():
            raise HTTPException(status_code=400, detail="Task prompt cannot be empty")
        
        result = run_task(task_prompt, task_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health", response_class=JSONResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "openai_configured": bool(config.OPENAI_API_KEY),
        "n8n_configured": bool(config.N8N_WEBHOOK_URL)
    }

@app.get("/api/config", response_class=JSONResponse)
async def get_config():
    """Get configuration info (without sensitive data)"""
    return {
        "debug": config.DEBUG,
        "host": config.HOST,
        "port": config.PORT,
        "openai_configured": bool(config.OPENAI_API_KEY),
        "n8n_configured": bool(config.N8N_WEBHOOK_URL),
        "faiss_configured": True,
        "memory_path": config.MEMORY_PATH
    }

@app.get("/api/n8n/status", response_class=JSONResponse)
async def get_n8n_status_api():
    """Get n8n integration status"""
    return get_n8n_status()

@app.post("/api/n8n/test", response_class=JSONResponse)
async def test_n8n_api():
    """Test n8n webhook connection"""
    success = test_n8n_connection()
    return {
        "success": success,
        "message": "n8n connection test completed",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/n8n/event", response_class=JSONResponse)
async def send_n8n_event(event_type: str, data: dict):
    """Send custom event to n8n"""
    try:
        from n8n_integration import N8NEventType
        event_enum = N8NEventType(event_type)
        success = n8n.send_event(event_enum, data)
        return {
            "success": success,
            "event_type": event_type,
            "timestamp": datetime.now().isoformat()
        }
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid event type: {event_type}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    )
