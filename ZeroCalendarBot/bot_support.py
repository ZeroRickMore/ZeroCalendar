from dotenv import load_dotenv
import os
from pathlib import Path

def load_env_vars() -> None:
    script_dir = Path(__file__).resolve().parent
    env_path = script_dir / '.env'
    load_dotenv(dotenv_path=env_path)

def get_bot_token() -> str:
    return os.getenv("BOT_TOKEN")

def get_group_id() -> int:
    return int(os.getenv("GROUP_ID"))

def get_debug_chat_id() -> int:
    return int(os.getenv("DEBUG_CHAT_ID"))