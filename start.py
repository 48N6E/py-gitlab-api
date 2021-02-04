# -*- coding: utf-8 -*-


import os
import gitlab
import sys
import requests


PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_PATH)

"""
gitlab 经常使用到的api
DOC_URL: http://python-gitlab.readthedocs.io/en/stable/
"""
class GitlabAPI():
    def __init__(self):
        PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(PROJECT_PATH)
        config_path = PROJECT_PATH + "/py-gitlab-api/config/python-gitlab.cfg"
        if os.path.exists(config_path):
            self.gl = gitlab.Gitlab.from_config('devgitlab', [config_path])
        elif os.path.exists(os.getenv('HOME') + '/.python-gitlab.cfg'):
            self.gl = gitlab.Gitlab.from_config('devgitlab', [os.getenv('HOME') + '/.python-gitlab.cfg'])
        else:
            print('You need to make sure there is a file named "/etc/python-gitlab.cfg" or "~/.python-gitlab.cfg"')
            sys.exit(5)
    ## login
    def get_users_list(self):
        users = self.gl.users.list()
        print(users)
        return users

    def get_user_id(self):
        users = self.gl.users.list(search='denis.mao')
        print(users)
        return users

    #设置用户角色
    def set_user_role(self):
        user = self.gl.users.list(username='denis.mao')[0]
        attrs = user.customattributes.list()
        users = self.gl.users.list(custom_attributes={'role': 'QA'})
        print(attrs)
        print(users)
        return user



    #List the merge requests available on the GitLab server:
    def list_merge_requests(self):
        mrs = self.gl.mergerequests.list()
        print(mrs)
        return mrs


    def applications(self):
        applications = self.gl.applications.list()
        print(applications)

###组操作
    """
    获取所有组，形成字典，key=组名，value=
    """
    def get_all_groups_id(self) -> dict:
        groups = self.gl.groups.list()
        group_dict = {}
        for id in groups:
            groupname = self.gl.groups.get(id.id).name
            group_dict[groupname] = id.id
        print(group_dict)
        return group_dict

    #Get a group’s detail:
    """
    获取单个组详细信息，默认恢复group object
    """
    def get_group_detail(self,groupname) :
        group_dict = self.get_all_groups_id()
        if groupname in group_dict:
            id = group_dict.get(groupname)
            group = self.gl.groups.get(id)
        else:
            print("{}组不存在".format(groupname))
        print(group)
        return group

    #List a group’s projects
    """
    列出单个组下面的所有项目:
        args:
            groupname 组名
        返回项目名字典value为key，包含id和description
    """
    def get_group_projects(self,groupname) -> dict :
        group_dict = self.get_all_groups_id()
        if groupname in group_dict:
            id = group_dict.get(groupname)
            group = self.gl.groups.get(id)
            projects = group.projects.list()
            projectname = {}
            for name in  projects:
                projectname[name.name] = {'id':name.id,'description':name.description}
        else:
            print("{}组不存在".format(groupname))
        #print(projectname)
        return projectname

    #Create a group
    """
    创建单个组
        args:
            groupname 组名
        返回值，true或者false
    """
    # def create_group(self):
    #     url = "http://10.10.10.245:8090/api/v4/groups"
    #     private_token = 'Q78JYAUzUqvPSdkVessf'
    #     user_info = [
    #         ('test789', 'test789'),
    #         ('test456', 'test456')
    #     ]
    #     payload = "name=%s&path=%s&"
    #     for item in user_info:
    #         data = (payload % item) + "private_token=" + private_token
    #         response = requests.post(url, data=data)

        #group = self.gl.groups.create({'name': 'group1', 'path': 'group1'})


    """
    创建单个组下的子组
        args:
            name 组名
            parent 上级组名
        返回值，true或者false
    """
    def create_subgroup(self,name,parent):
## 这里要注意创建分组的时候.data参数中需要指定name,path,parent_id(就是上一级分组的ID)三个参数.在之前的调试过程中,因为没有指定parent_id,程序一直抛出401权限认证失败的异常.
        group_id = self.get_group_detail(parent).id
        group = self.gl.groups.create({'name': name, 'path': name,"parent_id": group_id })


    """
    创建单个组
        args:
            name 组名
        返回值，true或者false
    """
#todo
    def create_group(self,name):
        ## 这里要注意创建分组的时候.data参数中需要指定name,path,parent_id(就是上一级分组的ID)三个参数.在之前的调试过程中,因为没有指定parent_id,程序一直抛出401权限认证失败的异常.
        #group_id = self.get_group_detail(parent).id
        group = self.gl.groups.create({'name': name,'path':name,})
#todo
    def change_owner_group(self,goupname):
        group = self.get_group_detail(goupname)
        group.description = 'My awesome group'


if __name__ == '__main__':
    test = GitlabAPI()
    #test.get_users_list()
    #test.get_user_id()
    #test.set_user_role()
    #test.all('jenkins')
    #test.group
    #test.get_all_groups_id()
    #test.get_group_detail("hnp")
    #test.get_group_projects("DM")
    #test.create_subgroup('gouptest','hnp')
    #test.change_owner_group('gouptest')
    test.create_group("test1")





