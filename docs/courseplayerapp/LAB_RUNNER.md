# Lab Runner Specification

## Platform Information
- **Platform**: EdGuide
- **Domain**: gai-observe.online
- **Purpose**: Define interactive lab environment and sandbox architecture

---

## Overview

The Lab Runner provides hands-on, interactive coding environments where students can practice concepts learned in videos. Access is tier-gated: Basic users can view code, while Intermediate and Advanced users can execute and experiment.

---

## Lab Types

### 1. Jupyter Notebooks

**Basic Tier** 🔒
- **Access**: View-only (rendered notebook)
- **Display**: Static HTML rendering
- **Features**:
  - Syntax-highlighted code cells
  - Rendered markdown explanations
  - Output displays (charts, tables)
  - Can read but cannot edit or execute

**Intermediate & Advanced Tiers** ✅
- **Access**: Full interactive JupyterLab
- **Features**:
  - Edit code cells
  - Execute Python/R code
  - Install packages (pip, conda)
  - Upload/download files
  - Terminal access
  - Multiple notebooks in workspace
  - Kernel management
  - Extensions support

**Jupyter Configuration**:
```yaml
jupyter_config:
  interface: "JupyterLab 4.0+"
  kernels:
    - python3 (default)
    - r
    - julia (optional)
  
  extensions:
    - ipywidgets
    - matplotlib
    - plotly
    - bokeh
  
  max_output_size: "10MB"
  max_cell_execution_time: "300s"  # 5 minutes
```

### 2. Code Editors (Monaco Editor)

**Features**:
- **VS Code in Browser**: Monaco editor (same as VS Code)
- **Syntax Highlighting**: Python, JavaScript, Java, C++, SQL, etc.
- **Auto-completion**: IntelliSense for installed packages
- **Real-time Validation**: Linting and error detection
- **Multi-file Support**: Work with multiple files
- **Find/Replace**: Advanced search functionality
- **Command Palette**: VS Code-like command access

**Supported Languages**:
```python
supported_languages = [
    "python",
    "javascript",
    "typescript",
    "java",
    "cpp",
    "r",
    "sql",
    "html",
    "css",
    "markdown",
    "json",
    "yaml"
]
```

**Configuration**:
```typescript
monaco_config = {
  theme: "vs-dark",  // or "vs-light"
  fontSize: 14,
  minimap: { enabled: true },
  wordWrap: "on",
  autoIndent: "advanced",
  formatOnPaste: true,
  formatOnType: true,
  suggestOnTriggerCharacters: true,
  quickSuggestions: true,
  tabSize: 4,
  insertSpaces: true
}
```

### 3. Terminal Access (Web-Based)

**Technology**: xterm.js + backend shell

**Intermediate & Advanced Tiers Only** ✅

**Features**:
- Full bash terminal in browser
- SSH-like experience
- Command history
- Tab completion
- Color support (ANSI)
- Copy/paste support
- Resizable terminal

**Restrictions**:
- No sudo access to host system
- Limited to sandbox container
- Whitelisted commands only for network access
- Resource limits enforced

**Whitelisted Commands**:
```yaml
allowed_commands:
  package_managers:
    - pip
    - pip3
    - conda
    - npm
    - apt-get (limited packages)
  
  development_tools:
    - python
    - python3
    - node
    - git
    - gcc
    - make
  
  utilities:
    - ls, cd, pwd, mkdir, rm, cp, mv
    - cat, grep, find, wget, curl
    - vim, nano, emacs
    - top, ps, kill
```

---

## Sandbox Architecture

### Container Specifications

```yaml
sandbox_container:
  technology: "Docker"
  isolation: "one_container_per_user_session"
  
  resources:
    cpu: "2_cores"
    memory: "4GB"
    storage: "10GB_ephemeral"
    swap: "1GB"
  
  limits:
    max_processes: 100
    max_file_descriptors: 1024
    max_network_connections: 50
  
  timeout:
    session: "2_hours"
    idle: "30_minutes"
    
  base_image: "edguide/lab-runner:latest"
  
  included_packages:
    python:
      - numpy
      - pandas
      - matplotlib
      - scikit-learn
      - tensorflow
      - pytorch
      - jupyter
    
    system:
      - git
      - vim
      - curl
      - wget
```

### Lifecycle Management

```python
# lab/sandbox_manager.py

from docker import from_env as docker_client
from datetime import datetime, timedelta

class SandboxManager:
    def __init__(self):
        self.docker = docker_client()
        self.max_containers_per_user = 3
    
    async def create_sandbox(self, user_id, lab_id, tier):
        """Create a new sandbox environment"""
        
        # Check if user already has too many containers
        existing = await self.get_user_containers(user_id)
        if len(existing) >= self.max_containers_per_user:
            # Clean up idle containers
            await self.cleanup_idle_containers(user_id)
        
        # Create container
        container = self.docker.containers.run(
            image="edguide/lab-runner:latest",
            detach=True,
            name=f"lab_{user_id}_{lab_id}_{int(datetime.now().timestamp())}",
            
            # Resource limits
            cpu_period=100000,
            cpu_quota=200000,  # 2 cores
            mem_limit="4g",
            memswap_limit="5g",
            
            # Environment
            environment={
                "USER_ID": user_id,
                "LAB_ID": lab_id,
                "TIER": tier,
                "SESSION_TIMEOUT": "7200"  # 2 hours
            },
            
            # Network isolation
            network_mode="bridge",
            
            # Storage
            volumes={
                f"user_{user_id}_workspace": {
                    "bind": "/workspace",
                    "mode": "rw"
                }
            },
            
            # Security
            cap_drop=["ALL"],
            cap_add=["CHOWN", "SETUID", "SETGID"],
            security_opt=["no-new-privileges"],
            
            # Labels for tracking
            labels={
                "user_id": user_id,
                "lab_id": lab_id,
                "created_at": datetime.now().isoformat(),
                "tier": tier
            }
        )
        
        # Wait for container to be ready
        await self.wait_for_ready(container)
        
        # Initialize workspace
        await self.initialize_workspace(container, lab_id)
        
        # Schedule auto-cleanup
        await self.schedule_cleanup(container, hours=2)
        
        return {
            "container_id": container.id,
            "jupyter_url": f"https://lab.gai-observe.online/{container.id}",
            "terminal_url": f"https://terminal.gai-observe.online/{container.id}",
            "expires_at": datetime.now() + timedelta(hours=2)
        }
    
    async def initialize_workspace(self, container, lab_id):
        """Initialize lab workspace with starter files"""
        
        # Get lab files from storage
        lab_files = await get_lab_files(lab_id)
        
        # Copy files into container
        for file_path, content in lab_files.items():
            container.exec_run(
                f"bash -c 'echo {content} > /workspace/{file_path}'"
            )
        
        # Set permissions
        container.exec_run("chown -R jupyter:jupyter /workspace")
    
    async def cleanup_idle_containers(self, user_id):
        """Clean up containers that have been idle > 30 minutes"""
        
        containers = self.docker.containers.list(
            filters={"label": f"user_id={user_id}"}
        )
        
        for container in containers:
            # Check last activity
            last_activity = await self.get_last_activity(container.id)
            idle_time = datetime.now() - last_activity
            
            if idle_time > timedelta(minutes=30):
                await self.stop_sandbox(container.id)
    
    async def stop_sandbox(self, container_id):
        """Stop and remove a sandbox container"""
        
        try:
            container = self.docker.containers.get(container_id)
            
            # Save workspace before stopping
            await self.save_workspace(container)
            
            # Stop and remove
            container.stop(timeout=10)
            container.remove()
            
        except Exception as e:
            print(f"Error stopping container {container_id}: {e}")
    
    async def save_workspace(self, container):
        """Save user's workspace to persistent storage"""
        
        user_id = container.labels.get("user_id")
        lab_id = container.labels.get("lab_id")
        
        # Archive workspace
        archive_stream, _ = container.get_archive("/workspace")
        
        # Save to object storage (S3/GCS)
        await save_to_storage(
            f"workspaces/{user_id}/{lab_id}/workspace.tar",
            archive_stream
        )
```

### Network Security

```yaml
network_policy:
  default: "deny_all"
  
  allowed_outbound:
    # Package repositories
    - pypi.org:443 (pip)
    - conda.anaconda.org:443 (conda)
    - npmjs.com:443 (npm)
    - github.com:443 (git clone)
    
    # Data sources (educational datasets)
    - data.gai-observe.online:443
    
    # API endpoints (for specific labs)
    - api.gai-observe.online:443
  
  blocked:
    - all_other_internet_access
    - local_network_access
    - other_containers
  
  rate_limits:
    max_requests_per_minute: 100
    max_bandwidth: "10MB/s"
```

---

## Lab Features by Tier

### Basic Tier: View-Only Mode

**UI Implementation**:
```python
# ui/pages/lab_runner.py

def render_lab_view_only(lab_id, user_tier):
    """Render lab in view-only mode for Basic tier"""
    
    st.title("🔒 Lab Environment (View-Only)")
    st.info("⬆️ Upgrade to Intermediate to execute code interactively")
    
    # Get lab content
    lab = get_lab_content(lab_id)
    
    # Display instructions
    st.markdown(lab["instructions"])
    
    # Display code cells (syntax highlighted, not editable)
    for i, cell in enumerate(lab["code_cells"]):
        st.subheader(f"Step {i+1}: {cell['title']}")
        st.markdown(cell["description"])
        
        # Code display (read-only)
        st.code(cell["code"], language="python")
        
        # Expected output
        if cell.get("expected_output"):
            with st.expander("Expected Output"):
                st.code(cell["expected_output"])
    
    # Upgrade CTA
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info("💡 Run this code yourself! Upgrade to Intermediate tier")
    with col2:
        st.button("⬆️ Upgrade Now", type="primary")
```

### Intermediate & Advanced Tiers: Interactive Mode

**UI Implementation**:
```python
def render_lab_interactive(lab_id, user_id, user_tier):
    """Render interactive lab environment"""
    
    st.title("🧪 Interactive Lab Environment")
    
    # Check for existing sandbox
    sandbox = await get_or_create_sandbox(user_id, lab_id, user_tier)
    
    # Lab layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Main work area
        tab1, tab2, tab3 = st.tabs(["📓 Notebook", "💻 Code Editor", "⌨️ Terminal"])
        
        with tab1:
            # Embedded JupyterLab
            st.components.v1.iframe(
                src=sandbox["jupyter_url"],
                height=800,
                scrolling=True
            )
        
        with tab2:
            # Monaco code editor
            render_monaco_editor(sandbox["container_id"])
        
        with tab3:
            # Web terminal
            st.components.v1.iframe(
                src=sandbox["terminal_url"],
                height=600
            )
    
    with col2:
        # Sidebar: Instructions and hints
        st.subheader("📋 Instructions")
        
        lab = get_lab_content(lab_id)
        st.markdown(lab["instructions"])
        
        # Progress
        st.markdown("---")
        st.subheader("✅ Progress")
        progress = get_lab_progress(user_id, lab_id)
        
        for step in lab["steps"]:
            completed = step["id"] in progress["completed_steps"]
            icon = "✅" if completed else "⬜"
            st.write(f"{icon} {step['title']}")
        
        # Hints system
        st.markdown("---")
        st.subheader("💡 Hints")
        
        for i, hint in enumerate(lab.get("hints", [])):
            with st.expander(f"Hint {i+1}"):
                st.write(hint)
        
        # Validation
        st.markdown("---")
        if st.button("🔍 Check Solution", use_container_width=True):
            result = await validate_lab_solution(user_id, lab_id, sandbox)
            
            if result["passed"]:
                st.success("✅ Correct! Well done!")
                await mark_lab_complete(user_id, lab_id)
            else:
                st.error("❌ Not quite right. Try again!")
                for error in result["errors"]:
                    st.write(f"• {error}")
        
        # Save/Load workspace
        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("💾 Save", use_container_width=True):
                await save_workspace(sandbox["container_id"])
                st.success("Saved!")
        
        with col_b:
            if st.button("🔄 Reset", use_container_width=True):
                if st.confirm("Reset to original state?"):
                    await reset_workspace(sandbox["container_id"], lab_id)
                    st.rerun()
```

---

## File Upload/Download

**Intermediate & Advanced Tiers Only** ✅

```python
# lab/file_manager.py

class LabFileManager:
    def __init__(self, max_file_size_mb=100):
        self.max_file_size = max_file_size_mb * 1024 * 1024
    
    async def upload_file(self, container_id, file, destination_path):
        """Upload file to sandbox container"""
        
        # Validate file size
        if file.size > self.max_file_size:
            raise ValueError(f"File too large. Max size: {self.max_file_size_mb}MB")
        
        # Validate file type (security)
        allowed_extensions = [
            '.py', '.ipynb', '.csv', '.txt', '.json',
            '.jpg', '.png', '.pdf', '.md', '.yml'
        ]
        
        if not any(file.name.endswith(ext) for ext in allowed_extensions):
            raise ValueError("File type not allowed")
        
        # Upload to container
        container = docker_client.containers.get(container_id)
        
        # Write file
        container.exec_run(
            f"bash -c 'cat > /workspace/{destination_path}'",
            stdin=True,
            stream=True
        ).send(file.read())
        
        return {
            "success": True,
            "path": f"/workspace/{destination_path}",
            "size": file.size
        }
    
    async def download_file(self, container_id, file_path):
        """Download file from sandbox container"""
        
        container = docker_client.containers.get(container_id)
        
        # Get file from container
        bits, stat = container.get_archive(f"/workspace/{file_path}")
        
        # Stream to user
        return bits
    
    async def list_files(self, container_id):
        """List files in workspace"""
        
        container = docker_client.containers.get(container_id)
        
        result = container.exec_run("ls -lah /workspace")
        
        return result.output.decode()
```

---

## Package Installation

**Tier-Based Restrictions**:

**Intermediate Tier**:
- Curated package list (pre-approved)
- Common data science packages allowed
- Installation time limit: 5 minutes
- Disk quota: 2GB for packages

**Advanced Tier**:
- Any package from PyPI/Conda
- Custom packages (from GitHub)
- Installation time limit: 10 minutes
- Disk quota: 5GB for packages

```python
# lab/package_manager.py

class PackageManager:
    # Curated list for Intermediate tier
    ALLOWED_PACKAGES_INTERMEDIATE = [
        "numpy", "pandas", "matplotlib", "seaborn",
        "scikit-learn", "scipy", "statsmodels",
        "requests", "beautifulsoup4", "pillow",
        "jupyter", "ipywidgets", "plotly", "bokeh"
    ]
    
    async def install_package(self, container_id, package_name, tier):
        """Install Python package in sandbox"""
        
        # Validate for Intermediate tier
        if tier == "intermediate":
            if package_name not in self.ALLOWED_PACKAGES_INTERMEDIATE:
                raise ValueError(
                    f"Package '{package_name}' not in allowed list for Intermediate tier. "
                    "Upgrade to Advanced for unrestricted package installation."
                )
        
        # Install package
        container = docker_client.containers.get(container_id)
        
        result = container.exec_run(
            f"pip install {package_name}",
            stream=True
        )
        
        # Stream output
        for line in result.output:
            yield line.decode()
```

---

## Integration with SimulationPlayer

```python
# integrations/simulationplayer_client.py

class SimulationPlayerClient:
    async def launch_simulation(
        self,
        simulation_id: str,
        user_id: str,
        context: dict
    ) -> str:
        """
        Launch simulation from CoursePlayerApp
        
        Args:
            simulation_id: Unique simulation identifier
            user_id: User ID
            context: Context data (course_id, module_id, lab_id)
        
        Returns:
            simulation_url: URL to access simulation
        """
        
        response = await http_client.post(
            f"{SIMULATIONPLAYER_API}/simulations/launch",
            json={
                "simulation_id": simulation_id,
                "user_id": user_id,
                "context": context,
                "callback_url": f"{COURSEPLAYERAPP_API}/api/simulations/callback"
            }
        )
        
        return response["simulation_url"]
    
    async def get_simulation_progress(
        self,
        user_id: str,
        simulation_id: str
    ) -> dict:
        """
        Get simulation completion status
        
        Returns:
            {
                "status": "completed" | "in_progress" | "not_started",
                "score": 85,
                "completed_at": "2026-01-12T10:30:00Z"
            }
        """
        
        response = await http_client.get(
            f"{SIMULATIONPLAYER_API}/simulations/{simulation_id}/progress",
            params={"user_id": user_id}
        )
        
        return response

# Usage in lab
async def launch_simulation_from_lab(lab_id, user_id):
    """Launch simulation related to current lab"""
    
    lab = get_lab_content(lab_id)
    
    if lab.get("simulation_id"):
        sim_client = SimulationPlayerClient()
        
        simulation_url = await sim_client.launch_simulation(
            simulation_id=lab["simulation_id"],
            user_id=user_id,
            context={
                "course_id": lab["course_id"],
                "module_id": lab["module_id"],
                "lab_id": lab_id
            }
        )
        
        # Open in new tab/iframe
        return simulation_url
```

---

## Lab Validation System

```python
# lab/validator.py

class LabValidator:
    async def validate_solution(self, user_id, lab_id, sandbox_container):
        """Validate student's lab solution"""
        
        lab = get_lab_content(lab_id)
        validation_tests = lab["validation_tests"]
        
        results = {
            "passed": True,
            "tests_passed": 0,
            "tests_failed": 0,
            "errors": []
        }
        
        container = docker_client.containers.get(sandbox_container)
        
        for test in validation_tests:
            # Run test in container
            exec_result = container.exec_run(
                f"python /workspace/run_test.py {test['id']}",
                workdir="/workspace"
            )
            
            if exec_result.exit_code == 0:
                results["tests_passed"] += 1
            else:
                results["passed"] = False
                results["tests_failed"] += 1
                results["errors"].append(test["error_message"])
        
        return results
```

---

## Performance & Monitoring

### Container Metrics

```python
# monitoring/container_metrics.py

async def track_container_metrics(container_id):
    """Track resource usage of sandbox containers"""
    
    container = docker_client.containers.get(container_id)
    stats = container.stats(stream=False)
    
    metrics = {
        "cpu_usage_percent": calculate_cpu_percent(stats),
        "memory_usage_mb": stats["memory_stats"]["usage"] / 1024 / 1024,
        "memory_limit_mb": stats["memory_stats"]["limit"] / 1024 / 1024,
        "network_rx_bytes": stats["networks"]["eth0"]["rx_bytes"],
        "network_tx_bytes": stats["networks"]["eth0"]["tx_bytes"],
        "timestamp": datetime.now()
    }
    
    # Send to monitoring system
    await send_metrics(metrics)
    
    # Alert if over limits
    if metrics["cpu_usage_percent"] > 90:
        await alert("High CPU usage in container", container_id)
    
    if metrics["memory_usage_mb"] > 3800:  # 95% of 4GB
        await alert("High memory usage in container", container_id)
```

---

## Related Documentation

- [System Architecture](./ARCHITECTURE.md)
- [Feature Gating](./FEATURE_GATING.md)
- [UI/UX Design](./UI_UX_DESIGN.md)
- [Integrations](./INTEGRATIONS.md)

---

**Last Updated**: January 2026  
**Platform**: EdGuide (gai-observe.online)  
**Version**: 1.0
