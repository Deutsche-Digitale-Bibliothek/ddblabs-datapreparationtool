import shutil, errno

def copyanything(source, destination):
    try:
        shutil.copytree(source, destination)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(source, destination)
            print("DEBUG: OSError")
        elif exc.errno == errno.EEXIST:
            pass
        else:
            raise
    except FileExistsError as exc2:
        print("DEBUG: FileExistsError")
        pass