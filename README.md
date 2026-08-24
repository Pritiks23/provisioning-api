# provisioning-api
                         Client
                           │
                     HTTP :80 / :443
                           │
                           ▼
                     ┌──────────┐
                     │  NGINX   │
                     │ :80      │
                     └────┬─────┘
                          │
                     HTTP :8000
                          │
                          ▼
                  ┌───────────────┐
                  │ GPU Provision │
                  │    API        │
                  │   FastAPI     │
                  └───────┬───────┘
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
        PostgreSQL     GPU Nodes    Monitoring
        Inventory       SSH/API      Metrics
             │            │
             ▼            ▼
       ┌──────────┐   ┌──────────────┐
       │ rack-01  │   │ gpu-node-01  │
       │ rack-02  │   │ A100 x 8     │
       │ rack-03  │   │ Ubuntu       │
       └──────────┘   │ NVIDIA Driver│
                      │ CUDA         │
                      └──────────────┘
