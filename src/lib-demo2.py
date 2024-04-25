from gitlab import Gitlab
from gitlab.const import AccessLevel
import static
from gitlab.exceptions import (
    GitlabAuthenticationError as GLAuthErr,
    GitlabCreateError as GLCreateErr,
    GitlabDeleteError as GLDeleteErr,
    GitlabListError as GLListErr,
    GitlabGetError as GLGetErr
)

def create_mr(gl:Gitlab, pid:int, info:dict, retry:bool=True, times:int=25):
    rc = None
    mrid = -1
    left = times
    if retry:
        left = times
        assert times > 0
    else:
        left = 1
    while left > 0:
        try:
            proj = gl.projects.get(pid)
            assert proj
            mr = proj.mergerequests.create(info)
            mrid = mr.get_id()
            print(mr.asdict())
            static.logger.info("create_mr(pid:'%s',b'%s'->b'%s') with mrid('%s')", pid, info['source_branch'], info['target_branch'], mrid)
            rc = True
            break
        except (GLAuthErr, GLGetErr, GLCreateErr, AssertionError) as e:
            static.logger.error("create_mr(pid:'%s',b'%s'->b'%s') : %s", pid, info['source_branch'], info['target_branch'], e)
            rc = False
            left = left - 1
    return rc, mrid

def get_mr_stat_by_id(gl:Gitlab, mrid:int, retry:bool=True, times:int=25):
    rc = None
    sta = None
    left = times
    if retry:
        left = times
        assert left > 0
    else:
        left = 1
    while left > 0:
        try:
            projs = gl.projects.list(search=mrid)
            assert projs[0].asdict()['name'] == mrid 
            pid = projs[0].get_id()
            static.logger.info("get_pid_by_name(name:'%s') with pid('%s')", mrid, pid)
            rc = True
            break
        except (GLAuthErr, GLListErr, GLGetErr) as e:
            static.logger.error("get_pid_by_name(name:'%s') : %s", mrid, e)
            rc = False
            left = left - 1
    return rc, pid

def get_pid_by_name(gl:Gitlab, name:str, retry:bool=True, times:int=25):
    rc = None
    pid = -1
    left = times
    if retry:
        left = times
        assert left > 0
    else:
        left = 1
    while left > 0:
        try:
            projs = gl.projects.list(search=name)
            assert projs[0].asdict()['name'] == name
            pid = projs[0].get_id()
            static.logger.info("get_pid_by_name(name:'%s') with pid('%s')", name, pid)
            rc = True
            break
        except (GLAuthErr, GLListErr, GLGetErr) as e:
            static.logger.error("get_pid_by_name(name:'%s') : %s", name, e)
            rc = False
            left = left - 1
    return rc, pid

def get_uid_by_name(gl:Gitlab, name:str, retry:bool=True, times:int=25):
    rc = None
    uid = -1
    left = times
    if retry:
        left = times
        assert left > 0
    else:
        left = 1
    while left > 0:
        try:
            users = gl.users.list(search=name)
            assert users[0].asdict()['name'] == name
            uid = users[0].get_id()
            static.logger.info("get_uid_by_name(name:'%s') with uid('%s')", name, uid)
            rc = True
            break
        except (GLAuthErr, GLListErr, GLGetErr) as e:
            static.logger.error("get_uid_by_name(name:'%s') : %s", name, e)
            rc = False
            left = left - 1
    return rc, uid

def get_gid_by_name(gl:Gitlab, name:str, retry:bool=True, times:int=25):
    rc = None
    ret_gid = -1
    left = times
    if retry:
        left = times
        assert left > 0
    else:
        left = 1
    while left > 0:
        try:
            grp = gl.groups.list(search=name)
            assert grp[0].asdict()['name'] == name
            ret_gid = grp[0].get_id()
            static.logger.info("get_gid_by_name(name:'%s') with gid('%s')", name, ret_gid)
            rc = True
            break
        except (GLAuthErr, GLListErr, GLGetErr) as e:
            static.logger.error("get_gid_by_name(name:'%s') : %s", name, e)
            rc = False
            left = left - 1
    return rc, ret_gid

if __name__ == "__main__":
    gl = Gitlab(url=static.global_url, private_token=static.global_pat)

    mr = {'title':'test mr api','source_branch':'newb', 'target_branch':'main',
          'assignee_id':1, 'remove_source_branch': False}
    # rc, mrid = create_mr(gl=gl, pid=37, info=mr)

    # rc, pid = get_pid_by_name(gl=gl, name='mrproj')
    # assert rc
    # print('pid:', pid)

    # rc, uid = get_uid_by_name(gl=gl, name='胡勋棋')
    # assert rc
    # print('uid:', uid)

    rc, gid = get_gid_by_name(gl=gl, name='mrtest')
    assert rc