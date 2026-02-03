from loguru import logger
import docker
from docker.models.containers import Container

class Executor:
    def restart_container(self, container: Container):
        logger.info(f"🔧 Executing Fix: Restarting {container.name}...")
        try:
            container.restart()
            logger.success(f"✅ {container.name} successfully restarted!")
        except Exception as e:
            logger.critical(f"❌ Failed to restart container: {e}")

    def scale_up(self, container: Container):
        logger.info("🔧 Scaling up logic would go here (requires Docker Swarm/K8s).")
        # For now, we just restart as a fallback
        self.restart_container(container)