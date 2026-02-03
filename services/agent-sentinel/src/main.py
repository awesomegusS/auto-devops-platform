import time
from loguru import logger
import docker
import os
from dotenv import load_dotenv

# Import our new modules
from brain import Brain
from executor import Executor

load_dotenv()
TARGET_NAME = os.getenv("TARGET_CONTAINER", "production-victim")

class SentinelAgent:
    def __init__(self):
        self.client = docker.from_env()
        self.brain = Brain()
        self.executor = Executor()
        logger.info("🤖 Sentinel Agent Initialized.")

    def get_target(self):
        try:
            return self.client.containers.get(TARGET_NAME)
        except docker.errors.NotFound:
            logger.error(f"Target {TARGET_NAME} not found!")
            return None

    def run_loop(self):
        logger.info("🚀 Monitoring Loop Started...")
        while True:
            container = self.get_target()
            
            if container:
                container.reload() # Refresh state
                status = container.status
                
                # If dead, we investigate
                if status == "exited" or status == "dead":
                    logger.warning(f"🚨 ALERT: {TARGET_NAME} is DOWN. State: {status}")
                    
                    # 1. Gather Evidence
                    logs = container.logs(tail=20).decode('utf-8')
                    
                    # 2. Think (LLM Analysis)
                    decision = self.brain.analyze_logs(logs)
                    logger.info(f"🧠 Diagnosis: {decision['root_cause']}")
                    logger.info(f"💡 Prescription: {decision['suggested_action']}")

                    # 3. Act
                    if decision['suggested_action'] == "restart":
                        self.executor.restart_container(container)
                    
                    # Sleep to prevent rapid-fire looping while it restarts
                    time.sleep(10)

                else:
                    logger.debug(f"Status: {status} (All Good)")

            time.sleep(5)

if __name__ == "__main__":
    agent = SentinelAgent()
    agent.run_loop()