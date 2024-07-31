from bevyframe import *
from dotenv import load_dotenv
import os


def get(r: Request) -> Response:
    return redirect('https://github.com/hereus-pbc/search')


# Placeholder for testing
def is_session_syned(r: Request) -> bool:
    return True


if __name__ == '__main__':
    load_dotenv('../.env')
    Frame(
        package='net.hereus.search',
        developer='hereus@hereus.net',
        administrator=False,
        secret=os.environ.get('SECRET'),
        style="../HereUS-UI-3.1/HereUS-UI-3.1.json",
        icon="https://www.hereus.net/static/favicon.png",
        keywords=["search", "theprotocols", "decentralized"],
        default_network="hereus.net",
    ).run(
        host='0.0.0.0',
        port=80,
        debug=True
    )
