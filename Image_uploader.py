import requests
import io
import time
from PIL import ImageGrab


def get_upload_link(url, token):
    """
    get the upload link to upload file through, raise Exception if anything wrong
    :param url: the web api url
    :param token: the auth tokens
    :return: returns the string of upload link
    """
    try:
        resp = requests.get(
            url, headers={'Authorization': 'Token {token}'.format(token=token)}
        )
    except requests.exceptions.RequestException as ex:
        raise Exception('Failed during process with exception:' + ex.strerror)
    return resp.json()


def get_timestamp():
    """
    returns a local timestamp string
    :return: string with format yy-mm-dd-HH-MM-SS
    """
    return time.strftime('%y-%m-%d-%H-%M-%S', time.localtime())


def get_clipboard_img(image_format='PNG'):
    """
    use pillow module to read image in clipboard, and convert it to binary data, raise Exception if anything wrong
    :param image_format: default to PNG
    :return: specified img object with given format
    """
    try:
        img = ImageGrab.grabclipboard()

        if img is None:
            raise Exception('No image found in clipboard')

        with io.BytesIO() as OUTPUT:
            img.save(OUTPUT, format=image_format)
            img_data = OUTPUT.getvalue()

        return img_data

    except AttributeError as error:
        raise Exception('Failed while reading data from img with :' + error.__str__())


def upload_image(upload_link, auth_token, image_content, image_type, image_name=get_timestamp()):
    """
    upload given image to seafile server with given parameters
    :param upload_link: upload link to upload image through
    :param auth_token: auth token for authorization
    :param image_content: image object
    :param image_type: image type
    :param image_name: uses the timestamp by deafault
    :return: image's full name if succeed, else raise Exceptions
    """
    image_full_name = image_name + '.' + image_type
    res = requests.post(
        upload_link, data={'filename': image_full_name, 'parent_dir': '/'},
        files={'file': (image_full_name, image_content)},
        headers={'Authorization': 'Token {token}'.format(token=auth_token)}
    )
    if res.status_code == 200:
        return image_full_name
    else:
        raise Exception('Upload failed with :' + str(res.status_code))


def get_image_url(domain, repo_id, image_name, auth_token):
    """
    gets the share link with given image name
    :param domain:
    :param repo_id:
    :param image_name:
    :param auth_token:
    :return: the share link if succeed else raise Exception
    """
    url = '{domain}/api2/repos/{repo_id}/file/shared-link/'.format(domain=domain, repo_id=repo_id)
    path = '/{file}'.format(file=image_name)
    token = 'Token {token}'.format(token=auth_token)

    res = requests.put(url, data={'p': path}, headers={'Authorization': token})

    if res.status_code == 201:
        return res.headers['Location']
    else:
        raise Exception('Failed to get image share link with ' + str(res.status_code))