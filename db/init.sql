CREATE TABLE gpu_nodes (
    id SERIAL PRIMARY KEY,
    hostname VARCHAR(100) UNIQUE NOT NULL,
    gpu_model VARCHAR(50) NOT NULL,
    gpu_count INTEGER NOT NULL,
    status VARCHAR(30) NOT NULL,
    rack VARCHAR(50) NOT NULL
);

INSERT INTO gpu_nodes
(hostname, gpu_model, gpu_count, status, rack)
VALUES
('gpu-node-01', 'A100', 8, 'available', 'rack-01'),
('gpu-node-02', 'H100', 8, 'available', 'rack-01'),
('gpu-node-03', 'A100', 8, 'provisioned', 'rack-02'),
('gpu-node-04', 'H200', 8, 'available', 'rack-02');
