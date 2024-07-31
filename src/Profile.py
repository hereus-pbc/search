from bevyframe import *
from TheProtocols import ID, CredentialsDidntWorked


def get(r: Request) -> Page:
    return redirect('https://account.hereus.net/')
