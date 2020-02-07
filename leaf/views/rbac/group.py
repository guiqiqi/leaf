"""用户组管理视图函数"""

# from . import rbac

# from ...api import wrapper
# from ...rbac.model import User
# from ...rbac.model import Group


# @rbac.route("/group/<string:groupid>", methods=["GET"])
# @wrapper.require("leaf.views.rbac.group.query")
# @wrapper.wrap("group")
# def query_group_byid(groupid: str) -> Group:
#     """根据给定的 id 查找用户组"""
