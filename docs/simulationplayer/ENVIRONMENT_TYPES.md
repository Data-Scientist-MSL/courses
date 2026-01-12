# SimulationPlayer Environment Types

This document specifies the 7 environment types supported by SimulationPlayer. Each environment provides a specialized interactive learning experience tailored to different technical domains.

---

## Environment Architecture

All environments extend a common base class:

```python
class Environment(ABC):
    """Base class for all simulation environments"""
    
    @abstractmethod
    def initialize(self, initial_state: dict) -> None:
        """Set up environment with initial configuration"""
        pass
    
    @abstractmethod
    def execute_action(self, action: Action) -> ActionResult:
        """Execute user action and return result"""
        pass
    
    @abstractmethod
    def get_state(self) -> dict:
        """Get current environment state"""
        pass
    
    @abstractmethod
    def reset(self) -> None:
        """Reset environment to initial state"""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Clean up resources (containers, files, etc.)"""
        pass
    
    @abstractmethod
    def render_ui(self) -> StreamlitComponent:
        """Render environment-specific UI"""
        pass
```

---

## 1️⃣ Terminal Simulator

### Purpose
Practice bash/shell commands in a safe, sandboxed environment with realistic terminal behavior and command validation.

### Features

#### Virtual Filesystem
- Mock directory structure with realistic paths
- In-memory file creation, modification, deletion
- Persistent across steps within simulation
- Pre-populated with scenario-specific files

```python
filesystem = {
    '/home/user': {
        'type': 'directory',
        'contents': {
            'project': {
                'type': 'directory',
                'contents': {
                    'app.py': {'type': 'file', 'content': '# Sample app\n...'}
                }
            }
        }
    }
}
```

#### Command Execution
- Real command execution in Docker container
- Command history (up/down arrows)
- Tab completion for commands and files
- Environment variables
- Piping and redirection support

#### Output Rendering
- Colored output (ANSI codes)
- Formatted output (tables, JSON)
- Error vs. success differentiation
- Scrollable output area

#### Command Validation
- Syntax validation (command structure)
- Semantic validation (correct flags, arguments)
- Output verification
- Filesystem state checking

### Validation Types

#### 1. Command Exact Match
```yaml
validation:
  type: command_exact
  expected: "docker pull nginx"
```

#### 2. Command Contains
```yaml
validation:
  type: command_contains
  substring: "docker pull"
```

#### 3. Command Regex
```yaml
validation:
  type: command_regex
  pattern: "^docker (pull|image pull) nginx(:latest)?$"
```

#### 4. Exit Code
```yaml
validation:
  type: exit_code
  expected: 0
```

#### 5. Output Contains
```yaml
validation:
  type: output_contains
  text: "Status: Downloaded newer image"
```

#### 6. Filesystem State
```yaml
validation:
  type: file_exists
  path: "/home/user/output.txt"
  
validation:
  type: file_content_contains
  path: "/home/user/config.yml"
  text: "port: 8080"
```

### Use Cases

1. **Git Workflows**
   - Initialize repositories
   - Commit, branch, merge operations
   - Conflict resolution
   - Remote operations (simulated)

2. **Docker Commands**
   - Pull images
   - Run containers
   - Inspect containers
   - Manage volumes and networks

3. **System Administration**
   - File permissions (chmod, chown)
   - Process management (ps, kill)
   - System monitoring (top, df, du)
   - Package management (apt, yum - simulated)

4. **File Operations**
   - Navigation (cd, ls, pwd)
   - File manipulation (cp, mv, rm, touch)
   - Text processing (grep, sed, awk)
   - Archiving (tar, zip)

### Implementation

#### Docker Container Setup
```python
class TerminalSimulator(Environment):
    def initialize(self, initial_state: dict):
        # Create Docker container with bash
        self.container = docker_client.containers.run(
            image='ubuntu:22.04',
            command='/bin/bash',
            stdin_open=True,
            tty=True,
            detach=True,
            mem_limit='512m',
            cpu_period=100000,
            cpu_quota=50000,
            network_disabled=True,  # Security
            working_dir=initial_state.get('working_directory', '/home/user')
        )
        
        # Set up initial filesystem
        for file_path, file_content in initial_state.get('files', {}).items():
            self._create_file(file_path, file_content)
```

#### Command Execution
```python
def execute_action(self, action: Action) -> ActionResult:
    command = action.command
    
    # Execute in container
    exec_result = self.container.exec_run(
        cmd=f'/bin/bash -c "{command}"',
        stdout=True,
        stderr=True,
        stdin=False,
        tty=False,
        demux=True
    )
    
    return ActionResult(
        exit_code=exec_result.exit_code,
        stdout=exec_result.output[0].decode('utf-8') if exec_result.output[0] else '',
        stderr=exec_result.output[1].decode('utf-8') if exec_result.output[1] else '',
        timestamp=datetime.now()
    )
```

#### Command Parser
```python
class CommandParser:
    def parse(self, command: str) -> ParsedCommand:
        # Handle pipes, redirections, etc.
        parts = shlex.split(command)
        return ParsedCommand(
            command=parts[0],
            args=parts[1:],
            pipes=self._extract_pipes(command),
            redirections=self._extract_redirections(command)
        )
```

### UI Component

```python
def render_ui(self) -> None:
    st.subheader("💻 Terminal")
    
    # Command history display
    history_container = st.container()
    with history_container:
        for cmd in self.command_history:
            st.text(f"$ {cmd.command}")
            if cmd.output:
                st.code(cmd.output, language='bash')
    
    # Command input
    command = st.text_input(
        "Command:",
        key="terminal_input",
        placeholder="$ Enter command..."
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("▶️ Execute"):
            self.execute_command(command)
    
    # Output display
    if self.last_result:
        if self.last_result.exit_code == 0:
            st.success("Command executed successfully")
        else:
            st.error(f"Error (exit code {self.last_result.exit_code})")
        
        if self.last_result.stdout:
            st.code(self.last_result.stdout, language='bash')
        if self.last_result.stderr:
            st.error(self.last_result.stderr)
```

---

## 2️⃣ Code Editor Simulator

### Purpose
Practice writing and editing code with real-time feedback, syntax highlighting, and automated validation.

### Features

#### Monaco Editor Integration
- Full-featured VS Code editor component
- Syntax highlighting for 50+ languages
- IntelliSense/autocomplete
- Multiple file editing
- Keyboard shortcuts (Ctrl+S, Ctrl+Z, etc.)

#### Real-Time Features
- **Linting**: On-the-fly error detection
- **Formatting**: Auto-format on save
- **Type Checking**: Real-time type validation
- **Diff View**: Compare original vs. modified code

#### Code Execution
- Execute code in sandboxed environment
- Capture stdout, stderr, return values
- Timeout protection (5 seconds default)
- Memory and CPU limits

#### Validation Capabilities
- **Syntax Validation**: Code parses correctly
- **Diff Validation**: Specific lines changed
- **Functional Validation**: Output matches expected
- **Style Validation**: Follows style guides (PEP8, etc.)
- **Test Case Validation**: Unit tests pass

### Validation Types

#### 1. Code Diff Validation
```yaml
validation:
  type: code_diff
  changes:
    - line: 15
      expected_contains: "return sum(numbers)"
    - line: 3
      expected_removed: True  # Line should be deleted
```

#### 2. Functional Validation
```yaml
validation:
  type: functional_output
  test_cases:
    - input: [1, 2, 3]
      expected_output: 6
    - input: [10, -5, 3]
      expected_output: 8
```

#### 3. Style Validation
```yaml
validation:
  type: style_check
  tool: black  # or flake8, pylint
  max_violations: 0
```

#### 4. Test Case Validation
```yaml
validation:
  type: unit_tests
  test_file: "test_solution.py"
  min_passing: 5
```

#### 5. AST-Based Validation
```yaml
validation:
  type: ast_check
  requirements:
    - has_function: "calculate_sum"
    - has_docstring: True
    - uses_type_hints: True
```

### Use Cases

1. **Python Functions**
   - Implement algorithms
   - Fix bugs in existing code
   - Add type hints and documentation
   - Optimize performance

2. **Data Transformations**
   - Pandas DataFrame operations
   - Data cleaning and preprocessing
   - Feature engineering
   - Visualization code

3. **Bug Fixes**
   - Identify and fix logic errors
   - Handle edge cases
   - Fix security vulnerabilities
   - Improve error handling

4. **Refactoring**
   - Extract functions
   - Rename variables
   - Simplify complex logic
   - Apply design patterns

### Implementation

#### Monaco Editor Setup
```python
class CodeEditorSimulator(Environment):
    def render_ui(self):
        from streamlit_monaco import st_monaco
        
        # Monaco editor
        edited_code = st_monaco(
            value=self.current_code,
            height=400,
            language=self.language,
            theme="vs-dark",
            options={
                'minimap': {'enabled': False},
                'fontSize': 14,
                'scrollBeyondLastLine': False,
                'automaticLayout': True
            },
            key="code_editor"
        )
        
        self.current_code = edited_code
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("▶️ Run Code"):
                self.execute_code()
        with col2:
            if st.button("🔍 Check Solution"):
                self.validate_code()
        with col3:
            if st.button("📊 Show Diff"):
                self.show_diff()
```

#### Code Execution Sandbox
```python
def execute_code(self, code: str, test_input: Any = None) -> ExecutionResult:
    # Create isolated container
    container = docker_client.containers.run(
        image='python:3.10-slim',
        command='python -c',
        stdin_open=True,
        tty=False,
        detach=True,
        mem_limit='256m',
        cpu_quota=50000,
        network_disabled=True,
        remove=True
    )
    
    try:
        # Execute with timeout
        exec_result = container.exec_run(
            cmd=['python', '-c', code],
            stdin=True,
            stdout=True,
            stderr=True,
            demux=True,
            timeout=5
        )
        
        return ExecutionResult(
            success=exec_result.exit_code == 0,
            stdout=exec_result.output[0].decode() if exec_result.output[0] else '',
            stderr=exec_result.output[1].decode() if exec_result.output[1] else '',
            exit_code=exec_result.exit_code
        )
    finally:
        container.stop()
```

#### AST-Based Validation
```python
import ast

class ASTValidator:
    def validate(self, code: str, requirements: dict) -> ValidationResult:
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return ValidationResult(success=False, error=str(e))
        
        # Check for required function
        if 'has_function' in requirements:
            func_name = requirements['has_function']
            if not self._has_function(tree, func_name):
                return ValidationResult(
                    success=False,
                    error=f"Function '{func_name}' not found"
                )
        
        # Check for docstrings
        if requirements.get('has_docstring'):
            if not self._has_docstring(tree):
                return ValidationResult(
                    success=False,
                    error="Missing docstring"
                )
        
        return ValidationResult(success=True)
```

#### Diff View
```python
def show_diff(self):
    import difflib
    
    original_lines = self.original_code.splitlines()
    current_lines = self.current_code.splitlines()
    
    diff = difflib.unified_diff(
        original_lines,
        current_lines,
        lineterm='',
        fromfile='original.py',
        tofile='modified.py'
    )
    
    diff_text = '\n'.join(diff)
    st.code(diff_text, language='diff')
```

---

## 3️⃣ Infrastructure Builder

### Purpose
Design cloud and container architectures using a visual drag-and-drop interface with real-time validation.

### Features

#### Component Library
- **AWS Services**: EC2, S3, RDS, Lambda, API Gateway, etc.
- **GCP Services**: Compute Engine, Cloud Storage, Cloud Functions, etc.
- **Azure Services**: VMs, Blob Storage, Functions, etc.
- **Docker**: Containers, volumes, networks
- **Kubernetes**: Pods, services, deployments

#### Visual Canvas
- Drag-drop interface
- Automatic layout assistance
- Grid snapping
- Zoom and pan
- Component grouping

#### Connection Validation
- Valid service connections only
- Port compatibility checking
- Network connectivity rules
- Security group validation

#### Configuration Panels
- Service-specific properties
- Environment variables
- Port mappings
- Volume mounts
- Resource limits

#### Export Capabilities
- **Terraform**: Generate .tf files
- **CloudFormation**: Generate templates
- **docker-compose.yml**: Generate compose files
- **Kubernetes YAML**: Generate manifests

### Validation Types

#### 1. Component Presence
```yaml
validation:
  type: component_required
  components:
    - type: "aws:ec2"
      min_count: 1
    - type: "aws:rds"
      min_count: 1
```

#### 2. Connection Validity
```yaml
validation:
  type: connection_valid
  connections:
    - from: "web_server"
      to: "database"
      protocol: "tcp"
      port: 5432
```

#### 3. Configuration Correctness
```yaml
validation:
  type: configuration_check
  component: "web_server"
  properties:
    port: 80
    environment:
      - "NODE_ENV=production"
```

#### 4. Best Practices
```yaml
validation:
  type: best_practice
  rules:
    - security_group_not_0.0.0.0
    - health_check_configured
    - backup_enabled
    - encryption_at_rest
```

### Use Cases

1. **Docker Compose Design**
   - Multi-container applications
   - Service dependencies
   - Network configurations
   - Volume management

2. **AWS Architecture**
   - 3-tier web applications
   - Serverless architectures
   - Data pipelines
   - High-availability setups

3. **Kubernetes Manifests**
   - Microservices deployment
   - StatefulSets and Deployments
   - Services and Ingress
   - ConfigMaps and Secrets

4. **MLOps Pipelines**
   - Data ingestion
   - Training pipelines
   - Model serving
   - Monitoring infrastructure

### Implementation

#### React Flow Integration
```python
class InfrastructureBuilder(Environment):
    def render_ui(self):
        # Use streamlit-agraph or custom React component
        from streamlit_agraph import agraph, Node, Edge, Config
        
        nodes = [
            Node(
                id=comp.id,
                label=comp.name,
                size=25,
                shape="box",
                image=comp.icon_url
            )
            for comp in self.components
        ]
        
        edges = [
            Edge(
                source=conn.from_id,
                target=conn.to_id,
                label=conn.protocol
            )
            for conn in self.connections
        ]
        
        config = Config(
            width=800,
            height=600,
            directed=True,
            physics=True,
            hierarchical=False
        )
        
        selected = agraph(nodes=nodes, edges=edges, config=config)
        
        # Configuration panel
        if selected:
            self.show_config_panel(selected)
```

#### Component Model
```python
@dataclass
class InfraComponent:
    id: str
    type: str  # "aws:ec2", "docker:container", etc.
    name: str
    icon: str
    properties: dict
    connections: list[str]
    position: tuple[int, int]
    
@dataclass
class Connection:
    id: str
    from_id: str
    to_id: str
    protocol: str
    port: int
    bidirectional: bool = False
```

#### Export to IaC
```python
class TerraformExporter:
    def export(self, components: list[InfraComponent]) -> str:
        tf_resources = []
        
        for component in components:
            if component.type.startswith('aws:'):
                tf_resources.append(self._aws_to_terraform(component))
            elif component.type.startswith('gcp:'):
                tf_resources.append(self._gcp_to_terraform(component))
        
        return '\n\n'.join(tf_resources)
    
    def _aws_to_terraform(self, component: InfraComponent) -> str:
        if component.type == 'aws:ec2':
            return f'''
resource "aws_instance" "{component.id}" {{
  ami           = "{component.properties['ami']}"
  instance_type = "{component.properties['instance_type']}"
  
  tags = {{
    Name = "{component.name}"
  }}
}}
'''
```

---

## 4️⃣ Database Query Simulator

### Purpose
Practice SQL queries against realistic sample databases with instant feedback and performance insights.

### Features

#### SQL Editor
- Syntax highlighting
- Autocomplete (table names, columns)
- Multi-query support
- Query history
- Keyboard shortcuts

#### Sample Databases
- Pre-loaded with realistic data
- Multiple database options (e-commerce, social network, healthcare, etc.)
- Data preview capability
- Schema visualization

#### Query Execution
- Instant results
- Result pagination
- Export to CSV/JSON
- Multiple result sets

#### Result Visualization
- Table view (sortable, filterable)
- Chart view (bar, line, pie)
- Query plan visualization
- Performance metrics

#### Query Analysis
- Explain plan
- Index usage
- Execution time
- Rows scanned vs. returned

### Validation Types

#### 1. Result Correctness
```yaml
validation:
  type: query_result
  expected_rows: 5
  expected_columns: ["name", "total_sales"]
  result_hash: "abc123..."  # Hash of expected results
```

#### 2. Query Structure
```yaml
validation:
  type: query_structure
  requirements:
    - has_join: True
    - join_type: "INNER JOIN"
    - has_where: True
    - has_group_by: True
```

#### 3. Performance
```yaml
validation:
  type: query_performance
  max_execution_time_ms: 100
  requires_index_usage: True
  max_rows_scanned: 1000
```

#### 4. Result Comparison
```yaml
validation:
  type: result_match
  compare_with: "SELECT name, SUM(amount) FROM..."
  tolerance: 0.01  # For floating point
```

### Use Cases

1. **SELECT Queries**
   - Basic SELECT with WHERE
   - Sorting and limiting
   - Aggregations (COUNT, SUM, AVG)
   - DISTINCT values

2. **JOINs**
   - INNER JOIN
   - LEFT/RIGHT JOIN
   - FULL OUTER JOIN
   - CROSS JOIN
   - Self-joins

3. **Window Functions**
   - ROW_NUMBER, RANK, DENSE_RANK
   - Running totals
   - Moving averages
   - Partitioning

4. **Subqueries**
   - Scalar subqueries
   - Correlated subqueries
   - EXISTS and IN
   - Common Table Expressions (CTEs)

### Implementation

#### DuckDB Integration
```python
import duckdb

class DatabaseQuerySimulator(Environment):
    def initialize(self, initial_state: dict):
        # Create in-memory database
        self.conn = duckdb.connect(':memory:')
        
        # Load sample data
        sample_db = initial_state.get('database', 'ecommerce')
        self._load_sample_database(sample_db)
        
        # Set query timeout
        self.conn.execute("SET statement_timeout = 5000")  # 5 seconds
    
    def _load_sample_database(self, db_name: str):
        # Load from embedded SQL files
        schema_path = f"scenarios/databases/{db_name}/schema.sql"
        data_path = f"scenarios/databases/{db_name}/data.sql"
        
        with open(schema_path) as f:
            self.conn.execute(f.read())
        
        with open(data_path) as f:
            self.conn.execute(f.read())
```

#### Query Execution
```python
def execute_action(self, action: Action) -> ActionResult:
    query = action.query
    
    try:
        # Execute query
        start_time = time.time()
        result = self.conn.execute(query)
        execution_time = (time.time() - start_time) * 1000  # ms
        
        # Fetch results
        rows = result.fetchall()
        columns = [desc[0] for desc in result.description]
        
        # Get query plan
        plan = self.conn.execute(f"EXPLAIN {query}").fetchall()
        
        return ActionResult(
            success=True,
            rows=rows,
            columns=columns,
            row_count=len(rows),
            execution_time_ms=execution_time,
            query_plan=plan
        )
    except Exception as e:
        return ActionResult(
            success=False,
            error=str(e)
        )
```

#### UI Component
```python
def render_ui(self):
    st.subheader("💾 SQL Query Editor")
    
    # Database schema viewer
    with st.expander("📋 Database Schema"):
        self.show_schema()
    
    # SQL editor
    query = st.text_area(
        "SQL Query:",
        height=150,
        placeholder="SELECT * FROM customers WHERE..."
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("▶️ Execute"):
            result = self.execute_query(query)
            self.display_results(result)
    
    # Results display
    if self.last_result:
        if self.last_result.success:
            st.success(f"Query executed in {self.last_result.execution_time_ms:.2f}ms")
            
            # Results table
            st.dataframe(self.last_result.to_dataframe())
            
            # Query plan
            with st.expander("📊 Query Plan"):
                st.code('\n'.join(self.last_result.query_plan))
        else:
            st.error(self.last_result.error)
```

---

## 5️⃣ API Interaction Simulator

### Purpose
Practice making REST and GraphQL API calls with request building, authentication, and response handling.

### Features

#### Request Builder
- HTTP method selector (GET, POST, PUT, PATCH, DELETE)
- URL builder with path parameters
- Header editor (key-value pairs)
- Query parameter builder
- Request body editor (JSON, form-data, raw)
- File upload support

#### Authentication Simulation
- API key authentication
- Bearer token (JWT)
- OAuth 2.0 flow simulation
- Basic authentication
- Custom headers

#### Mock API Backend
- Configurable mock responses
- Response delays (simulate latency)
- Error injection (timeout, 500, 404, etc.)
- State management (CRUD operations persist)

#### Response Viewer
- Status code display
- Response headers
- JSON formatting and syntax highlighting
- Response time
- Response size
- Pretty-print vs. raw view

#### Documentation Viewer
- Swagger/OpenAPI integration
- Endpoint documentation
- Example requests/responses
- Schema validation

### Validation Types

#### 1. Request Structure
```yaml
validation:
  type: request_structure
  method: POST
  endpoint: "/api/users"
  headers:
    Content-Type: "application/json"
    Authorization: "Bearer {token}"
```

#### 2. Request Body
```yaml
validation:
  type: request_body
  schema:
    type: object
    required: ["name", "email"]
    properties:
      name:
        type: string
      email:
        type: string
        format: email
```

#### 3. Response Handling
```yaml
validation:
  type: response_check
  expected_status: 201
  response_contains:
    id: ".*"
    name: "John Doe"
```

#### 4. Error Handling
```yaml
validation:
  type: error_handling
  scenarios:
    - status: 404
      action: "retry_with_different_id"
    - status: 429
      action: "implement_backoff"
```

### Use Cases

1. **RESTful API Consumption**
   - GET requests with query params
   - POST/PUT with JSON bodies
   - File uploads
   - Pagination handling

2. **GraphQL Queries**
   - Query construction
   - Variables usage
   - Fragments
   - Mutations

3. **Authentication Flows**
   - API key usage
   - JWT token acquisition and usage
   - OAuth 2.0 authorization code flow
   - Refresh token handling

4. **Error Handling**
   - Retry logic
   - Exponential backoff
   - Graceful degradation
   - Error message parsing

### Implementation

#### Mock API Server
```python
from flask import Flask, request, jsonify
import threading

class APIInteractionSimulator(Environment):
    def initialize(self, initial_state: dict):
        # Start mock API server
        self.app = Flask(__name__)
        self.api_spec = initial_state.get('api_spec', {})
        self.state = {}  # For stateful operations
        
        # Register endpoints from spec
        for endpoint in self.api_spec['endpoints']:
            self._register_endpoint(endpoint)
        
        # Start server in background thread
        self.server_thread = threading.Thread(
            target=lambda: self.app.run(port=5000, debug=False)
        )
        self.server_thread.daemon = True
        self.server_thread.start()
    
    def _register_endpoint(self, endpoint: dict):
        @self.app.route(endpoint['path'], methods=[endpoint['method']])
        def handler():
            # Validate request
            if endpoint.get('auth_required'):
                if not request.headers.get('Authorization'):
                    return jsonify({'error': 'Unauthorized'}), 401
            
            # Return mock response
            response = endpoint['response']
            status = endpoint.get('status', 200)
            
            # Simulate delay
            if endpoint.get('delay_ms'):
                time.sleep(endpoint['delay_ms'] / 1000)
            
            return jsonify(response), status
```

#### Request Builder UI
```python
def render_ui(self):
    st.subheader("🌐 API Request Builder")
    
    # Method and URL
    col1, col2 = st.columns([1, 4])
    with col1:
        method = st.selectbox("Method", ["GET", "POST", "PUT", "PATCH", "DELETE"])
    with col2:
        url = st.text_input("URL", value="http://localhost:5000/api/users")
    
    # Headers
    with st.expander("📋 Headers"):
        headers = st.data_editor(
            self.headers,
            num_rows="dynamic",
            column_config={
                "key": st.column_config.TextColumn("Header Name"),
                "value": st.column_config.TextColumn("Header Value")
            }
        )
    
    # Query params
    with st.expander("🔍 Query Parameters"):
        params = st.data_editor(
            self.params,
            num_rows="dynamic"
        )
    
    # Request body
    if method in ["POST", "PUT", "PATCH"]:
        st.text("Request Body:")
        body = st.text_area("JSON Body", height=150)
    
    # Send button
    if st.button("📤 Send Request"):
        response = self.send_request(method, url, headers, params, body)
        self.display_response(response)
```

#### Response Display
```python
def display_response(self, response):
    # Status
    status_color = "green" if 200 <= response.status_code < 300 else "red"
    st.markdown(f"**Status:** :{status_color}[{response.status_code}]")
    st.text(f"Time: {response.elapsed.total_seconds() * 1000:.0f}ms")
    
    # Headers
    with st.expander("Response Headers"):
        st.json(dict(response.headers))
    
    # Body
    st.text("Response Body:")
    try:
        body = response.json()
        st.json(body)
    except:
        st.code(response.text)
```

---

## 6️⃣ ML Pipeline Builder

### Purpose
Design and validate machine learning workflows visually using a node-based pipeline editor.

### Features

#### Node-Based Pipeline Editor
- Drag-drop components
- Visual data flow
- Component library (scikit-learn, pandas, etc.)
- Connection validation (type checking)
- Pipeline execution simulation

#### Component Library
- **Data Loaders**: CSV, JSON, SQL, API
- **Preprocessors**: Normalization, encoding, imputation
- **Feature Engineering**: PCA, polynomial features, binning
- **Models**: Linear, tree-based, ensemble, neural networks
- **Evaluators**: Metrics, cross-validation, confusion matrix
- **Visualizers**: Plots, charts, dashboards

#### Data Flow Visualization
- Show data shape at each stage
- Highlight data transformations
- Type compatibility checking
- Missing data tracking

#### Pipeline Validation
- Component compatibility
- Data shape validation
- Required parameter checking
- Best practice enforcement

#### Execution Simulation
- Step-by-step execution
- Intermediate results display
- Performance metrics
- Error detection

### Validation Types

#### 1. Pipeline Structure
```yaml
validation:
  type: pipeline_structure
  required_components:
    - type: "data_loader"
    - type: "train_test_split"
    - type: "model"
    - type: "evaluator"
```

#### 2. Data Flow
```yaml
validation:
  type: data_flow
  checks:
    - from: "data_loader"
      to: "preprocessor"
      shape: "(n_samples, n_features)"
    - from: "model"
      to: "evaluator"
      type: "predictions"
```

#### 3. Configuration
```yaml
validation:
  type: component_config
  component: "random_forest"
  properties:
    n_estimators: {min: 10, max: 1000}
    max_depth: {min: 1, max: 50}
    random_state: {required: True}
```

#### 4. Best Practices
```yaml
validation:
  type: best_practice
  rules:
    - train_test_split_before_preprocessing
    - normalization_before_pca
    - cross_validation_used
    - hyperparameter_tuning_present
```

### Use Cases

1. **End-to-End ML Workflows**
   - Load data
   - Preprocess
   - Train model
   - Evaluate
   - Deploy

2. **Data Preprocessing**
   - Handle missing values
   - Encode categorical variables
   - Normalize/standardize
   - Feature selection

3. **Model Selection**
   - Compare multiple models
   - Hyperparameter tuning
   - Ensemble methods
   - Cross-validation

4. **Evaluation Pipelines**
   - Multiple metrics
   - Confusion matrix
   - ROC curves
   - Feature importance

### Implementation

#### Pipeline Node Model
```python
@dataclass
class PipelineNode:
    id: str
    type: str  # "data_loader", "model", "preprocessor", etc.
    component: str  # "RandomForestClassifier", "StandardScaler", etc.
    parameters: dict
    inputs: list[str]  # Node IDs
    outputs: list[str]  # Node IDs
    position: tuple[int, int]
    
    def execute(self, input_data):
        # Execute component logic
        if self.type == "model":
            model = self._create_model()
            return model.fit(input_data['X'], input_data['y'])
        elif self.type == "preprocessor":
            transformer = self._create_transformer()
            return transformer.fit_transform(input_data)
```

#### Visual Pipeline Editor
```python
def render_ui(self):
    from streamlit_agraph import agraph, Node, Edge
    
    # Component palette
    with st.sidebar:
        st.subheader("🧩 Components")
        component = st.selectbox("Add Component", [
            "Data Loader",
            "Train/Test Split",
            "StandardScaler",
            "RandomForestClassifier",
            "Model Evaluator"
        ])
        if st.button("➕ Add"):
            self.add_component(component)
    
    # Pipeline canvas
    nodes = [
        Node(
            id=node.id,
            label=node.component,
            shape="box"
        )
        for node in self.pipeline_nodes
    ]
    
    edges = [
        Edge(source=conn.from_id, target=conn.to_id)
        for conn in self.connections
    ]
    
    selected = agraph(nodes=nodes, edges=edges)
    
    # Component configuration
    if selected:
        self.show_component_config(selected)
```

#### Pipeline Execution
```python
def execute_pipeline(self):
    # Topological sort to determine execution order
    execution_order = self._topological_sort(self.pipeline_nodes)
    
    data_cache = {}
    
    for node in execution_order:
        # Get input data from previous nodes
        input_data = {
            input_id: data_cache[input_id]
            for input_id in node.inputs
        }
        
        # Execute node
        output_data = node.execute(input_data)
        
        # Cache output
        data_cache[node.id] = output_data
        
        # Display intermediate results
        st.write(f"✅ {node.component} completed")
        st.write(f"Output shape: {output_data.shape if hasattr(output_data, 'shape') else 'N/A'}")
    
    return data_cache
```

---

## 7️⃣ Docker Compose Designer

### Purpose
Build docker-compose.yml files interactively with visual service relationship diagrams and real-time validation.

### Features

#### Service Definition Wizard
- Step-by-step service creation
- Image selection
- Port mapping
- Volume configuration
- Network setup
- Environment variables
- Dependencies

#### YAML Editor
- Syntax highlighting
- Auto-completion
- Real-time validation
- Format on save
- Error highlighting

#### Visual Service Diagram
- Service boxes with ports
- Network connections
- Volume mounts
- Dependency arrows
- Color-coded status

#### Configuration Panels
- **Service**: Image, command, entrypoint
- **Ports**: Host:container mappings
- **Volumes**: Bind mounts, named volumes
- **Networks**: Network modes, custom networks
- **Environment**: Key-value pairs, .env file
- **Resources**: CPU, memory limits
- **Health Checks**: Commands, intervals

#### Live YAML Preview
- Real-time YAML generation
- Validation feedback
- Copy to clipboard
- Download file

#### Deployment Simulation
- `docker-compose up` simulation
- Service startup order
- Health check simulation
- Log output preview

### Validation Types

#### 1. YAML Syntax
```yaml
validation:
  type: yaml_syntax
  strict: True
```

#### 2. Service Configuration
```yaml
validation:
  type: service_config
  service: "web"
  checks:
    - has_image: True
    - has_ports: True
    - has_healthcheck: True
```

#### 3. Network Connectivity
```yaml
validation:
  type: network_connectivity
  requirements:
    - service: "web"
      can_reach: "database"
      network: "backend"
```

#### 4. Volume Mounts
```yaml
validation:
  type: volume_validation
  service: "app"
  volumes:
    - type: "bind"
      source: "./data"
      target: "/app/data"
      read_only: True
```

#### 5. Best Practices
```yaml
validation:
  type: best_practices
  rules:
    - no_latest_tag
    - health_checks_present
    - restart_policy_set
    - resource_limits_set
    - networks_explicit
```

### Use Cases

1. **Multi-Container Applications**
   - Web + Database + Cache
   - Microservices architecture
   - Full-stack applications
   - Load-balanced setups

2. **Development Environments**
   - Local database
   - Mock API servers
   - Message queues
   - Monitoring stack

3. **Testing Environments**
   - Integration test dependencies
   - Isolated test databases
   - Mock external services

4. **Production-Like Setups**
   - Load balancers
   - Reverse proxies
   - SSL termination
   - Logging and monitoring

### Implementation

#### Service Model
```python
@dataclass
class DockerService:
    name: str
    image: str
    ports: list[str]  # ["8080:80"]
    volumes: list[str]  # ["./data:/app/data"]
    environment: dict[str, str]
    networks: list[str]
    depends_on: list[str]
    healthcheck: dict
    restart: str = "unless-stopped"
    
    def to_yaml(self) -> dict:
        service_def = {
            'image': self.image,
        }
        
        if self.ports:
            service_def['ports'] = self.ports
        
        if self.volumes:
            service_def['volumes'] = self.volumes
        
        if self.environment:
            service_def['environment'] = self.environment
        
        if self.networks:
            service_def['networks'] = self.networks
        
        if self.depends_on:
            service_def['depends_on'] = self.depends_on
        
        if self.healthcheck:
            service_def['healthcheck'] = self.healthcheck
        
        service_def['restart'] = self.restart
        
        return service_def
```

#### UI Component
```python
def render_ui(self):
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🛠️ Service Builder")
        
        # Service name
        service_name = st.text_input("Service Name")
        
        # Image
        image = st.text_input("Docker Image", placeholder="nginx:latest")
        
        # Ports
        st.text("Ports (host:container)")
        ports = st.data_editor(
            self.current_ports,
            num_rows="dynamic"
        )
        
        # Volumes
        st.text("Volumes")
        volumes = st.data_editor(
            self.current_volumes,
            num_rows="dynamic"
        )
        
        # Add service button
        if st.button("➕ Add Service"):
            self.add_service(service_name, image, ports, volumes)
    
    with col2:
        st.subheader("📄 docker-compose.yml")
        
        # Generate YAML
        compose_yaml = self.generate_yaml()
        
        # YAML editor
        edited_yaml = st.text_area(
            "YAML",
            value=compose_yaml,
            height=400
        )
        
        # Validate button
        if st.button("✅ Validate"):
            validation_result = self.validate_yaml(edited_yaml)
            if validation_result.success:
                st.success("Valid docker-compose.yml!")
            else:
                st.error(validation_result.error)
    
    # Visual diagram
    st.subheader("📊 Service Diagram")
    self.show_service_diagram()
```

#### YAML Generation
```python
def generate_yaml(self) -> str:
    compose_dict = {
        'version': '3.8',
        'services': {},
        'networks': {},
        'volumes': {}
    }
    
    # Add services
    for service in self.services:
        compose_dict['services'][service.name] = service.to_yaml()
    
    # Add networks
    for network in self.networks:
        compose_dict['networks'][network] = {'driver': 'bridge'}
    
    # Add volumes
    for volume in self.volumes:
        compose_dict['volumes'][volume] = {}
    
    # Convert to YAML
    return yaml.dump(compose_dict, default_flow_style=False, sort_keys=False)
```

#### Validation
```python
import yaml
from jsonschema import validate, ValidationError

def validate_yaml(self, yaml_content: str) -> ValidationResult:
    try:
        # Parse YAML
        compose_dict = yaml.safe_load(yaml_content)
        
        # Validate against schema
        schema = self.load_compose_schema()
        validate(instance=compose_dict, schema=schema)
        
        # Additional validation
        errors = []
        
        # Check for best practices
        for service_name, service in compose_dict.get('services', {}).items():
            # No 'latest' tag
            if service.get('image', '').endswith(':latest'):
                errors.append(f"Service '{service_name}' uses ':latest' tag")
            
            # Health checks
            if not service.get('healthcheck'):
                errors.append(f"Service '{service_name}' missing health check")
        
        if errors:
            return ValidationResult(success=False, warnings=errors)
        
        return ValidationResult(success=True)
        
    except yaml.YAMLError as e:
        return ValidationResult(success=False, error=f"YAML syntax error: {e}")
    except ValidationError as e:
        return ValidationResult(success=False, error=f"Schema validation error: {e.message}")
```

---

## Environment Comparison Matrix

| Feature | Terminal | Code Editor | Infrastructure | Database | API | ML Pipeline | Docker Compose |
|---------|----------|-------------|----------------|----------|-----|-------------|----------------|
| **Complexity** | Low | Medium | High | Medium | Medium | High | Medium |
| **Execution Model** | Command-line | Code exec | Design-only | Query exec | HTTP requests | Pipeline exec | Design + simulate |
| **Validation Approach** | Output-based | Multi-criteria | Structural | Result-based | Request/response | Graph-based | YAML + structural |
| **Docker Required** | Yes | Yes | No | No | Optional | Optional | Yes (simulate) |
| **Real-Time Feedback** | Immediate | Immediate | On-action | Immediate | On-request | On-execute | On-edit |
| **Best For** | DevOps tasks | Coding practice | Architecture | Data analysis | API testing | ML workflows | Container orchestration |

---

## Common Patterns

### Error Handling
All environments implement consistent error handling:
```python
try:
    result = environment.execute_action(action)
except TimeoutError:
    return ActionResult(error="Execution timeout (5 minutes exceeded)")
except ResourceExhaustedError:
    return ActionResult(error="Resource limit exceeded")
except Exception as e:
    return ActionResult(error=f"Unexpected error: {str(e)}")
```

### State Serialization
All environments must support state serialization:
```python
def get_state(self) -> dict:
    return {
        'environment_type': self.type,
        'current_state': self._serialize_state(),
        'timestamp': datetime.now().isoformat()
    }

def restore_state(self, state: dict):
    self._deserialize_state(state['current_state'])
```

### Resource Cleanup
All environments must clean up resources:
```python
def cleanup(self):
    # Stop containers
    if self.container:
        self.container.stop()
        self.container.remove()
    
    # Delete temp files
    if self.temp_dir:
        shutil.rmtree(self.temp_dir)
    
    # Close connections
    if self.db_connection:
        self.db_connection.close()
```

---

## Extensibility

New environment types can be added by:
1. Extending `Environment` base class
2. Implementing all abstract methods
3. Defining validation rules
4. Creating UI component
5. Adding scenario templates
6. Writing documentation

Example skeleton:
```python
class CustomEnvironment(Environment):
    def initialize(self, initial_state: dict) -> None:
        # Setup environment
        pass
    
    def execute_action(self, action: Action) -> ActionResult:
        # Execute user action
        pass
    
    def get_state(self) -> dict:
        # Return current state
        pass
    
    def reset(self) -> None:
        # Reset to initial state
        pass
    
    def cleanup(self) -> None:
        # Clean up resources
        pass
    
    def render_ui(self) -> StreamlitComponent:
        # Render Streamlit UI
        pass
```

---

This comprehensive environment type specification enables SimulationPlayer to support diverse technical learning scenarios while maintaining consistency, safety, and excellent user experience.
