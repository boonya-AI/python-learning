import os


def environment():
    return os.environ


def support_methods():
    running_programs = ['os.system', 'os.popen', 'os.execv', 'os.spawnv']
    spawning_processes = ['os.fork', 'os.pipe', 'os.waitpid', 'os.kill']
    files_locks = ['os.open', 'os.read', 'os.write']
    file_processing = ['os.remove', 'os.rename', 'os.mkfifo', 'os.mkdir', 'os.rmdir']
    admin_tools = ['os.getcwd', 'os.chdir', 'os.chmod', 'os.getpid', 'os.listdir', 'os.access']
    portability_tools = ['os.sep', 'os.pathsep', 'os.curdir', 'os.path.split', 'os.path.join']
    pathname_tools = ['os.path.exists(xxx)', 'os.path.isdir(xxx)', 'os.path.getsize(xxx)']


def sys_arg(file):
    os.system("python {} arg arg &".format(file))
