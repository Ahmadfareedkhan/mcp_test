import os
import groq
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Initialize Groq client - make sure to set GROQ_API_KEY environment variable
client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_command_with_groq(user_query: str) -> str:
    """
    Sends the user query to Groq LLM instance and returns a recommended system command string.
    """
    system_prompt = (
        """You are a highly skilled Windows Command-Line Assistant. Your sole task is to translate a user's natural language request into the exact Windows command that fulfills the request, using PowerShell syntax where applicable. Do not include any explanation, commentary, or additional text—only output the single, complete command.

            For example:
            - If the request is "list the top CPU processes", your response should be:
            powershell /c "Get-Process | Sort-Object CPU -Descending | Select-Object -First 10"
            - If the request is "show free disk space on all drives", your response should be:
            powershell /c "Get-PSDrive | Select-Object Name, Free, Used, @{Name='Total';Expression={$_.Used + $_.Free}}"

            Now, given the following request:
            {user_query}

            Output only the command that directly satisfies this request.
            """
    )

    try:
        # Call Groq API
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            model="llama3-8b-8192",  # or another Groq model
            temperature=0.1,
            max_tokens=100
        )
        
        # Extract the command from response
        command = completion.choices[0].message.content.strip()
        
        # Clean up any markdown formatting
        command = command.replace("```", "").replace("`", "")
        logger.info(f"Groq generated command: {command}")
        
        return command

    except Exception as e:
        logger.error(f"Groq API request failed: {e}")
        # Return a fallback command for Windows
        return 'powershell /c "Get-Process | Sort-Object CPU -Descending | Select-Object -First 10"'