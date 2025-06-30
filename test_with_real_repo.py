#!/usr/bin/env python3
"""
Test Multi-LLM Pipeline with Real Repository Content
"""

import os
import sys
import logging
from typing import Dict, Any, List

from pipeline_stages import PipelineStages
from report_generator import ReportGenerator
from security_utils import SecurityUtils

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_sample_ai_code() -> List[Dict[str, Any]]:
    """Create sample AI/ML code files typical for JanusAI project"""
    
    sample_files = [
        {
            'path': 'src/ppo_trainer.py',
            'content': '''import torch
import torch.nn as nn
import numpy as np
from typing import Dict, List, Optional

class PPOTrainer:
    def __init__(self, policy_net, value_net, lr=3e-4):
        self.policy_net = policy_net
        self.value_net = value_net
        self.optimizer = torch.optim.Adam(
            list(policy_net.parameters()) + list(value_net.parameters()), 
            lr=lr
        )
        
    def compute_advantages(self, rewards, values, dones, gamma=0.99, lam=0.95):
        advantages = []
        last_advantage = 0
        
        for t in reversed(range(len(rewards))):
            if t == len(rewards) - 1:
                next_value = 0
            else:
                next_value = values[t + 1]
            
            delta = rewards[t] + gamma * next_value * (1 - dones[t]) - values[t]
            advantage = delta + gamma * lam * (1 - dones[t]) * last_advantage
            advantages.insert(0, advantage)
            last_advantage = advantage
            
        return advantages
    
    def update_policy(self, states, actions, old_log_probs, advantages, clip_ratio=0.2):
        # PPO policy update - potential issues with tensor shapes
        new_log_probs = self.policy_net.get_log_prob(states, actions)
        ratio = torch.exp(new_log_probs - old_log_probs)
        
        surr1 = ratio * advantages
        surr2 = torch.clamp(ratio, 1 - clip_ratio, 1 + clip_ratio) * advantages
        policy_loss = -torch.min(surr1, surr2).mean()
        
        # No gradient clipping - could cause instability
        self.optimizer.zero_grad()
        policy_loss.backward()
        self.optimizer.step()
        
        return policy_loss.item()''',
            'status': 'modified',
            'additions': 45,
            'deletions': 0
        },
        {
            'path': 'src/neural_network.py', 
            'content': '''import torch
import torch.nn as nn
import torch.nn.functional as F

class PolicyNetwork(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        # No input validation
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, output_dim)
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x):
        # Potential numerical instability
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return F.softmax(x, dim=-1)  # Could cause vanishing gradients
    
    def get_log_prob(self, states, actions):
        logits = self.forward(states)
        # No numerical stability checks
        log_probs = torch.log(logits)
        action_log_probs = log_probs.gather(1, actions.unsqueeze(1))
        return action_log_probs.squeeze()

class ValueNetwork(nn.Module):
    def __init__(self, input_dim, hidden_dim=128):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(), 
            nn.Linear(hidden_dim, 1)
        )
    
    def forward(self, x):
        return self.network(x).squeeze()
        
def create_networks(state_dim, action_dim, hidden_dim=256):
    policy = PolicyNetwork(state_dim, hidden_dim, action_dim)
    value = ValueNetwork(state_dim, hidden_dim)
    return policy, value''',
            'status': 'added',
            'additions': 50,
            'deletions': 0
        },
        {
            'path': 'src/data_handler.py',
            'content': '''import json
import pickle
import os
from typing import Any, Dict, List

def save_model_data(data, filename):
    # No error handling or path validation
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def load_config(config_path):
    # No file existence check
    with open(config_path, 'r') as f:
        return json.load(f)

def process_training_data(raw_data):
    # No input validation
    processed = []
    for item in raw_data:
        # Potential KeyError if 'state' missing
        state = item['state']
        action = item['action'] 
        reward = item['reward']
        
        # No bounds checking
        normalized_state = [x / 255.0 for x in state]
        processed.append({
            'state': normalized_state,
            'action': action,
            'reward': reward
        })
    
    return processed

class DataManager:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        # No directory validation
        
    def save_episode(self, episode_data, episode_id):
        filepath = os.path.join(self.data_dir, f"episode_{episode_id}.pkl")
        save_model_data(episode_data, filepath)
        
    def load_all_episodes(self):
        episodes = []
        # Could crash if directory doesn't exist
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.pkl'):
                filepath = os.path.join(self.data_dir, filename)
                with open(filepath, 'rb') as f:
                    episodes.append(pickle.load(f))
        return episodes''',
            'status': 'modified',
            'additions': 42,
            'deletions': 5
        }
    ]
    
    return sample_files

def main():
    print("="*80)
    print("Testing Multi-LLM Pipeline with JanusAI-style Code")
    print("="*80)
    
    try:
        # Initialize pipeline components
        pipeline_stages = PipelineStages()
        report_generator = ReportGenerator()
        
        # Create sample AI/ML code files
        sample_files = create_sample_ai_code()
        print(f"Created {len(sample_files)} AI/ML code files for analysis")
        
        # Run Stage 1: Gemini Analysis
        print("\n🔍 Stage 1: Gemini Analysis - Analyzing AI/ML code...")
        analysis_results = pipeline_stages.stage_1_gemini_analysis(sample_files)
        
        # Count issues found
        total_issues = 0
        for file_path, result in analysis_results.items():
            if result.get('status') == 'completed':
                issues = result.get('analysis', {}).get('issues', [])
                total_issues += len(issues)
                print(f"  - {file_path}: {len(issues)} issues found")
        
        print(f"Total issues identified: {total_issues}")
        
        # Run Stage 2: ChatGPT Generation
        print("\n🛠️ Stage 2: ChatGPT Generation - Generating improvements...")
        generation_results = pipeline_stages.stage_2_chatgpt_generation(analysis_results, sample_files)
        
        improved_files = sum(1 for r in generation_results.values() if r.get('status') == 'completed')
        print(f"Successfully improved {improved_files} files")
        
        # Run Stage 3: Claude Integration  
        print("\n🔗 Stage 3: Claude Integration - Integrating improvements...")
        integration_results = pipeline_stages.stage_3_claude_integration(generation_results, sample_files)
        
        integrated_files = sum(1 for r in integration_results.values() if r.get('status') == 'completed')
        print(f"Successfully integrated {integrated_files} files")
        
        # Run Stage 4: DeepSeek Verification
        print("\n✅ Stage 4: DeepSeek Verification - Final quality check...")
        verification_results = pipeline_stages.stage_4_deepseek_verification(integration_results)
        
        passed_verification = sum(1 for r in verification_results.values() if r.get('verification_passed', False))
        print(f"Verification passed: {passed_verification}/{len(verification_results)} files")
        
        # Generate final report
        print("\n📋 Generating comprehensive report...")
        pipeline_results = {
            'stage_1': analysis_results,
            'stage_2': generation_results, 
            'stage_3': integration_results,
            'stage_4': verification_results
        }
        
        final_report = report_generator.generate_comprehensive_report(pipeline_results)
        
        print("\n" + "="*80)
        print("MULTI-LLM PIPELINE RESULTS FOR JANUSAI_V2")
        print("="*80)
        print(final_report)
        print("="*80)
        print("✅ Pipeline test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()