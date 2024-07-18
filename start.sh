#!/bin/bash

# Запуск агента SSH и добавление ключа
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/github

# Функция для клонирования репозитория, если директория не существует
clone_if_not_exists() {
    local DIR=$1
    shift
    local CMD=$@

    if [ ! -d "$DIR" ]; then
        echo "Клонируется: $CMD"
        $CMD
    else
        echo "Директория $DIR уже существует, клонирование не требуется."
    fi
}

# Функция для pull изменений в существующем репозитории
pull_repo() {
    local repo_dir=$1
    if [ -d "$repo_dir" ]; then
        echo "Pull репозитория $repo_dir"
        git -C "$repo_dir" pull
    else
        echo "ОШИБКА: Директория $repo_dir не существует"
    fi
}

# Обработка аргументов командной строки
branch="main"  # По умолчанию использовать ветку main

while [[ "$1" =~ ^- && ! "$1" == "--" ]]; do case $1 in
  --dev )
    branch="dev"
    ;;
  --main )
    branch="main"
    ;;
esac; shift; done
if [[ "$1" == '--' ]]; then shift; fi

# Клонирование и pull репозиториев
clone_if_not_exists "chat-boty-backend" "git clone --branch $branch git@github.com:Alexey-zaliznuak/chat-boty-backend.git"
clone_if_not_exists "chat-boty-client" "git clone --branch $branch git@github.com:maxi-q/chat-boty-client.git"

echo "Pull gateway repository"
git pull

echo "Pull backend"
pull_repo "chat-boty-backend"

echo "Pull client"
pull_repo "chat-boty-client"

echo "Остановка и удаление существующих контейнеров Docker"
docker compose down

echo "Сборка и запуск Docker Compose"
docker compose up --build -d
