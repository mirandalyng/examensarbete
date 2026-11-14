import logfire
from logfire import VariablesOptions
from dotenv import load_dotenv
import os

load_dotenv()

# Configureate Logfire with API-key and support for variables (prompts)
logfire.configure(variables=VariablesOptions())

# Fetches prompt from Logfire with given name and version (lable)
def get_prompt(
    name: str = "prompt_music_agent_instructions",
    default: str = "music assistant",
    label: str = "latest"
):
    # Defines lable in Logifre; default is used if missing
    prompt = logfire.var(name=f"prompt__{name}", type=str, default=default)
    # Forces a new fetch so that we get the latest version
    prompt.refresh_sync(force=True)
    # Fetches the value for selected lable (e.g "latest")
    resolved = prompt.get(label=label)
    # print (resolved.lable)
    return resolved.value


# Test: writes out production-version of prompt when file is run directly 
if __name__ == "__main__":
    prompt = get_prompt(label="latest")
    print(prompt)