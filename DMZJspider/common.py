#codng:utf-8
from  config import default_cmd
host = 'https://manhua.dmzj.com'
root_url = 'https://manhua.dmzj.com/'
image_host = 'https://images.dmzj.com/'
#链接
api_url = 'https://manhua.dmzj.com/tags/category_search/{status}-{category}-{region}-{letter}-{theme}-{sort_0}-{sort_1}-{page}.shtml'
api = 'https://sacg.dmzj.com/mh/index.php?c=category&m=doSearch&status={status}&reader_group={category}&zone={region}&initial={letter}&type={theme}{order}&p={page}&callback=NNN'
search_api ='https://sacg.dmzj.com/comicsum/search.php?s={key}'
#一页多少漫画书，网站固定
per_page = 30
#超时重试次数
RETRY = 5
#状态映射
KIND = {
    '0':u'全部',
    '1':u'连载中',
    '2':u'已完结'
}
SORT = {
    '0':False,
    '1':'&_order=t',
    '2':'&_order=h'
}
#快捷命令映射
SHORT_CUT = {
    'all':'000000',
    'all-2':'000002',
    'all-3':'000001',
    '1*':default_cmd,
}
#命令映射
CMD = {
    'status':{'0':'0','1':'2309','2':'2310'},
    'category':{'0':'0','1':'3262','2':'3263','3':'3264','4':'13626'},
    'region':{'0':'0','1':'2304','2':'2306','3':'2305','4':'2307','5':'2308','6':'8435'},
    'letter':{'0':'all','9':'9','A':'A','B':'B','C':'C','D':'D','E':'E','F':'F','G':'G',
              'H':'H','I':'I','J':'J','K':'K','L':'L','M':'M','N':'N','O':'O','P':'P',
              'Q':'Q','R':'R','S':'S','T':'T','U':'U','V':'V','W':'W','X':'X','Y':'Y','Z':'Z'},
    'theme':{'0':'0','1':'5','2':'6','3':'7','4':'8','5':'9','6':'10','7':'11','8':'12','9':'13',
             '1-0':'14','1-1':'17','1-2':'3242','1-3':'3243','1-4':'3244','1-5':'3245','1-6':'3246',
             '1-7':'3248','1-8':'3249','1-9':'3250','2-0':'3251','2-1':'3252','2-2':'3253','2-3':'3254','2-4':'3255',
             '2-5':'3324','2-6':'3325','2-7':'3326','2-8':'3327','2-9':'3328','3-0':'3365','3-1':'4459','3-2':'4518',
             '3-3':'5077','3-4':'5345','3-5':'5806','3-6':'5848','3-7':'6219','3-8':'6316','3-9':'6437',
             '4-0': '7568', '4-1': '7900', '4-2': '13627', '4-3': '4', '4-4': '16',},
    'sort':{'0':['0','0'],'1':['1','0'],'2':['0','1']},
}

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
}