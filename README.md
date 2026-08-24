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
I built a GPU infrastructure provisioning system to simulate managing GPU servers in a rack.

The basic idea is that instead of manually logging into every GPU server and configuring it, I want a central application where someone can request a GPU server to be provisioned.

I started with three components: Nginx, a FastAPI application, and PostgreSQL.

First, I created a PostgreSQL database to represent my GPU inventory. The database contains information like the hostname of each GPU server, what GPU it has, how many GPUs it has, what rack it's in, and whether it's available or already provisioned.

For example, I have gpu-node-01, which has eight A100 GPUs and starts as available.

Next, I created a Python FastAPI application. This is the actual backend of my system. It provides HTTP API endpoints. For example, GET /gpus asks the backend to retrieve the GPU inventory from PostgreSQL. I also created POST /provision/{hostname}, which changes a GPU node from available to provisioned.

Then I put Nginx in front of the API. Nginx acts as a reverse proxy. Instead of the user connecting directly to the FastAPI application on port 8000, the user connects to Nginx on port 80. Nginx receives the request and forwards it to FastAPI.

This means your application doesn't have to be directly exposed to the outside world.
This becomes much more useful when you have multiple FastAPI instances: Nginx can distribute requests between them.

So if I open the website and request /gpus, the request travels from my browser to Nginx, then from Nginx to FastAPI, then FastAPI queries PostgreSQL, and PostgreSQL returns the GPU information.

I then added a simple dashboard so that instead of seeing raw JSON, I can see the GPU nodes in a UI. When I click the Provision button, the browser sends a POST request to FastAPI. FastAPI updates PostgreSQL, changing the node from available to provisioned, and the UI refreshes to show the new state.

I used Docker Compose to run all three components as separate containers. When I ran docker compose up --build, Docker built the FastAPI image from the Dockerfile, downloaded the Nginx and PostgreSQL images, created a Docker network, created the three containers, and started them.

I also used curl to test the API directly from the command line. This is useful because it lets me test the backend without relying on the UI.

At the end, I had a working flow:

Browser → Nginx → FastAPI → PostgreSQL → GPU inventory.
