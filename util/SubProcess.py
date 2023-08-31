import subprocess


def call_file(file):
    subprocess.call("python {}".format(file))


def call_cmd_file(file):
    subprocess.call("cmd /C python {}".format(file))


def call_type_file(file):
    subprocess.call("type {}".format(file), shell=True)


def call_popen_communicate(file):
    pipe = subprocess.Popen("python {}".format(file), stdout=subprocess.PIPE)
    pipe.communicate()
    return pipe.returncode


def call_popen_stdout_read_wait(file):
    pipe = subprocess.Popen("python {}".format(file), stdout=subprocess.PIPE)
    pipe.stdout.read()
    pipe.wait()


