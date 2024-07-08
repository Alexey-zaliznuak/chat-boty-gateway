#!/bin/bash

# Функция для пуллинга репозитория
pull_repo() {
    local repo_dir=$1
    if [ -d "$repo_dir" ]; then
        echo "Pull $repo_dir  repository"
        git -C "$repo_dir" pull
    else
        echo "ERROR: $repo_dir directory does not exist"
    fi
}

echo "Pull gateway repository"
git pull

pull_repo "chat-boty-backend"

pull_repo "chat-boty-client"

echo "Start Docker Compose"
docker-compose up -d
