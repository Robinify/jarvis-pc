#!/usr/bin/env python3
"""
Jarvis - AI Assistant for macOS
Main entry point
"""

import sys
import os
from pathlib import Path

# Add jarvis module to path
sys.path.insert(0, str(Path(__file__).parent))

from jarvis.core import Jarvis
from jarvis.utils import setup_logging, load_config


def main():
    """Main entry point for Jarvis"""
    try:
        # Load configuration
        config_path = Path.home() / ".jarvis" / "config.yaml"
        if not config_path.exists():
            config_path = Path(__file__).parent / "config.yaml"
        
        config = load_config(config_path)
        
        # Setup logging
        setup_logging(config.get("logging", {}))
        
        # Initialize Jarvis
        jarvis = Jarvis(config)
        
        # Start interactive loop
        jarvis.start()
        
    except KeyboardInterrupt:
        print("\n\nJarvis shutting down. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
