import os
import io
from msgpack import packb
import mimetypes
from falcon import HTTP_200, MEDIA_MSGPACK

class ImageResource(object):

    def __init__(self):
        self.ImageHandler = ImageHandler(os.path.dirname(__file__))

    # Get an image based on netid and id
    def on_get(self, req, resp, name):

        resp.content_type = mimetypes.guess_type(name)
        resp.stream, resp.content_length = self.ImageHandler.load_image(name)
        resp.status = HTTP_200

class ImageHandler(object):

    CHUNK_SIZE_BYTES = 4096

    def __init__(self, file):
        self.storagePath = os.path.join(file, '../../images')

    # Return requested image
    def load_image(self, name):

        if name == 'undefined' or name == 'null':
            resp.status = HTTP_200
            return

        imagePath = os.path.join(self.storagePath, name)
        stream = io.open(imagePath, 'rb')
        content_length = os.path.getsize(imagePath)
        return stream, content_length

    # Save image and return path
    def save_image(self, req, netid, id):

        ext = mimetypes.guess_extension(req.content_type)
        name = '{}_{}{}'.format(netid, id, ext)
        imagePath = os.path.join(self.storagePath, name)

        with io.open(imagePath, 'wb') as imageFile:
            while True:
                chunk = req.stream.read(self.CHUNK_SIZE_BYTES)
                if not chunk:
                    break

                imageFile.write(chunk)

        # Check if file is empty
        if os.stat(imagePath).st_size == 0:
            name = None

        return name

    # Delete image from deleted fun fact
    def delete_image(self, name):
        imagePath = os.path.join(self.storagePath, name)
        try:
            if os.path.exists(imagePath):
                os.remove(imagePath)
        except:
            return False
        return True
