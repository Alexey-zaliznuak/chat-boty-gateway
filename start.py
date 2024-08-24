import os
import subprocess

from dotenv import load_dotenv

load_dotenv(override=True)


MODE = os.getenv("MODE")


if not MODE:
    raise RuntimeError("No mode provided")


DOCKER_COMPOSE_FILE_NAME = {
    "development": "dev.docker-compose.yml",
    "production": "prod.docker-compose.yml"
}[MODE]


def run_command(command: str, print_blank_end_line: bool = True):
    """Run command in terminal."""
    process = subprocess.run(command, shell=True)

    if process.returncode != 0:
        raise Exception(f"Command {command} failed with code: {process.returncode}")

    if print_blank_end_line:
        print()


def main():
    # Pull images
    print("Pull docker images:")
    run_command(f"sudo docker compose -f {DOCKER_COMPOSE_FILE_NAME} pull")

    # Rstart Docker Compose
    print("Stopping Docker Compose:")
    try:
        run_command(f"sudo docker compose -f {DOCKER_COMPOSE_FILE_NAME} down")
    except Exception as e:
        print(e + "\n")
        print("Error ignored")

    print("Restart Docker Compose:")
    run_command(f"sudo docker compose -f {DOCKER_COMPOSE_FILE_NAME} up -d")


if __name__ == "__main__":
    main()
