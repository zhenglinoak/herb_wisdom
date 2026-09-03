from chat.dao import HistoryDao
from common import ResponseUtil


def get_menu(d):
    r1=HistoryDao.get_menu(d['user_name'])
    if not r1:
        return ResponseUtil.response(code=200,msg="暂无聊天记录",data=[])
    r2=[]
    for i in r1:
        r2.append({
            "title":i['question'],
            "history_id":i['history_id']
        })
    return ResponseUtil.response(code=200,msg="获取成功",data=r2)



def get_history_content(history_id):
    r1=HistoryDao.get_history_content(history_id)
    r2=[]
    for i in r1:
        r2.append({
            "sender":"user",
            "text":i['question']
        })
        r2.append({
            "sender":"ai",
            "text":i['answer']
        })

    return ResponseUtil.response(code=200,msg="获取成功",data=r2)

def get_history_mysql(history_id):
    r1=HistoryDao.get_history_content(history_id)
    return r1



def delete_history(history_id):
    r=HistoryDao.delete_history(history_id)
    if r:
        return ResponseUtil.response(code=200,msg="删除成功")
    else:
        return ResponseUtil.response(code=500,msg="删除失败")



if __name__ == '__main__':
    # data={'user_name': 'zz', 'exp': 1786475515, 'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJ6eiIsImV4cCI6MTc4NjQ3NTUxNX0.nNJcowwygc8pnhcMWLyTgrL50lG1bwB0uOvZxdpRjOk'}
    # print(get_menu(data))

    print(get_history_mysql(47))