"""
LangChain-Inspired Workflow Management for Multi-LLM Pipeline
Advanced orchestration, memory management, and chain-of-thought capabilities
"""

import json
import logging
import asyncio
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, asdict
from enum import Enum
import time
from datetime import datetime
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkflowStatus(Enum):
    """Workflow execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    PAUSED = "paused"


class NodeType(Enum):
    """Types of workflow nodes"""
    LLM_CALL = "llm_call"
    TRANSFORM = "transform"
    CONDITION = "condition"
    PARALLEL = "parallel"
    SEQUENCE = "sequence"
    MEMORY_STORE = "memory_store"
    MEMORY_RETRIEVE = "memory_retrieve"


@dataclass
class WorkflowContext:
    """Context passed between workflow nodes"""
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    session_id: str
    execution_id: str
    timestamp: str
    
    def copy(self) -> 'WorkflowContext':
        """Create a copy of the context"""
        return WorkflowContext(
            data=self.data.copy(),
            metadata=self.metadata.copy(),
            session_id=self.session_id,
            execution_id=self.execution_id,
            timestamp=self.timestamp
        )


@dataclass
class WorkflowNode:
    """Base workflow node"""
    node_id: str
    node_type: NodeType
    name: str
    description: str
    function: Optional[Callable] = None
    parameters: Optional[Dict[str, Any]] = None
    retry_count: int = 3
    timeout: int = 300  # 5 minutes
    dependencies: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}
        if self.dependencies is None:
            self.dependencies = []


class WorkflowMemory:
    """Advanced memory management for workflows"""
    
    def __init__(self, max_entries: int = 1000):
        self.memory: Dict[str, Any] = {}
        self.max_entries = max_entries
        self.access_count: Dict[str, int] = {}
        self.timestamps: Dict[str, float] = {}
        
    def store(self, key: str, value: Any, metadata: Optional[Dict[str, Any]] = None):
        """Store data in memory with metadata"""
        if len(self.memory) >= self.max_entries:
            self._evict_oldest()
            
        self.memory[key] = {
            'value': value,
            'metadata': metadata if metadata is not None else {},
            'stored_at': time.time()
        }
        self.access_count[key] = 0
        self.timestamps[key] = time.time()
        
        logger.debug(f"Stored in memory: {key}")
    
    def retrieve(self, key: str) -> Any:
        """Retrieve data from memory"""
        if key in self.memory:
            self.access_count[key] += 1
            self.timestamps[key] = time.time()
            return self.memory[key]['value']
        return None
    
    def get_metadata(self, key: str) -> Dict[str, Any]:
        """Get metadata for a memory entry"""
        if key in self.memory:
            return self.memory[key]['metadata']
        return {}
    
    def search(self, query: str) -> List[str]:
        """Search memory keys by query"""
        matching_keys = []
        query_lower = query.lower()
        
        for key in self.memory.keys():
            if query_lower in key.lower():
                matching_keys.append(key)
                
        return sorted(matching_keys, key=lambda k: self.access_count.get(k, 0), reverse=True)
    
    def _evict_oldest(self):
        """Evict the oldest, least accessed entry"""
        if not self.memory:
            return
            
        # Find least accessed, oldest entry
        min_access = min(self.access_count.values())
        oldest_candidates = [k for k, v in self.access_count.items() if v == min_access]
        
        if oldest_candidates:
            oldest_key = min(oldest_candidates, key=lambda k: self.timestamps[k])
            del self.memory[oldest_key]
            del self.access_count[oldest_key]
            del self.timestamps[oldest_key]
            logger.debug(f"Evicted from memory: {oldest_key}")
    
    def clear(self):
        """Clear all memory"""
        self.memory.clear()
        self.access_count.clear()
        self.timestamps.clear()
        logger.info("Memory cleared")


class WorkflowOrchestrator:
    """Advanced workflow orchestration engine"""
    
    def __init__(self, memory_size: int = 1000):
        self.nodes: Dict[str, WorkflowNode] = {}
        self.edges: Dict[str, List[str]] = {}  # node_id -> [next_node_ids]
        self.workflows: Dict[str, Dict[str, Any]] = {}
        self.memory = WorkflowMemory(memory_size)
        self.execution_history: List[Dict[str, Any]] = []
        
    def add_node(self, node: WorkflowNode) -> 'WorkflowOrchestrator':
        """Add a node to the workflow"""
        self.nodes[node.node_id] = node
        if node.node_id not in self.edges:
            self.edges[node.node_id] = []
        logger.info(f"Added workflow node: {node.name} ({node.node_id})")
        return self
    
    def add_edge(self, from_node: str, to_node: str) -> 'WorkflowOrchestrator':
        """Add an edge between nodes"""
        if from_node not in self.edges:
            self.edges[from_node] = []
        self.edges[from_node].append(to_node)
        logger.debug(f"Added edge: {from_node} -> {to_node}")
        return self
    
    def create_llm_node(self, node_id: str, name: str, llm_function: Callable, 
                       system_prompt: str = "", user_prompt_template: str = ""):
        """Create an LLM processing node"""
        def llm_wrapper(context: WorkflowContext) -> WorkflowContext:
            try:
                # Format prompts with context data
                formatted_user_prompt = user_prompt_template.format(**context.data)
                
                # Call LLM function
                response = llm_function(formatted_user_prompt, system_prompt)
                
                # Store response in context
                context.data[f"{node_id}_response"] = response
                context.metadata[f"{node_id}_completed"] = True
                
                # Store in memory for future reference
                self.memory.store(
                    f"{context.session_id}_{node_id}_response",
                    response,
                    {"node_id": node_id, "timestamp": context.timestamp}
                )
                
                logger.info(f"LLM node {name} completed successfully")
                return context
                
            except Exception as e:
                logger.error(f"LLM node {name} failed: {e}")
                context.metadata[f"{node_id}_error"] = str(e)
                raise
        
        node = WorkflowNode(
            node_id=node_id,
            node_type=NodeType.LLM_CALL,
            name=name,
            description=f"LLM processing: {name}",
            function=llm_wrapper,
            parameters={"system_prompt": system_prompt, "user_prompt_template": user_prompt_template}
        )
        
        return self.add_node(node)
    
    def create_transform_node(self, node_id: str, name: str, transform_function: Callable):
        """Create a data transformation node"""
        def transform_wrapper(context: WorkflowContext) -> WorkflowContext:
            try:
                result = transform_function(context.data)
                context.data.update(result)
                context.metadata[f"{node_id}_completed"] = True
                logger.info(f"Transform node {name} completed successfully")
                return context
            except Exception as e:
                logger.error(f"Transform node {name} failed: {e}")
                context.metadata[f"{node_id}_error"] = str(e)
                raise
        
        node = WorkflowNode(
            node_id=node_id,
            node_type=NodeType.TRANSFORM,
            name=name,
            description=f"Data transformation: {name}",
            function=transform_wrapper
        )
        
        return self.add_node(node)
    
    def create_condition_node(self, node_id: str, name: str, condition_function: Callable,
                            true_path: str, false_path: str):
        """Create a conditional branching node"""
        def condition_wrapper(context: WorkflowContext) -> WorkflowContext:
            try:
                result = condition_function(context.data)
                context.data[f"{node_id}_condition_result"] = result
                context.metadata[f"{node_id}_branch"] = true_path if result else false_path
                context.metadata[f"{node_id}_completed"] = True
                logger.info(f"Condition node {name} evaluated to {result}")
                return context
            except Exception as e:
                logger.error(f"Condition node {name} failed: {e}")
                context.metadata[f"{node_id}_error"] = str(e)
                raise
        
        node = WorkflowNode(
            node_id=node_id,
            node_type=NodeType.CONDITION,
            name=name,
            description=f"Conditional branch: {name}",
            function=condition_wrapper,
            parameters={"true_path": true_path, "false_path": false_path}
        )
        
        return self.add_node(node)
    
    def create_memory_store_node(self, node_id: str, name: str, key_template: str, 
                                value_path: str):
        """Create a node that stores data in memory"""
        def memory_store_wrapper(context: WorkflowContext) -> WorkflowContext:
            try:
                key = key_template.format(**context.data)
                value = context.data.get(value_path)
                
                self.memory.store(key, value, {
                    "node_id": node_id,
                    "session_id": context.session_id,
                    "timestamp": context.timestamp
                })
                
                context.metadata[f"{node_id}_stored_key"] = key
                context.metadata[f"{node_id}_completed"] = True
                logger.info(f"Memory store node {name} stored: {key}")
                return context
            except Exception as e:
                logger.error(f"Memory store node {name} failed: {e}")
                context.metadata[f"{node_id}_error"] = str(e)
                raise
        
        node = WorkflowNode(
            node_id=node_id,
            node_type=NodeType.MEMORY_STORE,
            name=name,
            description=f"Memory storage: {name}",
            function=memory_store_wrapper,
            parameters={"key_template": key_template, "value_path": value_path}
        )
        
        return self.add_node(node)
    
    def create_memory_retrieve_node(self, node_id: str, name: str, key_template: str,
                                  output_key: str):
        """Create a node that retrieves data from memory"""
        def memory_retrieve_wrapper(context: WorkflowContext) -> WorkflowContext:
            try:
                key = key_template.format(**context.data)
                value = self.memory.retrieve(key)
                
                if value is not None:
                    context.data[output_key] = value
                    context.metadata[f"{node_id}_retrieved"] = True
                else:
                    context.metadata[f"{node_id}_not_found"] = True
                
                context.metadata[f"{node_id}_completed"] = True
                logger.info(f"Memory retrieve node {name} processed key: {key}")
                return context
            except Exception as e:
                logger.error(f"Memory retrieve node {name} failed: {e}")
                context.metadata[f"{node_id}_error"] = str(e)
                raise
        
        node = WorkflowNode(
            node_id=node_id,
            node_type=NodeType.MEMORY_RETRIEVE,
            name=name,
            description=f"Memory retrieval: {name}",
            function=memory_retrieve_wrapper,
            parameters={"key_template": key_template, "output_key": output_key}
        )
        
        return self.add_node(node)
    
    async def execute_workflow(self, start_node: str, initial_context: WorkflowContext,
                             max_steps: int = 100) -> WorkflowContext:
        """Execute workflow starting from a specific node"""
        execution_id = hashlib.md5(f"{start_node}_{time.time()}".encode()).hexdigest()[:8]
        initial_context.execution_id = execution_id
        
        logger.info(f"Starting workflow execution {execution_id} from node: {start_node}")
        
        execution_log = {
            "execution_id": execution_id,
            "start_node": start_node,
            "start_time": time.time(),
            "steps": [],
            "status": WorkflowStatus.RUNNING.value
        }
        
        current_context = initial_context.copy()
        current_nodes = [start_node]
        step_count = 0
        
        try:
            while current_nodes and step_count < max_steps:
                step_count += 1
                next_nodes = []
                
                for node_id in current_nodes:
                    if node_id not in self.nodes:
                        logger.warning(f"Node {node_id} not found, skipping")
                        continue
                    
                    node = self.nodes[node_id]
                    step_start = time.time()
                    
                    logger.info(f"Executing node: {node.name} ({node_id})")
                    
                    try:
                        # Execute node function with retry logic
                        for retry in range(node.retry_count):
                            try:
                                if node.function:
                                    # Check if function is async
                                    if asyncio.iscoroutinefunction(node.function):
                                        current_context = await asyncio.wait_for(
                                            node.function(current_context),
                                            timeout=node.timeout
                                        )
                                    else:
                                        # Execute sync function
                                        current_context = node.function(current_context)
                                break
                            except Exception as e:
                                if retry < node.retry_count - 1:
                                    logger.warning(f"Node {node_id} retry {retry + 1}/{node.retry_count}: {e}")
                                    await asyncio.sleep(2 ** retry)  # Exponential backoff
                                else:
                                    raise
                        
                        step_duration = time.time() - step_start
                        
                        step_log = {
                            "step": step_count,
                            "node_id": node_id,
                            "node_name": node.name,
                            "duration": step_duration,
                            "status": "completed",
                            "timestamp": datetime.now().isoformat()
                        }
                        
                        execution_log["steps"].append(step_log)
                        
                        # Determine next nodes
                        if node.node_type == NodeType.CONDITION:
                            # Branch based on condition result
                            branch = current_context.metadata.get(f"{node_id}_branch")
                            if branch:
                                next_nodes.append(branch)
                        else:
                            # Add all connected nodes
                            next_nodes.extend(self.edges.get(node_id, []))
                        
                        logger.info(f"Node {node.name} completed in {step_duration:.2f}s")
                        
                    except Exception as e:
                        step_log = {
                            "step": step_count,
                            "node_id": node_id,
                            "node_name": node.name,
                            "status": "failed",
                            "error": str(e),
                            "timestamp": datetime.now().isoformat()
                        }
                        execution_log["steps"].append(step_log)
                        logger.error(f"Node {node.name} failed: {e}")
                        raise
                
                current_nodes = next_nodes
            
            execution_log["status"] = WorkflowStatus.COMPLETED.value
            execution_log["end_time"] = time.time()
            execution_log["total_duration"] = execution_log["end_time"] - execution_log["start_time"]
            
            logger.info(f"Workflow execution {execution_id} completed successfully in {step_count} steps")
            
        except Exception as e:
            execution_log["status"] = WorkflowStatus.FAILED.value
            execution_log["error"] = str(e)
            execution_log["end_time"] = time.time()
            logger.error(f"Workflow execution {execution_id} failed: {e}")
            raise
        
        finally:
            self.execution_history.append(execution_log)
        
        return current_context
    
    def get_execution_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent execution history"""
        return self.execution_history[-limit:]
    
    def get_workflow_stats(self) -> Dict[str, Any]:
        """Get workflow statistics"""
        total_executions = len(self.execution_history)
        successful = sum(1 for ex in self.execution_history if ex["status"] == WorkflowStatus.COMPLETED.value)
        failed = sum(1 for ex in self.execution_history if ex["status"] == WorkflowStatus.FAILED.value)
        
        avg_duration = 0
        if self.execution_history:
            durations = [ex.get("total_duration", 0) for ex in self.execution_history if "total_duration" in ex]
            avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            "total_nodes": len(self.nodes),
            "total_edges": sum(len(edges) for edges in self.edges.values()),
            "total_executions": total_executions,
            "successful_executions": successful,
            "failed_executions": failed,
            "success_rate": successful / total_executions if total_executions > 0 else 0,
            "average_duration": avg_duration,
            "memory_entries": len(self.memory.memory)
        }
    
    def visualize_workflow(self) -> str:
        """Generate a text visualization of the workflow"""
        lines = ["Workflow Graph:"]
        lines.append("=" * 50)
        
        for node_id, node in self.nodes.items():
            node_line = f"[{node_id}] {node.name} ({node.node_type.value})"
            lines.append(node_line)
            
            # Show connections
            edges = self.edges.get(node_id, [])
            if edges:
                for edge in edges:
                    target_node = self.nodes.get(edge)
                    target_name = target_node.name if target_node else edge
                    lines.append(f"  └─> [{edge}] {target_name}")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def export_workflow(self, filename: str):
        """Export workflow configuration to JSON"""
        workflow_data = {
            "nodes": {node_id: {
                "node_type": node.node_type.value,
                "name": node.name,
                "description": node.description,
                "parameters": node.parameters,
                "retry_count": node.retry_count,
                "timeout": node.timeout,
                "dependencies": node.dependencies
            } for node_id, node in self.nodes.items()},
            "edges": self.edges,
            "exported_at": datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(workflow_data, f, indent=2)
        
        logger.info(f"Workflow exported to {filename}")
    
    def clear_workflow(self):
        """Clear all workflow nodes and edges"""
        self.nodes.clear()
        self.edges.clear()
        self.memory.clear()
        logger.info("Workflow cleared")


# Utility functions for common workflow patterns
def create_sequential_workflow(orchestrator: WorkflowOrchestrator, 
                             node_configs: List[Dict[str, Any]]) -> str:
    """Create a sequential workflow from node configurations"""
    previous_node = None
    start_node = None
    
    for config in node_configs:
        node_id = config["node_id"]
        node_type = config["node_type"]
        
        if node_type == "llm":
            orchestrator.create_llm_node(
                node_id=node_id,
                name=config["name"],
                llm_function=config["function"],
                system_prompt=config.get("system_prompt", ""),
                user_prompt_template=config.get("user_prompt_template", "")
            )
        elif node_type == "transform":
            orchestrator.create_transform_node(
                node_id=node_id,
                name=config["name"],
                transform_function=config["function"]
            )
        
        if start_node is None:
            start_node = node_id
        
        if previous_node:
            orchestrator.add_edge(previous_node, node_id)
        
        previous_node = node_id
    
    return start_node


def create_parallel_workflow(orchestrator: WorkflowOrchestrator,
                           parallel_configs: List[Dict[str, Any]],
                           merge_node_id: str, merge_function: Callable) -> str:
    """Create a parallel workflow that merges results"""
    start_nodes = []
    
    # Create parallel branches
    for config in parallel_configs:
        node_id = config["node_id"]
        
        if config["node_type"] == "llm":
            orchestrator.create_llm_node(
                node_id=node_id,
                name=config["name"],
                llm_function=config["function"],
                system_prompt=config.get("system_prompt", ""),
                user_prompt_template=config.get("user_prompt_template", "")
            )
        
        start_nodes.append(node_id)
        orchestrator.add_edge(node_id, merge_node_id)
    
    # Create merge node
    orchestrator.create_transform_node(
        node_id=merge_node_id,
        name="Merge Results",
        transform_function=merge_function
    )
    
    return start_nodes[0] if start_nodes else merge_node_id