import patoolib
import os
import shutil


FORMATS = (".zip", ".rar", ".7z")

for folder, sub, file in os.walk(os.getcwd()):
    for arch in file:
        filepath = os.path.join(folder, arch)
        name = os.path.splitext(filepath)[0]
        extension = os.path.splitext(filepath)[1]
        print(filepath, name)
        if extension in FORMATS:
            if os.path.exists(name):
                shutil.rmtree(name)
                print(name)
            patoolib.extract_archive(filepath, outdir=name)
            os.remove(filepath)
