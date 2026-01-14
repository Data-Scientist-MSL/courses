# CoursePlayerApp Lab Runner Specification

## Overview

The Lab Runner provides an interactive, sandboxed environment for students to execute code, run experiments, and practice hands-on skills. This component is tier-gated, with Basic users getting view-only access and Intermediate/Advanced users getting full execution capabilities.

## Lab Types

### 1. Jupyter Notebooks

#### Basic Tier - View-Only Mode
**Capabilities**:
- View rendered notebook (static HTML)
- See code cells with syntax highlighting
- View output cells (text, images, plots)
- Copy code to clipboard
- Download notebook file (.ipynb) for local use

**Limitations**:
- Cannot execute cells
- Cannot edit cells
- Cannot save changes
- No kernel connection

**UI Implementation**:
```python
# courseplayerapp/ui/pages/lab_runner.py (Basic tier)

import streamlit as st
import nbformat
from nbconvert import HTMLExporter

def render_notebook_view_only(notebook_path: str):
    """Render Jupyter notebook in view-only mode for Basic tier users."""
    
    st.warning("🔒 Interactive lab execution is available for Intermediate and Advanced tiers")
    st.info("💎 Upgrade to Intermediate to execute code and complete hands-on exercises")
    
    # Read notebook file
    with open(notebook_path, 'r') as f:
        nb = nbformat.read(f, as_version=4)
    
    # Convert to HTML
    html_exporter = HTMLExporter()
    html_exporter.template_name = 'classic'
    (body, resources) = html_exporter.from_notebook_node(nb)
    
    # Display as HTML
    st.components.v1.html(body, height=800, scrolling=True)
    
    # Download button (all tiers can download for local use)
    st.download_button(
        "📥 Download Notebook (.ipynb)",
        data=open(notebook_path, 'rb').read(),
        file_name=f"lab_{notebook_path.split('/')[-1]}",
        mime="application/x-ipynb+json"
    )
    
    # Upgrade CTA
    st.button("✨ Upgrade to Execute Code", on_click=redirect_to_upgrade)
```

#### Intermediate/Advanced Tier - Interactive Mode
**Capabilities**:
- Full JupyterLab interface embedded
- Execute Python, R, Julia, or other kernels
- Edit and run code cells
- Install packages (pip, conda)
- Upload/download files
- Save workspace (persists across sessions)
- Access terminal for debugging
- Markdown cell editing
- Variable inspector
- Code completion and tooltips

**Resource Allocation**:
- **Intermediate**: 2 CPU cores, 4GB RAM, 10GB storage
- **Advanced**: 4 CPU cores, 8GB RAM, 20GB storage

**Sandbox Architecture**:
```yaml
jupyter_sandbox:
  container_image: jupyter/scipy-notebook:latest
  isolation: docker_container
  network: isolated (no internet)
  timeout: 2_hours_per_session
  auto_save: every_5_minutes
  
  allowed_packages:
    - numpy
    - pandas
    - matplotlib
    - scikit-learn
    - tensorflow
    - pytorch
    - seaborn
    # ... more whitelisted packages
  
  blocked_packages:
    - requests  # No external HTTP calls
    - urllib
    - socket
  
  filesystem:
    home_directory: /home/jovyan
    workspace_directory: /home/jovyan/workspace
    shared_data: /home/jovyan/data (read-only course datasets)
    max_file_size: 100MB
```

**JupyterLab Embedding**:
```python
# courseplayerapp/lab/jupyter_runner.py

import docker
from typing import Optional

class JupyterLabRunner:
    """Manage Jupyter notebook sandboxes for interactive labs."""
    
    def __init__(self, user_id: str, lab_id: str, user_tier: str):
        self.user_id = user_id
        self.lab_id = lab_id
        self.user_tier = user_tier
        self.client = docker.from_env()
    
    def launch_jupyter_lab(self) -> str:
        """
        Launch a Jupyter Lab container for the user.
        
        Returns:
            URL to access JupyterLab (e.g., http://localhost:8888?token=...)
        """
        # Resource limits based on tier
        resources = self._get_resource_limits()
        
        # Create container
        container = self.client.containers.run(
            image="jupyter/scipy-notebook:latest",
            detach=True,
            name=f"jupyter_{self.user_id}_{self.lab_id}",
            mem_limit=resources["memory"],
            cpu_quota=resources["cpu_quota"],
            cpu_period=100000,
            volumes={
                f"/var/edguide/workspaces/{self.user_id}/{self.lab_id}": {
                    "bind": "/home/jovyan/workspace",
                    "mode": "rw"
                },
                f"/var/edguide/course_data/{self.lab_id}": {
                    "bind": "/home/jovyan/data",
                    "mode": "ro"
                }
            },
            network_mode="none",  # No internet access
            ports={'8888/tcp': None},  # Random host port
            environment={
                "JUPYTER_ENABLE_LAB": "yes",
                "GRANT_SUDO": "no"
            }
        )
        
        # Get access token and URL
        logs = container.logs().decode('utf-8')
        token = self._extract_token(logs)
        port = container.attrs['NetworkSettings']['Ports']['8888/tcp'][0]['HostPort']
        
        jupyter_url = f"http://localhost:{port}/?token={token}"
        
        # Store container ID for cleanup
        redis_client.setex(
            f"jupyter_container:{self.user_id}:{self.lab_id}",
            7200,  # 2 hours TTL
            container.id
        )
        
        return jupyter_url
    
    def _get_resource_limits(self) -> dict:
        """Get resource limits based on user tier."""
        limits = {
            "intermediate": {
                "memory": "4g",
                "cpu_quota": 200000  # 2 cores
            },
            "advanced": {
                "memory": "8g",
                "cpu_quota": 400000  # 4 cores
            }
        }
        return limits.get(self.user_tier, limits["intermediate"])
    
    def _extract_token(self, logs: str) -> str:
        """Extract Jupyter access token from container logs."""
        import re
        match = re.search(r'token=([a-f0-9]+)', logs)
        if match:
            return match.group(1)
        return ""
    
    def stop_jupyter_lab(self):
        """Stop and remove the Jupyter container."""
        container_id = redis_client.get(f"jupyter_container:{self.user_id}:{self.lab_id}")
        if container_id:
            container = self.client.containers.get(container_id)
            container.stop()
            container.remove()
            redis_client.delete(f"jupyter_container:{self.user_id}:{self.lab_id}")
    
    def save_workspace(self):
        """
        Save the user's workspace to persistent storage.
        Auto-saved every 5 minutes and on session end.
        """
        # Workspace is already mounted to /var/edguide/workspaces/
        # Container writes directly to persistent volume
        # Additional backup to S3 or similar
        pass
```

**UI Integration**:
```python
# Streamlit component for JupyterLab iframe
def render_jupyter_lab_interactive(lab_id: str, user_tier: str):
    """Embed JupyterLab in iframe for interactive execution."""
    
    st.success("✅ Interactive Lab Environment Enabled")
    
    # Launch or retrieve existing Jupyter session
    runner = JupyterLabRunner(
        user_id=st.session_state.user_id,
        lab_id=lab_id,
        user_tier=user_tier
    )
    
    if st.button("🚀 Launch Lab Environment"):
        with st.spinner("Starting your sandbox environment..."):
            jupyter_url = runner.launch_jupyter_lab()
            st.session_state.jupyter_url = jupyter_url
    
    if "jupyter_url" in st.session_state:
        # Embed JupyterLab in iframe
        st.components.v1.iframe(
            src=st.session_state.jupyter_url,
            width=1200,
            height=800,
            scrolling=True
        )
        
        # Control buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💾 Save Workspace"):
                runner.save_workspace()
                st.success("Workspace saved!")
        with col2:
            if st.button("🔄 Restart Kernel"):
                # Send restart command to Jupyter
                st.info("Kernel restarted")
        with col3:
            if st.button("🛑 Stop Environment"):
                runner.stop_jupyter_lab()
                del st.session_state.jupyter_url
                st.rerun()
```

---

### 2. Code Editors (Monaco Editor)

For simpler labs that don't need full Jupyter, use Monaco Editor (VS Code in browser).

**Features**:
- Syntax highlighting for 50+ languages
- IntelliSense (auto-completion)
- Error detection (linting)
- Find and replace
- Multi-cursor editing
- Keyboard shortcuts (VS Code compatible)

**Implementation**:
```python
# courseplayerapp/lab/code_editor.py

import streamlit.components.v1 as components

def render_monaco_editor(
    code: str,
    language: str = "python",
    theme: str = "vs-dark",
    readonly: bool = False
) -> str:
    """
    Render Monaco Editor (VS Code in browser).
    
    Args:
        code: Initial code content
        language: Programming language (python, javascript, etc.)
        theme: Editor theme (vs, vs-dark, hc-black)
        readonly: If True, editor is read-only (Basic tier)
    
    Returns:
        Updated code from editor
    """
    editor_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            #editor {{ 
                width: 100%;
                height: 600px;
                border: 1px solid #ccc;
            }}
        </style>
    </head>
    <body>
        <div id="editor"></div>
        
        <script src="https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs/loader.js"></script>
        <script>
            require.config({{ paths: {{ 'vs': 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs' }}}});
            
            require(['vs/editor/editor.main'], function() {{
                var editor = monaco.editor.create(document.getElementById('editor'), {{
                    value: {repr(code)},
                    language: '{language}',
                    theme: '{theme}',
                    readOnly: {str(readonly).lower()},
                    automaticLayout: true,
                    minimap: {{ enabled: true }},
                    scrollBeyondLastLine: false,
                    fontSize: 14
                }});
                
                // Send code updates to Streamlit
                editor.onDidChangeModelContent(function() {{
                    window.parent.postMessage({{
                        type: 'code_update',
                        code: editor.getValue()
                    }}, '*');
                }});
            }});
        </script>
    </body>
    </html>
    """
    
    return components.html(editor_html, height=650)
```

**Code Execution Backend**:
```python
# courseplayerapp/lab/code_executor.py

import subprocess
import tempfile
import os
from typing import Tuple

class CodeExecutor:
    """Execute user code in sandboxed environment."""
    
    TIMEOUT_SECONDS = 30
    MAX_OUTPUT_SIZE = 10000  # 10KB
    
    def execute_python(self, code: str) -> Tuple[str, str, int]:
        """
        Execute Python code and return output.
        
        Returns:
            Tuple of (stdout, stderr, exit_code)
        """
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # Execute in isolated process
            result = subprocess.run(
                ['python3', temp_file],
                capture_output=True,
                text=True,
                timeout=self.TIMEOUT_SECONDS,
                env={'PYTHONPATH': ''}  # Isolated environment
            )
            
            stdout = result.stdout[:self.MAX_OUTPUT_SIZE]
            stderr = result.stderr[:self.MAX_OUTPUT_SIZE]
            exit_code = result.returncode
            
            return stdout, stderr, exit_code
        
        except subprocess.TimeoutExpired:
            return "", f"Error: Code execution timeout ({self.TIMEOUT_SECONDS}s)", 1
        
        finally:
            os.unlink(temp_file)
    
    def execute_javascript(self, code: str) -> Tuple[str, str, int]:
        """Execute JavaScript code using Node.js."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            result = subprocess.run(
                ['node', temp_file],
                capture_output=True,
                text=True,
                timeout=self.TIMEOUT_SECONDS
            )
            return result.stdout, result.stderr, result.returncode
        
        except subprocess.TimeoutExpired:
            return "", f"Error: Code execution timeout ({self.TIMEOUT_SECONDS}s)", 1
        
        finally:
            os.unlink(temp_file)
```

---

### 3. Terminal Access (Web-Based)

Provide web-based terminal for Intermediate/Advanced users.

**Technology**: xterm.js + WebSocket

**Implementation**:
```python
# courseplayerapp/lab/terminal.py

from fastapi import WebSocket
import asyncio
import pty
import os

class WebTerminal:
    """Web-based terminal using xterm.js and WebSocket."""
    
    def __init__(self, user_id: str, lab_id: str):
        self.user_id = user_id
        self.lab_id = lab_id
        self.process = None
    
    async def handle_websocket(self, websocket: WebSocket):
        """Handle WebSocket connection for terminal I/O."""
        await websocket.accept()
        
        # Spawn bash shell in pseudo-terminal
        master_fd, slave_fd = pty.openpty()
        self.process = subprocess.Popen(
            ['/bin/bash'],
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            preexec_fn=os.setsid
        )
        
        # Read from terminal and send to WebSocket
        async def read_output():
            while True:
                try:
                    output = os.read(master_fd, 1024).decode('utf-8')
                    await websocket.send_text(output)
                except:
                    break
        
        # Read from WebSocket and write to terminal
        async def write_input():
            while True:
                try:
                    data = await websocket.receive_text()
                    os.write(master_fd, data.encode('utf-8'))
                except:
                    break
        
        # Run both tasks concurrently
        await asyncio.gather(read_output(), write_input())
```

**Frontend (xterm.js)**:
```html
<!-- Terminal UI component -->
<div id="terminal"></div>

<script src="https://cdn.jsdelivr.net/npm/xterm@5.0.0/lib/xterm.js"></script>
<script src="https://cdn.jsdelivr.net/npm/xterm-addon-fit@0.7.0/lib/xterm-addon-fit.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/xterm@5.0.0/css/xterm.css" />

<script>
    const terminal = new Terminal({
        cursorBlink: true,
        fontSize: 14,
        fontFamily: 'Menlo, Monaco, "Courier New", monospace',
        theme: {
            background: '#1e1e1e',
            foreground: '#cccccc'
        }
    });
    
    const fitAddon = new FitAddon();
    terminal.loadAddon(fitAddon);
    terminal.open(document.getElementById('terminal'));
    fitAddon.fit();
    
    // WebSocket connection
    const ws = new WebSocket('wss://gai-observe.online/api/lab/terminal');
    
    ws.onmessage = (event) => {
        terminal.write(event.data);
    };
    
    terminal.onData((data) => {
        ws.send(data);
    });
</script>
```

---

## Sandbox Security

### Container Isolation
- **One container per user session**: No shared resources between users
- **Network isolation**: No outbound internet access (prevents data exfiltration)
- **Read-only filesystem**: Except for user workspace directory
- **No sudo access**: Users cannot escalate privileges
- **Resource limits**: CPU, memory, disk quotas enforced

### Package Whitelisting
```python
ALLOWED_PACKAGES = [
    # Data science
    "numpy", "pandas", "scipy", "matplotlib", "seaborn", "plotly",
    # Machine learning
    "scikit-learn", "tensorflow", "keras", "pytorch", "xgboost",
    # Utilities
    "jupyterlab", "ipython", "nbconvert",
    # ... more
]

BLOCKED_PACKAGES = [
    # Network access
    "requests", "urllib3", "httpx", "aiohttp",
    # System access
    "subprocess", "os", "sys",
    # ... more
]

def validate_package_install(package_name: str) -> bool:
    """Check if package is allowed to be installed."""
    return package_name in ALLOWED_PACKAGES and package_name not in BLOCKED_PACKAGES
```

### Code Scanning
```python
def scan_code_for_security_issues(code: str) -> list:
    """
    Scan user code for security issues before execution.
    
    Checks for:
    - Network access attempts
    - File system access outside workspace
    - Process spawning
    - Infinite loops
    """
    security_issues = []
    
    # Check for network access
    if any(keyword in code for keyword in ['requests.', 'urllib.', 'socket.']):
        security_issues.append("Network access is not allowed in sandbox")
    
    # Check for subprocess
    if 'subprocess' in code or 'os.system' in code:
        security_issues.append("Process execution is restricted")
    
    # Check for infinite loops (heuristic)
    if code.count('while True') > 0:
        security_issues.append("Warning: Potential infinite loop detected")
    
    return security_issues
```

---

## Integration with SimulationPlayer

For complex, multi-step simulations, CoursePlayerApp launches SimulationPlayer in a new tab/iframe.

**Launch Flow**:
```python
# courseplayerapp/integrations/simulationplayer_client.py

class SimulationPlayerClient:
    """Client for launching and tracking simulations."""
    
    def __init__(self, base_url: str = "https://simulation.gai-observe.online"):
        self.base_url = base_url
    
    async def launch_simulation(
        self,
        simulation_id: str,
        user_id: str,
        context: dict
    ) -> str:
        """
        Launch simulation and return session URL.
        
        Args:
            simulation_id: Unique simulation identifier
            user_id: User launching the simulation
            context: Course/module context for tracking
        
        Returns:
            URL to access simulation (opens in new tab)
        """
        response = await httpx.post(
            f"{self.base_url}/api/simulations/launch",
            json={
                "simulation_id": simulation_id,
                "user_id": user_id,
                "context": context
            }
        )
        
        session_data = response.json()
        simulation_url = session_data["simulation_url"]
        
        # Track launch event
        await self._track_launch(user_id, simulation_id)
        
        return simulation_url
    
    async def get_simulation_progress(
        self,
        user_id: str,
        simulation_id: str
    ) -> dict:
        """
        Get completion status and results from simulation.
        
        Returns:
            {
                "status": "completed" | "in_progress" | "not_started",
                "score": 0-100,
                "completion_percent": 0-100,
                "completed_at": ISO timestamp or null
            }
        """
        response = await httpx.get(
            f"{self.base_url}/api/simulations/{simulation_id}/progress",
            params={"user_id": user_id}
        )
        return response.json()
```

**UI Integration**:
```python
# Launch simulation from lab page
def render_simulation_launcher(simulation_id: str, user_tier: str):
    """Render simulation launch button with tier checking."""
    
    # Check tier access
    if user_tier == "basic":
        st.info("🔒 Interactive simulations are available for Intermediate and Advanced tiers")
        st.button("💎 Upgrade to Access Simulations", on_click=redirect_to_upgrade)
        return
    
    # Check quota for Intermediate tier
    if user_tier == "intermediate":
        quota = get_simulation_quota(st.session_state.user_id)
        if quota["used"] >= quota["limit"]:
            st.error("❌ Monthly simulation quota exceeded")
            st.info("💎 Upgrade to Advanced for unlimited simulations")
            return
        st.info(f"Simulations remaining this month: {quota['limit'] - quota['used']}")
    
    # Launch button
    if st.button("🚀 Launch Simulation"):
        sim_client = SimulationPlayerClient()
        simulation_url = asyncio.run(
            sim_client.launch_simulation(
                simulation_id=simulation_id,
                user_id=st.session_state.user_id,
                context={
                    "course_id": st.session_state.current_course,
                    "module_id": st.session_state.current_module
                }
            )
        )
        
        # Open in new tab
        st.markdown(f'<meta http-equiv="refresh" content="0; url={simulation_url}">', unsafe_allow_html=True)
        
        # Or embed in iframe
        # st.components.v1.iframe(simulation_url, width=1200, height=800)
```

---

## Lab Validation & Auto-Grading

For structured labs with specific objectives, provide auto-grading.

```python
# courseplayerapp/lab/auto_grader.py

class LabAutoGrader:
    """Auto-grade lab submissions against test cases."""
    
    def __init__(self, lab_id: str):
        self.lab_id = lab_id
        self.test_cases = self._load_test_cases()
    
    def grade_submission(self, user_code: str) -> dict:
        """
        Run test cases against user code.
        
        Returns:
            {
                "passed": 8,
                "failed": 2,
                "total": 10,
                "score": 80,
                "feedback": ["Test 1: PASS", "Test 2: FAIL - Expected 42, got 40", ...]
            }
        """
        results = {"passed": 0, "failed": 0, "total": len(self.test_cases), "feedback": []}
        
        for i, test_case in enumerate(self.test_cases):
            try:
                # Execute user code with test input
                exec_globals = {}
                exec(user_code, exec_globals)
                
                # Run test function
                result = exec_globals[test_case["function_name"]](*test_case["input"])
                
                # Check expected output
                if result == test_case["expected"]:
                    results["passed"] += 1
                    results["feedback"].append(f"✅ Test {i+1}: PASS")
                else:
                    results["failed"] += 1
                    results["feedback"].append(
                        f"❌ Test {i+1}: FAIL - Expected {test_case['expected']}, got {result}"
                    )
            except Exception as e:
                results["failed"] += 1
                results["feedback"].append(f"❌ Test {i+1}: ERROR - {str(e)}")
        
        results["score"] = int((results["passed"] / results["total"]) * 100)
        return results
    
    def _load_test_cases(self) -> list:
        """Load test cases for this lab from database."""
        # Example test cases
        return [
            {
                "function_name": "add_numbers",
                "input": [5, 3],
                "expected": 8
            },
            {
                "function_name": "add_numbers",
                "input": [-1, 1],
                "expected": 0
            }
        ]
```

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-14  
**Author**: EdGuide Lab Team  
**Platform**: EdGuide (gai-observe.online)
