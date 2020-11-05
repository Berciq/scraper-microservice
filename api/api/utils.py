from os import makedirs
from os.path import dirname, join


class ImageStore:
    
    def get_image(self, path: str) -> bytes:
        pass

    def put_image(self, path: str, buf: bytes):
        pass


class FileSystemImageStore(ImageStore):

    def __init__(self, root_path):
        self.root_path = root_path

    def get_image(self, path: str) -> bytes:
        """
        Returns a bytes object representing the image.

        :param path: path to access the image file

        :return: image as bytes object
        """
        return open(join(self.root_path, path), 'rb').read()

    def put_image(self, path: str, buf: bytes):
        fname = join(self.root_path, path)
        makedirs(dirname(fname), exist_ok=True)
        with open(fname, 'wb') as f:
            f.write(buf)
