# SimulationPlayer Scenario Authoring Guide

This guide explains how to create engaging, educational simulation scenarios for SimulationPlayer. Scenarios are defined in YAML format and validated against a JSON Schema.

---

## Table of Contents

1. [Scenario YAML Schema](#scenario-yaml-schema)
2. [Authoring Workflow](#authoring-workflow)
3. [Best Practices](#best-practices)
4. [Validation Schema](#validation-schema)
5. [Example Walkthroughs](#example-walkthroughs)
6. [Common Patterns](#common-patterns)
7. [Troubleshooting](#troubleshooting)

---

## Scenario YAML Schema

### Complete Schema Structure

```yaml
scenario:
  # === METADATA ===
  id: string                    # Unique identifier (e.g., "docker-first-container")
  title: string                 # Display name (e.g., "Docker: Your First Container")
  description: string           # Brief overview (2-3 sentences)
  difficulty: beginner | intermediate | advanced
  estimated_time: integer       # Minutes to complete
  tier_access: basic | intermediate | advanced  # CoursesGTM tier requirement
  
  # === PREREQUISITES ===
  prerequisites:
    - scenario_id_1             # Must complete these first
    - scenario_id_2
  
  # === LEARNING OBJECTIVES ===
  learning_objectives:
    - "Understand Docker images and containers"
    - "Practice pulling and running containers"
    - "Learn container lifecycle management"
  
  # === ENVIRONMENT SETUP ===
  environment:
    type: terminal | code_editor | infrastructure | database | api | ml_pipeline | docker_compose
    docker_required: boolean
    
    initial_state:
      working_directory: string               # e.g., "/home/user"
      files:                                  # Pre-created files
        - path: string
          content: string
      environment_variables:                  # Env vars
        VAR_NAME: value
      docker_images:                          # Pre-pulled images (optional)
        - nginx:latest
  
  # === STEPS ===
  steps:
    - id: string                              # Unique within scenario
      title: string                           # Step name
      description: string                     # What to do
      objective: string                       # Learning goal
      
      # Guidance
      guidance:
        initial: string                       # Markdown text shown at step start
        hints:
          - level: 1
            text: string
          - level: 2
            text: string
          - level: 3
            text: string
      
      # Validation
      validation:
        type: command_execution | code_output | file_content | state_check
        rules:
          - rule_type: string                 # e.g., command_exact, output_contains
            parameters:
              key: value
        
        accepted_variations:                  # Alternative valid solutions
          - "docker pull nginx:latest"
          - "docker image pull nginx"
        
        post_validation:                      # Check side effects after action
          - type: container_running | file_exists | service_healthy
            parameters:
              name: value
      
      # Feedback
      success_message: string                 # Markdown, shown on success
      
      # Error Recovery
      error_recovery:
        common_mistakes:
          - pattern: string                   # Regex to match mistake
            message: string                   # User-friendly explanation
            hint: string                      # How to fix
            correction: string                # Optional: exact fix
  
  # === COMPLETION ===
  completion:
    badge: string                             # Badge name/icon
    points: integer                           # Points awarded
    next_scenario: string                     # Suggested next scenario
    
    summary:
      text: string                            # Congratulations message
      key_takeaways:
        - string
  
  # === ANALYTICS ===
  analytics:
    track_metrics:
      - time_per_step
      - hints_requested
      - mistakes_made
      - retry_count
```

---

## Authoring Workflow

### Step 1: Define Learning Objectives

Start by clearly defining what learners will achieve:

```yaml
learning_objectives:
  - "Pull Docker images from Docker Hub"
  - "Run containers in detached mode"
  - "Inspect running containers"
  - "Execute commands inside containers"
  - "Stop and remove containers"
```

**Guidelines**:
- Use action verbs (pull, run, inspect, execute)
- Be specific and measurable
- Align with course curriculum
- Limit to 3-7 objectives per scenario

### Step 2: Choose Environment Type

Select the most appropriate environment:

| Type | Best For |
|------|----------|
| `terminal` | Shell commands, CLI tools, system administration |
| `code_editor` | Writing/editing code, bug fixes, refactoring |
| `infrastructure` | Cloud architecture, container orchestration design |
| `database` | SQL queries, database operations |
| `api` | REST/GraphQL API interaction, HTTP requests |
| `ml_pipeline` | ML workflow design, data pipelines |
| `docker_compose` | Multi-container application design |

```yaml
environment:
  type: terminal
  docker_required: true
```

### Step 3: Break Down Task into Steps

Divide the scenario into 5-10 atomic steps:

**Atomic Step Criteria**:
- One clear action per step
- Completable in 1-3 minutes
- Has verifiable outcome
- Builds on previous steps

**Example**:
```yaml
steps:
  - id: "step_1_pull"
    title: "Pull NGINX Image"
    objective: "Download the official NGINX image from Docker Hub"
    
  - id: "step_2_run"
    title: "Run NGINX Container"
    objective: "Start NGINX in detached mode on port 8080"
    
  - id: "step_3_inspect"
    title: "Inspect Container"
    objective: "View container details and status"
```

### Step 4: For Each Step, Define Components

#### 4.1 Write Clear Objective and Description

```yaml
- id: "pull_nginx"
  title: "Pull NGINX Image"
  description: |
    Docker images are templates for containers. Before we can run NGINX, 
    we need to download its image from Docker Hub.
  objective: "Download the official nginx image using docker pull"
```

#### 4.2 Create Initial Guidance

```yaml
guidance:
  initial: |
    ## Downloading Docker Images
    
    Docker Hub is a public registry where official and community images are stored.
    To download an image, we use the `docker pull` command followed by the image name.
    
    **Your Task**: Pull the official nginx image.
    
    💡 The official NGINX image is simply called "nginx"
```

#### 4.3 Define 3-Level Hints

```yaml
hints:
  - level: 1
    text: "Use the 'docker pull' command to download images from Docker Hub."
  - level: 2
    text: "The official NGINX image is simply called 'nginx'. Try: docker pull <image-name>"
  - level: 3
    text: "Run this command: `docker pull nginx`"
```

**Hint Level Guidelines**:
- **Level 1**: Concept/tool reminder (no command syntax)
- **Level 2**: Command structure (placeholders, not exact)
- **Level 3**: Nearly complete solution (minimal blanks)

#### 4.4 Define Validation Rules

```yaml
validation:
  type: command_execution
  rules:
    - rule_type: command_regex
      parameters:
        pattern: "^docker (pull|image pull) nginx(:.*)?$"
        flags: IGNORECASE
    
    - rule_type: exit_code
      parameters:
        expected: 0
    
    - rule_type: output_contains
      parameters:
        text: "Status: Downloaded"
        location: stdout
  
  accepted_variations:
    - "docker pull nginx"
    - "docker pull nginx:latest"
    - "docker image pull nginx"
  
  post_validation:
    - type: docker_image_exists
      parameters:
        image_name: "nginx"
```

#### 4.5 Identify Common Mistakes

```yaml
error_recovery:
  common_mistakes:
    - pattern: "^docker pull$"
      message: "The docker pull command requires an image name."
      hint: "Specify which image to pull. Try: docker pull <image-name>"
      
    - pattern: "^pull nginx$"
      message: "Don't forget the 'docker' command prefix."
      hint: "Docker commands start with 'docker'. Try: docker pull nginx"
      correction: "docker pull nginx"
    
    - pattern: "^docker run nginx$"
      message: "You're trying to run the container, but we haven't pulled the image yet."
      hint: "First, we need to download the image with 'docker pull'"
```

#### 4.6 Write Success Message

```yaml
success_message: |
  🎉 **Great job!** You've successfully pulled the NGINX image.
  
  Docker has downloaded the image layers and cached them locally. 
  Now you can create containers from this image instantly.
  
  **Next**: Let's run an NGINX container!
```

### Step 5: Test Scenario End-to-End

Before finalizing:

1. **Manual Walkthrough**: Complete the scenario yourself
2. **Test Variations**: Try accepted variations
3. **Test Mistakes**: Trigger common mistakes
4. **Time It**: Verify estimated_time is accurate
5. **Check Difficulty**: Ensure difficulty level matches experience

### Step 6: Validate YAML Against Schema

```bash
# Validate scenario YAML
python -m simulationplayer.tools.validate_scenario scenarios/docker-first-container.yml

# Output:
# ✅ Scenario valid
# - 5 steps defined
# - All validation rules valid
# - No missing required fields
```

---

## Best Practices

### Content Guidelines

#### ✅ DO

1. **Keep Steps Atomic**
   ```yaml
   # GOOD: One clear action
   - title: "Pull NGINX Image"
     objective: "Download nginx image from Docker Hub"
   
   # GOOD: Next step
   - title: "Run NGINX Container"
     objective: "Start nginx in detached mode"
   ```

2. **Provide Multiple Valid Solutions**
   ```yaml
   accepted_variations:
     - "docker pull nginx"
     - "docker pull nginx:latest"
     - "docker pull nginx:1.21"
     - "docker image pull nginx"
   ```

3. **Write Encouraging Error Messages**
   ```yaml
   # GOOD
   message: "Good try! The docker pull command needs an image name to know what to download."
   
   # BAD
   message: "Error: Missing argument"
   ```

4. **Include "Why" Context**
   ```yaml
   guidance:
     initial: |
       We're pulling the image first because Docker needs a local copy 
       before it can create containers. Think of it like downloading an 
       app before you can run it.
   ```

5. **Balance Guidance**
   ```yaml
   # GOOD: Nudges without spoiling
   hints:
     - level: 1
       text: "Use the docker pull command"
     - level: 2  
       text: "The image is called 'nginx'"
     - level: 3
       text: "Try: docker pull nginx"
   
   # BAD: Gives away answer too early
   hints:
     - level: 1
       text: "Run: docker pull nginx"
   ```

6. **Test With Real Users**
   - Conduct user testing
   - Gather feedback on clarity
   - Identify unexpected mistakes
   - Adjust difficulty based on data

#### ❌ DON'T

1. **Don't Combine Multiple Actions**
   ```yaml
   # BAD: Too complex for one step
   - title: "Pull and Run NGINX"
     objective: "Download and start NGINX container"
   
   # GOOD: Split into two steps
   - title: "Pull NGINX Image"
   - title: "Run NGINX Container"
   ```

2. **Don't Use Vague Objectives**
   ```yaml
   # BAD
   objective: "Work with Docker"
   
   # GOOD
   objective: "Pull the nginx image from Docker Hub"
   ```

3. **Don't Overload with Information**
   ```yaml
   # BAD: Too much text
   description: |
     Docker is a containerization platform that allows you to package applications
     and their dependencies into portable containers. Containers are isolated 
     environments that share the host OS kernel but have their own filesystem,
     network, and process space. This makes them more lightweight than VMs...
     [continues for 10 paragraphs]
   
   # GOOD: Concise and relevant
   description: |
     Docker images are templates for containers. We need to download the 
     NGINX image before we can run it.
   ```

4. **Don't Reveal Solutions Too Early**
   ```yaml
   # BAD
   guidance:
     initial: "Run this command: docker pull nginx"
   
   # GOOD
   guidance:
     initial: "Use the docker pull command to download the nginx image from Docker Hub"
   ```

5. **Don't Ignore Edge Cases**
   ```yaml
   # BAD: Only validates happy path
   validation:
     rules:
       - rule_type: command_exact
         parameters:
           expected: "docker pull nginx"
   
   # GOOD: Handles variations
   validation:
     rules:
       - rule_type: command_regex
         parameters:
           pattern: "^docker (pull|image pull) nginx(:.*)?$"
   ```

### Technical Guidelines

#### Validation Rules

**Use Regex for Flexibility**:
```yaml
# Allows: docker pull nginx, docker pull nginx:latest, docker pull nginx:1.21
validation:
  rules:
    - rule_type: command_regex
      parameters:
        pattern: "^docker pull nginx(:[\\w\\.-]+)?$"
```

**Chain Validations**:
```yaml
# Check multiple criteria
validation:
  rules:
    - rule_type: command_contains
      parameters:
        substring: "docker run"
    
    - rule_type: command_contains
      parameters:
        substring: "-d"  # Detached mode
    
    - rule_type: exit_code
      parameters:
        expected: 0
  
  post_validation:
    - type: container_running
      parameters:
        container_name_pattern: "nginx"
```

**Post-Validation for Side Effects**:
```yaml
# Verify container is actually running
post_validation:
  - type: container_running
    parameters:
      image: "nginx"
      status: "running"
  
  - type: container_port_exposed
    parameters:
      port: 8080
```

#### Error Recovery

**Build Common Mistake Database**:
```yaml
error_recovery:
  common_mistakes:
    # Missing flag
    - pattern: "^docker run nginx$"
      message: "Container runs in foreground, blocking your terminal."
      hint: "Add the -d flag to run in detached (background) mode."
      correction: "docker run -d nginx"
    
    # Wrong order
    - pattern: "^docker run nginx -d$"
      message: "Flags should come before the image name."
      hint: "Put -d before nginx."
      correction: "docker run -d nginx"
    
    # Typo
    - pattern: "^docker pul nginx$"
      message: "Typo detected: 'pul' should be 'pull'."
      hint: "Check your spelling."
      correction: "docker pull nginx"
```

---

## Validation Schema

### JSON Schema for Scenario YAML

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SimulationPlayer Scenario Schema",
  "type": "object",
  "required": ["scenario"],
  "properties": {
    "scenario": {
      "type": "object",
      "required": ["id", "title", "description", "difficulty", "estimated_time", "environment", "steps"],
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^[a-z0-9-]+$",
          "description": "Unique identifier (lowercase, hyphens only)"
        },
        "title": {
          "type": "string",
          "minLength": 5,
          "maxLength": 100
        },
        "description": {
          "type": "string",
          "minLength": 20,
          "maxLength": 500
        },
        "difficulty": {
          "type": "string",
          "enum": ["beginner", "intermediate", "advanced"]
        },
        "estimated_time": {
          "type": "integer",
          "minimum": 1,
          "maximum": 120
        },
        "tier_access": {
          "type": "string",
          "enum": ["basic", "intermediate", "advanced"],
          "default": "intermediate"
        },
        "prerequisites": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "learning_objectives": {
          "type": "array",
          "minItems": 1,
          "maxItems": 10,
          "items": {
            "type": "string",
            "minLength": 10
          }
        },
        "environment": {
          "type": "object",
          "required": ["type"],
          "properties": {
            "type": {
              "type": "string",
              "enum": ["terminal", "code_editor", "infrastructure", "database", "api", "ml_pipeline", "docker_compose"]
            },
            "docker_required": {
              "type": "boolean",
              "default": false
            },
            "initial_state": {
              "type": "object",
              "properties": {
                "working_directory": {"type": "string"},
                "files": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "required": ["path", "content"],
                    "properties": {
                      "path": {"type": "string"},
                      "content": {"type": "string"}
                    }
                  }
                },
                "environment_variables": {
                  "type": "object",
                  "additionalProperties": {"type": "string"}
                }
              }
            }
          }
        },
        "steps": {
          "type": "array",
          "minItems": 1,
          "maxItems": 15,
          "items": {
            "type": "object",
            "required": ["id", "title", "objective", "validation"],
            "properties": {
              "id": {
                "type": "string",
                "pattern": "^[a-z0-9_]+$"
              },
              "title": {
                "type": "string",
                "minLength": 5,
                "maxLength": 100
              },
              "description": {"type": "string"},
              "objective": {
                "type": "string",
                "minLength": 10,
                "maxLength": 200
              },
              "guidance": {
                "type": "object",
                "properties": {
                  "initial": {"type": "string"},
                  "hints": {
                    "type": "array",
                    "minItems": 3,
                    "maxItems": 3,
                    "items": {
                      "type": "object",
                      "required": ["level", "text"],
                      "properties": {
                        "level": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 3
                        },
                        "text": {"type": "string"}
                      }
                    }
                  }
                }
              },
              "validation": {
                "type": "object",
                "required": ["type", "rules"],
                "properties": {
                  "type": {
                    "type": "string",
                    "enum": ["command_execution", "code_output", "file_content", "state_check"]
                  },
                  "rules": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                      "type": "object",
                      "required": ["rule_type", "parameters"],
                      "properties": {
                        "rule_type": {"type": "string"},
                        "parameters": {"type": "object"}
                      }
                    }
                  },
                  "accepted_variations": {
                    "type": "array",
                    "items": {"type": "string"}
                  },
                  "post_validation": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "required": ["type", "parameters"],
                      "properties": {
                        "type": {"type": "string"},
                        "parameters": {"type": "object"}
                      }
                    }
                  }
                }
              },
              "success_message": {"type": "string"},
              "error_recovery": {
                "type": "object",
                "properties": {
                  "common_mistakes": {
                    "type": "array",
                    "items": {
                      "type": "object",
                      "required": ["pattern", "message", "hint"],
                      "properties": {
                        "pattern": {"type": "string"},
                        "message": {"type": "string"},
                        "hint": {"type": "string"},
                        "correction": {"type": "string"}
                      }
                    }
                  }
                }
              }
            }
          }
        },
        "completion": {
          "type": "object",
          "properties": {
            "badge": {"type": "string"},
            "points": {
              "type": "integer",
              "minimum": 0
            },
            "next_scenario": {"type": "string"},
            "summary": {
              "type": "object",
              "properties": {
                "text": {"type": "string"},
                "key_takeaways": {
                  "type": "array",
                  "items": {"type": "string"}
                }
              }
            }
          }
        },
        "analytics": {
          "type": "object",
          "properties": {
            "track_metrics": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": ["time_per_step", "hints_requested", "mistakes_made", "retry_count"]
              }
            }
          }
        }
      }
    }
  }
}
```

### Validation Tool Usage

```bash
# Validate scenario
python -m simulationplayer.tools.validate_scenario my_scenario.yml

# Validate with detailed output
python -m simulationplayer.tools.validate_scenario my_scenario.yml --verbose

# Validate entire directory
python -m simulationplayer.tools.validate_scenario scenarios/ --recursive
```

---

## Example Walkthroughs

### Example 1: Simple Terminal Scenario

```yaml
scenario:
  id: "git-first-commit"
  title: "Git: Your First Commit"
  description: "Learn the basic Git workflow by initializing a repository and making your first commit."
  difficulty: beginner
  estimated_time: 10
  tier_access: intermediate
  
  prerequisites: []
  
  learning_objectives:
    - "Initialize a Git repository"
    - "Stage files with git add"
    - "Create commits with meaningful messages"
  
  environment:
    type: terminal
    docker_required: true
    initial_state:
      working_directory: "/home/user/project"
      files:
        - path: "/home/user/project/README.md"
          content: "# My Project\n"
  
  steps:
    - id: "init_repo"
      title: "Initialize Repository"
      description: "Create a new Git repository in the current directory"
      objective: "Run git init to create a .git directory"
      
      guidance:
        initial: |
          Before we can track changes, we need to initialize a Git repository.
          The `git init` command creates a .git directory that stores all version history.
        
        hints:
          - level: 1
            text: "Use the git init command to create a repository"
          - level: 2
            text: "Run: git init"
          - level: 3
            text: "Type exactly: `git init`"
      
      validation:
        type: command_execution
        rules:
          - rule_type: command_exact
            parameters:
              expected: "git init"
          - rule_type: exit_code
            parameters:
              expected: 0
        
        post_validation:
          - type: directory_exists
            parameters:
              path: "/home/user/project/.git"
      
      success_message: |
        ✅ Repository initialized! The .git directory now tracks all changes.
    
    - id: "stage_file"
      title: "Stage README"
      description: "Add README.md to the staging area"
      objective: "Use git add to stage README.md"
      
      guidance:
        initial: |
          Staging prepares files for the next commit. Think of it as a 
          preview of what will be saved.
        
        hints:
          - level: 1
            text: "Use git add to stage files"
          - level: 2
            text: "Specify the file: git add README.md"
          - level: 3
            text: "Run: `git add README.md`"
      
      validation:
        type: command_execution
        rules:
          - rule_type: command_regex
            parameters:
              pattern: "^git add README\\.md$"
        
        post_validation:
          - type: git_staged_files
            parameters:
              includes: "README.md"
      
      success_message: "📝 README.md is now staged!"
    
    - id: "commit"
      title: "Create Commit"
      description: "Save the staged changes with a commit message"
      objective: "Make your first commit with a meaningful message"
      
      guidance:
        initial: |
          Commits are snapshots of your project. Always include a clear 
          message describing what changed.
        
        hints:
          - level: 1
            text: "Use git commit with the -m flag for a message"
          - level: 2
            text: "Format: git commit -m \"Your message\""
          - level: 3
            text: "Try: `git commit -m \"Initial commit\"`"
      
      validation:
        type: command_execution
        rules:
          - rule_type: command_contains
            parameters:
              substring: "git commit"
          - rule_type: command_contains
            parameters:
              substring: "-m"
          - rule_type: exit_code
            parameters:
              expected: 0
      
      error_recovery:
        common_mistakes:
          - pattern: "^git commit$"
            message: "Commits need a message to describe the changes."
            hint: "Add -m followed by a message in quotes"
            correction: "git commit -m \"Initial commit\""
      
      success_message: |
        🎉 First commit created! You've saved a snapshot of your project.
  
  completion:
    badge: "Git Beginner"
    points: 100
    next_scenario: "git-branching-basics"
    summary:
      text: "You've learned the basic Git workflow!"
      key_takeaways:
        - "git init creates a repository"
        - "git add stages changes"
        - "git commit saves snapshots"
```

---

## Common Patterns

### Pattern 1: Progressive Complexity

Build scenarios that increase in difficulty:

```yaml
# Scenario 1: Basic
steps:
  - title: "Run simple command"
  
# Scenario 2: Intermediate  
steps:
  - title: "Run command with flags"
  
# Scenario 3: Advanced
steps:
  - title: "Chain multiple commands"
```

### Pattern 2: Mistake-Driven Learning

Anticipate and handle common errors:

```yaml
error_recovery:
  common_mistakes:
    - pattern: "mistake_pattern"
      message: "What went wrong"
      hint: "How to fix"
      correction: "Exact fix"
```

### Pattern 3: Scaffolded Hints

Provide increasingly specific hints:

```yaml
hints:
  - level: 1
    text: "What tool/concept to use"
  - level: 2
    text: "Command structure with placeholders"
  - level: 3
    text: "Nearly complete solution"
```

### Pattern 4: Multi-Criteria Validation

Validate multiple aspects:

```yaml
validation:
  rules:
    - rule_type: command_structure
    - rule_type: output_verification
    - rule_type: side_effect_check
```

---

## Troubleshooting

### Issue: Validation Too Strict

**Problem**: Users can't complete step with valid variations

**Solution**: Use regex and accepted_variations
```yaml
validation:
  rules:
    - rule_type: command_regex
      parameters:
        pattern: "^docker (pull|image pull) nginx(:.*)?$"
  accepted_variations:
    - "docker pull nginx"
    - "docker pull nginx:latest"
```

### Issue: Hints Too Revealing

**Problem**: Level 1 hint gives away answer

**Solution**: Make hints more progressive
```yaml
# BAD
hints:
  - level: 1
    text: "Run docker pull nginx"

# GOOD
hints:
  - level: 1
    text: "Use the docker pull command"
  - level: 2
    text: "The image name is 'nginx'"
  - level: 3
    text: "Try: docker pull nginx"
```

### Issue: Steps Too Complex

**Problem**: Step takes >5 minutes or has multiple objectives

**Solution**: Split into smaller steps
```yaml
# BAD: Too complex
- title: "Set up database and load data"

# GOOD: Atomic steps
- title: "Start database container"
- title: "Connect to database"
- title: "Load sample data"
```

### Issue: Unclear Success Criteria

**Problem**: Users don't know if they succeeded

**Solution**: Add post_validation and clear success messages
```yaml
post_validation:
  - type: container_running
    parameters:
      image: "nginx"

success_message: |
  ✅ NGINX container is running! You can verify with: docker ps
```

---

## Template Scenarios

### Terminal Scenario Template

```yaml
scenario:
  id: "template-terminal"
  title: "Template: Terminal Scenario"
  description: "Description here"
  difficulty: intermediate
  estimated_time: 15
  tier_access: intermediate
  
  environment:
    type: terminal
    docker_required: true
  
  steps:
    - id: "step_1"
      title: "Step Title"
      objective: "What to accomplish"
      
      guidance:
        initial: "Guidance text"
        hints:
          - level: 1
            text: "Concept hint"
          - level: 2
            text: "Structure hint"
          - level: 3
            text: "Solution hint"
      
      validation:
        type: command_execution
        rules:
          - rule_type: command_regex
            parameters:
              pattern: "pattern"
      
      success_message: "Success!"
```

---

## Conclusion

Creating great scenarios requires:
- Clear learning objectives
- Atomic, well-defined steps
- Progressive hints that teach
- Flexible validation
- Anticipation of common mistakes
- Encouraging, educational feedback

Use this guide as a reference when authoring scenarios, and always test with real users to ensure an engaging learning experience.
