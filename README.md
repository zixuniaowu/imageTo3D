# ImageTo3D

A project for converting images to 3D models using deep learning techniques.

## Features

- Convert 2D images to 3D models
- FastAPI-based web interface
- Docker support with GPU acceleration
- Easy deployment using docker-compose

## Requirements

- Docker and docker-compose
- NVIDIA GPU with CUDA support
- NVIDIA Container Toolkit

## Installation

1. Clone the repository:
```bash
git clone https://github.com/zixuniaowu/imageTo3D.git
cd imageTo3D
```

2. Build and run the Docker container:
```bash
docker-compose up --build
```

3. Access the web interface at `http://localhost:8000`

## Directory Structure

- `/app`: Main application code
- `/uploads`: Directory for uploaded images
- `/outputs`: Directory for generated 3D models

## License

MIT