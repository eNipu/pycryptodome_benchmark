import tarfile
from io import StringIO, BytesIO
from os import listdir
from os.path import isfile, join
from zipfile import ZipFile

def read_dir(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    # print(onlyfiles)
    return onlyfiles

def zip_a_dir(path,  zip_name):
    files = read_dir(path)
    # print(files)
    """
    returns: zip archive
    """
    archive = BytesIO()
    zip_file_path = join(path, zip_name)

    with ZipFile(archive, 'w') as zip_archive:
        # Create three files on zip archive
        for f in files:
            file_path = join(path, f)
            # print(f"file={type(f)}, {file_path}")
            with zip_archive.open(file_path, 'w') as file1:
                for data in read_large_bin_file(file_path):
                    # print(type(data))
                    file1.write(data)

    # archive
    with open(join('./enc', zip_name), 'wb') as f:
        f.write(archive.getbuffer())
    archive.close()



def read_large_bin_file(filename, buf_size=1024):
    with open(filename, "rb") as f:
        while True:
            data = f.read(buf_size)
            if not data:
                # print("reading-----------")
                break
            yield data

def string_to_tarfile(input:str):
    tar = tarfile.TarFile("test.tar", "w")

    string = StringIO.StringIO()
    string.write(input)
    string.seek(0)
    info = tarfile.TarInfo(name="foo.bin")
    info.size = len(string.buf)
    tar.addfile(tarinfo=info, fileobj=string)

    tar.close()
