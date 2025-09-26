"""
Agent Configuration System

This module provides configuration and selection capabilities for AI agents in the Web Knowledge System.
Allows users to select which agent teams and individual agents to use in workflows.
"""

from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass
from enum import Enum
import json
import os

class AgentTeam(Enum):
    """Enumeration of available agent teams"""
    RESEARCH_ANALYSIS = "research_analysis"
    DATA_STRATEGY = "data_strategy"
    COMPLIANCE_RISK = "compliance_risk"
    INFORMATION_MANAGEMENT = "information_management"
    TENDER_RESPONSE = "tender_response"
    PROJECT_DELIVERY = "project_delivery"
    TECHNICAL_DOCUMENTATION = "technical_documentation"

@dataclass
class AgentInfo:
    """Information about a specific agent"""
    name: str
    role: str
    team: AgentTeam
    description: str
    enabled: bool = True

@dataclass
class TeamInfo:
    """Information about an agent team"""
    name: str
    team: AgentTeam
    agents: List[AgentInfo]
    description: str
    enabled: bool = True
    order: int = 0  # Order in workflow execution

class AgentConfiguration:
    """Manages agent selection and configuration"""
    
    def __init__(self):
        self.teams = self._initialize_teams()
        self.config_file = "agent_config.json"
        self.load_config()
    
    def _initialize_teams(self) -> Dict[AgentTeam, TeamInfo]:
        """Initialize all available agent teams with their agents"""
        
        teams = {}
        
        # Research & Analysis Team
        teams[AgentTeam.RESEARCH_ANALYSIS] = TeamInfo(
            name="Research & Analysis",
            team=AgentTeam.RESEARCH_ANALYSIS,
            description="Core research, analysis, and content creation capabilities",
            order=1,
            agents=[
                AgentInfo(
                    name="research_specialist",
                    role="Research Specialist",
                    team=AgentTeam.RESEARCH_ANALYSIS,
                    description="Conducts comprehensive research and gathers relevant information"
                ),
                AgentInfo(
                    name="data_analyst",
                    role="Data Analyst",
                    team=AgentTeam.RESEARCH_ANALYSIS,
                    description="Analyzes data and provides insights"
                ),
                AgentInfo(
                    name="content_writer",
                    role="Content Writer",
                    team=AgentTeam.RESEARCH_ANALYSIS,
                    description="Creates well-structured content and reports"
                )
            ]
        )
        
        # Data Strategy Team
        teams[AgentTeam.DATA_STRATEGY] = TeamInfo(
            name="Data Strategy",
            team=AgentTeam.DATA_STRATEGY,
            description="DAMA-DMBOK frameworks and data governance structures",
            order=2,
            agents=[
                AgentInfo(
                    name="data_governance_specialist",
                    role="Data Governance Specialist",
                    team=AgentTeam.DATA_STRATEGY,
                    description="Creates comprehensive DAMA-DMBOK frameworks"
                ),
                AgentInfo(
                    name="dcam_template_specialist",
                    role="DCAM Template Specialist",
                    team=AgentTeam.DATA_STRATEGY,
                    description="Develops DCAM templates and data architecture"
                ),
                AgentInfo(
                    name="tranch_guidance_specialist",
                    role="Tranch Guidance Specialist",
                    team=AgentTeam.DATA_STRATEGY,
                    description="Provides tranch implementation guidance"
                )
            ]
        )
        
        # Compliance & Risk Team
        teams[AgentTeam.COMPLIANCE_RISK] = TeamInfo(
            name="Compliance & Risk",
            team=AgentTeam.COMPLIANCE_RISK,
            description="Compliance frameworks and risk management",
            order=3,
            agents=[
                AgentInfo(
                    name="compliance_specialist",
                    role="Compliance Specialist",
                    team=AgentTeam.COMPLIANCE_RISK,
                    description="Ensures regulatory compliance and standards"
                ),
                AgentInfo(
                    name="risk_management_specialist",
                    role="Risk Management Specialist",
                    team=AgentTeam.COMPLIANCE_RISK,
                    description="Identifies and manages risks"
                ),
                AgentInfo(
                    name="audit_governance_specialist",
                    role="Audit Governance Specialist",
                    team=AgentTeam.COMPLIANCE_RISK,
                    description="Provides audit and governance frameworks"
                )
            ]
        )
        
        # Information Management Team
        teams[AgentTeam.INFORMATION_MANAGEMENT] = TeamInfo(
            name="Information Management",
            team=AgentTeam.INFORMATION_MANAGEMENT,
            description="Information governance and metadata management",
            order=4,
            agents=[
                AgentInfo(
                    name="information_governance_specialist",
                    role="Information Governance Specialist",
                    team=AgentTeam.INFORMATION_MANAGEMENT,
                    description="Manages information governance frameworks"
                ),
                AgentInfo(
                    name="metadata_management_specialist",
                    role="Metadata Management Specialist",
                    team=AgentTeam.INFORMATION_MANAGEMENT,
                    description="Handles metadata standards and management"
                ),
                AgentInfo(
                    name="data_quality_specialist",
                    role="Data Quality Specialist",
                    team=AgentTeam.INFORMATION_MANAGEMENT,
                    description="Ensures data quality and integrity"
                )
            ]
        )
        
        # Tender Response Team
        teams[AgentTeam.TENDER_RESPONSE] = TeamInfo(
            name="Tender Response",
            team=AgentTeam.TENDER_RESPONSE,
            description="Tender analysis and proposal development",
            order=5,
            agents=[
                AgentInfo(
                    name="tender_specialist",
                    role="Tender Response Specialist",
                    team=AgentTeam.TENDER_RESPONSE,
                    description="Analyzes tender requirements and creates response strategies"
                ),
                AgentInfo(
                    name="proposal_writer",
                    role="Proposal Writer",
                    team=AgentTeam.TENDER_RESPONSE,
                    description="Creates compelling tender responses and proposals"
                ),
                AgentInfo(
                    name="compliance_expert",
                    role="Tender Compliance Expert",
                    team=AgentTeam.TENDER_RESPONSE,
                    description="Ensures tender compliance with procurement standards"
                )
            ]
        )
        
        # Project Delivery Team
        teams[AgentTeam.PROJECT_DELIVERY] = TeamInfo(
            name="Project Delivery",
            team=AgentTeam.PROJECT_DELIVERY,
            description="Technical implementation and project management",
            order=6,
            agents=[
                AgentInfo(
                    name="data_engineer",
                    role="Data Engineer",
                    team=AgentTeam.PROJECT_DELIVERY,
                    description="Designs and implements data engineering solutions"
                ),
                AgentInfo(
                    name="data_scientist",
                    role="Data Scientist",
                    team=AgentTeam.PROJECT_DELIVERY,
                    description="Develops data science models and analytics"
                ),
                AgentInfo(
                    name="data_architect",
                    role="Data Architect",
                    team=AgentTeam.PROJECT_DELIVERY,
                    description="Designs data architecture and technical solutions"
                ),
                AgentInfo(
                    name="devops_engineer",
                    role="DevOps Engineer",
                    team=AgentTeam.PROJECT_DELIVERY,
                    description="Manages deployment and infrastructure"
                ),
                AgentInfo(
                    name="project_manager",
                    role="Project Manager",
                    team=AgentTeam.PROJECT_DELIVERY,
                    description="Oversees project delivery and coordination"
                )
            ]
        )
        
        # Technical Documentation Team
        teams[AgentTeam.TECHNICAL_DOCUMENTATION] = TeamInfo(
            name="Technical Documentation",
            team=AgentTeam.TECHNICAL_DOCUMENTATION,
            description="Technical documentation and knowledge management",
            order=7,
            agents=[
                AgentInfo(
                    name="technical_writer",
                    role="Technical Writer",
                    team=AgentTeam.TECHNICAL_DOCUMENTATION,
                    description="Creates technical documentation and guides"
                ),
                AgentInfo(
                    name="knowledge_manager",
                    role="Knowledge Manager",
                    team=AgentTeam.TECHNICAL_DOCUMENTATION,
                    description="Manages knowledge repositories and documentation"
                ),
                AgentInfo(
                    name="quality_assurance_specialist",
                    role="Quality Assurance Specialist",
                    team=AgentTeam.TECHNICAL_DOCUMENTATION,
                    description="Ensures documentation quality and standards"
                )
            ]
        )
        
        return teams
    
    def get_available_teams(self) -> List[TeamInfo]:
        """Get all available teams"""
        return list(self.teams.values())
    
    def get_enabled_teams(self) -> List[TeamInfo]:
        """Get only enabled teams"""
        return [team for team in self.teams.values() if team.enabled]
    
    def get_team_by_name(self, team_name: str) -> Optional[TeamInfo]:
        """Get team by name"""
        for team in self.teams.values():
            if team.name.lower() == team_name.lower():
                return team
        return None
    
    def enable_team(self, team: AgentTeam) -> bool:
        """Enable a team"""
        if team in self.teams:
            self.teams[team].enabled = True
            self.save_config()
            return True
        return False
    
    def disable_team(self, team: AgentTeam) -> bool:
        """Disable a team"""
        if team in self.teams:
            self.teams[team].enabled = False
            self.save_config()
            return True
        return False
    
    def enable_agent(self, team: AgentTeam, agent_name: str) -> bool:
        """Enable a specific agent within a team"""
        if team in self.teams:
            for agent in self.teams[team].agents:
                if agent.name == agent_name:
                    agent.enabled = True
                    self.save_config()
                    return True
        return False
    
    def disable_agent(self, team: AgentTeam, agent_name: str) -> bool:
        """Disable a specific agent within a team"""
        if team in self.teams:
            for agent in self.teams[team].agents:
                if agent.name == agent_name:
                    agent.enabled = False
                    self.save_config()
                    return True
        return False
    
    def get_enabled_agents_for_team(self, team: AgentTeam) -> List[AgentInfo]:
        """Get enabled agents for a specific team"""
        if team in self.teams:
            return [agent for agent in self.teams[team].agents if agent.enabled]
        return []
    
    def get_all_enabled_agents(self) -> Dict[AgentTeam, List[AgentInfo]]:
        """Get all enabled agents organized by team"""
        enabled_agents = {}
        for team, team_info in self.teams.items():
            if team_info.enabled:
                enabled_agents[team] = self.get_enabled_agents_for_team(team)
        return enabled_agents
    
    def get_workflow_order(self) -> List[TeamInfo]:
        """Get teams in workflow execution order"""
        enabled_teams = self.get_enabled_teams()
        return sorted(enabled_teams, key=lambda x: x.order)
    
    def save_config(self) -> bool:
        """Save configuration to file"""
        try:
            config_data = {
                "teams": {}
            }
            
            for team_enum, team_info in self.teams.items():
                config_data["teams"][team_enum.value] = {
                    "enabled": team_info.enabled,
                    "agents": {
                        agent.name: agent.enabled 
                        for agent in team_info.agents
                    }
                }
            
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving agent config: {e}")
            return False
    
    def load_config(self) -> bool:
        """Load configuration from file"""
        try:
            if not os.path.exists(self.config_file):
                return True  # Use defaults if no config file
            
            with open(self.config_file, 'r') as f:
                config_data = json.load(f)
            
            # Apply team settings
            if "teams" in config_data:
                for team_name, team_config in config_data["teams"].items():
                    try:
                        team_enum = AgentTeam(team_name)
                        if team_enum in self.teams:
                            self.teams[team_enum].enabled = team_config.get("enabled", True)
                            
                            # Apply agent settings
                            if "agents" in team_config:
                                for agent_name, agent_enabled in team_config["agents"].items():
                                    for agent in self.teams[team_enum].agents:
                                        if agent.name == agent_name:
                                            agent.enabled = agent_enabled
                                            break
                    except ValueError:
                        continue  # Skip invalid team names
            
            return True
        except Exception as e:
            print(f"Error loading agent config: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """Reset configuration to defaults"""
        try:
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
            
            # Reinitialize teams with defaults
            self.teams = self._initialize_teams()
            return True
        except Exception as e:
            print(f"Error resetting config: {e}")
            return False
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of current configuration"""
        enabled_teams = self.get_enabled_teams()
        total_agents = sum(len(team.agents) for team in enabled_teams)
        enabled_agents = sum(len(self.get_enabled_agents_for_team(team.team)) for team in enabled_teams)
        
        return {
            "total_teams": len(self.teams),
            "enabled_teams": len(enabled_teams),
            "total_agents": total_agents,
            "enabled_agents": enabled_agents,
            "workflow_order": [team.name for team in self.get_workflow_order()]
        }

# Global configuration instance
agent_config = AgentConfiguration()
