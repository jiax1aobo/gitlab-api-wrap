from gitlab import Gitlab
import gitlab.const as GLCons
import gitlab.exceptions as GLErr
import logging

logpath = "demo1.log"
logfmt = "%(asctime)s:[%(levelname)s] %(message)s"
dtfmt = "%Y/%m/%d %I:%M:%S %p"
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename=logpath, encoding="utf-8", format=logfmt, datefmt=dtfmt)

global_url = "http://10.20.4.136:82"
global_pat = "glpat-A88kkCnryEx8G_3NcFFs"

def create_group(gl:Gitlab, info:dict, retry:bool=True, times:int=25):
    rc = None
    gid = -1
    if retry:
        left = times
    else:
        left = 1
    while left > 0:
        try:
            grp = gl.groups.create(info)
            assert grp
            gid = grp.get_id()
            logger.info("create_group('%s') with gid('%s')", info['name'], gid)
            rc = True
            break
        except (GLErr.GitlabAuthenticationError, GLErr.GitlabCreateError, AssertionError) as e:
            logger.error("create_group('%s') : %s", info['name'], e)
            rc = False 
            left = left - 1
    return rc, gid

def remove_group(gl:Gitlab, gid:int, retry:bool=True, times:int=25):
    rc = None
    left = times
    if retry:
        left = left - 1
    else:
        left = 1
    while left > 0:
        try:
            gl.groups.delete(gid)
            logger.info("remove_group(gid='%s')", gid)
            rc = True
            break
        except (GLErr.GitlabAuthenticationError, GLErr.GitlabDeleteError) as e:
            logger.error("remove_group(gid:'%s') : %s", gid, e)
            rc = False
            left = left - 1
    return rc

def create_member(gl:Gitlab, gid:int, uid:int, alv:int=GLCons.AccessLevel.DEVELOPER, retry:bool=True, times:int=25):
    rc = None
    mid = None
    if retry:
        left = times
    else:
        left = 1
    while left > 0:
        try:
            grp = gl.groups.get(gid)
            assert grp
            mbr = grp.members.create({'user_id':uid, 'access_level':alv})
            assert mbr
            mid = mbr.get_id()
            logger.info("create_member(uid:'%s',gid:'%s') with mid('%s')", uid, gid, mid)
            rc = True
            break
        except (GLErr.GitlabAuthenticationError, GLErr.GitlabGetError, GLErr.GitlabCreateError, AssertionError) as e:
            logger.error("create_member(uid:'%s',gid:'%s') : %s", uid, gid, e)
            rc = False
            if retry:
                left = left - 1
            else:
                break
    return rc, mid

def remove_member(gl:Gitlab, mid:int, gid:int, retry:bool=True, times:int=25) -> int:
    rc = None
    left = times
    if retry:
        left = times
    else:
        left = 1
    while left > 0:
        try:
            grp = gl.groups.get(gid)
            grp.members.delete(mid)
            logger.info("remove_member(mid:'%s')", mid)
            rc = True
            break
        except (GLErr.GitlabAuthenticationError, GLErr.GitlabGetError, GLErr.GitlabDeleteError) as e:
            rc = False
            logger.error("remove_member(mid:'%s') : %s", mid, e)
            left = left - 1
    return rc

def create_user(gl:Gitlab, info:dict, retry:bool=True, times:int=25):
    rc = None
    uid = -1
    left = times
    if retry:
        left = times
    else:
        left = 1
    while left > 0:
        try:
            user = gl.users.create(info)
            assert user
            uid = user.get_id()
            logger.info("create_user('%s') with uid('%s')", info['username'], uid)
            rc = True
            break
        except (GLErr.GitlabAuthenticationError, GLErr.GitlabCreateError, AssertionError) as e:
            logger.error("create_user('%s') : %s", info['username'], e)
            rc = False 
            left = left - 1
    return rc, uid

def remove_user(gl:Gitlab, uid:int, retry:bool=True, times:int=25):
    rc = None
    left = times
    if retry:
        left = times
    else:
        left = 1
    while left > 0:
        try:
            gl.users.delete(uid)
            logger.info("remove_user(uid:'%s')", uid)
            rc = True
            break
        except (GLErr.GitlabAuthenticationError, GLErr.GitlabDeleteError) as e:
            logger.error("remove_user(uid:'%s') : %s", uid, e)
            rc = False
            left = left - 1
    return rc
    
def create_project(gl:Gitlab, info:dict, retry:bool=True, times:int=25):
    rc = None
    pid = -1
    left = times
    if retry:
        left = times
    else:
        left = 1
    while left > 0:
        try:
            proj = gl.projects.create(info)
            assert proj
            pid = proj.get_id()
            logger.info("create_project('%s') with pid('%s')", info['name'], pid)
            rc = True
            break
        except (GLErr.GitlabAuthenticationError, GLErr.GitlabCreateError, AssertionError) as e:
            logger.error("create_project('%s') : %s", info['name'], e)
            rc = False
            left = left - 1
    return rc, pid

if __name__ == "__main__":
    gl = Gitlab(url=global_url, private_token=global_pat)

    group = {'name':'group6', 'path':'group6'}
    user = {'name':'tu6', 'username':'tu6', 'email':'tu6@test.com',
        'password':'sundb231', 'reset_password':False, 'force_random_password':False}

    rc, gid = create_group(gl=gl, info=group)
    assert rc == True
    rc, uid = create_user(gl=gl, info=user)
    assert rc == True
    rc, mid = create_member(gl=gl, gid=gid, uid=uid, alv=20) 
    assert rc == True

    # gid = 105
    # uid = 83
    # mid = 83
    remove_member(gl=gl, mid=mid, gid=gid)
    remove_user(gl=gl, uid=uid)
    remove_group(gl=gl, gid=gid)
