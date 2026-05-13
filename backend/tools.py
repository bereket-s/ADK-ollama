"""
Tools available to ADK agents - search, calculator, code runner, time, wiki
"""
import math
import datetime
import re
import subprocess
import sys

def get_current_time() -> dict:
    """Get the current date and time."""
    now = datetime.datetime.now()
    return {
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "date": now.strftime("%B %d, %Y"),
        "time": now.strftime("%I:%M %p"),
        "weekday": now.strftime("%A"),
        "timezone": "Local"
    }

def calculator(expression: str) -> dict:
    """Evaluate a mathematical expression safely."""
    try:
        allowed = set("0123456789+-*/().% ")
        safe_expr = expression.replace("^", "**").replace("sqrt", "math.sqrt").replace("pi", "math.pi")
        result = eval(safe_expr, {"__builtins__": {}, "math": math})
        return {"expression": expression, "result": result, "formatted": f"{result:,.4f}".rstrip("0").rstrip(".")}
    except Exception as e:
        return {"error": str(e), "expression": expression}

def search_knowledge_base(query: str) -> dict:
    """Search a built-in knowledge base about AI, ADK, and Ollama topics."""
    kb = {
        "ollama": "Ollama is an open-source tool that lets you run large language models locally. It supports models like Llama 3, Mistral, Phi-3, Gemma, and CodeLlama. It exposes a REST API at localhost:11434.",
        "adk": "Google Agent Development Kit (ADK) is an open-source Python framework for building AI agents. It supports multi-agent orchestration, tool use, memory, and integrates with Gemini and other LLMs via LiteLLM.",
        "llama": "Llama 3.2 is Meta's latest open-source language model available in 3B, 8B, and 70B parameter sizes. It excels at reasoning, coding, and instruction following.",
        "rag": "Retrieval-Augmented Generation (RAG) combines LLMs with a vector database to answer questions from custom documents. It retrieves relevant chunks and passes them as context to the model.",
        "fine-tuning": "Fine-tuning is the process of further training a pre-trained model on a specific dataset to specialize its behavior. LoRA (Low-Rank Adaptation) is a popular parameter-efficient fine-tuning method.",
        "quantization": "Quantization reduces model precision (e.g., from 32-bit to 4-bit integers) to reduce memory usage. GGUF is the format used by llama.cpp and Ollama for quantized models.",
        "litellm": "LiteLLM is a Python library that provides a unified OpenAI-compatible interface to 100+ LLM providers including OpenAI, Anthropic, Gemini, and local models via Ollama.",
        "transformer": "The Transformer architecture (introduced in 'Attention Is All You Need', 2017) is the foundation of modern LLMs. It uses self-attention mechanisms to process sequences in parallel.",
        "agent": "An AI agent is an autonomous system that uses an LLM as its reasoning engine, enhanced with tools (search, code execution, APIs) and memory to complete multi-step tasks.",
        "mistral": "Mistral 7B is a high-performance open-source model from Mistral AI. Despite its size, it rivals much larger models in many benchmarks and is very fast on consumer hardware.",
    }
    q = query.lower()
    results = []
    for key, value in kb.items():
        if key in q or any(word in q for word in key.split()):
            results.append({"topic": key, "content": value})
    if not results:
        results = [{"topic": "general", "content": f"No specific knowledge found for '{query}'. The agent will use its general knowledge to answer."}]
    return {"query": query, "results": results, "count": len(results)}

def run_python_code(code: str) -> dict:
    """Execute a Python code snippet safely and return the output."""
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True, text=True, timeout=10
        )
        return {
            "code": code,
            "stdout": result.stdout[:1000] if result.stdout else "",
            "stderr": result.stderr[:500] if result.stderr else "",
            "exit_code": result.returncode,
            "success": result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {"error": "Code execution timed out (10s limit)", "code": code}
    except Exception as e:
        return {"error": str(e), "code": code}

def analyze_text(text: str) -> dict:
    """Analyze text for basic statistics."""
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return {
        "characters": len(text),
        "words": len(words),
        "sentences": len(sentences),
        "avg_words_per_sentence": round(len(words) / max(len(sentences), 1), 1),
        "unique_words": len(set(w.lower().strip(".,!?") for w in words)),
        "estimated_read_time_seconds": round(len(words) / 3)
    }

# Tool registry for the API
TOOLS = {
    "get_current_time": {
        "fn": get_current_time,
        "description": "Get the current date and time",
        "parameters": []
    },
    "calculator": {
        "fn": calculator,
        "description": "Evaluate a mathematical expression",
        "parameters": [{"name": "expression", "type": "string", "description": "Math expression to evaluate"}]
    },
    "search_knowledge_base": {
        "fn": search_knowledge_base,
        "description": "Search AI knowledge base for information about LLMs, ADK, Ollama",
        "parameters": [{"name": "query", "type": "string", "description": "Search query"}]
    },
    "run_python_code": {
        "fn": run_python_code,
        "description": "Execute Python code and return output",
        "parameters": [{"name": "code", "type": "string", "description": "Python code to run"}]
    },
    "analyze_text": {
        "fn": analyze_text,
        "description": "Analyze text for word count, sentences, reading time",
        "parameters": [{"name": "text", "type": "string", "description": "Text to analyze"}]
    }
}
