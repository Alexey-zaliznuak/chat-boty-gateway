#!/bin/bash

eval "$(ssh-agent -s)"
ssh-add ~/.ssh/github

clone_if_not_exists() {
    local DIR=$1
    shift
    local CMD=$@

    if [ ! -d "$DIR" ]; then
        $CMD
    fi
}

pull_repo() {
    local repo_dir=$1
    if [ -d "$repo_dir" ]; then
        echo "Pull $repo_dir  repository"
        git -C "$repo_dir" pull
    else
        echo "ERROR: $repo_dir directory does not exist"
    fi
}


clone_if_not_exists "chat-boty-backend" "git clone --branch dev git@github.com:Alexey-zaliznuak/chat-boty-backend.git"
clone_if_not_exists "chat-boty-client" "git clone --branch dev git@github.com:maxi-q/chat-boty-client.git"


echo "Pull gateway repository"
git pull


echo "Pull backend"
pull_repo "chat-boty-backend"

echo "Pull client"
pull_repo "chat-boty-client"

echo "Stopping and removing existing Docker containers"
docker compose down

echo "Building and starting Docker Compose"
docker compose up --build -d
