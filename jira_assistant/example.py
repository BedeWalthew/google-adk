"""
Example usage of the Jira Issue Retrieval Assistant
"""

import os
from dotenv import load_dotenv
from agent import root_agent

# Load environment variables from .env file
load_dotenv()

def main():
    """Run example interactions with the Jira assistant"""
    
    # Check if credentials are set
    if os.getenv("JIRA_EMAIL") == "your_jira_email@example.com":
        print("Please update your .env file with actual Jira credentials before running this example.")
        return
    
    # Example 1: List projects
    print("\n=== Example 1: List Projects ===")
    response = root_agent.run("List all projects in my Jira instance")
    print(response)
    
    # Example 2: Search for issues
    print("\n=== Example 2: Search for Issues ===")
    project_key = input("Enter a project key from the list above: ")
    response = root_agent.run(f"Find all open issues in the {project_key} project")
    print(response)
    
    # Example 3: Get issue details
    print("\n=== Example 3: Get Issue Details ===")
    issue_key = input("Enter an issue key (e.g., PROJECT-123): ")
    response = root_agent.run(f"Show me details for issue {issue_key}")
    print(response)
    
    # Example 4: Add a comment
    print("\n=== Example 4: Add a Comment ===")
    issue_key = input("Enter an issue key to comment on: ")
    comment = input("Enter your comment: ")
    response = root_agent.run(f"Add a comment to issue {issue_key} saying: {comment}")
    print(response)

if __name__ == "__main__":
    main()
