"""
System Integration and Commands
"""

import logging
import subprocess
import psutil
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class SystemCommands:
    """Handle system commands and information"""
    
    def __init__(self, config: Dict):
        """Initialize system commands"""
        self.enable_commands = config.get("enable_commands", True)
        self.max_command_timeout = config.get("max_command_timeout", 30)
        self.safe_mode = config.get("safe_mode", True)
        
        # Unsafe commands to restrict
        self.dangerous_commands = {
            "rm", "rmdir", "rm -rf", "sudo", "chmod", "chown",
            "killall", "kill -9", "format", "dd", "mkfs"
        }
        
        logger.info("System commands handler initialized")
    
    def execute(self, command: str) -> str:
        """Execute a system command safely"""
        if not self.enable_commands:
            return "System commands are disabled."
        
        # Safety check
        if self.safe_mode and self._is_dangerous(command):
            return f"Safety check: This command appears to be dangerous and is blocked: {command}"
        
        try:
            logger.info(f"Executing command: {command}")
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.max_command_timeout
            )
            
            output = result.stdout.strip() or result.stderr.strip()
            if not output:
                output = "Command executed successfully with no output."
            
            return output[:500]  # Limit output length
        
        except subprocess.TimeoutExpired:
            return f"Command timed out after {self.max_command_timeout} seconds."
        except Exception as e:
            logger.error(f"Command execution error: {e}")
            return f"Error executing command: {str(e)[:100]}"
    
    def _is_dangerous(self, command: str) -> bool:
        """Check if command is potentially dangerous"""
        command_lower = command.lower()
        return any(dangerous in command_lower for dangerous in self.dangerous_commands)
    
    def get_system_info(self) -> str:
        """Get current system information"""
        try:
            # CPU information
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Memory information
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_gb = memory.used / (1024**3)
            memory_total_gb = memory.total / (1024**3)
            
            # Disk information
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_used_gb = disk.used / (1024**3)
            disk_total_gb = disk.total / (1024**3)
            
            # Battery information (if available)
            battery_info = ""
            try:
                battery = psutil.sensors_battery()
                if battery:
                    battery_info = f"\nBattery: {battery.percent}% - {'plugged in' if battery.power_plugged else 'on battery'}"
            except:
                pass
            
            info = f"""
System Information ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}):

CPU: {cpu_percent}% ({cpu_count} cores)
Memory: {memory_percent}% ({memory_used_gb:.1f}GB / {memory_total_gb:.1f}GB)
Disk: {disk_percent}% ({disk_used_gb:.1f}GB / {disk_total_gb:.1f}GB){battery_info}
"""
            return info
        
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return f"Error retrieving system information: {str(e)[:100]}"
