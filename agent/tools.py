"""
Simple dictionary-based search tool for factual information.
This tool contains a small knowledge base of factual information
that the agent can query when users ask factual questions.
"""

from langchain.tools import tool


# Simple knowledge base with factual information
KNOWLEDGE_BASE = {
    "capital": {
        "france": "Paris",
        "japan": "Tokyo",
        "germany": "Berlin",
        "italy": "Rome",
        "spain": "Madrid",
        "usa": "Washington D.C.",
        "uk": "London",
        "canada": "Ottawa",
        "australia": "Canberra",
        "india": "New Delhi",
    },
    "population": {
        "paris": "approximately 2.2 million (city proper), 12.4 million (metro area)",
        "tokyo": "approximately 14 million (city proper), 37 million (metro area)",
        "berlin": "approximately 3.7 million",
        "london": "approximately 9 million",
    },
    "science": {
        "speed of light": "approximately 299,792,458 meters per second",
        "boiling point of water": "100 degrees Celsius or 212 degrees Fahrenheit at sea level",
        "gravity on earth": "approximately 9.8 m/s²",
        "number of planets": "8 planets in our solar system",
    },
    "technology": {
        "python": "a high-level, interpreted programming language created by Guido van Rossum in 1991",
        "ai": "Artificial Intelligence - the simulation of human intelligence by machines",
        "langchain": "a framework for developing applications powered by language models",
        "langgraph": "a library for building stateful, multi-actor applications with LLMs",
    },
}


@tool
def search_facts(query: str) -> str:
    """
    Search for factual information in the knowledge base.
    
    This tool searches through a small dictionary of factual information
    including capitals, population data, science facts, and technology definitions.
    
    Args:
        query: The factual question or search term (e.g., "capital of France", "speed of light")
        
    Returns:
        A string containing the factual answer or a message if not found.
    """
    query_lower = query.lower()
    
    # Search through all categories
    for category, items in KNOWLEDGE_BASE.items():
        for key, value in items.items():
            # Check if the key is mentioned in the query
            if key in query_lower:
                if category == "capital":
                    return f"The capital of {key.title()} is {value}."
                elif category == "population":
                    return f"The population of {key.title()} is {value}."
                elif category == "science":
                    return f"{key.title()}: {value}."
                elif category == "technology":
                    return f"{key.title()}: {value}."
    
    # If no match found
    return f"I don't have factual information about '{query}' in my knowledge base. This might require general knowledge or a conversational response."


# Export the tool
__all__ = ["search_facts"]
