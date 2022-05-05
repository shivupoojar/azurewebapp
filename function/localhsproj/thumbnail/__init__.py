from io import BytesIO
from logging import FileHandler
import logging
import azure.functions as func
from PIL import Image

def image_to_thumbnail(input_str):
	new_size = 200,200 
	local_file_name_thumb= input_str[:-4] + "_thumb.jpg"
    im = Image.open(local_blob.name)
    im.thumbnail(new_size)
    im.save(local_file_name_thumb, quality=95)

    # write the stream to the output file in blob storage
    new_thumbfile = open(local_file_name_thumb,"rb")
    outputblob.set(new_thumbfile.read())

def main(myblob: func.InputStream, blobout: func.Out[bytes], context: func.Context):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    input = myblob.read()
    input_str = input.decode("UTF-8").encode('latin-1', 'ignore').decode('latin-1')
    sisu = image_to_thumbnail(input_str)
    blobout.set(sisu)
