import logging
import json
import os
from datetime import datetime

class EnterpriseLogger:
    def __init__(self, name="AutoDevEnterprise"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create handlers if they don't exist
        if not self.logger.handlers:
            # Console Handler
            c_handler = logging.StreamHandler()
            c_handler.setLevel(logging.INFO)
            
            # File Handler (JSON Format for Splunk/ELK)
            os.makedirs("workspace/logs", exist_ok=True)
            f_handler = logging.FileHandler(f"workspace/logs/ade_{datetime.now().strftime('%Y%m%d')}.json")
            f_handler.setLevel(logging.DEBUG)

            # JSON Formatter
            class JsonFormatter(logging.Formatter):
                def format(self, record):
                    log_record = {
                        "timestamp": datetime.utcnow().isoformat(),
                        "level": record.levelname,
                        "module": record.module,
                        "message": record.getMessage(),
                        "thread": record.threadName
                    }
                    return json.dumps(log_record)

            f_handler.setFormatter(JsonFormatter())
            
            # Standard Console Formatter
            c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            c_handler.setFormatter(c_format)

            self.logger.addHandler(c_handler)
            self.logger.addHandler(f_handler)

    def log_event(self, role, action, status, details=None):
        self.logger.info(f"[{role}] {action} - {status} | {details or ''}")

    def error(self, message):
        self.logger.error(message)

# Singleton instance
ade_logger = EnterpriseLogger().logger
