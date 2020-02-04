
from config import *
from api  import API
from deco import register

class FangLine:

    def __init__(self,cookie=COOKIE):
        self.headers = {
            'cookie':cookie,
            'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Origin':'http://www.fangline.cn',
            'Host':	'www.fangline.cn',
            'X-Requested-With':	'XMLHttpRequest',
        }

    @register('post',API.List)
    def SearchSellHouses(self, page=1, area=None, subArea=None):
        '''
        出售的房源
        :param page:结果页码
        :param area:区域，如：朝阳,西城
        :param subArea:子区域，如：朝阳-三元桥,朝阳-CBD
        '''
        config = {
            'params': {
            },
            'data': {
                "pageNo": page,
                "pageSize": 30,
                "bizType": "sell",
                'districtNames': area,
                'areas': subArea,
                "filterParam": "3,2,4",
                "sort": "createTime"
            },
            'headers': self.headers

        }
        return config

    @register('post', API.List)
    def SearchRentHouses(self, page=1,area=None,subArea=None):
        '''
        出租的房源
        :param page:结果页码
        :param area:区域，如：朝阳
        :param subArea:子区域，如：朝阳-三元桥,朝阳-CBD
        '''
        config = {
            'params': {
            },
            'data': {
                "pageNo": page,
                "pageSize": 30,
                "bizType": "rent",
                'districtNames': area,
                'areas': subArea,
                "filterParam": "3,2,4",
                "sort": "createTime"
            },
            'headers': self.headers

        }
        return config

    @register('post',API.Base)
    def SearchWantSellHouses(self, page=1, area=None, subArea=None):
        '''
        求购的房源
        :param page:结果页码
        :param area:区域，如：朝阳
        :param subArea:子区域，如：朝阳-三元桥,朝阳-CBD
        '''
        config = {
            'params': {
                'method': 'listResources'
            },
            'data': {
                "pageNo": page,
                "pageSize": 30,
                "bizType": "wantSell",
                'subscribeDistrict': area,
                'subscribeArea': subArea,
                "status": "3,2,4",
                "orderCol": "createTime"
            },
            'headers': self.headers

        }
        return config

    @register('post', API.Base)
    def SearchWantRentHouses(self, page=1, area=None, subArea=None):
        '''
        求租的房源
        :param page:结果页码
        :param area:区域，如：朝阳
        :param subArea:子区域，如：朝阳-三元桥,朝阳-CBD
        '''
        config = {
            'params': {
                'method': 'listResources'
            },
            'data': {
                "pageNo": page,
                "pageSize": 30,
                "bizType": "wantRent",
                'subscribeDistrict': area,
                'subscribeArea': subArea,
                "status": "3,2,4",
                "orderCol": "createTime"
            },
            'headers':self.headers
        }
        return config

    @register('post',API.Query)
    def GetHouseDetail(self,Id):
        '''
        房源详情,需设置cookie
        :param Id: 房源id，非houseId
        '''
        config = {
            'data': {
                'id':Id,
            },
            'headers': self.headers
        }
        return config