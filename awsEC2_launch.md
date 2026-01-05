# Django on AWS EC2 with Docker & Docker Compose

Launch EC2

AMI: Ubuntu 22.04

Instance type: t3.small

Security Group:

    - SSH 22 → My IP

    - HTTP 80 → 0.0.0.0/0

    - Custom TCP 8000 → 0.0.0.0/0

## SSH from Windows (PowerShell)

ssh -i $env:USERPROFILE\.ssh\django-rasa-key.pem ubuntu@<PUBLIC_IP>

## System setup (inside EC2)

sudo apt update
sudo apt upgrade -y
sudo reboot

## Install Docker

    sudo apt remove -y docker docker-engine docker.io containerd runc

    sudo apt update
    sudo apt install -y ca-certificates curl gnupg lsb-release

    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
    https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

    docker --version

## Docker permissions important

    sudo usermod -aG docker ubuntu
    exit

## Project directory

    mkdir -p ~/apps/django-rasa
    cd ~/apps/django-rasa

## Backend (Django) setup

    mkdir backend
    cd backend

## requirements.txt

    nano requirements.txt

## Create Django project (no root issues)

    docker run --rm \
    -u $(id -u):$(id -g) \
    -v "$PWD:/app" \
    -w /app \
    python:3.11-slim \
    sh -c "pip install django && django-admin startproject config"
