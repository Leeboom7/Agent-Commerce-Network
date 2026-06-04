# Alibaba Cloud Deployment Guide

## Prerequisites

1. Alibaba Cloud account with billing enabled
2. Qwen Cloud API key from [Model Studio](https://modelstudio.alibabacloud.com)
3. Hackathon credits applied to your account

## Step 1: Launch ECS Instance

```bash
# Via Alibaba Cloud CLI
aliyun ecs CreateInstance \
  --InstanceType ecs.c7.large \
  --ImageId centos_7_9_x64_20G_alibase_2024 \
  --SecurityGroupId <your-sg-id> \
  --InstanceName acp-demo \
  --InternetMaxBandwidthOut 10
```

Or use the [ECS Console](https://ecs.console.aliyun.com) with:
- Instance Type: 2 vCPU, 4 GB RAM (minimum)
- OS: Ubuntu 22.04 or CentOS 7.9
- Storage: 40 GB
- Bandwidth: 10 Mbps

## Step 2: Install Dependencies

```bash
ssh root@<your-ecs-ip>

# Update system
apt update && apt upgrade -y  # Ubuntu
# yum update -y               # CentOS

# Install Python 3.12+
apt install python3.12 python3.12-venv python3.12-dev -y

# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/<your-username>/agent-commerce-network.git
cd agent-commerce-network

# Install dependencies
uv pip install --system -e ".[demo]"
```

## Step 3: Configure Environment

```bash
# Create .env file
cat > .env << EOF
QWEN_API_KEY=<your-qwen-api-key>
QWEN_BASE_URL=https://dashscope-intl.aliyuncs.com/compatible-mode/v1
ACP_DEPLOY_ENV=production
EOF
```

## Step 4: Run Demo

```bash
# Run the Streamlit demo app
python -m streamlit run demo/app.py --server.port 8501 --server.address 0.0.0.0
```

## Step 5: Configure Security Group

Open port 8501 in your Alibaba Cloud security group to allow web access.

## Step 6: (Optional) Set Up Nginx Reverse Proxy

```bash
apt install nginx -y

cat > /etc/nginx/sites-available/acp << 'EOF'
server {
    listen 80;
    server_name <your-domain-or-ip>;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
EOF

ln -s /etc/nginx/sites-available/acp /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

## Verification

1. Open `http://<your-ecs-ip>:8501` in browser
2. You should see the ACP demo dashboard
3. Click "Run Demo Scenario" to watch the full competitive analysis pipeline
