import requests

global_url = "http://10.20.4.136:82/"
global_pat = "glpat-A88kkCnryEx8G_3NcFFs"
global_hdr = {"PRIVATE-TOKEN": global_pat}

def print_response(resp:requests.Response):
    ret = {
        'text': resp.text,
        'content': resp.content,
        'json': resp.json(),
        'headers': resp.headers,
        'cookies': resp.cookies,
        'url': resp.url,
        'status': resp.status_code
    }
    print(ret)

def api_demo1():
    api = global_url + 'api/v4/groups'
    dat = {"pagination": "keyset", "per_page": 20, "order_by": "id", "sort": "asc"}
    hdr = global_hdr
    req = requests.get(url=api, headers=hdr, data=dat)
    print("Status Code:", req.status_code)
    print("Text:", req.text)
    print("Content:", req.content)
    print("JSON:", req.json())
    print("Headers:", req.headers)
    print("Cookies:", req.cookies)
    print("URL:", req.url)


def api_create_group(info:dict) -> int:
    api = global_url + "api/v4/groups"
    hdr = {**global_hdr, "Content-Type": "application/json"}
    req = requests.post(url=api, headers=hdr, json=info)
    return req.status_code

def api_create_user(info:dict) -> int:
    api = global_url + "api/v4/users"
    hdr = {**global_hdr, "Content-Type": "application/json"}
    res = requests.post(url=api, headers=hdr, json=info)
    if res.status_code != 201:
        print_response(res)
    return res.status_code

if __name__ == "__main__":
    # api_demo1()

    # create group
    # group_info = {'name':'group4', 'path':'group4'}
    # api_create_group(group_info)

    # create user
    user_info = {'email':'u1@test.com', 'name':'测试用户1', 'username':'u1'}
    rc = api_create_user(user_info)
    assert rc == 201