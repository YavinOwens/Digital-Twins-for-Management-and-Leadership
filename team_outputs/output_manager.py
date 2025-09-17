"""
Team Output Manager for CrewAI Multi-Agent Workflow

This module handles saving and organizing team outputs from different workflows
into structured markdown files.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


class TeamOutputManager:
    """
    Manages saving and organizing team outputs from CrewAI workflows.
    """
    
    def __init__(self, base_dir: str = "team_outputs"):
        """
        Initialize the TeamOutputManager.
        
        Args:
            base_dir: Base directory for storing team outputs
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
    
    def save_workflow_outputs(
        self, 
        workflow_type: str, 
        query: str, 
        team_outputs: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Save outputs from a complete workflow run.
        
        Args:
            workflow_type: Type of workflow (e.g., "seven_team_workflow")
            query: Original user query
            team_outputs: Dictionary of team outputs
            metadata: Additional metadata to save
            
        Returns:
            Path to the created output directory
        """
        # Create timestamp-based directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        workflow_name = workflow_type.replace("_", "-").replace("workflow", "workflow")
        output_dir = self.base_dir / f"{workflow_name}_{timestamp}"
        output_dir.mkdir(exist_ok=True)
        
        # Save query and metadata
        self._save_query_and_metadata(output_dir, query, metadata)
        
        # Save each team's output
        for team_name, team_output in team_outputs.items():
            self._save_team_output(output_dir, team_name, team_output)
        
        # Create index file
        self._create_index_file(output_dir, workflow_type, query, team_outputs)
        
        print(f"📁 Team outputs saved to: {output_dir}")
        return str(output_dir)
    
    def save_individual_team_output(
        self, 
        workflow_type: str, 
        team_name: str, 
        team_output: str,
        query: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Save output from a single team.
        
        Args:
            workflow_type: Type of workflow
            team_name: Name of the team
            team_output: Team's output content
            query: Original user query
            metadata: Additional metadata
            
        Returns:
            Path to the saved file
        """
        # Create workflow directory if it doesn't exist
        workflow_dir = self.base_dir / workflow_type
        workflow_dir.mkdir(exist_ok=True)
        
        # Create timestamp-based filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{team_name}_{timestamp}.md"
        file_path = workflow_dir / filename
        
        # Prepare content
        content = self._format_team_output(team_name, team_output, query, metadata)
        
        # Save file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"📄 {team_name} output saved to: {file_path}")
        return str(file_path)
    
    def _save_query_and_metadata(
        self, 
        output_dir: Path, 
        query: str, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Save query and metadata to the output directory."""
        # Save query
        query_file = output_dir / "query.md"
        with open(query_file, 'w', encoding='utf-8') as f:
            f.write(f"# Query\n\n{query}\n")
        
        # Save metadata if provided
        if metadata:
            metadata_file = output_dir / "metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, default=str)
    
    def _save_team_output(
        self, 
        output_dir: Path, 
        team_name: str, 
        team_output: str
    ) -> None:
        """Save individual team output to markdown file."""
        # Clean team name for filename
        clean_name = team_name.lower().replace(" ", "_").replace("&", "and")
        filename = f"{clean_name}.md"
        file_path = output_dir / filename
        
        # Format and save content
        content = self._format_team_output(team_name, team_output)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _format_team_output(
        self, 
        team_name: str, 
        team_output: str, 
        query: str = "", 
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Format team output into markdown."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        content = f"# {team_name}\n\n"
        content += f"**Generated:** {timestamp}\n\n"
        
        if query:
            content += f"**Query:** {query}\n\n"
        
        if metadata:
            content += "**Metadata:**\n"
            for key, value in metadata.items():
                content += f"- **{key}:** {value}\n"
            content += "\n"
        
        content += "---\n\n"
        content += team_output
        
        return content
    
    def _create_index_file(
        self, 
        output_dir: Path, 
        workflow_type: str, 
        query: str, 
        team_outputs: Dict[str, Any]
    ) -> None:
        """Create an index file for the workflow outputs."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        content = f"# {workflow_type.replace('_', ' ').title()}\n\n"
        content += f"**Generated:** {timestamp}\n\n"
        content += f"**Query:** {query}\n\n"
        content += "## Team Outputs\n\n"
        
        for team_name, team_output in team_outputs.items():
            clean_name = team_name.lower().replace(" ", "_").replace("&", "and")
            content += f"- [{team_name}](./{clean_name}.md)\n"
        
        content += "\n## Files in this Directory\n\n"
        content += "- `query.md` - Original user query\n"
        content += "- `metadata.json` - Workflow metadata\n"
        content += "- `{team_name}.md` - Individual team outputs\n"
        content += "- `index.md` - This index file\n"
        
        index_file = output_dir / "index.md"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def list_workflow_outputs(self, workflow_type: Optional[str] = None) -> List[str]:
        """
        List available workflow outputs.
        
        Args:
            workflow_type: Optional workflow type to filter by
            
        Returns:
            List of output directory paths
        """
        if workflow_type:
            workflow_dir = self.base_dir / workflow_type
            if workflow_dir.exists():
                return [str(f) for f in workflow_dir.iterdir() if f.is_dir()]
            return []
        else:
            return [str(f) for f in self.base_dir.iterdir() if f.is_dir()]
    
    def get_output_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all saved outputs.
        
        Returns:
            Dictionary with output summary
        """
        summary = {
            "total_workflows": 0,
            "workflow_types": {},
            "total_files": 0,
            "last_updated": None
        }
        
        for workflow_dir in self.base_dir.iterdir():
            if workflow_dir.is_dir():
                summary["total_workflows"] += 1
                workflow_type = workflow_dir.name
                
                if workflow_type not in summary["workflow_types"]:
                    summary["workflow_types"][workflow_type] = 0
                
                summary["workflow_types"][workflow_type] += 1
                
                # Count files in this workflow
                file_count = len([f for f in workflow_dir.iterdir() if f.is_file()])
                summary["total_files"] += file_count
                
                # Update last updated time
                if not summary["last_updated"] or workflow_dir.stat().st_mtime > summary["last_updated"]:
                    summary["last_updated"] = datetime.fromtimestamp(workflow_dir.stat().st_mtime)
        
        return summary


# Convenience function for backward compatibility
def save_team_outputs(
    workflow_type: str, 
    query: str, 
    team_outputs: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    Convenience function to save team outputs with default settings.
    
    Args:
        workflow_type: Type of workflow
        query: Original user query
        team_outputs: Dictionary of team outputs
        metadata: Additional metadata
        
    Returns:
        Path to the created output directory
    """
    manager = TeamOutputManager()
    return manager.save_workflow_outputs(workflow_type, query, team_outputs, metadata)
