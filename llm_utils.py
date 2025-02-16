import requests
import json
import logging

logger = logging.getLogger(__name__)

# Default Ollama endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_command_with_ollama(user_query: str) -> str:
    system_prompt = (
        "You are a command-line assistant. Output ONLY the exact command to run, nothing else.\n"
        "- For Windows, use: tasklist /FO TABLE\n"
        "- For Linux, use: ps aux --sort=-%cpu | head -n 11\n"
        f"Request: {user_query}\n"
        "Command (respond with ONLY the command):"
    )

    payload = {
        "model": "deepseek-r1:1.5b",
        "prompt": system_prompt,
        "temperature": 0.1,
        "stop": ["\n", "```"]
    }

    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=60, stream=True)
        resp.raise_for_status()
        
        generated_chunks = []
        for line in resp.iter_lines(decode_unicode=True):
            if not line or not line.strip():
                continue
            try:
                data = json.loads(line)
                if data.get("done"):
                    break
                chunk = data.get("response", "")
                generated_chunks.append(chunk)
            except json.JSONDecodeError:
                continue

        command = "".join(generated_chunks).strip()
        command = command.replace("```", "").replace("`", "")
        
        if command.startswith("Okay") or command.startswith("Let") or "<think>" in command:
            logger.info("Got explanation instead of command, using fallback")
            return "tasklist /FO TABLE"
            
        if not command:
            logger.info("Empty command response, using fallback")
            return "tasklist /FO TABLE"
            
        return command

    except Exception as e:
        logger.error(f"Ollama request failed: {e}")
        return "tasklist /FO TABLE"