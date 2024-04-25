from gitlab import (Gitlab,
    GitlabAuthenticationError as GLAuthErr,
    GitlabCreateError as GLCreateErr,
    GitlabGetError as GLGetErr)
import gitlab.const as GLCons
import logging

logpath = "demo1.log"
logfmt = "%(asctime)s:[%(levelname)s] %(message)s"
dtfmt = "%Y/%m/%d %I:%M:%S %p"
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename=logpath, encoding="utf-8", format=logfmt, datefmt=dtfmt)

global_url = "http://10.20.4.136:82"
global_pat = "glpat-A88kkCnryEx8G_3NcFFs"

def try_do(api, retry:bool=True, times:int=25, **args):
    """ if retry is False, don't set times """
    left = 0
    if retry:
        left = times
    else:
        left = 1
    ret = None
    while left > 0:
        ret = api(args)
        if ret[0]:
            break
        else: 
            left = left - 1
    return ret

def create_group(gl:Gitlab, info:dict):
    grp = None
    stat = False
    try:
        grp = gl.groups.create(info)
        assert grp 
        logger.info("Call of create_group('%s')", info['name'])
        stat = True
    except (GLAuthErr, GLCreateErr) as e:
        logger.error(e)
        stat = False
    return stat, grp.get_id()

if __name__ == "__main__":
    gl = Gitlab(url=global_url, private_token=global_pat)

    user = {'name':'tu61', 'username':'tu61', 'email':'tu61@test.com', 'password':'sundb231'}
    try_do(api=create_group, gl=gl, info=user, retry=True, times=10)