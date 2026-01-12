# SimulationPlayer Example Scenarios

This document provides 5 complete, production-ready example scenarios in YAML format, demonstrating different environment types and learning patterns.

---

## Scenario Index

1. **Docker First Container** (Terminal) - Beginner, 15min
2. **Git Workflow** (Terminal) - Beginner, 20min
3. **Python Bug Fix** (Code Editor) - Beginner, 10min
4. **SQL Joins** (Database) - Intermediate, 15min
5. **ML Pipeline** (ML Pipeline Builder) - Intermediate/Advanced, 20min

---

## Example 1: Docker First Container

**File**: `scenarios/docker-first-container.yml`

This scenario teaches Docker basics through a 5-step hands-on workflow.

```yaml
scenario:
  id: "docker-first-container"
  title: "Docker: Your First Container"
  description: "Learn Docker fundamentals by pulling an image, running a container, inspecting it, executing commands inside, and cleaning up."
  difficulty: beginner
  estimated_time: 15
  tier_access: intermediate
  
  learning_objectives:
    - "Pull Docker images from Docker Hub"
    - "Run containers in detached mode"
    - "Inspect running containers"
    - "Execute commands inside containers"
    - "Stop and remove containers"
  
  environment:
    type: terminal
    docker_required: true
  
  steps:
    - id: "pull_nginx"
      title: "Pull NGINX Image"
      objective: "Use docker pull to download the nginx image"
      
      guidance:
        initial: |
          Docker images are templates for containers. Use `docker pull` to download 
          the official NGINX image from Docker Hub.
        
        hints:
          - level: 1
            text: "Use the 'docker pull' command."
          - level: 2
            text: "The image is called 'nginx'."
          - level: 3
            text: "Try: docker pull nginx"
      
      validation:
        type: command_execution
        rules:
          - rule_type: command_regex
            parameters:
              pattern: "^docker (pull|image pull) nginx"
          - rule_type: exit_code
            parameters:
              expected: 0
      
      success_message: "🎉 NGINX image downloaded successfully!"
    
    - id: "run_nginx"
      title: "Run NGINX Container"
      objective: "Start nginx in detached mode on port 8080"
      
      hints:
          - level: 1
            text: "Use docker run with -d and -p flags."
          - level: 2
            text: "Format: docker run -d -p 8080:80 nginx"
          - level: 3
            text: "Try: docker run -d -p 8080:80 nginx"
      
      validation:
        rules:
          - rule_type: command_contains
            parameters:
              substring: "-d"
        
        post_validation:
          - type: container_running
            parameters:
              image: "nginx"
      
      error_recovery:
        common_mistakes:
          - pattern: "^docker run nginx$"
            message: "Missing -d flag. Container runs in foreground."
            hint: "Add -d to run detached."
            correction: "docker run -d -p 8080:80 nginx"
    
    - id: "inspect"
      title: "Inspect Container"
      objective: "List running containers with docker ps"
      
      validation:
        rules:
          - rule_type: command_regex
            parameters:
              pattern: "^docker (ps|container ls)"
    
    - id: "exec"
      title: "Execute Command"
      objective: "Run nginx -v inside the container"
      
      validation:
        rules:
          - rule_type: command_contains
            parameters:
              substring: "docker exec"
          - rule_type: command_contains
            parameters:
              substring: "nginx -v"
    
    - id: "cleanup"
      title: "Clean Up"
      objective: "Stop and remove the container"
      
      validation:
        rules:
          - rule_type: command_regex
            parameters:
              pattern: "docker (rm -f|stop.*rm)"
  
  completion:
    badge: "Docker Novice"
    points: 150
    next_scenario: "docker-volumes"
```

---

## Example 2: Git Basic Workflow

**File**: `scenarios/git-basic-workflow.yml`

```yaml
scenario:
  id: "git-basic-workflow"
  title: "Git: Basic Workflow"
  description: "Master Git fundamentals: init, add, commit, branch, and merge."
  difficulty: beginner
  estimated_time: 20
  tier_access: intermediate
  
  learning_objectives:
    - "Initialize a Git repository"
    - "Stage and commit changes"
    - "Create and merge branches"
  
  environment:
    type: terminal
    docker_required: true
    initial_state:
      working_directory: "/home/user/project"
      files:
        - path: "README.md"
          content: "# My Project\n"
  
  steps:
    - id: "init"
      title: "Initialize Repository"
      objective: "Run git init"
      
      validation:
        rules:
          - rule_type: command_exact
            parameters:
              expected: "git init"
        
        post_validation:
          - type: directory_exists
            parameters:
              path: ".git"
    
    - id: "add"
      title: "Stage Files"
      objective: "Add files with git add"
      
      validation:
        rules:
          - rule_type: command_regex
            parameters:
              pattern: "^git add (\\.|--all)"
    
    - id: "commit"
      title: "Create Commit"
      objective: "Commit with a message"
      
      validation:
        rules:
          - rule_type: command_contains
            parameters:
              substring: "git commit -m"
      
      error_recovery:
        common_mistakes:
          - pattern: "^git commit$"
            message: "Missing -m flag for commit message."
            correction: "git commit -m \"Initial commit\""
    
    - id: "branch"
      title: "Create Branch"
      objective: "Create feature branch"
      
      validation:
        rules:
          - rule_type: command_regex
            parameters:
              pattern: "^git checkout -b feature"
    
    - id: "merge"
      title: "Merge Branch"
      objective: "Merge feature into main"
      
      validation:
        rules:
          - rule_type: command_contains
            parameters:
              substring: "git merge"
  
  completion:
    badge: "Git Apprentice"
    points: 200
```

---

## Example 3: Python Bug Fix

**File**: `scenarios/python-bug-fix.yml`

```yaml
scenario:
  id: "python-bug-fix"
  title: "Python: Fix the Sum Function"
  description: "Debug an off-by-one error in a sum function."
  difficulty: beginner
  estimated_time: 10
  tier_access: intermediate
  
  environment:
    type: code_editor
    initial_state:
      files:
        - path: "sum.py"
          content: |
            def calculate_sum(numbers):
                total = 0
                for i in range(len(numbers) - 1):  # BUG
                    total += numbers[i]
                return total
  
  steps:
    - id: "run_code"
      title: "Run Buggy Code"
      objective: "Execute to see the bug"
      
      validation:
        type: code_execution
        rules:
          - rule_type: code_executed
    
    - id: "fix_bug"
      title: "Fix Loop Range"
      objective: "Change to range(len(numbers))"
      
      hints:
        - level: 1
          text: "The problem is in the range() call."
        - level: 2
          text: "Remove the '- 1' from the range."
        - level: 3
          text: "Change to: for i in range(len(numbers)):"
      
      validation:
        rules:
          - rule_type: line_content
            parameters:
              line_number: 3
              expected_regex: "range\\(len\\(numbers\\)\\)"
        
        post_validation:
          - type: code_passes_tests
            parameters:
              test_cases:
                - input: [[1,2,3,4,5]]
                  expected: 15
  
  completion:
    badge: "Debugger"
    points: 100
```

---

## Example 4: SQL Joins

**File**: `scenarios/sql-joins.yml`

```yaml
scenario:
  id: "sql-joins"
  title: "SQL: INNER JOIN Mastery"
  description: "Learn to join tables, filter, aggregate, and sort."
  difficulty: intermediate
  estimated_time: 15
  tier_access: intermediate
  
  environment:
    type: database
    initial_state:
      database: "ecommerce"
  
  steps:
    - id: "basic_join"
      title: "Basic INNER JOIN"
      objective: "Join customers and orders"
      
      guidance:
        initial: |
          Join the customers and orders tables on customer_id.
          Show customer names with their order totals.
      
      validation:
        rules:
          - rule_type: query_structure
            parameters:
              has_join: true
              tables: ["customers", "orders"]
          - rule_type: result_columns
            parameters:
              expected: ["name", "total"]
    
    - id: "join_filter"
      title: "JOIN with WHERE"
      objective: "Filter orders over $100"
      
      validation:
        rules:
          - rule_type: query_structure
            parameters:
              has_where: true
          - rule_type: result_validation
            parameters:
              all_rows_satisfy: "total > 100"
    
    - id: "join_aggregate"
      title: "JOIN with Aggregation"
      objective: "Calculate total spending per customer"
      
      hints:
        - level: 3
          text: "SELECT name, SUM(total) FROM customers JOIN orders ON customers.id = orders.customer_id GROUP BY name"
      
      validation:
        rules:
          - rule_type: query_structure
            parameters:
              has_group_by: true
              has_aggregate: true
  
  completion:
    badge: "SQL Joiner"
    points: 175
```

---

## Example 5: ML Pipeline

**File**: `scenarios/ml-pipeline.yml`

```yaml
scenario:
  id: "ml-pipeline"
  title: "ML: Build Your First Pipeline"
  description: "Design a complete ML pipeline: load, preprocess, train, evaluate."
  difficulty: intermediate
  estimated_time: 20
  tier_access: advanced
  
  environment:
    type: ml_pipeline
    initial_state:
      dataset: "iris"
  
  steps:
    - id: "load_data"
      title: "Add Data Loader"
      objective: "Load the Iris dataset"
      
      validation:
        type: pipeline_structure
        rules:
          - rule_type: component_exists
            parameters:
              component_type: "data_loader"
    
    - id: "split_data"
      title: "Train/Test Split"
      objective: "Split 80/20"
      
      validation:
        rules:
          - rule_type: component_exists
            parameters:
              component_type: "train_test_split"
          - rule_type: component_config
            parameters:
              test_size: 0.2
    
    - id: "normalize"
      title: "Add Normalization"
      objective: "Add StandardScaler"
      
      validation:
        rules:
          - rule_type: component_exists
            parameters:
              component_type: "standard_scaler"
          - rule_type: pipeline_order
            parameters:
              sequence: ["split", "scaler"]
    
    - id: "model"
      title: "Add Classifier"
      objective: "Add Random Forest"
      
      validation:
        rules:
          - rule_type: component_exists
            parameters:
              component_type: "random_forest"
          - rule_type: component_config
            parameters:
              n_estimators: 100
    
    - id: "evaluate"
      title: "Add Evaluator"
      objective: "Measure performance"
      
      validation:
        rules:
          - rule_type: pipeline_complete
            parameters:
              has_evaluation: true
  
  completion:
    badge: "ML Engineer"
    points: 250
```

---

## Scenario Design Patterns

### Pattern 1: Progressive Difficulty
Each scenario starts simple and builds complexity step-by-step.

### Pattern 2: Immediate Feedback
Every step provides instant validation and encouragement.

### Pattern 3: Error Recovery
Common mistakes are anticipated with helpful corrections.

### Pattern 4: Multiple Paths
Accepted variations allow different valid approaches.

### Pattern 5: Contextual Learning
Guidance explains "why" not just "how".

---

## Usage

These scenarios serve as:
- **Templates** for creating new scenarios
- **Reference** for best practices
- **Examples** of different difficulty levels
- **Demonstrations** of each environment type

Copy and modify these templates to create custom learning experiences for your courses.
