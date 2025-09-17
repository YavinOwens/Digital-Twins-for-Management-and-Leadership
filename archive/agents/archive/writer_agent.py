"""
Content Writer Agent for CrewAI Workflow

This module defines the Content Writer agent responsible for creating comprehensive
executive reports that synthesize research and analysis into actionable insights.
"""

from crewai import Agent
from typing import List, Optional, Any


def create_writer_agent(llm, conversation_history: Optional[List[Any]] = None, use_tools: bool = True) -> Agent:
    """
    Create a Content Writer agent for the CrewAI workflow
    
    Args:
        llm: The language model to use for the agent
        conversation_history: Previous conversation context for continuity
        use_tools: Whether to enable tool usage for the agent (not used for writer)
        
    Returns:
        Agent: Configured Content Writer agent
    """
    
    # Build context from conversation history
    context_info = ""
    if conversation_history and len(conversation_history) > 1:
        context_info = f"""
        
        CONVERSATION CONTEXT:
        This is part of an ongoing conversation. Previous topics discussed include:
        {chr(10).join([f"- {msg['content'][:100]}..." for msg in conversation_history[-3:] if msg['role'] == 'user'])}
        
        Please reference and build upon previous discussions when relevant, and maintain continuity 
        in the conversation flow. If the current question relates to previous topics, acknowledge 
        the connection and provide comparative or building insights.
        """
    
    writer = Agent(
        role='Content Writer',
        goal='Write comprehensive, detailed executive reports that synthesize research and analysis into actionable insights for senior leaders',
        backstory=f"""You are an expert business writer and consultant who specializes in creating
        comprehensive executive-level reports. You MUST write complete, detailed content for every
        section requested - never summaries or placeholders. You excel at synthesizing complex
        information into clear, actionable insights that senior leaders can immediately use for
        decision-making. You have excellent conversational memory and can reference previous
        discussions, build upon earlier insights, and maintain continuity across multiple exchanges.

        CRITICAL RULES:
        1. NEVER use placeholders like "[Insert content here]" or "[The actual content would continue here]"
        2. NEVER write summaries of what should be in the report - WRITE THE ACTUAL CONTENT
        3. ALWAYS write complete paragraphs with full details
        4. ALWAYS provide specific examples, statistics, and concrete recommendations
        5. Your reports must be 5000-9500 words with comprehensive coverage
        6. Write as if you are creating a final, publishable executive report
        7. Do NOT use ellipsis (...) or continuation phrases - write the complete content
        8. ONLY use references from the actual research data provided - NEVER make up citations
        9. Use ONLY the real sources found in the research results - check the References section

        {context_info}""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    return writer
