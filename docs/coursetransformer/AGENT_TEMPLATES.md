# CourseTransformer - Agent Implementation Templates

This document provides code templates and patterns for implementing the CourseTransformer agents.

## Base Agent Class

All agents inherit from a common base class that provides LLM integration, tool management, and state handling.

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from langchain.agents import AgentExecutor
from langchain.tools import Tool
from langchain.prompts import PromptTemplate

class BaseAgent(ABC):
    """Base class for all transformation agents"""
    
    def __init__(self, llm_client, principles: Dict[str, Any]):
        """
        Initialize agent with LLM and guiding principles
        
        Args:
            llm_client: LLM client (OLLAMA, OpenAI, etc.)
            principles: Guiding principles configuration
        """
        self.llm = llm_client
        self.principles = principles
        self.tools = self._setup_tools()
        self.executor = self._create_executor()
    
    @abstractmethod
    def _setup_tools(self) -> List[Tool]:
        """Define agent-specific tools"""
        pass
    
    @abstractmethod
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent logic and return updated state"""
        pass
    
    def _create_executor(self) -> AgentExecutor:
        """Create LangChain agent executor"""
        from langchain.agents import initialize_agent, AgentType
        
        return initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
    
    def _build_prompt(self, task: str, context: Dict[str, Any]) -> str:
        """Build LLM prompt with context"""
        template = PromptTemplate(
            input_variables=["task", "context", "principles"],
            template="""You are an expert {agent_type} for course transformation.

Task: {task}

Context:
{context}

Guiding Principles:
{principles}

Please complete the task following the principles."""
        )
        
        return template.format(
            agent_type=self.__class__.__name__,
            task=task,
            context=str(context),
            principles=str(self.principles)
        )
    
    def _log(self, message: str, level: str = "INFO"):
        """Log agent activity"""
        import logging
        logger = logging.getLogger(self.__class__.__name__)
        getattr(logger, level.lower())(message)
    
    def _handle_error(self, error: Exception, state: Dict[str, Any]) -> Dict[str, Any]:
        """Handle agent errors"""
        self._log(f"Error: {str(error)}", "ERROR")
        state["errors"].append({
            "agent": self.__class__.__name__,
            "error": str(error),
            "timestamp": datetime.utcnow().isoformat()
        })
        return state
```

## Example: Ingestion Agent

```python
from pathlib import Path
import PyPDF2
import pdfplumber
from typing import Dict, Any, List

class IngestionAgent(BaseAgent):
    """Parse legacy course content from multiple formats"""
    
    def _setup_tools(self) -> List[Tool]:
        """Setup ingestion-specific tools"""
        return [
            Tool(
                name="parse_r_code",
                func=self._parse_r_file,
                description="Parse R file and extract functions, libraries, logic"
            ),
            Tool(
                name="extract_pdf_text",
                func=self._extract_from_pdf,
                description="Extract text from PDF preserving structure"
            ),
            Tool(
                name="parse_markdown",
                func=self._parse_markdown_file,
                description="Parse Markdown into structured AST"
            ),
            Tool(
                name="extract_concepts",
                func=self._extract_concepts_with_llm,
                description="Use LLM to extract educational concepts from text"
            )
        ]
    
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute ingestion workflow"""
        try:
            self._log("Starting ingestion...")
            
            course_path = state["legacy_course_path"]
            file_formats = state.get("file_formats", ["R", "MD", "PDF"])
            
            # Parse files
            parsed_content = self._parse_course_directory(course_path, file_formats)
            
            # Extract concepts
            concepts = self._extract_concepts(parsed_content)
            
            # Build course structure
            structure = self._identify_course_structure(course_path)
            
            # Code inventory
            code_inventory = self._analyze_code_base(parsed_content)
            
            # Update state
            state["ingestion_output"] = {
                "parsed_content": parsed_content,
                "extracted_concepts": concepts,
                "structure": structure,
                "code_inventory": code_inventory,
                "metadata": self._extract_metadata(parsed_content)
            }
            
            self._log(f"Ingestion complete. Extracted {len(concepts)} concepts.")
            return state
            
        except Exception as e:
            return self._handle_error(e, state)
    
    def _parse_r_file(self, filepath: str) -> Dict[str, Any]:
        """Parse R file and extract information"""
        with open(filepath, 'r') as f:
            code = f.read()
        
        # Extract libraries
        libraries = []
        for line in code.split('\n'):
            if 'library(' in line or 'require(' in line:
                lib = line.split('(')[1].split(')')[0].strip('"'')
                libraries.append(lib)
        
        # Extract functions (simple parsing)
        functions = []
        lines = code.split('\n')
        for i, line in enumerate(lines):
            if '<- function(' in line:
                func_name = line.split('<-')[0].strip()
                functions.append({
                    "name": func_name,
                    "line": i + 1
                })
        
        return {
            "filepath": filepath,
            "language": "R",
            "libraries": list(set(libraries)),
            "functions": functions,
            "raw_code": code
        }
    
    def _extract_from_pdf(self, filepath: str) -> str:
        """Extract text from PDF"""
        text = ""
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception:
            # Fallback to PyPDF2
            with open(filepath, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        
        return text
    
    def _parse_markdown_file(self, filepath: str) -> Dict[str, Any]:
        """Parse Markdown file"""
        import markdown
        from bs4 import BeautifulSoup
        
        with open(filepath, 'r') as f:
            md_content = f.read()
        
        # Convert to HTML then parse structure
        html = markdown.markdown(md_content)
        soup = BeautifulSoup(html, 'html.parser')
        
        headers = [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3'])]
        
        return {
            "filepath": filepath,
            "content": md_content,
            "headers": headers
        }
    
    def _extract_concepts_with_llm(self, text: str) -> List[Dict[str, str]]:
        """Use LLM to extract concepts"""
        prompt = self._build_prompt(
            task="Extract educational concepts from this text",
            context={"text": text[:2000]}  # Limit for token constraints
        )
        
        response = self.llm.generate(prompt)
        # Parse LLM response (assumed JSON format)
        # ... parsing logic
        return []  # Placeholder
    
    def _parse_course_directory(self, course_path: str, formats: List[str]) -> Dict:
        """Parse entire course directory"""
        parsed = {"files": [], "total_size": 0}
        
        for file in Path(course_path).rglob("*"):
            if file.is_file():
                if any(file.suffix.lower() in [f".{fmt.lower()}" for fmt in formats]):
                    # Parse based on file type
                    if file.suffix == ".R":
                        content = self._parse_r_file(str(file))
                    elif file.suffix == ".md":
                        content = self._parse_markdown_file(str(file))
                    elif file.suffix == ".pdf":
                        content = {"text": self._extract_from_pdf(str(file))}
                    
                    parsed["files"].append(content)
        
        return parsed
    
    def _extract_concepts(self, parsed_content: Dict) -> List[Dict]:
        """Extract concepts from parsed content"""
        # Aggregate text
        all_text = ""
        for file in parsed_content.get("files", []):
            if "raw_code" in file:
                all_text += file["raw_code"] + "\n"
            if "text" in file:
                all_text += file["text"] + "\n"
        
        # Use LLM for concept extraction
        concepts = self._extract_concepts_with_llm(all_text)
        return concepts
    
    def _identify_course_structure(self, course_path: str) -> Dict:
        """Identify course structure from directory hierarchy"""
        structure = {"modules": []}
        
        # Simple structure extraction based on directory names
        for dir_path in Path(course_path).iterdir():
            if dir_path.is_dir():
                module = {
                    "module_id": dir_path.name,
                    "title": dir_path.name.replace('_', ' ').title(),
                    "lessons": []
                }
                structure["modules"].append(module)
        
        return structure
    
    def _analyze_code_base(self, parsed_content: Dict) -> Dict:
        """Analyze code inventory"""
        inventory = {}
        
        for file in parsed_content.get("files", []):
            lang = file.get("language")
            if lang:
                if lang not in inventory:
                    inventory[lang] = {"files": 0, "lines": 0, "libraries": set()}
                
                inventory[lang]["files"] += 1
                if "raw_code" in file:
                    inventory[lang]["lines"] += len(file["raw_code"].split('\n'))
                if "libraries" in file:
                    inventory[lang]["libraries"].update(file["libraries"])
        
        # Convert sets to lists for JSON serialization
        for lang in inventory:
            inventory[lang]["libraries"] = list(inventory[lang]["libraries"])
        
        return inventory
    
    def _extract_metadata(self, parsed_content: Dict) -> Dict:
        """Extract course metadata"""
        # Use LLM to extract metadata from first few files
        return {
            "title": "Extracted Course Title",
            "author": "Unknown",
            "topics": []
        }
```

## Example: Analysis Agent

```python
class AnalysisAgent(BaseAgent):
    """Analyze legacy content for relevance and gaps"""
    
    def _setup_tools(self) -> List[Tool]:
        return [
            Tool(
                name="check_relevance",
                func=self._check_concept_relevance,
                description="Check if a concept is still relevant in target year"
            ),
            Tool(
                name="identify_gaps",
                func=self._identify_missing_topics,
                description="Identify modern topics missing from curriculum"
            ),
            Tool(
                name="query_knowledge_base",
                func=self._query_kb,
                description="Query knowledge base for modern best practices"
            )
        ]
    
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute analysis workflow"""
        try:
            self._log("Starting analysis...")
            
            concepts = state["ingestion_output"]["extracted_concepts"]
            target_year = self.principles.get("target_year", 2026)
            
            # Analyze relevance
            relevance_report = self._analyze_relevance(concepts, target_year)
            
            # Identify gaps
            gaps = self._find_gaps(concepts)
            
            # Technology stack analysis
            code_inventory = state["ingestion_output"]["code_inventory"]
            tech_analysis = self._analyze_tech_stack(code_inventory)
            
            # Update state
            state["analysis_output"] = {
                "overall_relevance": self._calculate_overall_relevance(relevance_report),
                "concept_analysis": relevance_report,
                "missing_topics": gaps,
                "technology_analysis": tech_analysis
            }
            
            self._log("Analysis complete.")
            return state
            
        except Exception as e:
            return self._handle_error(e, state)
    
    def _check_concept_relevance(self, concept: str) -> Dict:
        """Check relevance of a single concept"""
        prompt = f"""Assess the relevance of this educational concept in {self.principles['target_year']}:
        
        Concept: {concept}
        
        Rate on scale 0-100 and categorize as: timeless, relevant, outdated, or obsolete.
        Provide brief reasoning."""
        
        response = self.llm.generate(prompt)
        # Parse response (implement actual parsing)
        return {"concept": concept, "relevance_score": 75, "status": "relevant"}
    
    def _identify_missing_topics(self, existing_concepts: List[str]) -> List[Dict]:
        """Identify modern topics missing from curriculum"""
        modern_topics = self.principles.get("modern_topics", {})
        critical = modern_topics.get("critical", [])
        important = modern_topics.get("important", [])
        
        gaps = []
        for topic in critical + important:
            if topic not in existing_concepts:
                gaps.append({
                    "topic": topic,
                    "priority": "critical" if topic in critical else "important",
                    "reasoning": f"Essential for {self.principles['target_year']} curriculum"
                })
        
        return gaps
    
    def _query_kb(self, query: str) -> List[str]:
        """Query knowledge base (RAG system)"""
        # Placeholder for RAG integration
        return []
    
    def _analyze_relevance(self, concepts: List[Dict], target_year: int) -> List[Dict]:
        """Analyze relevance of all concepts"""
        results = []
        for concept in concepts:
            relevance = self._check_concept_relevance(concept.get("concept", ""))
            results.append(relevance)
        return results
    
    def _find_gaps(self, concepts: List[Dict]) -> List[Dict]:
        """Find missing topics"""
        concept_names = [c.get("concept", "") for c in concepts]
        return self._identify_missing_topics(concept_names)
    
    def _analyze_tech_stack(self, code_inventory: Dict) -> Dict:
        """Analyze technology stack"""
        analysis = {}
        for lang, stats in code_inventory.items():
            if lang == "R":
                analysis[lang] = {
                    "status": "legacy",
                    "recommendation": "migrate to Python",
                    "modern_equivalent": "Python + pandas + scikit-learn"
                }
        return analysis
    
    def _calculate_overall_relevance(self, report: List[Dict]) -> float:
        """Calculate overall relevance score"""
        if not report:
            return 0.0
        scores = [r.get("relevance_score", 0) for r in report]
        return sum(scores) / len(scores) if scores else 0.0
```

## Agent Factory Pattern

```python
class AgentFactory:
    """Factory for creating agents"""
    
    @staticmethod
    def create_agent(
        agent_type: str,
        llm_client,
        principles: Dict[str, Any]
    ) -> BaseAgent:
        """Create agent instance by type"""
        agents = {
            "ingestion": IngestionAgent,
            "analysis": AnalysisAgent,
            "planning": PlanningAgent,
            "modernization": ModernizationAgent,
            "generation": GenerationAgent,
            "qa": QualityAgent,
            "export": ExportAgent
        }
        
        agent_class = agents.get(agent_type.lower())
        if not agent_class:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        return agent_class(llm_client, principles)
```

## Testing Agents

```python
import pytest
from unittest.mock import Mock, MagicMock

def test_ingestion_agent():
    """Test ingestion agent"""
    # Setup
    llm_mock = Mock()
    principles = {"target_year": 2026}
    agent = IngestionAgent(llm_mock, principles)
    
    # Create test state
    state = {
        "legacy_course_path": "/path/to/course",
        "file_formats": ["R", "MD"],
        "errors": []
    }
    
    # Execute
    result = agent.execute(state)
    
    # Assertions
    assert "ingestion_output" in result
    assert "extracted_concepts" in result["ingestion_output"]
    assert result["errors"] == []

def test_analysis_agent():
    """Test analysis agent"""
    llm_mock = Mock()
    llm_mock.generate.return_value = '{"relevance_score": 85, "status": "relevant"}'
    
    principles = {"target_year": 2026, "modern_topics": {"critical": ["transformers"]}}
    agent = AnalysisAgent(llm_mock, principles)
    
    state = {
        "ingestion_output": {
            "extracted_concepts": [{"concept": "linear_regression"}],
            "code_inventory": {"R": {"files": 10}}
        },
        "errors": []
    }
    
    result = agent.execute(state)
    
    assert "analysis_output" in result
    assert "overall_relevance" in result["analysis_output"]
    assert "missing_topics" in result["analysis_output"]
```

---

This provides a solid foundation for implementing all CourseTransformer agents with consistent patterns and best practices.
