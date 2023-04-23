import globals as g


def containters() -> list[dict[str, str]]:
    return [
        {
            "id": container.id,
            "name": container.name,
            "status": container.status,
        }
        for container in g.DOCKER_CLIENT.containers.list()
    ]


def start_container(container: dict[str, str]):
    g.DOCKER_CLIENT.containers.get(container["id"]).start()
