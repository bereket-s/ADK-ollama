from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import datetime

def rgb(r,g,b): return RGBColor(r,g,b)

BG     = rgb(6,8,16)
PURPLE = rgb(124,58,237)
CYAN   = rgb(6,182,212)
WHITE  = rgb(232,234,246)
GRAY   = rgb(107,122,153)
GREEN  = rgb(52,211,153)
AMBER  = rgb(245,158,11)

def set_bg(slide, prs):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = BG

def add_text(slide, text, l, t, w, h, size=18, bold=False, color=WHITE, align=PP_ALIGN.LEFT, wrap=True):
    txBox = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = "Calibri"
    return txBox

def add_rect(slide, l, t, w, h, fill_color, alpha=None):
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape

def add_slide(prs, layout_idx=6):
    layout = prs.slide_layouts[layout_idx]
    slide = prs.slides.add_slide(layout)
    set_bg(slide, prs)
    for ph in slide.placeholders:
        sp = ph._element
        sp.getparent().remove(sp)
    return slide

def title_bar(slide, label, color=PURPLE):
    add_rect(slide, 0, 0, 10, 0.08, color)
    add_text(slide, label, 0.3, 0.12, 9, 0.35, size=9, bold=True, color=color)

def slide_title(slide, text, sub=None):
    add_text(slide, text, 0.4, 0.55, 9.2, 0.8, size=32, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
    if sub:
        add_text(slide, sub, 0.4, 1.3, 9.2, 0.4, size=13, bold=False, color=GRAY, align=PP_ALIGN.LEFT)

def bullet(slide, items, l, t, w, spacing=0.38, icon_color=PURPLE):
    for i, (icon, text, sz) in enumerate(items):
        add_rect(slide, l, t+i*spacing, 0.06, 0.06, icon_color)
        add_text(slide, f"{icon}  {text}", l+0.12, t+i*spacing-0.05, w, 0.38, size=sz, color=WHITE)

def code_box(slide, code, l, t, w, h):
    add_rect(slide, l, t, w, h, rgb(0,0,0))
    box = slide.shapes.add_textbox(Inches(l+0.1), Inches(t+0.1), Inches(w-0.2), Inches(h-0.2))
    tf = box.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = code
    run.font.name = "Courier New"
    run.font.size = Pt(9.5)
    run.font.color.rgb = rgb(167,139,250)

prs = Presentation()
prs.slide_width  = Inches(10)
prs.slide_height = Inches(5.625)

# ── Slide 1: Title ──────────────────────────────────────────────
s = add_slide(prs)
add_rect(s, 0, 0, 10, 5.625, BG)
add_rect(s, 0, 0, 10, 0.1, PURPLE)
add_rect(s, 0, 5.525, 10, 0.1, CYAN)
add_text(s, "ADK + OLLAMA", 0.5, 0.8, 9, 1, size=52, bold=True, color=PURPLE, align=PP_ALIGN.CENTER)
add_text(s, "Local Multi-Agent AI System", 0.5, 1.85, 9, 0.6, size=22, bold=False, color=WHITE, align=PP_ALIGN.CENTER)
add_text(s, "LLM Demonstration Using Google Agent Development Kit", 0.5, 2.4, 9, 0.4, size=13, color=GRAY, align=PP_ALIGN.CENTER)
add_text(s, datetime.datetime.now().strftime("%B %Y"), 0.5, 4.8, 9, 0.4, size=11, color=GRAY, align=PP_ALIGN.CENTER)
for x, (lbl, col) in enumerate([("🔒 100% Private",PURPLE),("⚡ No API Cost",CYAN),("🛠️ Real Tools",GREEN),("🤖 Multi-Agent",AMBER)]):
    add_rect(s, 0.7+x*2.2, 3.2, 2.0, 0.5, rgb(20,20,40))
    add_text(s, lbl, 0.75+x*2.2, 3.28, 1.9, 0.38, size=11, bold=True, color=col, align=PP_ALIGN.CENTER)

# ── Slide 2: Which Demo & Why ────────────────────────────────────
s = add_slide(prs)
title_bar(s, "RECOMMENDATION", PURPLE)
slide_title(s, "Why ADK + Ollama?", "Chosen over standalone ADK or Ollama demos")
data = [
    ("✅ ADK Playground (Gemini)", "Simulated agents, needs cloud API, no real tool execution", GRAY),
    ("✅ Ollama Chat Demo",         "Real local LLM but no agents, no tools, no backend",         GRAY),
    ("🔥 ADK + Ollama (CHOSEN)",    "Real agents + real tools + local LLM + Python backend",     GREEN),
]
for i,(title,desc,col) in enumerate(data):
    add_rect(s, 0.4, 1.75+i*1.0, 9.2, 0.82, rgb(12,15,28))
    add_text(s, title, 0.55, 1.82+i*1.0, 5, 0.35, size=12, bold=True, color=col)
    add_text(s, desc,  0.55, 2.12+i*1.0, 8.8, 0.35, size=10, color=GRAY)

# ── Slide 3: Project Overview ────────────────────────────────────
s = add_slide(prs)
title_bar(s, "PROJECT OVERVIEW", CYAN)
slide_title(s, "What Was Built", "A full-stack local AI agent system powered by Ollama")
items = [
    ("🤖","Multi-agent orchestration — Research, Code, Orchestrator agents",11),
    ("🔧","5 real tools: calculator, Python runner, knowledge search, time, text analyzer",11),
    ("🌊","Streaming SSE responses — tokens arrive in real time",11),
    ("🐍","FastAPI Python backend — REST API on port 8000",11),
    ("🌐","HTML/JS frontend — no framework, runs in any browser on port 8081",11),
    ("🔒","Zero cloud dependency — 100% local, zero cost, private",11),
]
bullet(s, items, 0.4, 1.7, 9.0, spacing=0.47)

# ── Slide 4: Architecture ─────────────────────────────────────────
s = add_slide(prs)
title_bar(s, "ARCHITECTURE", PURPLE)
slide_title(s, "System Architecture")
boxes = [
    (0.3, 2.2, 1.6, 1.1, "🌐\nBrowser\nFrontend", PURPLE),
    (2.2, 2.2, 1.6, 1.1, "⚡\nFastAPI\nBackend :8000", CYAN),
    (4.1, 1.5, 1.6, 1.1, "🔬 Research\nAgent", rgb(124,58,237)),
    (4.1, 2.75, 1.6, 1.1,"💻 Code\nAgent", rgb(6,182,212)),
    (4.1, 4.0, 1.6, 1.1, "🤖 Orchestrator\nAgent", rgb(245,158,11)),
    (6.2, 2.0, 1.6, 1.1, "🔧\nTools\n5 Functions", GREEN),
    (8.1, 2.2, 1.6, 1.1, "🦙\nOllama\n:11434", AMBER),
]
for (l,t,w,h,lbl,col) in boxes:
    add_rect(s, l, t, w, h, rgb(12,15,30))
    add_text(s, lbl, l+0.05, t+0.1, w-0.1, h-0.15, size=10, bold=True, color=col, align=PP_ALIGN.CENTER)
arrows = [(1.9,2.65,2.2,2.65),(3.8,2.65,4.1,2.65),(5.7,2.65,6.2,2.65),(7.8,2.65,8.1,2.65)]
for (x1,y1,x2,y2) in arrows:
    from pptx.util import Inches as I
    line = s.shapes.add_connector(1, I(x1),I(y1),I(x2),I(y2))
    line.line.color.rgb = PURPLE
    line.line.width = Pt(1.5)

# ── Slide 5: Tech Stack ───────────────────────────────────────────
s = add_slide(prs)
title_bar(s, "TECHNOLOGY STACK", GREEN)
slide_title(s, "Technologies Used")
stack = [
    ("🐍 Python 3.11+", "Core backend language", PURPLE),
    ("⚡ FastAPI",        "REST API + Server-Sent Events (SSE) streaming", CYAN),
    ("🦙 Ollama",         "Local LLM runtime — runs Llama 3.2 on your machine", AMBER),
    ("🤖 ADK Patterns",   "Agent + Tool architecture inspired by Google ADK", GREEN),
    ("📡 httpx",          "Async HTTP client for Ollama API communication", PURPLE),
    ("🌐 HTML/JS/CSS",    "Zero-framework frontend — pure browser tech", CYAN),
    ("🔗 LiteLLM-ready",  "Architecture compatible with LiteLLM Ollama provider", GREEN),
]
for i,(tech,desc,col) in enumerate(stack):
    col2 = 0 if i%2==0 else 4.8
    row  = i//2
    add_rect(s, 0.4+col2, 1.75+row*0.88, 4.4, 0.75, rgb(12,15,28))
    add_text(s, tech, 0.55+col2, 1.82+row*0.88, 4.0, 0.3, size=11, bold=True, color=col)
    add_text(s, desc,  0.55+col2, 2.1+row*0.88,  4.0, 0.3, size=9.5, color=GRAY)

# ── Slide 6: Agents ───────────────────────────────────────────────
s = add_slide(prs)
title_bar(s, "AGENTS", PURPLE)
slide_title(s, "Three Specialized Agents", "Each agent has a unique persona, tools, and system prompt")
agents = [
    ("🔬", "Research Agent", PURPLE, "System: Expert researcher with web knowledge\nTools: search_knowledge_base, calculator, analyze_text, get_current_time\nUse: Fact-finding, research synthesis, knowledge Q&A"),
    ("💻", "Code Agent", CYAN,   "System: Senior Python developer\nTools: run_python_code, calculator, get_current_time\nUse: Code generation, execution & debugging"),
    ("🤖", "Orchestrator", AMBER, "System: Master coordinator, delegates to sub-agents\nTools: ALL 5 tools available\nUse: Complex multi-step tasks requiring coordination"),
]
for i,(icon,name,col,desc) in enumerate(agents):
    add_rect(s, 0.3+i*3.2, 1.75, 3.0, 3.2, rgb(10,12,25))
    add_rect(s, 0.3+i*3.2, 1.75, 3.0, 0.55, col)
    add_text(s, f"{icon} {name}", 0.4+i*3.2, 1.82, 2.8, 0.4, size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, desc, 0.4+i*3.2, 2.42, 2.8, 2.4, size=9.5, color=GRAY)

# ── Slide 7: Tools ────────────────────────────────────────────────
s = add_slide(prs)
title_bar(s, "TOOLS", GREEN)
slide_title(s, "5 Real Execution Tools", "Tools are actual Python functions — not simulated")
tools = [
    ("🧮","calculator(expression)","Safely evaluates math: 1234*5678, sqrt(144), pi*r²"),
    ("🔍","search_knowledge_base(query)","Searches built-in AI knowledge base on LLMs, ADK, RAG"),
    ("🐍","run_python_code(code)","Executes Python via subprocess, returns real stdout/stderr"),
    ("🕐","get_current_time()","Returns current date, time, weekday in structured JSON"),
    ("📊","analyze_text(text)","Word count, sentence count, reading time analysis"),
]
for i,(icon,fn,desc) in enumerate(tools):
    add_rect(s, 0.35, 1.72+i*0.72, 9.3, 0.62, rgb(10,12,25))
    add_text(s, f"{icon}  {fn}", 0.5, 1.78+i*0.72, 3.8, 0.32, size=10.5, bold=True, color=CYAN, align=PP_ALIGN.LEFT)
    add_text(s, desc, 4.4, 1.78+i*0.72, 5.1, 0.32, size=10, color=GRAY)

# ── Slide 8: Code — agents.py ────────────────────────────────────
s = add_slide(prs)
title_bar(s, "CODE WALKTHROUGH — agents.py", CYAN)
slide_title(s, "Agent Definition Pattern")
code_box(s, '''AGENTS = {
    "research": {
        "name": "Research Agent",
        "model": "llama3.2",
        "system_prompt": """You are a Research Agent.
Use tools by outputting:
TOOL_CALL: {"tool": "tool_name", "args": {"param": "value"}}"""
    }
}

def parse_tool_calls(text: str) -> list:
    pattern = r\'TOOL_CALL:\\s*(\\{[^}]+\\})\'
    for match in re.finditer(pattern, text):
        yield json.loads(match.group(1))''', 0.35, 1.65, 5.8, 3.5)
    
add_text(s, "Key Design Pattern", 6.3, 1.65, 3.4, 0.35, size=11, bold=True, color=WHITE)
notes = [
    ("→","Agent picks tool via plain text JSON tag",10),
    ("→","No special SDK — works with any LLM",10),
    ("→","parse_tool_calls extracts JSON regex",10),
    ("→","System prompt engineers the behavior",10),
    ("→","Model, persona, tools per agent",10),
]
bullet(s, notes, 6.3, 2.1, 3.4, spacing=0.48, icon_color=CYAN)

# ── Slide 9: Code — app.py tool loop ─────────────────────────────
s = add_slide(prs)
title_bar(s, "CODE WALKTHROUGH — app.py", PURPLE)
slide_title(s, "Agentic Tool-Use Loop")
code_box(s, '''async def agent_run(agent_id, user_message, history):
    messages = [system_prompt, *history, user_message]

    for round in range(MAX_TOOL_ROUNDS):   # max 5 rounds
        full_response = ""

        # 1. Stream tokens from Ollama
        async for token in stream_ollama(model, messages):
            full_response += token
            yield sse("token", {"text": token})

        # 2. Extract any tool calls
        tool_calls = parse_tool_calls(full_response)
        if not tool_calls:
            yield sse("done", {"message": full_response})
            break

        # 3. Execute tools & feed results back
        for call in tool_calls:
            result = execute_tool(call["tool"], call["args"])
            yield sse("tool_result", {"result": result})
        messages.append({"role":"user","content": result})''', 0.35, 1.65, 9.3, 3.5)

# ── Slide 10: Frontend ────────────────────────────────────────────
s = add_slide(prs)
title_bar(s, "FRONTEND", AMBER)
slide_title(s, "HTML/JS Frontend Features", "Pure browser tech — no React, no npm")
feats = [
    ("🔴/🟢","Live status indicator — polls /api/health on load",11),
    ("🤖","Agent selector sidebar — dynamically loaded from /api/agents",11),
    ("📡","EventSource SSE reader — renders tokens as they arrive",11),
    ("🔧","Tool call visualizer — shows tool name, args, result inline",11),
    ("🎨","Dark glassmorphism UI — CSS gradients, blur, animations",11),
    ("💬","Conversation history — sent with every request for context",11),
]
bullet(s, feats, 0.4, 1.7, 9.0, spacing=0.47)

# ── Slide 11: How It Works — Flow ─────────────────────────────────
s = add_slide(prs)
title_bar(s, "DEMONSTRATION FLOW", GREEN)
slide_title(s, "End-to-End Request Flow")
steps = [
    ("1","User types message in browser","Frontend sends POST /api/chat/{agent_id}"),
    ("2","FastAPI receives request","Builds message history + system prompt"),
    ("3","Streams Ollama API","Token-by-token via /api/chat streaming"),
    ("4","Agent outputs TOOL_CALL","Backend parses JSON tag from response"),
    ("5","Tool executes locally","Real Python function runs, returns JSON"),
    ("6","Result fed back to model","Model incorporates result, continues generation"),
    ("7","Final answer streamed","Browser renders complete response with tool logs"),
]
for i,(num,title,detail) in enumerate(steps):
    col = PURPLE if i%2==0 else CYAN
    add_rect(s, 0.3, 1.65+i*0.52, 0.38, 0.38, col)
    add_text(s, num, 0.3, 1.65+i*0.52, 0.38, 0.38, size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text(s, title, 0.82, 1.68+i*0.52, 3.2, 0.32, size=10.5, bold=True, color=WHITE)
    add_text(s, detail, 4.1, 1.68+i*0.52, 5.7, 0.32, size=9.5, color=GRAY)

# ── Slide 12: Results & Conclusion ────────────────────────────────
s = add_slide(prs)
add_rect(s, 0, 0, 10, 5.625, BG)
add_rect(s, 0, 0, 10, 0.08, PURPLE)
add_text(s, "CONCLUSION", 0.4, 0.2, 9, 0.5, size=10, bold=True, color=PURPLE)
add_text(s, "Key Takeaways", 0.4, 0.65, 9, 0.7, size=30, bold=True, color=WHITE)
results = [
    ("🔒","Privacy-first AI","LLM runs 100% locally — data never leaves your machine"),
    ("💰","Zero cost","No API fees — unlimited requests with installed models"),
    ("🤖","Real ADK patterns","Multi-agent orchestration, tool calling, agentic loops"),
    ("⚡","Production-ready","FastAPI backend + SSE streaming + conversation history"),
]
for i,(icon,title,desc) in enumerate(results):
    col_idx = i%2
    row = i//2
    add_rect(s, 0.3+col_idx*4.9, 1.65+row*1.4, 4.5, 1.2, rgb(10,12,25))
    add_text(s, f"{icon} {title}", 0.5+col_idx*4.9, 1.75+row*1.4, 4.1, 0.4, size=13, bold=True, color=WHITE)
    add_text(s, desc, 0.5+col_idx*4.9, 2.1+row*1.4, 4.1, 0.55, size=10, color=GRAY)
add_text(s, "Built with: Python · FastAPI · Ollama · Llama 3.2 · ADK Patterns · HTML/CSS/JS",
         0.4, 4.9, 9.2, 0.4, size=9, color=GRAY, align=PP_ALIGN.CENTER)

# Save
out = r"C:\Users\berek\.gemini\antigravity\scratch\adk-ollama-agents\ADK_Ollama_Presentation.pptx"
prs.save(out)
print(f"Saved: {out}")
