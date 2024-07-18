import os
import subprocess
import argparse


def run_command(command):
    """Запуск команды в терминале."""
    process = subprocess.run(command, shell=True)
    if process.returncode != 0:
        raise Exception(f"Команда {command} завершилась с ошибкой {process.returncode}")


def clone_if_not_exists(dir_path, clone_command):
    """Клонирование репозитория, если директория не существует."""
    if not os.path.exists(dir_path):
        print(f"Клонируется: {clone_command}")
        run_command(clone_command)
    else:
        print(f"Директория {dir_path} уже существует, клонирование не требуется.")


def pull_repo(repo_dir):
    """Выполнение git pull в существующем репозитории."""
    if os.path.exists(repo_dir):
        print(f"Pull репозитория {repo_dir}")
        run_command(f"git -C {repo_dir} pull")
    else:
        print(f"ОШИБКА: Директория {repo_dir} не существует")


def main(branch):
    """Основная логика выполнения скрипта."""
    # Запуск агента SSH и добавление ключа
    run_command('eval "$(ssh-agent -s)"')
    run_command('SSH_AUTH_SOCK=$SSH_AUTH_SOCK ssh-add ~/.ssh/github')  # SSH_AUTH_SOCK=$SSH_AUTH_SOCK что бы был ssh агент текущего пользователя
    print()

    # Клонирование репозиториев
    clone_if_not_exists("chat-boty-backend", f"git clone --branch {branch} git@github.com:Alexey-zaliznuak/chat-boty-backend.git")
    clone_if_not_exists("chat-boty-client", f"git clone --branch {branch} git@github.com:maxi-q/chat-boty-client.git")
    print()

    # Pull изменений в репозиториях
    print("Pull gateway...")
    run_command("git pull")
    print()

    print("Pull backend...")
    pull_repo("chat-boty-backend")
    print()

    print("Pull client....")
    pull_repo("chat-boty-client")
    print()

    # Остановка и запуск Docker Compose
    print("Остановка и удаление существующих контейнеров Docker")
    run_command("sudo docker compose down")

    print("Сборка и запуск Docker Compose")
    run_command("sudo docker compose up --build -d")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Клонирование репозиториев и выполнение Docker Compose.")
    parser.add_argument('--dev', action='store_true', help='Использовать ветку dev для клонирования.')
    parser.add_argument('--master', action='store_true', help='Использовать ветку main для клонирования.')
    args = parser.parse_args()

    # Установка ветки по умолчанию (master)
    branch = "master"
    if args.dev:
        branch = "dev"

    main(branch)
