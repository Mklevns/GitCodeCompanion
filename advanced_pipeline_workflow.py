"""
Advanced Multi-LLM Pipeline with LangChain-Inspired Workflow Management
Orchestrates the 4-stage pipeline with memory, conditional logic, and advanced state management
"""

import asyncio
import logging
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib

from langchain_workflow import (
    WorkflowOrchestrator, WorkflowContext, WorkflowNode, NodeType, WorkflowStatus
)
from llm_clients import LLMClients
from pipeline_stages import PipelineStages
from git_github_utils import GitHubManager
from report_generator import ReportGenerator
from prompt_config import PromptConfigManager

logger = logging.getLogger(__name__)

class AdvancedMultiLLMPipeline:
    """Advanced Multi-LLM Pipeline with workflow orchestration"""
    
    def __init__(self, config_file: str = "prompt_config.json", demo_mode: bool = False):
        """Initialize the advanced pipeline"""
        self.llm_clients = LLMClients()
        self.pipeline_stages = PipelineStages(config_file)
        self.demo_mode = demo_mode
        
        # Initialize GitHub manager only if not in demo mode
        if not demo_mode:
            try:
                self.github_manager = GitHubManager()
            except ValueError as e:
                logger.warning(f"GitHub manager initialization failed: {e}, enabling demo mode")
                self.demo_mode = True
                self.github_manager = None
        else:
            self.github_manager = None
            
        self.report_generator = ReportGenerator()
        self.prompt_config = PromptConfigManager(config_file)
        
        # Initialize workflow orchestrator
        self.orchestrator = WorkflowOrchestrator(memory_size=1000)
        self.session_id = self._generate_session_id()
        
        # Setup the workflow
        self._setup_multi_llm_workflow()
        
        logger.info("Advanced Multi-LLM Pipeline initialized with workflow orchestration")
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().isoformat()
        return hashlib.md5(f"pipeline_{timestamp}".encode()).hexdigest()[:12]
    
    def _setup_multi_llm_workflow(self):
        """Setup the complete multi-LLM workflow"""
        
        # Node 1: File Retrieval and Preprocessing
        self.orchestrator.create_transform_node(
            node_id="file_retrieval",
            name="File Retrieval",
            transform_function=self._retrieve_changed_files
        )
        
        # Node 2: Quality Gate Check
        self.orchestrator.create_condition_node(
            node_id="quality_gate",
            name="Quality Gate",
            condition_function=self._quality_gate_check,
            true_path="stage_1_gemini",
            false_path="early_exit"
        )
        
        # Node 3: Stage 1 - Gemini Analysis
        self.orchestrator.create_llm_node(
            node_id="stage_1_gemini",
            name="Gemini Deep Analysis",
            llm_function=self._stage_1_wrapper,
            system_prompt="",  # Will be set dynamically
            user_prompt_template="Analyze these files: {files_summary}"
        )
        
        # Node 4: Analysis Quality Check
        self.orchestrator.create_condition_node(
            node_id="analysis_check",
            name="Analysis Quality Check",
            condition_function=self._analysis_quality_check,
            true_path="stage_2_chatgpt",
            false_path="analysis_retry"
        )
        
        # Node 5: Stage 2 - ChatGPT Generation
        self.orchestrator.create_llm_node(
            node_id="stage_2_chatgpt",
            name="ChatGPT Code Generation",
            llm_function=self._stage_2_wrapper,
            system_prompt="",  # Will be set dynamically
            user_prompt_template="Generate improvements based on: {analysis_results}"
        )
        
        # Node 6: Generation Quality Check
        self.orchestrator.create_condition_node(
            node_id="generation_check",
            name="Generation Quality Check",
            condition_function=self._generation_quality_check,
            true_path="stage_3_claude",
            false_path="generation_retry"
        )
        
        # Node 7: Stage 3 - Claude Integration
        self.orchestrator.create_llm_node(
            node_id="stage_3_claude",
            name="Claude Code Integration",
            llm_function=self._stage_3_wrapper,
            system_prompt="",  # Will be set dynamically
            user_prompt_template="Integrate code changes: {generated_code}"
        )
        
        # Node 8: Integration Quality Check
        self.orchestrator.create_condition_node(
            node_id="integration_check",
            name="Integration Quality Check",
            condition_function=self._integration_quality_check,
            true_path="stage_4_deepseek",
            false_path="integration_retry"
        )
        
        # Node 9: Stage 4 - DeepSeek Verification
        self.orchestrator.create_llm_node(
            node_id="stage_4_deepseek",
            name="DeepSeek Verification",
            llm_function=self._stage_4_wrapper,
            system_prompt="",  # Will be set dynamically
            user_prompt_template="Verify integrated code: {integrated_code}"
        )
        
        # Node 10: Final Quality Check
        self.orchestrator.create_condition_node(
            node_id="final_check",
            name="Final Quality Check",
            condition_function=self._final_quality_check,
            true_path="report_generation",
            false_path="verification_retry"
        )
        
        # Node 11: Report Generation
        self.orchestrator.create_transform_node(
            node_id="report_generation",
            name="Report Generation",
            transform_function=self._generate_final_report
        )
        
        # Node 12: GitHub Integration
        self.orchestrator.create_transform_node(
            node_id="github_integration",
            name="GitHub Integration",
            transform_function=self._post_to_github
        )
        
        # Memory Storage Nodes
        self.orchestrator.create_memory_store_node(
            node_id="store_analysis",
            name="Store Analysis Results",
            key_template="{session_id}_analysis",
            value_path="stage_1_response"
        )
        
        self.orchestrator.create_memory_store_node(
            node_id="store_generation",
            name="Store Generation Results",
            key_template="{session_id}_generation",
            value_path="stage_2_response"
        )
        
        # Retry Nodes
        self.orchestrator.create_transform_node(
            node_id="analysis_retry",
            name="Analysis Retry Handler",
            transform_function=self._handle_analysis_retry
        )
        
        self.orchestrator.create_transform_node(
            node_id="generation_retry",
            name="Generation Retry Handler",
            transform_function=self._handle_generation_retry
        )
        
        self.orchestrator.create_transform_node(
            node_id="early_exit",
            name="Early Exit Handler",
            transform_function=self._handle_early_exit
        )
        
        # Setup workflow edges
        self._setup_workflow_edges()
    
    def _setup_workflow_edges(self):
        """Setup workflow node connections"""
        # Main pipeline flow
        self.orchestrator.add_edge("file_retrieval", "quality_gate")
        self.orchestrator.add_edge("stage_1_gemini", "store_analysis")
        self.orchestrator.add_edge("store_analysis", "analysis_check")
        self.orchestrator.add_edge("stage_2_chatgpt", "store_generation")
        self.orchestrator.add_edge("store_generation", "generation_check")
        self.orchestrator.add_edge("stage_3_claude", "integration_check")
        self.orchestrator.add_edge("stage_4_deepseek", "final_check")
        self.orchestrator.add_edge("report_generation", "github_integration")
        
        # Retry flows
        self.orchestrator.add_edge("analysis_retry", "stage_1_gemini")
        self.orchestrator.add_edge("generation_retry", "stage_2_chatgpt")
        self.orchestrator.add_edge("integration_retry", "stage_3_claude")
        self.orchestrator.add_edge("verification_retry", "stage_4_deepseek")
    
    # Transform Functions
    def _retrieve_changed_files(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve changed files from PR"""
        try:
            pr_number = data.get('pr_number')
            if not self.demo_mode and self.github_manager and pr_number:
                files = self.github_manager.get_pr_changed_files(pr_number)
                data['changed_files'] = files
                data['files_count'] = len(files)
                data['files_summary'] = f"{len(files)} files changed"
                logger.info(f"Retrieved {len(files)} changed files from PR #{pr_number}")
            else:
                # Demo mode - use sample files
                from demo_mode import DemoPipeline
                demo = DemoPipeline()
                files = demo.create_sample_files()
                data['changed_files'] = files
                data['files_count'] = len(files)
                data['files_summary'] = f"{len(files)} sample files"
                logger.info(f"Using {len(files)} demo files")
            
            return data
        except Exception as e:
            logger.error(f"File retrieval failed: {e}")
            data['error'] = str(e)
            return data
    
    def _quality_gate_check(self, data: Dict[str, Any]) -> bool:
        """Check if files meet quality gate requirements"""
        files = data.get('changed_files', [])
        
        # Quality gate criteria
        if not files:
            logger.warning("No files to analyze")
            return False
        
        if len(files) > 50:
            logger.warning("Too many files changed (>50), consider splitting PR")
            data['quality_gate_warning'] = "Large PR detected"
        
        # Check for binary files
        code_files = [f for f in files if f.get('content') is not None]
        if len(code_files) == 0:
            logger.warning("No readable code files found")
            return False
        
        data['code_files'] = code_files
        logger.info(f"Quality gate passed: {len(code_files)} code files ready for analysis")
        return True
    
    def _analysis_quality_check(self, data: Dict[str, Any]) -> bool:
        """Check quality of analysis results"""
        response = data.get('stage_1_gemini_response', '')
        
        if not response or len(response) < 100:
            logger.warning("Analysis response too short")
            return False
        
        # Check for key analysis elements
        required_elements = ['issues', 'recommendations', 'analysis']
        found_elements = sum(1 for elem in required_elements if elem.lower() in response.lower())
        
        quality_score = found_elements / len(required_elements)
        data['analysis_quality_score'] = quality_score
        
        if quality_score < 0.5:
            logger.warning(f"Low analysis quality score: {quality_score}")
            return False
        
        logger.info(f"Analysis quality check passed: {quality_score}")
        return True
    
    def _generation_quality_check(self, data: Dict[str, Any]) -> bool:
        """Check quality of code generation"""
        response = data.get('stage_2_chatgpt_response', '')
        
        if not response or len(response) < 50:
            logger.warning("Generation response too short")
            return False
        
        # Check for code-like content
        code_indicators = ['def ', 'class ', 'function', 'import', 'return', '{', '}']
        found_indicators = sum(1 for indicator in code_indicators if indicator in response)
        
        if found_indicators < 2:
            logger.warning("Generated content doesn't appear to contain code")
            return False
        
        logger.info("Generation quality check passed")
        return True
    
    def _integration_quality_check(self, data: Dict[str, Any]) -> bool:
        """Check quality of code integration"""
        response = data.get('stage_3_claude_response', '')
        
        if not response:
            logger.warning("No integration response")
            return False
        
        logger.info("Integration quality check passed")
        return True
    
    def _final_quality_check(self, data: Dict[str, Any]) -> bool:
        """Final quality check before report generation"""
        verification = data.get('stage_4_deepseek_response', '')
        
        if not verification:
            logger.warning("No verification response")
            return False
        
        # Check if verification indicates success
        success_indicators = ['verified', 'passed', 'approved', 'quality']
        has_success = any(indicator in verification.lower() for indicator in success_indicators)
        
        data['pipeline_success'] = has_success
        logger.info(f"Final quality check: {'passed' if has_success else 'needs review'}")
        return True
    
    # LLM Wrapper Functions
    def _stage_1_wrapper(self, prompt: str, system_prompt: str) -> str:
        """Wrapper for Stage 1 Gemini analysis"""
        try:
            files = []  # Extract from context
            results = self.pipeline_stages.stage_1_gemini_analysis(files)
            return str(results)
        except Exception as e:
            logger.error(f"Stage 1 failed: {e}")
            return f"Stage 1 analysis failed: {e}"
    
    def _stage_2_wrapper(self, prompt: str, system_prompt: str) -> str:
        """Wrapper for Stage 2 ChatGPT generation"""
        try:
            # Get analysis results from memory
            analysis_results = {}
            original_files = []
            results = self.pipeline_stages.stage_2_chatgpt_generation(analysis_results, original_files)
            return str(results)
        except Exception as e:
            logger.error(f"Stage 2 failed: {e}")
            return f"Stage 2 generation failed: {e}"
    
    def _stage_3_wrapper(self, prompt: str, system_prompt: str) -> str:
        """Wrapper for Stage 3 Claude integration"""
        try:
            generated_code = {}
            original_files = []
            results = self.pipeline_stages.stage_3_claude_integration(generated_code, original_files)
            return str(results)
        except Exception as e:
            logger.error(f"Stage 3 failed: {e}")
            return f"Stage 3 integration failed: {e}"
    
    def _stage_4_wrapper(self, prompt: str, system_prompt: str) -> str:
        """Wrapper for Stage 4 DeepSeek verification"""
        try:
            integrated_code = {}
            results = self.pipeline_stages.stage_4_deepseek_verification(integrated_code)
            return str(results)
        except Exception as e:
            logger.error(f"Stage 4 failed: {e}")
            return f"Stage 4 verification failed: {e}"
    
    # Retry Handlers
    def _handle_analysis_retry(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle analysis retry logic"""
        retry_count = data.get('analysis_retry_count', 0) + 1
        data['analysis_retry_count'] = retry_count
        
        if retry_count > 3:
            logger.error("Analysis retry limit exceeded")
            data['analysis_failed'] = True
            return data
        
        logger.info(f"Retrying analysis (attempt {retry_count})")
        # Adjust prompts for retry
        data['retry_mode'] = True
        return data
    
    def _handle_generation_retry(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle generation retry logic"""
        retry_count = data.get('generation_retry_count', 0) + 1
        data['generation_retry_count'] = retry_count
        
        if retry_count > 3:
            logger.error("Generation retry limit exceeded")
            data['generation_failed'] = True
            return data
        
        logger.info(f"Retrying generation (attempt {retry_count})")
        return data
    
    def _handle_early_exit(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle early exit scenario"""
        logger.info("Early exit triggered - quality gate not met")
        data['early_exit'] = True
        data['exit_reason'] = data.get('quality_gate_reason', 'Quality gate not met')
        return data
    
    def _generate_final_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive final report"""
        try:
            # Collect all pipeline results
            pipeline_results = {
                'stage_1_results': data.get('stage_1_gemini_response', {}),
                'stage_2_results': data.get('stage_2_chatgpt_response', {}),
                'stage_3_results': data.get('stage_3_claude_response', {}),
                'stage_4_results': data.get('stage_4_deepseek_response', {}),
                'files_analyzed': data.get('files_count', 0),
                'pipeline_success': data.get('pipeline_success', False),
                'session_id': data.get('session_id', self.session_id)
            }
            
            report = self.report_generator.generate_comprehensive_report(pipeline_results)
            data['final_report'] = report
            
            logger.info("Final report generated successfully")
            return data
            
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            data['report_error'] = str(e)
            return data
    
    def _post_to_github(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Post results to GitHub"""
        try:
            pr_number = data.get('pr_number')
            report = data.get('final_report', '')
            
            if not self.demo_mode and self.github_manager and pr_number and report:
                success = self.github_manager.post_comment(pr_number, report)
                data['github_posted'] = success
                
                if success:
                    logger.info(f"Results posted to GitHub PR #{pr_number}")
                else:
                    logger.error("Failed to post to GitHub")
            else:
                logger.info("Demo mode - report generated without GitHub posting")
                data['github_posted'] = False
                data['demo_mode'] = True
            
            return data
            
        except Exception as e:
            logger.error(f"GitHub posting failed: {e}")
            data['github_error'] = str(e)
            return data
    
    async def run_advanced_pipeline(self, pr_number: Optional[int] = None) -> Dict[str, Any]:
        """Run the advanced multi-LLM pipeline with workflow orchestration"""
        
        # Create initial context
        context = WorkflowContext(
            data={
                'pr_number': pr_number,
                'session_id': self.session_id,
                'start_time': time.time(),
                'project_type': self.prompt_config.config.get('active_project_type', 'general')
            },
            metadata={
                'pipeline_version': '2.0.0',
                'workflow_enabled': True,
                'advanced_features': True
            },
            session_id=self.session_id,
            execution_id=f"exec_{int(time.time())}",
            timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"Starting advanced pipeline execution (session: {self.session_id})")
        
        try:
            # Execute the workflow
            final_context = await self.orchestrator.execute_workflow(
                start_node="file_retrieval",
                initial_context=context,
                max_steps=20
            )
            
            # Extract results
            results = {
                'success': not final_context.data.get('error'),
                'session_id': self.session_id,
                'execution_time': time.time() - context.data['start_time'],
                'files_analyzed': final_context.data.get('files_count', 0),
                'pipeline_success': final_context.data.get('pipeline_success', False),
                'github_posted': final_context.data.get('github_posted', False),
                'report': final_context.data.get('final_report', ''),
                'workflow_stats': self.orchestrator.get_workflow_stats(),
                'memory_usage': len(self.orchestrator.memory.memory)
            }
            
            logger.info(f"Advanced pipeline completed successfully in {results['execution_time']:.2f}s")
            return results
            
        except Exception as e:
            logger.error(f"Advanced pipeline failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'session_id': self.session_id,
                'workflow_stats': self.orchestrator.get_workflow_stats()
            }
    
    def get_workflow_visualization(self) -> str:
        """Get workflow visualization"""
        return self.orchestrator.visualize_workflow()
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get workflow execution history"""
        return self.orchestrator.get_execution_history()
    
    def export_workflow_config(self, filename: str):
        """Export workflow configuration"""
        self.orchestrator.export_workflow(filename)
    
    def clear_workflow_memory(self):
        """Clear workflow memory"""
        self.orchestrator.memory.clear()
        logger.info("Workflow memory cleared")


# Demo function for advanced pipeline
async def demo_advanced_pipeline():
    """Demonstrate the advanced pipeline with workflow orchestration"""
    print("=" * 80)
    print("Advanced Multi-LLM Pipeline with Workflow Orchestration")
    print("=" * 80)
    
    try:
        # Initialize advanced pipeline in demo mode
        pipeline = AdvancedMultiLLMPipeline(demo_mode=True)
        
        print("\n1. Workflow Visualization:")
        print("-" * 40)
        print(pipeline.get_workflow_visualization())
        
        print("\n2. Running Advanced Pipeline (Demo Mode):")
        print("-" * 40)
        
        # Run pipeline in demo mode
        results = await pipeline.run_advanced_pipeline(pr_number=None)
        
        print(f"\nExecution Results:")
        print(f"Success: {results['success']}")
        print(f"Execution Time: {results['execution_time']:.2f}s")
        print(f"Files Analyzed: {results['files_analyzed']}")
        print(f"Pipeline Success: {results['pipeline_success']}")
        print(f"Memory Usage: {results['memory_usage']} entries")
        
        print(f"\nWorkflow Statistics:")
        stats = results['workflow_stats']
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        print("\n3. Execution History:")
        print("-" * 40)
        history = pipeline.get_execution_history()
        for execution in history[-3:]:  # Show last 3 executions
            print(f"Execution {execution['execution_id']}: {execution['status']}")
            if 'total_duration' in execution:
                print(f"  Duration: {execution['total_duration']:.2f}s")
            print(f"  Steps: {len(execution.get('steps', []))}")
        
        print("\n" + "=" * 80)
        print("Advanced Pipeline Demo Complete!")
        print("=" * 80)
        
    except Exception as e:
        print(f"Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(demo_advanced_pipeline())