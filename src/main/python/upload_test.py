import requests

domain = 'http://pacolyon.cn:1953'
auth_token = '5a21181ad42d854c26ab9770d9ddc58804aa5a96'
upload_repo_id = '071ffd04-6d46-4008-a325-e3f4b2b63761'
upload_link = None


def get_upload_link() -> str:
    res = requests.get(
        domain + '/api2/repos/' + upload_repo_id + '/upload-link/',
        headers={'Authorization': 'Token {token}'.format(token=auth_token)}
    )

    return res.json()


def test_upload(file_name : str, image : object):
    global upload_link
    if upload_link is None:
        upload_link = get_upload_link()

    if upload_link is None:
        print("Failed to get upload_link, do it manually")
        return

    res = requests.post(
        upload_link, data={'filename': file_name, 'parent_dir': '/'},
        files={'file': (file_name, image)},
        headers={'Authorization': 'Token {token}'.format(token=auth_token)}
    )

    print('Request returns with ' + str(res.status_code))
