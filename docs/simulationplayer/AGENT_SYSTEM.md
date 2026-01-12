# SimulationPlayer Agent System

This document specifies the 5 AI-powered agents that provide intelligent guidance, validation, error recovery, hints, and contextual help throughout the simulation experience.

---

## Agent Architecture

All agents use OLLAMA for local LLM inference and share a common base architecture:

```python
class BaseAgent(ABC):
    """Base class for all AI agents"""
    
    def __init__(self, model: str, ollama_endpoint: str = "http://localhost:11434"):
        self.model = model
        self.ollama_endpoint = ollama_endpoint
        self.ollama_client = OllamaClient(ollama_endpoint)
        self.prompt_templates = self._load_prompt_templates()
        self.response_cache = {}  # Cache for common queries
    
    @abstractmethod
    def generate_response(self, context: dict) -> AgentResponse:
        """Generate agent-specific response based on context"""
        pass
    
    def _call_llm(self, prompt: str, system_prompt: str = None) -> str:
        """Make LLM API call with caching"""
        cache_key = hashlib.md5(f"{system_prompt}{prompt}".encode()).hexdigest()
        
        if cache_key in self.response_cache:
            return self.response_cache[cache_key]
        
        response = self.ollama_client.generate(
            model=self.model,
            prompt=prompt,
            system=system_prompt,
            options={
                'temperature': 0.7,
                'top_p': 0.9,
                'max_tokens': 500
            }
        )
        
        self.response_cache[cache_key] = response['response']
        return response['response']
    
    @abstractmethod
    def _load_prompt_templates(self) -> dict:
        """Load agent-specific prompt templates"""
        pass
```

---

## 1️⃣ Step Guide Agent

### Purpose
Provide personalized, contextual explanations for each simulation step without spoiling the solution.

### Capabilities

#### 1. Generate Personalized Explanations
- Explain what the current step aims to achieve
- Provide context on why this step matters
- Adapt language to user's skill level
- Encourage without revealing the answer

#### 2. Adapt Tone to User Tier
- **Basic Tier**: More detailed, beginner-friendly
- **Intermediate Tier**: Balanced detail, assumes basic knowledge
- **Advanced Tier**: Concise, assumes expertise

#### 3. Provide Context
- Link to broader learning objectives
- Connect to previous steps
- Explain real-world applications
- Highlight best practices

#### 4. Encourage Learning
- Positive reinforcement
- Build confidence
- Frame challenges as opportunities
- Celebrate progress

### Inputs
```python
@dataclass
class StepGuideInput:
    step_definition: Step
    user_context: UserContext
    previous_attempts: list[Attempt]
    scenario_context: ScenarioContext
    user_tier: str  # 'basic', 'intermediate', 'advanced'
```

### LLM Usage

**Model**: `llama3.2:3b` (lightweight, fast, good for short guidance)

**System Prompt Template**:
```python
SYSTEM_PROMPT = """You are a friendly, encouraging technical instructor guiding a student through an interactive lab simulation.

Your role is to:
1. Explain WHAT the student needs to accomplish (objective)
2. Explain WHY it's important (context and real-world relevance)
3. Provide a gentle nudge toward the APPROACH (without revealing the exact command/code)
4. Be encouraging and supportive

IMPORTANT:
- DO NOT reveal the exact solution or command
- DO NOT provide copy-paste code
- DO encourage experimentation
- DO use simple, clear language
- Keep responses to 2-4 sentences
- Match the tone to the student's skill level

Student Level: {user_tier}
Environment: {environment_type}
"""
```

**User Prompt Template**:
```python
USER_PROMPT = """Current Step: {step_title}

Objective: {step_objective}

Description: {step_description}

Student Context:
- Previous attempts: {num_attempts}
- Time on step: {time_spent}
- Hints used: {hints_used}

Generate clear, encouraging guidance for this step. Help the student understand what to do and why, without revealing the exact solution.
"""
```

### Output

```python
@dataclass
class StepGuideResponse:
    guidance_text: str  # Markdown-formatted guidance
    confidence: float  # 0-1, confidence in guidance quality
    key_concepts: list[str]  # Key concepts covered
    estimated_reading_time: int  # Seconds
```

### Example Prompts and Responses

#### Example 1: Docker Pull Image (Intermediate)

**Input**:
```python
step = {
    'title': 'Pull NGINX Image',
    'objective': 'Download the official NGINX image from Docker Hub',
    'description': 'Use Docker to pull the latest NGINX web server image'
}
user_context = {
    'tier': 'intermediate',
    'attempts': 0,
    'time_spent': '30s'
}
```

**Generated Guidance**:
```markdown
Great! Let's download the NGINX image from Docker Hub. Docker images are like templates for containers – think of them as pre-packaged applications ready to run.

The `docker pull` command downloads images from Docker Hub (Docker's public registry). You'll need to specify the image name, which is simply "nginx" for the official NGINX image.

This is a common first step in any Docker workflow – you can't run a container without an image!
```

#### Example 2: Python Bug Fix (Advanced)

**Input**:
```python
step = {
    'title': 'Fix Off-by-One Error',
    'objective': 'Correct the logic error causing incorrect array indexing',
    'description': 'The function returns wrong results for edge cases due to incorrect loop bounds'
}
user_context = {
    'tier': 'advanced',
    'attempts': 1,
    'time_spent': '2m 15s'
}
```

**Generated Guidance**:
```markdown
Classic off-by-one error. Look carefully at your loop bounds – are you covering all elements? Pay special attention to the final iteration and array boundaries.

Test with edge cases like empty arrays and single-element arrays to isolate the issue.
```

#### Example 3: SQL Join (Beginner - Basic Tier)

**Input**:
```python
step = {
    'title': 'Write INNER JOIN Query',
    'objective': 'Combine customers and orders tables',
    'description': 'Write a query that shows customer names with their order totals'
}
user_context = {
    'tier': 'basic',
    'attempts': 2,
    'time_spent': '5m'
}
```

**Generated Guidance**:
```markdown
You're working on connecting two tables – customers and orders. Think of it like merging two spreadsheets based on a common column.

An INNER JOIN combines rows from both tables where there's a match. You'll need to specify:
1. Which tables to join (customers and orders)
2. What column they have in common (usually customer_id)
3. Which columns you want to see in the results

The basic syntax is: SELECT columns FROM table1 INNER JOIN table2 ON matching_condition

Take your time – JOINs are one of the most powerful SQL features and worth understanding well!
```

### Implementation

```python
class StepGuideAgent(BaseAgent):
    def __init__(self):
        super().__init__(model='llama3.2:3b')
    
    def generate_response(self, context: dict) -> StepGuideResponse:
        # Extract context
        step = context['step_definition']
        user_context = context['user_context']
        
        # Build prompt
        system_prompt = self.prompt_templates['system'].format(
            user_tier=user_context.tier,
            environment_type=step.environment_type
        )
        
        user_prompt = self.prompt_templates['user'].format(
            step_title=step.title,
            step_objective=step.objective,
            step_description=step.description,
            num_attempts=len(user_context.previous_attempts),
            time_spent=user_context.time_on_step,
            hints_used=user_context.hints_used
        )
        
        # Call LLM
        guidance_text = self._call_llm(user_prompt, system_prompt)
        
        # Extract key concepts (simple keyword extraction)
        key_concepts = self._extract_key_concepts(step.description)
        
        return StepGuideResponse(
            guidance_text=guidance_text,
            confidence=0.85,
            key_concepts=key_concepts,
            estimated_reading_time=len(guidance_text.split()) // 3
        )
    
    def _extract_key_concepts(self, text: str) -> list[str]:
        # Simple keyword extraction (in production, use NLP library)
        keywords = ['docker', 'container', 'image', 'pull', 'run', 'join', 'sql', 'query']
        return [kw for kw in keywords if kw.lower() in text.lower()]
    
    def _load_prompt_templates(self) -> dict:
        return {
            'system': SYSTEM_PROMPT,
            'user': USER_PROMPT
        }
```

---

## 2️⃣ Validation Agent

### Purpose
Check if user's action meets step requirements using rule-based validation with fuzzy matching support.

### Capabilities

#### 1. Rule-Based Validation
- Command structure validation
- Output verification
- State change checking
- Multi-criteria validation

#### 2. Accept Multiple Valid Solutions
- Recognize equivalent commands
- Support alternative approaches
- Fuzzy matching for minor variations

#### 3. Fuzzy Matching
- Ignore whitespace differences
- Accept flag order variations
- Recognize command aliases
- Handle optional parameters

#### 4. Post-Action Validation
- Verify side effects
- Check environment state
- Validate file system changes
- Confirm service status

### Inputs

```python
@dataclass
class ValidationInput:
    user_action: Action
    step_definition: Step
    environment_state: dict
    validation_rules: list[ValidationRule]
```

### Validation Rule Types

#### 1. Command Exact Match
```python
{
    'type': 'command_exact',
    'expected': 'docker pull nginx'
}
```

#### 2. Command Contains
```python
{
    'type': 'command_contains',
    'substring': 'docker pull',
    'case_sensitive': False
}
```

#### 3. Command Regex
```python
{
    'type': 'command_regex',
    'pattern': r'^docker (pull|image pull) nginx(:[\w\.-]+)?$',
    'flags': re.IGNORECASE
}
```

#### 4. Exit Code
```python
{
    'type': 'exit_code',
    'expected': 0
}
```

#### 5. Output Contains
```python
{
    'type': 'output_contains',
    'text': 'Status: Downloaded',
    'location': 'stdout'  # or 'stderr'
}
```

#### 6. Output Regex
```python
{
    'type': 'output_regex',
    'pattern': r'sha256:[a-f0-9]{64}',
    'location': 'stdout'
}
```

#### 7. File Exists
```python
{
    'type': 'file_exists',
    'path': '/home/user/output.txt',
    'must_exist': True
}
```

#### 8. File Content
```python
{
    'type': 'file_content',
    'path': '/home/user/config.yml',
    'contains': 'port: 8080'
}
```

#### 9. Container Running
```python
{
    'type': 'container_running',
    'container_name': 'nginx_server',
    'expected_status': 'running'
}
```

#### 10. Code Passes Tests
```python
{
    'type': 'code_tests',
    'test_cases': [
        {'input': [1, 2, 3], 'expected': 6},
        {'input': [], 'expected': 0}
    ]
}
```

### Fuzzy Matching Examples

#### Command Equivalence
```python
COMMAND_ALIASES = {
    'docker ps': ['docker container ls', 'docker container list'],
    'docker images': ['docker image ls', 'docker image list'],
    'll': ['ls -la', 'ls -l -a']
}

def fuzzy_match_command(user_cmd: str, expected_cmd: str) -> bool:
    # Normalize whitespace
    user_normalized = ' '.join(user_cmd.split())
    expected_normalized = ' '.join(expected_cmd.split())
    
    # Exact match
    if user_normalized == expected_normalized:
        return True
    
    # Check aliases
    if user_normalized in COMMAND_ALIASES.get(expected_normalized, []):
        return True
    
    # Check flag order variations (for simple cases)
    if _flags_match(user_normalized, expected_normalized):
        return True
    
    return False
```

#### Flag Order Independence
```python
def _flags_match(cmd1: str, cmd2: str) -> bool:
    """Check if commands match ignoring flag order"""
    parts1 = cmd1.split()
    parts2 = cmd2.split()
    
    # Must have same base command
    if parts1[0] != parts2[0]:
        return False
    
    # Extract flags and arguments
    flags1 = {p for p in parts1[1:] if p.startswith('-')}
    flags2 = {p for p in parts2[1:] if p.startswith('-')}
    
    args1 = [p for p in parts1[1:] if not p.startswith('-')]
    args2 = [p for p in parts2[1:] if not p.startswith('-')]
    
    return flags1 == flags2 and args1 == args2
```

### Output

```python
@dataclass
class ValidationResult:
    is_valid: bool
    message: str
    errors: list[ValidationError]
    warnings: list[ValidationWarning]
    passed_rules: list[str]
    failed_rules: list[str]
    confidence: float  # 0-1
```

### Implementation

```python
class ValidationAgent(BaseAgent):
    def __init__(self):
        # Validation Agent doesn't necessarily need LLM for rule-based validation
        # But can use it for complex/ambiguous cases
        super().__init__(model='llama3.2:3b')
        self.validators = {
            'command_exact': self._validate_command_exact,
            'command_contains': self._validate_command_contains,
            'command_regex': self._validate_command_regex,
            'exit_code': self._validate_exit_code,
            'output_contains': self._validate_output_contains,
            'file_exists': self._validate_file_exists,
            'container_running': self._validate_container_running,
            # ... more validators
        }
    
    def generate_response(self, context: dict) -> ValidationResult:
        """This is actually 'validate' rather than 'generate_response'"""
        return self.validate(
            context['user_action'],
            context['validation_rules'],
            context['environment_state']
        )
    
    def validate(self, action: Action, rules: list[ValidationRule], 
                 env_state: dict) -> ValidationResult:
        errors = []
        warnings = []
        passed_rules = []
        failed_rules = []
        
        for rule in rules:
            validator = self.validators.get(rule.type)
            if not validator:
                warnings.append(f"Unknown validation rule: {rule.type}")
                continue
            
            try:
                result = validator(action, rule, env_state)
                if result.passed:
                    passed_rules.append(rule.type)
                else:
                    failed_rules.append(rule.type)
                    errors.append(result.error)
            except Exception as e:
                errors.append(f"Validation error: {str(e)}")
        
        is_valid = len(errors) == 0
        message = "All validations passed!" if is_valid else "Some validations failed"
        
        return ValidationResult(
            is_valid=is_valid,
            message=message,
            errors=errors,
            warnings=warnings,
            passed_rules=passed_rules,
            failed_rules=failed_rules,
            confidence=1.0 if is_valid else 0.0
        )
    
    def _validate_command_exact(self, action: Action, rule: ValidationRule, 
                                env_state: dict) -> RuleResult:
        expected = rule.parameters['expected']
        actual = action.command
        
        # Fuzzy match
        if self.fuzzy_match_command(actual, expected):
            return RuleResult(passed=True)
        
        return RuleResult(
            passed=False,
            error=f"Expected command '{expected}', got '{actual}'"
        )
    
    def _validate_output_contains(self, action: Action, rule: ValidationRule,
                                  env_state: dict) -> RuleResult:
        text = rule.parameters['text']
        location = rule.parameters.get('location', 'stdout')
        
        output = action.result.stdout if location == 'stdout' else action.result.stderr
        
        if text in output:
            return RuleResult(passed=True)
        
        return RuleResult(
            passed=False,
            error=f"Output does not contain '{text}'"
        )
    
    def fuzzy_match_command(self, user_cmd: str, expected_cmd: str) -> bool:
        # Normalize
        user_normalized = ' '.join(user_cmd.strip().split())
        expected_normalized = ' '.join(expected_cmd.strip().split())
        
        # Exact match
        if user_normalized == expected_normalized:
            return True
        
        # Common variations
        variations = [
            # docker pull nginx == docker pull nginx:latest
            (r'^docker pull nginx$', r'^docker pull nginx:latest$'),
            # docker run -d nginx == docker run --detach nginx
            (r'-d\b', r'--detach'),
            (r'-p\b', r'--publish'),
        ]
        
        for pattern, replacement in variations:
            if re.search(pattern, user_normalized) and re.search(replacement, expected_normalized):
                return True
        
        return False
    
    def _load_prompt_templates(self) -> dict:
        # Validation Agent primarily uses rule-based logic
        # LLM can be used for ambiguous cases
        return {}
```

---

## 3️⃣ Error Recovery Agent

### Purpose
Diagnose user mistakes and provide specific, actionable corrections with educational explanations.

### Capabilities

#### 1. Detect Common Mistakes
- Pattern matching against known error types
- Predefined mistake database
- Context-aware detection

#### 2. AI-Powered Error Analysis
- Handle novel/unexpected errors
- Use LLM to analyze unfamiliar failures
- Provide intelligent suggestions

#### 3. Provide Specific Corrections
- Exact fix when applicable
- Multiple solution paths
- Educational explanations

#### 4. Explain Educationally
- Why the error occurred
- What to learn from it
- How to avoid in future

### Inputs

```python
@dataclass
class ErrorRecoveryInput:
    user_action: Action
    step_definition: Step
    validation_errors: list[ValidationError]
    environment_state: dict
    previous_attempts: list[Attempt]
```

### Common Mistake Patterns

#### Pattern Database
```python
COMMON_MISTAKES = [
    {
        'pattern': r'^docker run nginx$',
        'expected': r'^docker run -d nginx$',
        'error_type': 'missing_flag',
        'explanation': 'Container runs in foreground, blocking terminal',
        'suggestion': 'Add -d flag to run in detached (background) mode',
        'correction': 'docker run -d nginx'
    },
    {
        'pattern': r'^git commit$',
        'expected': r'^git commit -m',
        'error_type': 'missing_required_flag',
        'explanation': 'Git commit requires a commit message',
        'suggestion': 'Add -m flag with a message',
        'correction': 'git commit -m "Your message"'
    },
    {
        'pattern': r'^docker ps$',
        'context': 'no containers shown',
        'error_type': 'missing_flag',
        'explanation': 'docker ps only shows running containers by default',
        'suggestion': 'Add -a flag to see all containers (including stopped)',
        'correction': 'docker ps -a'
    },
    {
        'pattern': r'^kubectl get pods$',
        'context': 'no pods found',
        'error_type': 'wrong_namespace',
        'explanation': 'Pods might be in different namespace',
        'suggestion': 'Specify namespace with -n flag or use --all-namespaces',
        'correction': 'kubectl get pods --all-namespaces'
    }
]
```

#### Mistake Detection
```python
def detect_common_mistake(user_cmd: str, expected_cmd: str, 
                         output: str) -> Optional[Mistake]:
    for pattern in COMMON_MISTAKES:
        if re.match(pattern['pattern'], user_cmd):
            # Check if context matches (if specified)
            if 'context' in pattern:
                if pattern['context'] not in output.lower():
                    continue
            
            return Mistake(
                type=pattern['error_type'],
                explanation=pattern['explanation'],
                suggestion=pattern['suggestion'],
                correction=pattern.get('correction')
            )
    
    return None
```

### LLM Usage

**Model**: `llama3.2:3b`

**System Prompt**:
```python
SYSTEM_PROMPT = """You are a technical debugging assistant helping students learn from their mistakes.

When a student makes an error, your job is to:
1. Identify what went wrong
2. Explain WHY it went wrong (educationally)
3. Suggest how to fix it
4. Encourage them to try again

Be supportive and educational. Frame mistakes as learning opportunities.

DO:
- Explain the root cause
- Provide specific, actionable fixes
- Use simple language
- Be encouraging

DON'T:
- Just give the answer without explanation
- Use condescending language
- Overwhelm with too much information
"""
```

**User Prompt**:
```python
USER_PROMPT = """Step Objective: {step_objective}

Expected Action: {expected_action}

Student's Action: {actual_action}

Error: {error_message}

Environment Output:
{output}

Analyze this error and provide:
1. What went wrong (1 sentence)
2. Why it happened (1-2 sentences)
3. How to fix it (specific suggestion)
"""
```

### Output

```python
@dataclass
class ErrorRecoveryResponse:
    error_type: str  # 'common_mistake' | 'validation_failure' | 'execution_error'
    explanation: str  # User-friendly error explanation
    suggestion: str  # How to fix it
    correction: Optional[str]  # Exact command/code to try (if applicable)
    learning_point: str  # Key takeaway
    confidence: float  # 0-1
```

### Example Scenarios

#### Example 1: Missing Docker Flag

**Input**:
```python
user_action = "docker run nginx"
expected = "docker run -d nginx"
error = "Container started but terminal is blocked"
```

**Response**:
```python
ErrorRecoveryResponse(
    error_type='common_mistake',
    explanation='Your container started successfully, but it's running in the foreground, which blocks your terminal.',
    suggestion='Add the -d (detached) flag to run the container in the background.',
    correction='docker run -d nginx',
    learning_point='The -d flag is essential for running containers as background services.',
    confidence=0.95
)
```

#### Example 2: Wrong Argument Order

**Input**:
```python
user_action = "docker run nginx -p 8080:80"
expected = "docker run -p 8080:80 nginx"
error = "Invalid syntax"
```

**Response**:
```python
ErrorRecoveryResponse(
    error_type='common_mistake',
    explanation='Docker flags must come before the image name.',
    suggestion='Put -p 8080:80 before nginx in your command.',
    correction='docker run -p 8080:80 nginx',
    learning_point='Docker command structure: docker run [FLAGS] IMAGE [COMMAND]',
    confidence=0.90
)
```

#### Example 3: Novel Error (LLM-Powered)

**Input**:
```python
user_action = "SELECT * FROM users WHERE age > 18 AND name LIKE '%John%' OR status = 'active'"
expected = "Proper use of AND/OR precedence"
error = "Results include inactive users named John"
```

**LLM Response**:
```python
ErrorRecoveryResponse(
    error_type='validation_failure',
    explanation='The AND and OR operators have different precedence. Your query is interpreted as (age > 18 AND name LIKE '%John%') OR (status = 'active'), which includes ALL active users, even if they're under 18.',
    suggestion='Use parentheses to control precedence: WHERE age > 18 AND (name LIKE '%John%' OR status = 'active')',
    correction='SELECT * FROM users WHERE age > 18 AND (name LIKE '%John%' OR status = 'active')',
    learning_point='Always use parentheses with AND/OR to make your intent explicit.',
    confidence=0.85
)
```

### Implementation

```python
class ErrorRecoveryAgent(BaseAgent):
    def __init__(self):
        super().__init__(model='llama3.2:3b')
        self.common_mistakes = self._load_common_mistakes()
    
    def generate_response(self, context: dict) -> ErrorRecoveryResponse:
        user_action = context['user_action']
        step_def = context['step_definition']
        errors = context['validation_errors']
        
        # First, check for common mistakes
        mistake = self._detect_common_mistake(
            user_action.command,
            step_def.expected_action,
            user_action.result.output
        )
        
        if mistake:
            return ErrorRecoveryResponse(
                error_type='common_mistake',
                explanation=mistake.explanation,
                suggestion=mistake.suggestion,
                correction=mistake.correction,
                learning_point=mistake.learning_point,
                confidence=0.90
            )
        
        # If not a known mistake, use LLM
        return self._ai_analyze_error(context)
    
    def _ai_analyze_error(self, context: dict) -> ErrorRecoveryResponse:
        system_prompt = self.prompt_templates['system']
        
        user_prompt = self.prompt_templates['user'].format(
            step_objective=context['step_definition'].objective,
            expected_action=context['step_definition'].expected_action,
            actual_action=context['user_action'].command,
            error_message=', '.join([e.message for e in context['validation_errors']]),
            output=context['user_action'].result.output
        )
        
        response_text = self._call_llm(user_prompt, system_prompt)
        
        # Parse LLM response (in production, use structured output)
        return ErrorRecoveryResponse(
            error_type='validation_failure',
            explanation=response_text,
            suggestion=response_text,  # LLM includes suggestion
            correction=None,  # Could extract if LLM provides code block
            learning_point='Review the explanation above',
            confidence=0.75
        )
    
    def _detect_common_mistake(self, user_cmd: str, expected_cmd: str, 
                               output: str) -> Optional[Mistake]:
        for pattern in self.common_mistakes:
            if re.match(pattern['pattern'], user_cmd):
                # Check context if specified
                if 'context' in pattern:
                    if pattern['context'].lower() not in output.lower():
                        continue
                
                return Mistake(**pattern)
        
        return None
    
    def _load_common_mistakes(self) -> list:
        # Load from configuration file
        return COMMON_MISTAKES
    
    def _load_prompt_templates(self) -> dict:
        return {
            'system': SYSTEM_PROMPT,
            'user': USER_PROMPT
        }
```

---

## 4️⃣ Hint Agent

### Purpose
Provide progressive hints when users are stuck, with 3 levels of increasing specificity.

### Capabilities

#### 1. 3-Level Progressive Hints
- **Level 1**: Gentle nudge (concept reminder)
- **Level 2**: More specific (command structure, approach)
- **Level 3**: Explicit (nearly the full answer)

#### 2. Adaptive Hint Offering
- Offer after 3 failed attempts
- Offer after 2 minutes of inactivity
- User can request manually

#### 3. Track Hint Usage
- Record which hints were used
- Feed into analytics
- Adjust difficulty recommendations

### Inputs

```python
@dataclass
class HintInput:
    step_definition: Step
    hint_level: int  # 1, 2, or 3
    user_context: UserContext
    previous_attempts: list[Attempt]
```

### Hint Levels

#### Scenario-Defined Hints
Hints can be predefined in scenario YAML:

```yaml
step:
  id: "pull_nginx"
  title: "Pull NGINX Image"
  hints:
    - level: 1
      text: "Use the 'docker pull' command to download images from Docker Hub."
    - level: 2
      text: "The official NGINX image is simply called 'nginx'."
    - level: 3
      text: "Try: `docker pull nginx`"
```

#### AI-Generated Hints
If hints not predefined, use LLM to generate progressive hints:

**System Prompt**:
```python
SYSTEM_PROMPT = """You are a helpful tutor providing progressive hints to students.

Hint Level Guidelines:
- Level 1: Remind them of the concept or tool to use. Don't mention specific commands.
- Level 2: Describe the structure or approach, but don't give the exact syntax.
- Level 3: Provide the nearly complete solution, but perhaps with one small blank to fill.

Keep hints concise (1-2 sentences).
Be encouraging and supportive.
"""
```

**User Prompt**:
```python
USER_PROMPT = """Step Objective: {step_objective}
Step Description: {step_description}

Student has attempted {num_attempts} times.
Time spent: {time_spent}

Generate a Level {hint_level} hint.
"""
```

### Output

```python
@dataclass
class HintResponse:
    level: int  # 1, 2, or 3
    text: str  # The hint text (markdown)
    is_final: bool  # True if this is level 3
    confidence: float  # 0-1
    estimated_value: float  # How helpful we think this hint is
```

### Example Hint Progressions

#### Example 1: Docker Pull

**Level 1**:
```
Use the 'docker pull' command to download images from Docker Hub.
```

**Level 2**:
```
The official NGINX image is simply called 'nginx'. The docker pull command syntax is: docker pull <image-name>
```

**Level 3**:
```
Try running: `docker pull nginx`
```

#### Example 2: SQL JOIN

**Level 1**:
```
You need to combine data from two tables. SQL's JOIN clause is designed for this.
```

**Level 2**:
```
Use INNER JOIN to connect the 'customers' and 'orders' tables. They share a common 'customer_id' column. The syntax is: SELECT columns FROM table1 INNER JOIN table2 ON matching_condition
```

**Level 3**:
```
Try: `SELECT customers.name, SUM(orders.total) FROM customers INNER JOIN orders ON customers.id = orders.customer_id GROUP BY customers.name`
```

#### Example 3: Python Bug Fix

**Level 1**:
```
Look carefully at the loop boundaries. Are you iterating over all elements?
```

**Level 2**:
```
The range function is exclusive of the upper bound. If your array has 5 elements (indices 0-4), range(5) gives you 0,1,2,3,4. Check if your range matches the array length.
```

**Level 3**:
```
Change `range(len(arr) - 1)` to `range(len(arr))` to include the last element.
```

### Adaptive Hint Offering

```python
class HintOfferingStrategy:
    def should_offer_hint(self, user_context: UserContext) -> tuple[bool, int]:
        """
        Returns (should_offer, suggested_level)
        """
        # After 3 failed attempts, offer level 1
        if user_context.failed_attempts >= 3 and user_context.hints_used == 0:
            return (True, 1)
        
        # After 5 failed attempts, escalate to level 2
        if user_context.failed_attempts >= 5 and user_context.hints_used == 1:
            return (True, 2)
        
        # After 7 failed attempts, offer final hint
        if user_context.failed_attempts >= 7 and user_context.hints_used == 2:
            return (True, 3)
        
        # After 2 minutes of inactivity
        if user_context.time_since_last_action > 120:  # seconds
            next_level = min(user_context.hints_used + 1, 3)
            return (True, next_level)
        
        return (False, 0)
```

### Implementation

```python
class HintAgent(BaseAgent):
    def __init__(self):
        super().__init__(model='llama3.2:3b')
    
    def generate_response(self, context: dict) -> HintResponse:
        step_def = context['step_definition']
        hint_level = context['hint_level']
        
        # First, check if hint is predefined
        if 'hints' in step_def and len(step_def['hints']) >= hint_level:
            predefined_hint = step_def['hints'][hint_level - 1]
            return HintResponse(
                level=hint_level,
                text=predefined_hint['text'],
                is_final=(hint_level == 3),
                confidence=1.0,
                estimated_value=0.8
            )
        
        # Otherwise, generate hint with LLM
        return self._generate_ai_hint(context)
    
    def _generate_ai_hint(self, context: dict) -> HintResponse:
        step_def = context['step_definition']
        hint_level = context['hint_level']
        user_context = context['user_context']
        
        system_prompt = self.prompt_templates['system']
        
        user_prompt = self.prompt_templates['user'].format(
            step_objective=step_def.objective,
            step_description=step_def.description,
            num_attempts=len(user_context.previous_attempts),
            time_spent=user_context.time_on_step,
            hint_level=hint_level
        )
        
        hint_text = self._call_llm(user_prompt, system_prompt)
        
        return HintResponse(
            level=hint_level,
            text=hint_text,
            is_final=(hint_level == 3),
            confidence=0.80,
            estimated_value=0.75
        )
    
    def _load_prompt_templates(self) -> dict:
        return {
            'system': SYSTEM_PROMPT,
            'user': USER_PROMPT
        }
```

---

## 5️⃣ Context Agent

### Purpose
Answer user questions about the step using RAG (Retrieval-Augmented Generation) with course materials.

### Capabilities

#### 1. Answer "Why" Questions
- Explain rationale behind commands
- Clarify best practices
- Provide context

#### 2. Provide Background Information
- Define technical terms
- Explain concepts
- Historical context

#### 3. Explain Best Practices
- Why certain approaches are preferred
- Common pitfalls
- Industry standards

#### 4. Link to Documentation
- Official documentation
- Course materials
- External resources

#### 5. RAG-Powered Responses
- Retrieve relevant course content
- Generate answer grounded in materials
- Provide citations

### Inputs

```python
@dataclass
class ContextInput:
    user_question: str
    step_definition: Step
    course_context: CourseContext
    scenario_context: ScenarioContext
```

### LLM Usage

**Model**: `llama3.1:8b` (more capable model for knowledge-intensive tasks)

**System Prompt**:
```python
SYSTEM_PROMPT = """You are a knowledgeable technical assistant helping students understand concepts during a lab simulation.

Your role is to:
1. Answer student questions clearly and accurately
2. Provide context and background information
3. Explain best practices and rationale
4. Ground answers in the provided course materials
5. Include relevant citations or references

Guidelines:
- Use simple, clear language
- Provide concrete examples
- Connect to the current lab context
- Be encouraging and supportive
- If you don't know something, say so

Available context:
- Course materials (provided)
- Current lab scenario
- Student's current step
"""
```

**User Prompt with RAG**:
```python
USER_PROMPT = """Student Question: {user_question}

Current Step: {step_title}
Step Objective: {step_objective}

Relevant Course Content:
{retrieved_context}

Answer the student's question using the provided course materials. Be clear, concise, and helpful.
"""
```

### RAG Implementation

```python
class ContextAgent(BaseAgent):
    def __init__(self, course_materials_path: str):
        super().__init__(model='llama3.1:8b')
        self.vector_store = self._build_vector_store(course_materials_path)
    
    def generate_response(self, context: dict) -> ContextResponse:
        user_question = context['user_question']
        step_def = context['step_definition']
        
        # Retrieve relevant context
        retrieved_docs = self.vector_store.similarity_search(
            user_question,
            k=3  # Top 3 most relevant documents
        )
        
        retrieved_context = '\n\n'.join([
            f"[Source: {doc.metadata['source']}]\n{doc.page_content}"
            for doc in retrieved_docs
        ])
        
        # Generate answer
        system_prompt = self.prompt_templates['system']
        
        user_prompt = self.prompt_templates['user'].format(
            user_question=user_question,
            step_title=step_def.title,
            step_objective=step_def.objective,
            retrieved_context=retrieved_context
        )
        
        answer = self._call_llm(user_prompt, system_prompt)
        
        return ContextResponse(
            answer=answer,
            sources=[doc.metadata['source'] for doc in retrieved_docs],
            confidence=0.85
        )
    
    def _build_vector_store(self, materials_path: str):
        """Build vector store from course materials"""
        from langchain.vectorstores import Chroma
        from langchain.embeddings import OllamaEmbeddings
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        
        # Load course materials
        documents = self._load_course_materials(materials_path)
        
        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(documents)
        
        # Create embeddings
        embeddings = OllamaEmbeddings(model='llama3.1:8b')
        
        # Build vector store
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory='./chroma_db'
        )
        
        return vector_store
    
    def _load_course_materials(self, path: str):
        """Load markdown files from course directory"""
        # Implementation would load all .md files
        pass
    
    def _load_prompt_templates(self) -> dict:
        return {
            'system': SYSTEM_PROMPT,
            'user': USER_PROMPT
        }
```

### Example Interactions

#### Example 1: Technical Clarification

**Question**: "What does the -d flag do in docker run?"

**Answer**:
```markdown
The `-d` flag (short for `--detach`) runs the container in detached mode, meaning it runs in the background and doesn't block your terminal.

Without `-d`, the container runs in the foreground and its logs are streamed to your terminal. This is useful for debugging but impractical for services that should run continuously.

Example:
- `docker run nginx` - Runs in foreground (terminal blocked)
- `docker run -d nginx` - Runs in background (terminal free)

**Best Practice**: Use `-d` for services (web servers, databases) and foreground mode for one-off commands or debugging.

[Source: Docker Documentation - Container Runtime Options]
```

#### Example 2: Concept Explanation

**Question**: "Why do we need to normalize data before training a model?"

**Answer**:
```markdown
Normalization (scaling features to similar ranges) is important for several reasons:

1. **Algorithm Performance**: Many ML algorithms (like neural networks, SVM, k-NN) are sensitive to feature scales. If one feature ranges from 0-1 and another from 0-10000, the larger scale dominates.

2. **Faster Convergence**: Gradient descent converges faster when features are on similar scales.

3. **Fair Feature Importance**: Prevents features with larger ranges from having undue influence.

**Common Methods**:
- StandardScaler: Mean=0, Std=1
- MinMaxScaler: Scale to [0, 1]
- RobustScaler: Uses median and quartiles (good for outliers)

In this lab, we're using StandardScaler before training our Random Forest because it helps the model learn more efficiently.

[Source: Module 4 - Data Preprocessing]
```

### Output

```python
@dataclass
class ContextResponse:
    answer: str  # Markdown-formatted answer
    sources: list[str]  # Citations
    confidence: float  # 0-1
    related_topics: list[str]  # Suggestions for further learning
```

---

## Agent Orchestration

### Agent Coordination

```python
class AgentOrchestrator:
    def __init__(self):
        self.step_guide = StepGuideAgent()
        self.validator = ValidationAgent()
        self.error_recovery = ErrorRecoveryAgent()
        self.hint = HintAgent()
        self.context = ContextAgent()
    
    def handle_step_start(self, step: Step, user: UserContext) -> StepGuideResponse:
        """Called when user starts a new step"""
        return self.step_guide.generate_response({
            'step_definition': step,
            'user_context': user,
            'previous_attempts': []
        })
    
    def handle_action(self, action: Action, step: Step) -> ValidationResult:
        """Called when user attempts an action"""
        return self.validator.validate(
            action,
            step.validation_rules,
            action.environment_state
        )
    
    def handle_failure(self, action: Action, step: Step, 
                      errors: list) -> ErrorRecoveryResponse:
        """Called when validation fails"""
        return self.error_recovery.generate_response({
            'user_action': action,
            'step_definition': step,
            'validation_errors': errors
        })
    
    def handle_hint_request(self, step: Step, user: UserContext, 
                           level: int) -> HintResponse:
        """Called when user requests a hint"""
        return self.hint.generate_response({
            'step_definition': step,
            'hint_level': level,
            'user_context': user
        })
    
    def handle_question(self, question: str, step: Step) -> ContextResponse:
        """Called when user asks a question"""
        return self.context.generate_response({
            'user_question': question,
            'step_definition': step
        })
```

---

## Performance Optimization

### Caching Strategy
```python
class AgentCache:
    def __init__(self):
        self.cache = {}
        self.ttl = 3600  # 1 hour
    
    def get(self, key: str) -> Optional[Any]:
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry['timestamp'] < self.ttl:
                return entry['value']
        return None
    
    def set(self, key: str, value: Any):
        self.cache[key] = {
            'value': value,
            'timestamp': time.time()
        }
```

### Async Processing
```python
import asyncio

class AsyncAgentOrchestrator:
    async def handle_step_start_async(self, step: Step, user: UserContext):
        """Non-blocking agent call"""
        return await asyncio.to_thread(
            self.step_guide.generate_response,
            {'step_definition': step, 'user_context': user}
        )
```

---

## Testing Agents

### Unit Tests
```python
def test_step_guide_agent():
    agent = StepGuideAgent()
    
    response = agent.generate_response({
        'step_definition': {'title': 'Test', 'objective': 'Test objective'},
        'user_context': {'tier': 'intermediate', 'attempts': 0}
    })
    
    assert response.guidance_text is not None
    assert len(response.guidance_text) > 0
    assert response.confidence > 0.5
```

### Integration Tests
```python
def test_error_recovery_flow():
    orchestrator = AgentOrchestrator()
    
    # Simulate failed action
    action = Action(command='docker run nginx')  # Missing -d flag
    step = Step(expected='docker run -d nginx')
    
    validation = orchestrator.handle_action(action, step)
    assert not validation.is_valid
    
    recovery = orchestrator.handle_failure(action, step, validation.errors)
    assert 'detached' in recovery.explanation.lower()
    assert recovery.correction == 'docker run -d nginx'
```

---

This comprehensive agent system provides intelligent, adaptive guidance that enhances learning without spoiling solutions, helping users develop real skills through supported practice.
