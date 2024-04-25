from gitlab import Gitlab
from gitlab.const import AccessLevel
# import static
from gitlab.exceptions import (
    GitlabAuthenticationError as GLAuthErr,
    GitlabCreateError as GLCreateErr,
    GitlabGetError as GLGetErr,
    GitlabUpdateError as GLUpdateErr
)
import logging
from datetime import datetime, timedelta

logpath = "demo1.log"
logfmt = "%(asctime)s:[%(levelname)s] %(message)s"
dtfmt = "%Y/%m/%d %I:%M:%S %p"
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename=logpath, encoding="utf-8", format=logfmt, datefmt=dtfmt)

global_url = "http://10.20.4.136:82"
global_pat = "glpat-A88kkCnryEx8G_3NcFFs"

def create_branch(gl:Gitlab, pid:int, info:dict, retry:bool=True, times:int=25):
    rc = None
    bid = -1
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
            brch = proj.branches.create(info)
            bid = brch.get_id()
            logger.info("create_branch(pid:'%s',name:'%s') with bid('%s')", pid, info['branch'], bid)
            rc = True
            break
        except (GLAuthErr, GLGetErr, GLCreateErr, AssertionError) as e:
            logger.error("create_branch(pid:'%s',name:'%s') : %s", pid, info['branch'], e)
            rc = False
            left = left - 1
    return rc, bid

def update_member_alv(gl:Gitlab, gid:int, mid:int, alv:int=20, retry:bool=True, times:int=25):
    rc = None
    left = times
    if retry:
        left = times
        assert times > 0
    else:
        left = 1
    while left > 0:
        try:
            grp = gl.groups.get(gid)
            assert grp
            memb = grp.members.get(mid)
            assert memb
            memb.access_level = alv
            memb.save()
            logger.info("update_member_alv(gid:'%s',mid:'%s',alv:'%s')", gid, mid, alv)
            rc = True
            break
        except (GLAuthErr, GLGetErr, GLUpdateErr, AssertionError) as e:
            logger.error("update_member_alv(gid:'%s',mid:'%s',alv:'%s') : %s", gid, mid, alv, e)
            rc = False
            left = left - 1
    return rc


def get_pat_for_uid(gl:Gitlab, uid:int, retry:bool=True, times:int=25):
    rc = None
    ret_pat = None
    left = times
    if retry:
        left = times
        assert times > 0
    else:
        left = 1 
    while left > 0:
        try:
            user = gl.users.get(uid)
            pat_info = {'name':'admin_pat', 'scopes':['api','read_user','read_api',
                        'read_repository','write_repository','sudo']}
            pat = user.personal_access_tokens.create(pat_info)
            ret_pat = pat.asdict()['token']
            rc = True
            logger.info("get_pat_by_uid(uid:'%s') with pat('%s')", uid, ret_pat)
            break
        except (GLAuthErr, GLGetErr, GLCreateErr) as e:
            logger.error("get_pat_by_uid(uid:'%s') : %s", uid, e)
            rc = False
            left = left - 1
    return rc, ret_pat

if __name__ == "__main__":
    gl = Gitlab(url=global_url, private_token=global_pat)

    # proj = gl.projects.get()

    brch = {'branch':'newd', 'ref':'main'}
    # rc, bid = create_branch(gl=gl, pid=37, info=brch)
    # assert rc

    # rc = update_member_alv(gl=gl, gid=111, mid=86, alv=AccessLevel.GUEST)
    # assert rc
    curr = {'uid':1, 'pat':global_pat, 'url':global_url}
    rc, pat = get_pat_for_uid(gl=gl, uid=86)
    assert rc