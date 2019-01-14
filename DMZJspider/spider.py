#coding:utf-8
import os
import re
import copy
import json
import execjs
import requests
from config import *
from common import *
from threads import CrawlThread
from requests.adapters import HTTPAdapter
from tools import show_tips,handle_key
from string import digits,ascii_letters,ascii_uppercase
from bs4 import BeautifulSoup as bs

class Spider(object):
    def __init__(self):
        self.books_count = 0
        self.page_count  = 0
        self.offset      = 0
        self.c_root      = os.getcwd()
        self.params      = None
        self.session     = requests.Session()
        self.session.mount('http://', HTTPAdapter(max_retries=RETRY))
        self.session.mount('https://', HTTPAdapter(max_retries=RETRY))

    @staticmethod
    def check_input(inputs):
        real_input = inputs.strip().replace(' ', '')
        if real_input in SHORT_CUT.keys():
            return SHORT_CUT[real_input]
        elif '-' in real_input:
            if len(real_input) != 8:
                print(u'>> [错误] 你的搜索命令字符串不正确，请确保每一个搜索项都被包含到。')
                return False
            else:
                rs = 0
                rc = 0
                if   real_input[3] not in ascii_uppercase :
                    if   real_input[3] not in ['0','9']:
                        print(u'>> [错误] 你的搜索命令字符串不正确，请确保每一个搜索项都被包含到。')
                        return False
                    else:
                        rc+=1
                for r in real_input:
                    if r in ascii_letters:
                        rs+=1
                if rs != 1:
                    if rc !=1:
                        print(u'>> [错误] 你的搜索命令字符串不正确，请确保每一个搜索项都被包含到。')
                        return False
                else:
                    if rc !=0:
                        print(u'>> [错误] 你的搜索命令字符串不正确，请确保每一个搜索项都被包含到。')
                        return False
                return real_input
        elif len(real_input) != 6:
            print(u'>> [错误] 你的搜索命令字符串不正确，请确保每一个搜索项都被包含到。')
            return False
        else:
            rs = 0
            for r in real_input:
                if r in digits:
                    rs += 1
                if r in ascii_uppercase and real_input.find(r) == 3:
                    rs += 1
            if rs != 6 :
                print(u'>> [错误] 你的搜索命令字符串不正确，请确保每一个搜索项都被包含到。')
                return False
            return real_input

    def download_many_or_one(self):
        while 1:
            model = input(u'>> 请输入搜索下载的模式，多本下载请输入 0 ，单本下载请输入 1 :').strip().replace(' ','')
            if model == '1':
                return 0
            elif model == '0':
                return 1
            else:
                print(u'>> 无效命令。')
                continue

    def parse_cmd(self,cmd):
        status = CMD['status'][cmd[0]]
        category = CMD['category'][cmd[1]]
        region = CMD['region'][cmd[2]]
        letter = CMD['letter'][cmd[3]]
        if '-' in cmd:
            index = cmd.index('-')
            code = cmd[index-1]+'-'+cmd[index+1]
            theme = CMD['theme'][code]
            theme_name  = NAMES['theme'][code]
        else:
            theme = CMD['theme'][cmd[4]]
            theme_name = NAMES['theme'][cmd[4]]
        order = SORT[cmd[-1]]
        order = order if order else ''
        self.params ={
            'status':status,
            'category':category,
            'region':region,
            'letter':letter,
            'theme':theme,
            'order':order,
            'page':1
        }
        url = api.format(**self.params)
        status_name=NAMES['status'][cmd[0]]
        category_name = NAMES['category'][cmd[1]]
        region_name = NAMES['region'][cmd[2]]
        kind = os.sep.join([status_name,region_name,category_name,theme_name])
        return url,kind

    def show_input_and_parse(self):
        while 1:
            inputs = input(u'>> 请根据上面的功能介绍，输入你的命令字符串:')
            real_inputs = self.check_input(inputs)
            if real_inputs:
                break
        path = input(u'>> 请输入保存路径,输入 1 则按照配置路径保存:').strip()
        path = path if path !='1' else download_dir
        url,status = self.parse_cmd(real_inputs)
        self.d_root = os.path.join(self.c_root, os.path.join(path, status))
        return url

    def __check_local(self,path):
        if os.path.exists(os.path.join(self.d_root,path)):
            return True
        else:
            return False

    def get_page_count(self,url):
        header['referer']=url
        s = requests.Session()
        while 1:
            resp = s.get(url,headers=header,timeout=60)
            if resp.status_code == 200:
                break
        json_data = json.loads(re.findall(r'NNN\((.+)\);',resp.text)[0])
        self.page_count = json_data['page_count']
        self.books_count = json_data['data_count']

    def search_and_download_book(self):
        while 1:
            book_name = input(u'>> 请输入你要搜索下载的漫画名称:').strip().replace(' ', '')
            url = search_api.format(key=book_name)
            res = self.session.get(url,headers=header)
            if res.status_code!=200:
                continue
            data = res.text.replace('var g_search_data = ','').replace(';','')
            try:
                book_data = json.loads(data)
            except Exception as e:
                book_data = json.loads(data.replace('null','\"\"').replace('\n',''))
            if not book_data:
                print(u'>> 没有找到《%s》相关结果.'%book_name)
                continue
            else:
                print(u'>> 共找到 %d 本相关漫画:'%len(book_data))
                for i in book_data:
                    print(u'* ID:%s 《%s》 作者: %s'%(i['id'],i['name'],i['comic_author']))
                if len(book_data)==1:
                    book = book_data[0]
                else:
                    while 1:
                        real_one = input(u'>> 请输入以上你要下载的漫画的ID:').strip().replace(' ', '')
                        try:
                            book = [i for i in book_data if i['id'] == real_one][0]
                            break
                        except Exception as e:
                            print(u'>> 漫画ID错误.')
                            continue
                try:
                    href = 'https:' + book['comic_url']
                    name = book['name']
                    C = book['comic_url'].split('/')[-1][0].upper()
                    path = input(u'>> 请输入保存路径,输入 1 则按照配置路径保存:').strip()
                    path = path if path != '1' else download_dir
                    self.d_root = os.path.join(self.c_root, path)
                    print(u'>> 开始下载《%s》' % name)
                except Exception as e:
                    print(u'>> [错误] 解析接口数据失败:%s' % book)
                    return
                else:
                    headers = copy.deepcopy(header)
                    headers['referer'] = href
                    self.get_book_chapters(href, name, C, headers)
                    print(u'>> [任务完成] 漫画《%s》下载完成。'%name)

    def start(self):
        if self.download_many_or_one():
            show_tips()
            url = self.show_input_and_parse()
            self.get_page_count(url)
            for i in range(1,self.page_count+1):
                self.params.update({'page': i})
                print(api.format(**self.params))    
                try:
                    link = api.format(**self.params)
                    self.get_page_books_link(link)
                except Exception as e:
                    print(u'>> [错误] 抓取搜索结果第 %d 页失败。msg:%s'%(i,e))
        else:
            self.search_and_download_book()

    def get_page_books_link(self,url):
        headers = copy.deepcopy(header)
        headers['referer']=url
        while 1:
            resp = self.session.get(url,headers=headers)
            if resp.status_code != 200:
                continue
            res = resp.text
            json_data = json.loads(re.findall(r'NNN\((.+)\);', res)[0])
            books = json_data['result']
            ok_or_error = json_data['status']
            if ok_or_error=='ERROR':return
            for i in books:
                try:
                    href = host+i['comic_url']
                    name = i['name']
                    print(u'>> 开始下载《%s》'%name)
                    C    = i['comic_url'].split('/')[1][0].upper()
                except Exception as e:
                    print(u'>> [错误] 解析接口数据失败:%s'%i)
                    return
                else:
                    self.get_book_chapters(href,name,C,headers)
             return

    def get_book_chapters(self,href,name,C,headers):
        name = handle_key(name)
        _dir = os.path.join(C,name)
        _path = os.path.join(self.d_root,_dir)
        if not self.__check_local(_dir):
            os.makedirs(_path)
        resp = self.session.get(href,headers =headers )
        soup = bs(resp.text,'lxml')
        several_parts_names = [handle_key(i.h2.text) for i in soup('div',class_="h2_title2")][:-2]
        main_page_parts = soup('div',class_='cartoon_online_border')
        other_page_parts = soup('div',class_='cartoon_online_border_other')
        main_page_part_name = several_parts_names[0]
        if len(several_parts_names)==1:
            for part in main_page_parts:
                self.download_part(part,_path,name,main_page_part_name)
        elif len(several_parts_names)>1:
            other_page_parts_names = several_parts_names[1:]
            other_parts_len = len(other_page_parts)
            for x in range(other_parts_len):
                other_part = other_page_parts[x]
                try:
                    other_part_name = other_page_parts_names[x]
                except:
                    print(u'>> [错误] 解析《%s》作品数(%d)与对应章节卡数(%d)不符合。'%(name,len(several_parts_names),other_parts_len))
                    return
                else:
                    o_dir = os.path.join(_dir, other_part_name)
                    o_path = os.path.join(self.d_root, o_dir)
                    self.download_part(other_part,o_path,name,other_part_name)
            for part in main_page_parts:
                m_dir = os.path.join(_dir, main_page_part_name)
                m_path = os.path.join(self.d_root, m_dir)
                self.download_part(part,m_path,name,main_page_part_name)

    def download_part(self,part,_path,name,full_name):
        lis = part('ul')[0]('li')
        for li in lis:
            try:
                page_name = li.a.text
                page_name = handle_key(page_name)
                page_url = host + li.a['href']
                _c_path = os.path.join(_path, page_name)
                if not self.__check_local(_c_path):
                    os.makedirs(_c_path)
            except Exception as e:
                print(u'>> [错误] 解析《%s》漫画章节页面数据出错。msg:%s'%(name,e))
                return
            else:
                try:
                    self.download_pics(page_url, _c_path,full_name+'-'+page_name)
                except Exception as e:
                    print(u'>> [错误] 解析《%s》漫画具体页脚本失败 '%(full_name+'-'+page_name))
                    continue

    def download_pics(self,url,path,full_name):
        headers = header
        headers['referer']=url
        headers.update({
            'accept': 'text/html, application/xhtml+xml, application/xml;q = 0.9, image/webp, image/apng, */*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN, zh;q = 0.9',
            'cache-control': 'max-age = 0',
        })
        try:
            resp = self.session.get(url,headers=headers,timeout=60)
            html = bs(resp.text,'lxml')
        except Exception as e:
            print(u'>> [失败] 获取漫画《%s》具体漫画页失败。msg:%s'%(full_name,e))
        else:
            try:
                script = html('script')[0].text.replace('\n','')
            except Exception as e:
                print(u'>> [错误] 获取《%s》漫画页JavaScript脚本出错。msg:%s'%(full_name,e))
                return
            else:
                func = '''
                function get_pages() {
                    %s
                    return eval(pages);
                }
                '''%script
                JsContext = execjs.compile(func)
                r = JsContext.call('get_pages')
                pages = r
                total = len(pages)
                offset = 0
                start = 1
                counter = 0
                while 1 :
                    threads = []
                    results = []
                    if offset >= total:
                        print(u'>> [完成] 《%s》 [总数:%d 页,下载成功：%d 页,下载失败：%d 页]' % (full_name, total,counter, total - counter))
                        return
                    count = total - offset if total - offset < MAX else MAX
                    offset += count
                    for i in  range(start,offset+1):
                        url = image_host+pages[i-1]
                        suffix = url.split('.')[-1]
                        _p_name = os.path.join(path,u'第%d页.%s'%(i,suffix))
                        if self.__check_local(_p_name):
                            counter+=1
                            continue
                        else:
                            res = CrawlThread(self.__download, args=(url,_p_name,headers))
                            threads.append(res)
                    for i in threads:
                        i.start()
                    for i in threads:
                        i.join()
                        results.append(i.get_result())
                    for res in results:
                        if res:
                            counter += 1
                    start = offset + 1

    def __download(self,url,name,headers):
        try:
            resp = self.session.get(url, headers=headers,timeout=60)
            with open(name,'wb') as f:
                f.write(resp.content)
        except Exception as e:
            print(u'>> [失败]  %s 下载失败 msg:%s'%(name,e))
            return False
        else:
            print(u'>> [新增]  %s 下载成功。'%name)
            return  True
























