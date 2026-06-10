"""
Utility functions
"""

import logging
import yaml
from pathlib import Path
from typing import Dict, Any


def setup_logging(config: Dict) -> None:
    """Setup logging configuration"""
    level = config.get("level", "INFO")
    log_file = config.get("file", "jarvis.log")
    console = config.get("console", True)
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level))
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, level))
    
    # Console handler
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)  # Only warnings to console
        logger.addHandler(console_handler)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)


def load_config(config_path: Path) -> Dict:
    """Load configuration from YAML file"""
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    
    return config or {}


def save_config(config: Dict, config_path: Path) -> None:
    """Save configuration to YAML file"""
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False)


def format_response(response: str, assistant_name: str = "Jarvis") -> str:
    """Format assistant response for display"""
    return f"{assistant_name}: {response}"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to maximum length"""
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text
