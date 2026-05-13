"""
FastAPI backend — ADK-style agents powered by local Ollama
Run: uvicorn app:app --reload --port 8000
"""
import json
import re
import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
import httpx

from agents import AGENTS, parse_tool_calls, execute_tool
from tools import TOOLS

app = FastAPI(title="ADK-Ollama Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_BASE = "http://localhost:11434"
MAX_TOOL_ROUNDS = 5


async def stream_ollama(model: str, messages: list):
    """Stream tokens from Ollama chat API."""
    async with httpx.AsyncClient(timeout=120) as client:
        async with client.stream("POST", f"{OLLAMA_BASE}/api/chat", json={
            "model": model,
            "messages": messages,
            "stream": True
        }) as resp:
            async for line in resp.aiter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if data.get("message", {}).get("content"):
                            yield data["message"]["content"]
                        if data.get("done"):
                            break
                    except json.JSONDecodeError:
                        pass


def sse(event: str, data: dict) -> str:
    return f"data: {json.dumps({'event': event, **data})}\n\n"


async def agent_run(agent_id: str, user_message: str, history: list):
    """Run an agent with tool-use loop, yielding SSE events."""
    agent = AGENTS[agent_id]
    model = agent["model"]
    system = agent["system_prompt"]

    messages = [{"role": "system", "content": system}]
    for h in history:
        messages.append(h)
    messages.append({"role": "user", "content": user_message})

    yield sse("agent_start", {"agent": agent["name"], "icon": agent["icon"], "model": model})

    for round_num in range(MAX_TOOL_ROUNDS):
        yield sse("thinking", {"round": round_num + 1})

        # Collect full response
        full_response = ""
        async for token in stream_ollama(model, messages):
            full_response += token
            yield sse("token", {"text": token})

        # Check for tool calls
        tool_calls = parse_tool_calls(full_response)

        if not tool_calls:
            # No more tool calls — final answer
            yield sse("done", {"message": full_response})
            messages.append({"role": "assistant", "content": full_response})
            break

        # Execute each tool
        messages.append({"role": "assistant", "content": full_response})
        tool_results = []

        for call in tool_calls:
            tool_name = call["data"].get("tool", "")
            args = call["data"].get("args", {})

            yield sse("tool_call", {"tool": tool_name, "args": args, "icon": get_tool_icon(tool_name)})
            await asyncio.sleep(0.3)

            result = execute_tool(tool_name, args)

            yield sse("tool_result", {"tool": tool_name, "result": result})
            tool_results.append(f"Tool `{tool_name}` returned:\n{result}")

        # Feed results back
        tool_content = "\n\n".join(tool_results)
        messages.append({"role": "user", "content": f"Tool results:\n{tool_content}\n\nNow provide your final answer."})

    else:
        yield sse("done", {"message": full_response})


def get_tool_icon(tool_name: str) -> str:
    icons = {
        "calculator": "🧮",
        "search_knowledge_base": "🔍",
        "run_python_code": "🐍",
        "get_current_time": "🕐",
        "analyze_text": "📊"
    }
    return icons.get(tool_name, "🔧")


@app.get("/api/health")
async def health():
    try:
        async with httpx.AsyncClient(timeout=3) as c:
            r = await c.get(f"{OLLAMA_BASE}/api/tags")
            models = r.json().get("models", [])
            return {"status": "ok", "ollama": "connected", "models": [m["name"] for m in models]}
    except Exception as e:
        return JSONResponse({"status": "error", "ollama": "offline", "error": str(e)}, status_code=503)


@app.get("/api/agents")
async def get_agents():
    return {
        aid: {
            "name": a["name"],
            "icon": a["icon"],
            "color": a["color"],
            "description": a["description"],
            "model": a["model"],
            "tools": list(TOOLS.keys())
        }
        for aid, a in AGENTS.items()
    }


@app.post("/api/chat/{agent_id}")
async def chat(agent_id: str, request: Request):
    if agent_id not in AGENTS:
        return JSONResponse({"error": "Unknown agent"}, status_code=404)

    body = await request.json()
    message = body.get("message", "")
    history = body.get("history", [])

    async def generate():
        async for event in agent_run(agent_id, message, history):
            yield event

    return StreamingResponse(generate(), media_type="text/event-stream", headers={
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no"
    })


@app.get("/api/models")
async def list_models():
    try:
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.get(f"{OLLAMA_BASE}/api/tags")
            return r.json()
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=503)


@app.post("/api/agents/{agent_id}/model")
async def set_model(agent_id: str, request: Request):
    if agent_id not in AGENTS:
        return JSONResponse({"error": "Unknown agent"}, status_code=404)
    body = await request.json()
    model = body.get("model")
    if model:
        AGENTS[agent_id]["model"] = model
    return {"agent": agent_id, "model": AGENTS[agent_id]["model"]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
