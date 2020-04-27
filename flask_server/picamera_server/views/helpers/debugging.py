import pydevd


def debug_remote(remote_ip: str, remote_port: int):
    """
    Ask for a debugger remote connection
    :param remote_ip:
    :param remote_port:
    :return:
    """
    pydevd.settrace(remote_ip, port=remote_port, stdoutToServer=True, stderrToServer=True)
