import base64

def convert_image_to_data_uri(image_filename):
    '''
    Convert an image file to a base64-encoded data URI.

    Parameters
    ----------
    image_filename : str
        The filename of the image to be converted.

    Returns
    -------
    str
        A base64-encoded data URI representing the image.
    '''
    # Open the image file in binary read mode
    with open(image_filename, 'rb') as image_file:
        # Read the binary content of the image file
        image_data = image_file.read()

    # Encode the binary image data to base64 format
    encoded_image_data = base64.b64encode(image_data)

    # Convert the base64-encoded data to a UTF-8 string
    utf8_encoded_image = encoded_image_data.decode('utf-8')

    # Create and return the data URI with the appropriate MIME type
    data_uri = 'data:image/png;base64,' + utf8_encoded_image
    return data_uri
