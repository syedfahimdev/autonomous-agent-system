import uuid
import json
import requests
from datetime import datetime
from typing import Dict, Any, List
from crewai import Crew, Task
from agents import researcher, planner, executor, reporter, bi_analyst, qa_specialist
from memory_manager import MemoryManager
import config

# Initialize memory manager
memory_manager = MemoryManager()

def send_to_n8n(task_id: str, result: str, task_type: str = "general"):
    """Send task results to n8n webhook"""
    if not config.N8N_WEBHOOK_URL:
        return
    
    try:
        payload = {
            "task_id": task_id,
            "result": result,
            "task_type": task_type,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        
        response = requests.post(config.N8N_WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            print(f"✅ Task results sent to n8n successfully")
        else:
            print(f"⚠️ Failed to send to n8n: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Error sending to n8n: {e}")

def save_report(task_id: str, result: str, task_type: str = "general"):
    """Save report to disk"""
    try:
        report_data = {
            "task_id": task_id,
            "task_type": task_type,
            "timestamp": datetime.now().isoformat(),
            "result": result
        }
        
        report_file = f"./data/reports/{task_id}.json"
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
            
        print(f"✅ Report saved: {report_file}")
        
    except Exception as e:
        print(f"⚠️ Error saving report: {e}")

def run_task(prompt: str, task_type: str = "general") -> Dict[str, Any]:
    """Run a comprehensive task with multiple agents"""
    task_id = str(uuid.uuid4())
    
    try:
        print(f"🚀 Starting task {task_id}: {prompt}")
        
        # Search for similar tasks in memory
        similar_tasks = memory_manager.search_similar_tasks(prompt, k=3)
        context = ""
        if similar_tasks:
            context = f"\n\nPrevious similar tasks:\n"
            for task in similar_tasks:
                context += f"- {task['content']}\n"
        
        # Create enhanced tasks for each agent
        research_task = Task(
            description=f"""Research the following topic thoroughly: {prompt}
            
            {context}
            
            Focus on:
            - Finding authoritative and recent sources
            - Cross-referencing information for accuracy
            - Identifying key trends and patterns
            - Gathering quantitative and qualitative data
            - Organizing findings in a structured manner""",
            expected_output="Comprehensive research findings with sources and key insights",
            agent=researcher
        )
        
        plan_task = Task(
            description="""Based on the research findings, create a detailed action plan. 
            
            Focus on:
            - Breaking down complex tasks into sequential steps
            - Identifying dependencies and critical path
            - Setting realistic timelines and milestones
            - Defining clear deliverables and success criteria
            - Anticipating potential challenges and mitigation strategies""",
            expected_output="Detailed action plan with timeline, milestones, and deliverables",
            agent=planner
        )
        
        execute_task = Task(
            description="""Execute the planned tasks with high quality and attention to detail.
            
            Focus on:
            - Following the established plan while remaining flexible
            - Maintaining high standards of quality and accuracy
            - Documenting progress and any deviations from plan
            - Identifying and resolving issues proactively
            - Ensuring deliverables meet or exceed expectations""",
            expected_output="Completed deliverables with documentation of execution process",
            agent=executor
        )
        
        bi_analysis_task = Task(
            description="""Analyze the research and execution results for business intelligence insights.
            
            Focus on:
            - Identifying key performance indicators and trends
            - Analyzing competitive landscape and market positioning
            - Providing actionable business recommendations
            - Creating data visualizations and dashboards
            - Forecasting potential outcomes and scenarios""",
            expected_output="Business intelligence analysis with strategic insights and recommendations",
            agent=bi_analyst
        )
        
        qa_task = Task(
            description="""Review and validate all deliverables for quality, accuracy, and completeness.
            
            Focus on:
            - Checking accuracy and completeness of information
            - Validating sources and cross-referencing data
            - Ensuring logical flow and coherence
            - Identifying potential errors or inconsistencies
            - Providing feedback for improvements""",
            expected_output="Quality assurance report with validation results and improvement suggestions",
            agent=qa_specialist
        )
        
        report_task = Task(
            description="""Compile a comprehensive final report synthesizing all findings and results.
            
            Focus on:
            - Synthesizing information from all sources into coherent narratives
            - Structuring reports with clear sections and logical flow
            - Highlighting key insights and actionable recommendations
            - Using appropriate formatting and visual elements
            - Ensuring reports are accessible to target audiences""",
            expected_output="Comprehensive final report with executive summary, findings, and recommendations",
            agent=reporter
        )
        
        # Create crew with enhanced task sequence
        crew = Crew(
            agents=[researcher, planner, executor, bi_analyst, qa_specialist, reporter],
            tasks=[research_task, plan_task, execute_task, bi_analysis_task, qa_task, report_task],
            verbose=True
        )
        
        # Run the crew with the prompt as input
        result = crew.kickoff({"task": prompt, "task_type": task_type})
        
        # Process results
        task_data = {
            "prompt": prompt,
            "result": str(result),
            "type": task_type,
            "timestamp": datetime.now().isoformat()
        }
        
        # Add to memory
        memory_manager.add_task_memory(task_id, task_data)
        
        # Save report
        save_report(task_id, str(result), task_type)
        
        # Send to n8n if configured
        send_to_n8n(task_id, str(result), task_type)
        
        return {
            "task_id": task_id,
            "status": "completed",
            "result": str(result),
            "task_type": task_type,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"❌ Task failed: {error_msg}")
        
        return {
            "task_id": task_id,
            "status": "failed",
            "error": error_msg,
            "task_type": task_type,
            "timestamp": datetime.now().isoformat()
        }

def get_task_history(limit: int = 10) -> List[Dict]:
    """Get recent task history"""
    return memory_manager.get_task_history(limit)

def search_tasks(query: str, k: int = 5) -> List[Dict]:
    """Search for similar tasks"""
    return memory_manager.search_similar_tasks(query, k)
