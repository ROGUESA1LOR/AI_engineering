# Overview  
This project uses bash and gnome-terminal please check your terminal before running it and make necessary changes accordingly
## Workflow  
This diagram below demonstrates the general workflow of project(work in progress).
```mermaid
graph LR
    %% Styling
    classDef process fill:#d68910,stroke:#ba4a00,stroke-width:2px,color:#fff;
    classDef store fill:#2e4053,stroke:#1a252f,stroke-width:3px,color:#fff;
    classDef entity fill:#27ae60,stroke:#1e8449,stroke-width:2px,color:#fff;

    %% Nodes
    H((Human Moderator)):::entity
    P1[Process 1.0:<br>Init & Orchestration]:::process
    P2[Process 2.0:<br>Llama Prompt Inference]:::process
    P3[Process 3.0:<br>Qwen Prompt Inference]:::process
    
    D1[/Current Session Pointer File/]:::store
    D2[/Central blackboard: state.json/]:::store
    D3[/FIFO Sync Sync Pipes/]:::store

    %% Level 1 Data Vectors
    H -->|Raw Topic & Model Choices| P1
    P1 -->|Write Database Template| D2
    P1 -->|Write Filename Pointer String| D1
    P1 -->|Write Starter Token| D3

    D3 -->|Blocking Sync Event Trigger| P2
    D1 -->|Read Active Target DB Name| P2
    D2 -->|Extract Dynamic Topic + Array Transcript via jq| P2
    P2 -->|Append Llama Node Stream via jq| D2
    P2 -->|Signal Next Task Node| D3

    D3 -->|Blocking Sync Event Trigger| P3
    D1 -->|Read Active Target DB Name| P3
    D2 -->|Extract Dynamic Topic + Array Transcript via jq| P3
    P3 -->|Append Qwen Node Stream via jq| D2
    P3 -->|Signal Loop Turn to Human| D3

    D3 -->|Unfreeze Window Display| H
    H -->|Inject Live Human Evaluation String| D2
    H -->|Flick Loop Reset String| D3
```
# DFD(Level 1)  
This diagram below lines out general data flow happening(work in progress).
```mermaid
graph TD
    %% Styling
    classDef master fill:#1a1a2e,stroke:#16c79a,stroke-width:2px,color:#fff;
    classDef modelA fill:#16a085,stroke:#117a65,stroke-width:2px,color:#fff;
    classDef modelB fill:#2980b9,stroke:#1f618d,stroke-width:2px,color:#fff;
    classDef state fill:#2c3e50,stroke:#34495e,stroke-width:2px,color:#fff;
    classDef pipe fill:#e74c3c,stroke:#c0392b,stroke-width:2px,color:#fff;

    %% Elements
    M[Master Controller: start.sh]:::master
    JSON[(Shared State: state.json)]:::state
    P1(((pipe1 Token Gate))):::pipe
    P2(((pipe2 Token Gate))):::pipe
    P3(((pipe3 Token Gate))):::pipe
    A[Terminal 1: MODEL1.sh <br> Llama 3.1 Defender]:::modelA
    B[Terminal 2: MODEL2.sh <br> Qwen 2.5 Attacker]:::modelB
    U[Human Moderator Control <br> Terminal Window]:::master

    %% Master Flow
    M -->|1. Setup Pipes & Init| JSON
    M -->|2. Ask Topic & Model| UserInput[User Enters Config]
    UserInput -->|3. Generate Root Dict| JSON
    M -->|4. Launch Independent Windows| A
    M -->|4. Launch Independent Windows| B
    M -->|5. Drop Spark Plug Token| P1

    %% Dynamic Triangle Loop
    P1 -->|Wake Up Signal| A
    JSON -.->|Read Global Topic & Transcript| A
    A -->|Think: Prompt Payload Injection| OllamaA[Ollama Execution Layer]
    OllamaA -->|Append Message Node via jq| JSON
    A -->|Flick Traffic Light| P2

    P2 -->|Wake Up Signal| B
    JSON -.->|Read Global Topic & Transcript| B
    B -->|Think: Opposing Rebuttal Prompt| OllamaB[Ollama Execution Layer]
    OllamaB -->|Append Message Node via jq| JSON
    B -->|Flick Traffic Light| P3

    P3 -->|Wake Up Signal| U
    U -->|Take Keyboard input: read -rp| HumanInput[Human Verdict String]
    HumanInput -->|Append Human Node via jq| JSON
    U -->|Flick Traffic Light Loop Reset| P1

```