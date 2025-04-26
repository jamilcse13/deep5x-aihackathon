# Shomadhan.io Search System

## Project Overview

This project implements a basic search system for Shomadhan.io e-commerce platform as part of the AI Engineering Hackathon. Our team joined the hackathon late with a focus on learning rather than competing.

## Infrastructure

We created a simple infrastructure with three EC2 instances:
- API Server (Search API)
- Load Balancer
- Grafana (Monitoring)

## Key Components

### Search API
- Simple keyword-based search
- JSON file for product data
- Basic result filtering
![Image](https://github.com/user-attachments/assets/9d402d91-ee27-48de-9b3e-e43db5962409)

## Architecture


Client → Load Balancer → API → Search Engine → JSON Data
                                                 ↑
                                                 ↓
                              Monitoring Dashboard ← Grafana


## Team

We participated primarily to learn about the hackathon process and gain insights from seeing how others approached the challenge.
