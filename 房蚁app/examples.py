
from config import *
from dbhelper import Database
from fangline import FangLine

mongo = Database(MONGO)
mongo.connect()

'''
    1. 获取杭州所有 出售 房源
    2. 将每一个房源和其详情存储进数据库
    
    tips:
    1.传入的cookie必须是登陆了 房蚁浙江站 的cookie，选择地区为 杭州
'''

def GetHouses(cookie,cate='sell',page=1):
    """
    :param cookie: 用户cookie
    :param cate: 四个类别：sell,rent,wantSell,wantRent
    """
    fl = FangLine(cookie)
    types = {
        'sell':fl.SearchSellHouses,
        'rent':fl.SearchRentHouses,
        'wantSell':fl.SearchWantSellHouses,
        'wantRent':fl.SearchWantRentHouses,
    }
    tip = {
        'sell': '出售',
        'rent': '出租',
        'wantSell': '求售',
        'wantRent': '求租',
    }
    table = MONGO[cate]
    total = 0
    count = 0
    while 1:
        print(f'开始爬取第{page}页')
        amount=0
        result = types[cate](page=page)
        if not total:
            total = result.get('total')
            print(f'获取到 当前地区 {tip[cate]} 房源总数为:{total}')
        rows = result.get('rows',[])
        for i in rows:
            _id = i['id']
            asks = mongo.select({'id':{'=':_id}},tname=table)
            if asks:
                continue
            mongo.save(i,tname=table)
            try:
                detail = fl.GetHouseDetail(_id)
                if detail:
                    ret_id = detail['data']['id']
                    ask = mongo.select({'id': {'=': ret_id}}, tname=MONGO['detail'])
                    if not ask:
                        detail.update({
                            'id':ret_id
                        })
                        mongo.save(detail, tname=MONGO['detail'])
            except:
                pass
            count += 1
            amount += 1
        print(f'已保存 房源:{count}个')
        if amount == 0:
            print('房源已爬取完毕。')
            return
        page += 1



