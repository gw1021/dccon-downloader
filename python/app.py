import requests
import os

PROTOCOL_PREFIX = 'https://'


def download(num=None):
    con_id = num
    if num is None:
        con_id = input("DCCON NUM :")
    if con_id == '':
        exit()

    loading_chars = ['|', '/', '-', '\\']
    package_url = f'{PROTOCOL_PREFIX}dccon.dcinside.com/index/package_detail'
    download_url = f'{PROTOCOL_PREFIX}dcimg5.dcinside.com/dccon.php?no='
    # Open session
    s = requests.Session()
    # Get Cookie (ci_c)
    r = s.get(package_url,
              headers={'X-Requested-With': 'XMLHttpRequest'})
    # Get Json (ci_c to ci_t)
    req = s.post(package_url,
                 headers={'X-Requested-With': 'XMLHttpRequest'},
                 data={'ci_t': r.cookies['ci_c'], 'package_idx': con_id})

    json_data = req.json()

    default_dir = os.path.dirname(os.path.abspath(__file__))
    download_path = os.path.join(default_dir, json_data['info']['title'])

    try:
        os.makedirs(download_path)
    except Exception as e:
        print(e)
    else:
        loading_cnt = 0

        for item in json_data['detail']:
            print(f'\rLoading... ({loading_chars[loading_cnt]})', end='')
            loading_cnt = (loading_cnt + 1) % 4
            filename = item['idx'] + '.' + item['ext']
            image = s.get(download_url + item['path'],
                          headers={'Referer': f'{PROTOCOL_PREFIX}dccon.dcinside.com/'})
            with open(os.path.join(download_path, filename), 'wb') as fd:
                for chunk in image.iter_content(chunk_size=128):
                    fd.write(chunk)
                fd.close()
        s.close()


if __name__ == "__main__":
    download()
