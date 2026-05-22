#!/bin/bash

set -e

echo "========================================"
echo "Subindo containers..."
echo "========================================"

docker compose up -d --build --force-recreate

echo ""
echo "==============================================="
echo "Aguardando containers iniciarem..."
echo "==============================================="

sleep 5

echo ""
echo "==============================================="
echo "Fazendo ingestão do documento (document.pdf)..."
echo "==============================================="

docker exec -it python_app bash -c 'python src/ingest.py'

echo ""
echo "==============================================="
echo "Entrando no container da aplicação..."
echo "==============================================="

docker exec -it python_app bash -c 'python src/chat.py'
