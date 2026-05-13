"""
ADK-style agents powered by local Ollama models.
Each agent has a name, persona, system prompt, and set of tools.
"""
import json
import re
from tools import TOOLS

AGENTS = {
    "research": {
        "name": "Research Agent",
        "icon": "🔬",
        "color": "#7c3aed",
        "model": "llama3.2:1b",
        "description": "Deep research and knowledge synthesis",
        "system_prompt": """You are a Research Agent powered by local Ollama AI (ADK pattern).
You have access to these tools: search_knowledge_base, get_current_time, analyze_text, calculator.

When you need information, use tools by outputting EXACTLY this JSON format on its own line:
TOOL_CALL: {"tool": "tool_name", "args": {"param": "value"}}

After receiving tool results, incorporate them into your response.
Be thorough, cite your tool usage, and provide well-structured answers.
Always mention that you are running locally with zero cloud dependency."""
    },
    "code": {
        "name": "Code Agent",
        "icon": "💻",
        "color": "#06b6d4",
        "model": "llama3.2:1b",
        "description": "Code generation, analysis and execution",
        "system_prompt": """You are a Code Agent powered by local Ollama AI (ADK pattern).
You specialize in writing, explaining, and executing code.
You have access to these tools: run_python_code, calculator, get_current_time.

When you want to run code, output EXACTLY:
TOOL_CALL: {"tool": "run_python_code", "args": {"code": "print('hello')"}}

Always:
1. Write clean, well-commented code
2. Execute code to verify it works before presenting
3. Explain what the code does step by step
4. Show actual output from execution"""
    },
    "orchestrator": {
        "name": "Multi-Agent Orchestrator",
        "icon": "🤖",
        "color": "#f59e0b",
        "model": "llama3.2:1b",
        "description": "Delegates tasks to specialized sub-agents",
        "system_prompt": """You are the Orchestrator Agent — the master coordinator in a multi-agent ADK system running on local Ollama.
You manage a team of specialized agents and delegate tasks intelligently.

Your team:
- Research Agent 🔬: Knowledge, analysis, facts
- Code Agent 💻: Programming, execution, debugging

You have ALL tools available: search_knowledge_base, calculator, run_python_code, get_current_time, analyze_text.

Use tools with:
TOOL_CALL: {"tool": "tool_name", "args": {"param": "value"}}

For complex tasks:
1. Break the task into subtasks
2. Assign each to the best agent (describe which agent handles which part)
3. Synthesize all results into a final comprehensive answer
4. Show your orchestration reasoning"""
    }
}

def parse_tool_calls(text: str) -> list:
    """Extract tool calls from model output."""
    calls = []
    pattern = r'TOOL_CALL:\s*(\{[^}]+\})'
    for match in re.finditer(pattern, text):
        try:
            call_data = json.loads(match.group(1))
            calls.append({"raw": match.group(0), "data": call_data})
        except json.JSONDecodeError:
            pass
    return calls

def execute_tool(tool_name: str, args: dict) -> str:
    """Execute a tool and return formatted result."""
    if tool_name not in TOOLS:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})
    tool = TOOLS[tool_name]
    fn = tool["fn"]
    try:
        result = fn(**args)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})
