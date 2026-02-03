# Auto-DevOps Sentinel: Self-Healing Infrastructure Agent

**An autonomous reliability agent that uses the Sidecar Pattern and Large Language Models (LLMs) to detect, diagnose, and heal container failures in real-time.**

## 📖 Overview

In modern microservices architectures, minimizing **Mean Time To Recovery (MTTR)** is critical. The Auto-DevOps Sentinel is a **Control Plane** component designed to automate Tier-1 Site Reliability Engineering (SRE) tasks.

By leveraging the **Docker Socket (`/var/run/docker.sock`)**, the agent gains privileged access to the host's container runtime. When a monitored service fails, the agent:
1.  **Detects** the state change immediately (via event loop).
2.  **Ingests** the crash logs.
3.  **Analyzes** the root cause using **Llama 3.3 (via Groq)**.
4.  **Executes** the appropriate remediation strategy (e.g., Service Restart) without human intervention.

## 🏗 Architecture

The system utilizes the **Sidecar/DaemonSet Pattern**, running the agent alongside the application workloads on a private bridge network.

```mermaid
graph TD
    subgraph "Docker Host"
        A[Production Victim API] -- "Writes Logs" --> L(Stdout/Stderr)
        B[Sentinel Agent] -- "Monitors State" --> D((Docker Socket))
        D -- "Restart Command" --> A
        B -- "Sends Logs" --> C[Llama 3.3 Inference Engine]
        C -- "Returns Diagnosis & Fix" --> B
    end