import os
import subprocess
import argparse


def check_path_exists(path: str):
    if not os.path.exists(path):
        raise OSError("Path does not exist")


def run_command(command: str, print_blank_end_line: bool = True):
    """Run command in terminal."""
    process = subprocess.run(command, shell=True)

    if process.returncode != 0:
        raise Exception(f"Command {command} failed with code: {process.returncode}")

    if print_blank_end_line:
        print()


def clone_if_not_exists(directory: str, repo: str, branch: str = None):
    """
    Cloning repo, if directory does not exist.
    Raise value error if clone requires but branch not provided.
    """
    if not os.path.exists(directory):
        if branch is None:
            raise ValueError("Branch argument not provided, but clone required, use --dev or --master")

        print(f"Cloning: {repo}")
        run_command(repo)
    else:
        print(f"Directory {directory} already exist, cloning not required.")


def pull_repo(repo_directory: str):
    """Run git pull in provided directory."""

    check_path_exists(repo_directory)

    print(f"Pull repo: {repo_directory}")
    run_command(f"git -C {repo_directory} pull")


def check_env_file_exists():
    env_file = '.env'

    if not os.path.isfile(env_file):
        raise EnvironmentError(f"Env file: {env_file} does not exist.")

    if os.path.getsize(env_file) == 0:
        raise EnvironmentError(f"Env file {env_file} is blank.")


def main(branch):
    check_env_file_exists()

    # Run ssh agent, add github ssh key
    run_command('eval "$(ssh-agent -s)"')
    run_command('SSH_AUTH_SOCK=$SSH_AUTH_SOCK ssh-add ~/.ssh/github')  # SSH_AUTH_SOCK=$SSH_AUTH_SOCK что бы был ssh агент текущего пользователя

    # Clone backend and client repo`s
    clone_if_not_exists("chat-boty-backend", f"git@github.com:Alexey-zaliznuak/chat-boty-backend.git", branch)
    clone_if_not_exists("chat-boty-client", f"git@github.com:maxi-q/chat-boty-client.git", branch)

    # Pull changes
    print("Pull gateway...")
    run_command("git pull")

    print("Pull backend...")
    pull_repo("chat-boty-backend")

    print("Pull client....")
    pull_repo("chat-boty-client")

    # Rstart Docker Compose
    print("Stopping Docker Compose")
    run_command("sudo docker compose down")

    print("Rebuild Docker Compose")
    run_command("sudo docker compose up --build -d")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Клонирование репозиториев и выполнение Docker Compose.")
    parser.add_argument('--dev', action='store_true', help='Use dev branch for cloning.')
    parser.add_argument('--master', action='store_true', help='Use master branch for cloning.')

    args = parser.parse_args()

    branch = None
    if args.dev:
        branch = "dev"
    elif args.master:
        branch = "master"

    main(branch)
