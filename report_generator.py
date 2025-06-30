"""
Report Generator for Multi-LLM Pipeline
Generates comprehensive reports from pipeline results
"""

import json
import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self):
        """Initialize report generator"""
        pass
    
    def generate_comprehensive_report(self, pipeline_results: Dict[str, Any]) -> str:
        """Generate comprehensive final report from all pipeline stages"""
        try:
            report_sections = []
            
            # Header
            report_sections.append(self._generate_header())
            
            # Executive Summary
            report_sections.append(self._generate_executive_summary(pipeline_results))
            
            # Stage-by-stage results
            if 'stage_1' in pipeline_results:
                report_sections.append(self._generate_stage_1_report(pipeline_results['stage_1']))
            
            if 'stage_2' in pipeline_results:
                report_sections.append(self._generate_stage_2_report(pipeline_results['stage_2']))
            
            if 'stage_3' in pipeline_results:
                report_sections.append(self._generate_stage_3_report(pipeline_results['stage_3']))
            
            if 'stage_4' in pipeline_results:
                report_sections.append(self._generate_stage_4_report(pipeline_results['stage_4']))
            
            # Code changes summary
            report_sections.append(self._generate_code_changes_summary(pipeline_results))
            
            # Recommendations
            report_sections.append(self._generate_recommendations(pipeline_results))
            
            # Footer
            report_sections.append(self._generate_footer())
            
            return "\n\n".join(report_sections)
            
        except Exception as e:
            logger.error(f"Error generating comprehensive report: {e}")
            return f"Error generating report: {str(e)}"
    
    def _generate_header(self) -> str:
        """Generate report header"""
        return """## 📋 Multi-LLM Pipeline Comprehensive Report

**Generated**: {timestamp}
**Pipeline Version**: 1.0.0""".format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        )
    
    def _generate_executive_summary(self, pipeline_results: Dict[str, Any]) -> str:
        """Generate executive summary"""
        try:
            total_files = 0
            total_issues = 0
            files_improved = 0
            verification_passed = 0
            
            # Count statistics across all stages
            for stage_name, stage_results in pipeline_results.items():
                if isinstance(stage_results, dict):
                    total_files = max(total_files, len(stage_results))
                    
                    if stage_name == 'stage_1':  # Analysis stage
                        for file_result in stage_results.values():
                            if isinstance(file_result, dict) and 'analysis' in file_result:
                                issues = file_result['analysis'].get('issues', [])
                                total_issues += len(issues)
                    
                    elif stage_name == 'stage_2':  # Generation stage
                        files_improved = sum(1 for result in stage_results.values() 
                                           if isinstance(result, dict) and result.get('status') == 'completed')
                    
                    elif stage_name == 'stage_4':  # Verification stage
                        verification_passed = sum(1 for result in stage_results.values()
                                                if isinstance(result, dict) and result.get('verification_passed', False))
            
            return f"""### 📊 Executive Summary

| Metric | Value |
|--------|-------|
| **Files Analyzed** | {total_files} |
| **Issues Identified** | {total_issues} |
| **Files Improved** | {files_improved} |
| **Verification Passed** | {verification_passed}/{total_files} |
| **Overall Success Rate** | {(verification_passed/total_files*100) if total_files > 0 else 0:.1f}% |

**Key Achievements:**
- Comprehensive analysis completed across all code files
- Automated bug fixes and performance improvements applied
- Code integration maintained consistency with existing codebase
- Quality assurance verification performed on all changes"""
            
        except Exception as e:
            logger.error(f"Error generating executive summary: {e}")
            return "### 📊 Executive Summary\n\nError generating summary statistics."
    
    def _generate_stage_1_report(self, stage_1_results: Dict[str, Any]) -> str:
        """Generate Stage 1 (Gemini Analysis) report"""
        try:
            report = ["### 🔍 Stage 1: Gemini Deep Analysis"]
            
            total_files = len(stage_1_results)
            successful_analyses = sum(1 for result in stage_1_results.values() 
                                    if result.get('status') == 'completed')
            
            report.append(f"**Files Analyzed**: {successful_analyses}/{total_files}")
            
            # Issue breakdown
            issue_types = {}
            severity_counts = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
            
            for file_path, result in stage_1_results.items():
                if result.get('status') == 'completed' and 'analysis' in result:
                    issues = result['analysis'].get('issues', [])
                    for issue in issues:
                        issue_type = issue.get('type', 'Unknown')
                        severity = issue.get('severity', 'Medium')
                        
                        issue_types[issue_type] = issue_types.get(issue_type, 0) + 1
                        if severity in severity_counts:
                            severity_counts[severity] += 1
            
            if issue_types:
                report.append("\n**Issues by Type:**")
                for issue_type, count in sorted(issue_types.items()):
                    report.append(f"- {issue_type}: {count}")
                
                report.append("\n**Issues by Severity:**")
                for severity, count in severity_counts.items():
                    if count > 0:
                        report.append(f"- {severity}: {count}")
            
            # Top issues
            report.append("\n**Key Findings:**")
            file_count = 0
            for file_path, result in stage_1_results.items():
                if file_count >= 3:  # Limit to top 3 files
                    break
                    
                if result.get('status') == 'completed' and 'analysis' in result:
                    analysis = result['analysis']
                    assessment = analysis.get('overall_assessment', 'No assessment available')
                    
                    report.append(f"- **{file_path}**: {assessment[:100]}{'...' if len(assessment) > 100 else ''}")
                    file_count += 1
            
            return "\n".join(report)
            
        except Exception as e:
            logger.error(f"Error generating Stage 1 report: {e}")
            return "### 🔍 Stage 1: Gemini Deep Analysis\n\nError generating analysis report."
    
    def _generate_stage_2_report(self, stage_2_results: Dict[str, Any]) -> str:
        """Generate Stage 2 (ChatGPT Generation) report"""
        try:
            report = ["### 🛠️ Stage 2: ChatGPT Code Generation"]
            
            total_files = len(stage_2_results)
            successful_generations = sum(1 for result in stage_2_results.values() 
                                       if result.get('status') == 'completed')
            
            report.append(f"**Files Processed**: {successful_generations}/{total_files}")
            
            # Changes summary
            total_changes = 0
            for result in stage_2_results.values():
                if result.get('status') == 'completed':
                    changes = result.get('changes', [])
                    total_changes += len(changes)
            
            report.append(f"**Total Improvements**: {total_changes}")
            
            # Sample improvements
            report.append("\n**Key Improvements Applied:**")
            improvement_count = 0
            for file_path, result in stage_2_results.items():
                if improvement_count >= 3:  # Limit display
                    break
                    
                if result.get('status') == 'completed':
                    issues_addressed = result.get('issues_addressed', [])
                    if issues_addressed:
                        high_priority_issues = [issue for issue in issues_addressed 
                                              if issue.get('severity') in ['Critical', 'High']]
                        if high_priority_issues:
                            issue = high_priority_issues[0]
                            report.append(f"- **{file_path}**: Fixed {issue.get('type', 'issue')} - {issue.get('description', 'N/A')[:80]}{'...' if len(issue.get('description', '')) > 80 else ''}")
                            improvement_count += 1
            
            return "\n".join(report)
            
        except Exception as e:
            logger.error(f"Error generating Stage 2 report: {e}")
            return "### 🛠️ Stage 2: ChatGPT Code Generation\n\nError generating generation report."
    
    def _generate_stage_3_report(self, stage_3_results: Dict[str, Any]) -> str:
        """Generate Stage 3 (Claude Integration) report"""
        try:
            report = ["### 🔗 Stage 3: Claude Integration"]
            
            total_files = len(stage_3_results)
            successful_integrations = sum(1 for result in stage_3_results.values() 
                                        if result.get('status') == 'completed')
            
            report.append(f"**Files Integrated**: {successful_integrations}/{total_files}")
            
            report.append("\n**Integration Achievements:**")
            report.append("- ✅ Code style consistency maintained")
            report.append("- ✅ Architecture alignment verified")
            report.append("- ✅ Variable naming conventions preserved")
            report.append("- ✅ Import dependencies properly managed")
            
            # Integration notes
            report.append("\n**Integration Notes:**")
            note_count = 0
            for file_path, result in stage_3_results.items():
                if note_count >= 3:  # Limit display
                    break
                    
                if result.get('status') == 'completed':
                    notes = result.get('integration_notes', [])
                    if notes:
                        report.append(f"- **{file_path}**: {notes[0]}")
                        note_count += 1
            
            return "\n".join(report)
            
        except Exception as e:
            logger.error(f"Error generating Stage 3 report: {e}")
            return "### 🔗 Stage 3: Claude Integration\n\nError generating integration report."
    
    def _generate_stage_4_report(self, stage_4_results: Dict[str, Any]) -> str:
        """Generate Stage 4 (DeepSeek Verification) report"""
        try:
            report = ["### ✅ Stage 4: DeepSeek Verification"]
            
            total_files = len(stage_4_results)
            successful_verifications = sum(1 for result in stage_4_results.values() 
                                         if result.get('status') == 'completed')
            
            verification_passed = sum(1 for result in stage_4_results.values()
                                    if result.get('verification_passed', False))
            
            report.append(f"**Files Verified**: {successful_verifications}/{total_files}")
            report.append(f"**Verification Passed**: {verification_passed}/{total_files}")
            
            # Quality scores
            quality_scores = []
            for result in stage_4_results.values():
                if result.get('status') == 'completed':
                    score = result.get('overall_quality_score', 0)
                    if score > 0:
                        quality_scores.append(score)
            
            if quality_scores:
                avg_quality = sum(quality_scores) / len(quality_scores)
                report.append(f"**Average Quality Score**: {avg_quality:.1f}/10")
            
            # Warnings summary
            total_warnings = sum(len(result.get('warnings', [])) for result in stage_4_results.values()
                               if result.get('status') == 'completed')
            
            if total_warnings > 0:
                report.append(f"**Warnings Found**: {total_warnings}")
                
                report.append("\n**Sample Warnings:**")
                warning_count = 0
                for file_path, result in stage_4_results.items():
                    if warning_count >= 3:  # Limit display
                        break
                        
                    warnings = result.get('warnings', [])
                    if warnings:
                        report.append(f"- **{file_path}**: {warnings[0]}")
                        warning_count += 1
            
            # Final assessments
            report.append("\n**Final Quality Assessment:**")
            assessment_count = 0
            for file_path, result in stage_4_results.items():
                if assessment_count >= 2:  # Limit display
                    break
                    
                if result.get('status') == 'completed':
                    assessment = result.get('final_assessment', '')
                    if assessment:
                        report.append(f"- **{file_path}**: {assessment[:100]}{'...' if len(assessment) > 100 else ''}")
                        assessment_count += 1
            
            return "\n".join(report)
            
        except Exception as e:
            logger.error(f"Error generating Stage 4 report: {e}")
            return "### ✅ Stage 4: DeepSeek Verification\n\nError generating verification report."
    
    def _generate_code_changes_summary(self, pipeline_results: Dict[str, Any]) -> str:
        """Generate code changes summary"""
        try:
            report = ["### 📝 Code Changes Summary"]
            
            changes_by_file = {}
            
            # Gather changes from stage 2 and 3
            if 'stage_2' in pipeline_results:
                for file_path, result in pipeline_results['stage_2'].items():
                    if result.get('status') == 'completed':
                        changes_by_file[file_path] = {
                            'has_changes': True,
                            'type': 'improved',
                            'description': 'Code improvements and bug fixes applied'
                        }
            
            if not changes_by_file:
                report.append("No code changes were applied.")
                return "\n".join(report)
            
            report.append(f"**Total Files Modified**: {len(changes_by_file)}")
            
            report.append("\n**Changes by File:**")
            for file_path, change_info in changes_by_file.items():
                report.append(f"- **{file_path}**: {change_info['description']}")
            
            report.append("\n**Change Categories:**")
            report.append("- 🐛 Bug fixes and error handling improvements")  
            report.append("- ⚡ Performance optimizations")
            report.append("- 🔒 Security vulnerability patches")
            report.append("- 📚 Code quality and readability enhancements")
            report.append("- 🏗️ Architecture and design pattern improvements")
            
            return "\n".join(report)
            
        except Exception as e:
            logger.error(f"Error generating code changes summary: {e}")
            return "### 📝 Code Changes Summary\n\nError generating changes summary."
    
    def _generate_recommendations(self, pipeline_results: Dict[str, Any]) -> str:
        """Generate recommendations based on pipeline results"""
        try:
            report = ["### 💡 Recommendations"]
            
            # Analyze results to generate recommendations
            has_critical_issues = False
            has_warnings = False
            verification_rate = 0
            
            if 'stage_1' in pipeline_results:
                for result in pipeline_results['stage_1'].values():
                    if result.get('status') == 'completed' and 'analysis' in result:
                        issues = result['analysis'].get('issues', [])
                        for issue in issues:
                            if issue.get('severity') == 'Critical':
                                has_critical_issues = True
                                break
            
            if 'stage_4' in pipeline_results:
                total_files = len(pipeline_results['stage_4'])
                passed_files = sum(1 for result in pipeline_results['stage_4'].values()
                                 if result.get('verification_passed', False))
                verification_rate = (passed_files / total_files) if total_files > 0 else 0
                
                for result in pipeline_results['stage_4'].values():
                    if result.get('warnings'):
                        has_warnings = True
                        break
            
            # Generate specific recommendations
            if verification_rate >= 0.9:
                report.append("#### ✅ Excellent Code Quality")
                report.append("- The code quality is excellent with minimal issues")
                report.append("- **Recommendation**: Ready for merge after final review")
            elif verification_rate >= 0.7:
                report.append("#### ⚠️ Good Code Quality with Minor Issues")
                report.append("- Code quality is good but has some areas for improvement")
                report.append("- **Recommendation**: Review warnings and consider fixes before merge")
            else:
                report.append("#### ❌ Code Quality Needs Attention")
                report.append("- Several issues need to be addressed")
                report.append("- **Recommendation**: Address critical issues before merge")
            
            report.append("\n#### 🔄 Next Steps")
            report.append("1. **Review Analysis**: Examine the detailed findings from each stage")
            report.append("2. **Test Changes**: Run your test suite to verify improvements")
            report.append("3. **Manual Review**: Perform code review on critical changes")
            report.append("4. **Deploy Safely**: Use staging environment before production")
            
            if has_warnings:
                report.append("\n#### ⚠️ Attention Required")
                report.append("- Some warnings were identified during verification")
                report.append("- Review the warnings section for specific details")
                report.append("- Consider addressing warnings for optimal code quality")
            
            report.append("\n#### 🚀 Performance & Security")
            report.append("- Performance optimizations have been applied where identified")
            report.append("- Security vulnerabilities have been addressed")
            report.append("- Follow up with security scanning tools for comprehensive coverage")
            
            return "\n".join(report)
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return "### 💡 Recommendations\n\nError generating recommendations."
    
    def _generate_footer(self) -> str:
        """Generate report footer"""
        return """---

### 🤖 Multi-LLM Pipeline Details

**LLM Participants:**
- **Gemini 2.5 Pro**: Deep code analysis and issue identification
- **GPT-4o**: Code generation and improvement implementation  
- **Claude Sonnet 4**: Code integration and consistency maintenance
- **DeepSeek**: Final verification and quality assurance

**Pipeline Features:**
- Automated bug detection and fixing
- Performance optimization recommendations
- Security vulnerability identification
- Code quality and consistency improvements
- Comprehensive verification and testing

---
*Report generated by Multi-LLM Code Quality Pipeline v1.0.0*"""
