import docker
import sys
import os

import tarfile
import time
from io import BytesIO

docker_image = "sandbox10:libsanbox"
docker_container = "sandbox-env"

sandbox_workspace = "/tmp/"

docker_client = docker.from_env()

'''
Start the sandbox docker container
'''
def start_container():
    try:
        docker_client.create_container(docker_image, "/bin/bash",
                                stdin_open = True,
                                detach = True,
                                tty = True,
                                name = docker_container,
                                working_dir = sandbox_workspace,)
    except:
        pass
    finally:
        docker_client.start("sandbox-env")

'''
Stop the sandbox docker container
'''
def stop_container():
    docker_client.stop("sandbox-env", 5)

'''
Put files into the sandbox

@Param srcs
    Source files' name, stored as a list
@Param dest
    Path in the sandbox

@return
    no return value
'''
def put_file(srcs, dest):
    current_dir = os.getcwd()

    tarStream = BytesIO()
    with tarfile.TarFile(fileobj = tarStream, mode = 'w') as tar:
        for src in srcs:
            file_name = os.path.basename(src)
            with open(src, 'r') as f:
                data = f.read().encode("utf-8")
                tarInfo = tarfile.TarInfo(name = file_name)
                tarInfo.size = len(data)
                # tarInfo.mtime = time.time()
                tar.addfile(tarInfo, BytesIO(data))

    tarStream.seek(0)
    docker_client.put_archive(container = docker_container,
                       path = dest,
                       data = tarStream)

'''
Put strings into sandbox files

@Param strings
    strings to be put, a list
@Param file_names
    target file name, a list
@Param dest
    file path

@return
    no return value
'''
def put_strings(strings, file_names, dest):
    tarStream = BytesIO()
    with tarfile.TarFile(fileobj = tarStream, mode = 'w') as tar:
        for it in range(0, len(strings)):
            file_name = file_names[it]
            data = strings[it].encode("utf-8")
            tarInfo = tarfile.TarInfo(name = file_name)
            tarInfo.size = len(data)
            # tarInfo.mtime = time.time()
            tar.addfile(tarInfo, BytesIO(data))

    tarStream.seek(0)
    docker_client.put_archive(container = docker_container,
                       path = dest,
                       data = tarStream)

# def clear_workspace():


'''
Execute a command in the sandbox

@Param command
    The command to be executed

@reutrn
    Execution output reuslt
'''
def execute(command, returnAsGenerator = False):
    exec_id = docker_client.exec_create(container = docker_container,
                                        cmd = command)
    return docker_client.exec_start(exec_id = exec_id["Id"],
                                    stream = returnAsGenerator).decode("utf-8")
