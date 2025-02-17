/* 
%%{init: {'theme': 'neutral', 'themeVariables': { 'primaryColor': '#f0f0f0' }}}%%
flowchart TD
    ... (rest of your flowchart)

    subgraph User Authentication
        actorU((User)):::actor
        actorA((Authentication Service)):::actor

        subgraph Swimlanes
            direction TB
            U[User]:::swimlane
            A[Authentication Service]:::swimlane
        end

        U --> A

        start([Start]) --> U
        U -->|Submit Credentials| A1[Verify Password]
        A1 --> decision1{Valid Credentials?}
        decision1 -->|Yes| A2[Generate Token]
        A2 --> U2[Login Success] --> end1([End])
        decision1 -->|No| U3[Display Error: Invalid Credentials]
        U3 --> decision2{Retry?}
        decision2 -->|Yes| start
        decision2 -->|No| end2([End])

        classDef actor fill:#ffd700,stroke:#000
        classDef swimlane fill:#e0e0e0,stroke:#666,stroke-width:2px
    end

    %%{init: {'theme': 'neutral', 'themeVariables': { 'primaryColor': '#f0f0f0' }}}%%
flowchart TD
    subgraph Transaction Handling
        actorU((User)):::actor
        actorT((Transaction Service)):::actor

        subgraph Swimlanes
            direction TB
            U[User]:::swimlane
            T[Transaction Service]:::swimlane
        end

        U --> T

        start([Start]) --> U1[Initiate Transaction] --> T1[Verify Account Balance]
        T1 --> decision1{Sufficient Balance?}
        decision1 -->|Yes| T2[Complete Transaction]
        T2 --> T3[Generate Transaction History] --> U2[Transaction Success] --> end1([End])
        decision1 -->|No| U3[Display Error: Insufficient Funds]
        U3 --> decision2{Retry?}
        decision2 -->|Yes| U1
        decision2 -->|No| end2([End])

        classDef actor fill:#ffd700,stroke:#000
        classDef swimlane fill:#e0e0e0,stroke:#666,stroke-width:2px
    end
*/