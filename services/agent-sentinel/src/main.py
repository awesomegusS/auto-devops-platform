import time
from loguru import logger
import docker
from docker.models.containers import Container
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()

TARGET_NAME = os.getenv("TARGET_CONTAINER", "production-victim")

class SentinelAgent:
    def __init__(self):
        # Initialize Docker Client from the socket mounted in docker-compose
        try:
            self.client = docker.from_env()
            logger.info("🐳 Docker Client connected successfully.")
        except Exception as e:
            logger.critical(f"Failed to connect to Docker Socket: {e}")
            raise e

    def get_target_container(self) -> Container:
        """Finds the victim container by name."""
        try:
            return self.client.containers.get(TARGET_NAME)
        except docker.errors.NotFound:
            logger.error(f"Target {TARGET_NAME} not found!")
            return None

    def analyze_logs(self, container: Container):
        """
        Fetches the last 10 lines of logs.
        TODO: Connect this to the LLM 'Brain' module.
        """
        logs = container.logs(tail=10).decode('utf-8')
        logger.debug(f"Fetched logs from {container.name}")
        return logs

    def run_loop(self):
        logger.info("🚀 Agent Sentinel starting monitoring loop...")
        while True:
            container = self.get_target_container()
            
            if container:
                # Check health status
                container.reload() # Refresh state
                status = container.status
                logger.info(f"Target Status: {status}")

                if status == "exited" or status == "dead":
                    logger.warning("🚨 TARGET IS DOWN. Initiating Analysis Protocol...")
                    logs = self.analyze_logs(container)
                    # TODO: Pass logs to LLM -> Get decision -> Execute Fix
                
            time.sleep(5) # Polling interval

if __name__ == "__main__":
    agent = SentinelAgent()
    agent.run_loop()