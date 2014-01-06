# -*- coding: utf-8 -*-
'''
Created on 2013年12月17日

字典 forum_cols 键值学院代码 值是一个col_forum_info对象
列表 cols 按序存储学院代码 为forum_cols排序显示

对象 col_forum_info 有3个属性：学院名 学院论坛名 学院论坛链接
对象 headline 存储 每条新闻的 标题 和发布日期 
 

@author: User
'''
import re
import json
import traceback
import ini_redis
from ini_redis import the_redis


fetched_headlines={'col_name:catalog_name':None,}
#每个爬虫返回的ForumColClassifiedHeadlines实例 名字通过反射增加为
#这个字典变量的键-值
#用来在模板中通过名字找到要显示的信息列表
#后来没有使用这个变量 而是在 before_quest中增加的g中了

class ForumColInfo():
    '''一个学院论坛信息 学院名 论坛名 论坛地址'''
    def __init__(self,forum_name='',col_name='',href='',col='',\
                 catalogs=['fores','news']):
        self.col_name=col_name
        self.forum_name=forum_name
        self.href=href
        col=col
        #存储这个学院论坛需要显示的信息类型 比如 预告 新闻 从而对应执行不同的爬虫
        self.catalogs=catalogs

class Headline():
    '''存储一条新闻的信息：标题 日期 连接'''
    def __init__(self,title='',trimed_title='',href='',date='1970-01-01'):
        self.title=title
        self.trimed_title=trimed_title
        self.href=href
        self.date=date

class ForumColClassifiedHeadlines():
    '''工厂 
    一个对象存储一个学院一类信息的列表 和ForumColsHeadlines相比
    不是存储所有学院的信息 只存储一个学院的信息 仍然是存储一类信息
    
    两个类方法 用来实现 序列和对象的相互转换 以便dumps和loads 流程为：
    
    爬取出实例 -> 类方法生成序列 -> 序列dumps为json串 ->json串存入 redis
    redis取出json串(byte) -> 解码为str -> loads为序列对象 (encoding)-> 类方法由序列到实例
    '''
    def __init__(self,name='col_name:catalog_name',headlines=None):
        '''如果参数中headlines=[] 好像所有的实例都会引用这个匿名列表'''
        self.name=name
        self.headlines=headlines
    
    @classmethod
    def instance_to_jsonsequence(cls,obj):
        '''
        不一定用作回调函数 用来将 实例转换为序列对象
        '''
        jsonsequence={obj.name:[]}
        for headline in obj.headlines:
            headline_dic=headline.__dict__
            jsonsequence.get(obj.name).append(headline_dic)
        
        return jsonsequence
    
    @classmethod    
    def jsonsequence_to_instance(cls,fcch_json_d):
        '''
        不能用作回调函数
        回调函数会被调用多次 以便全部解析出字典 每次只解析出字典的一部分
        所以回调函数无法处理整个字典
        这个类方法对loads后的序列对象进行处理并创建实例
        fcch_json_d是fcch_json loads后的序列对象
        fcch_json的格式取决于如何将这个对象json化 设计的格式如下:
        '{"col_name:catalog_name":\
        [\
        {"title":"title","trimed_title":"t...","href":"http://","date":"1970-01-01"},\
        {"title":"title","trimed_title":"t...","href":"http://","date":"1970-01-01"}\
        ]}'
        '''
        dict_key=list(fcch_json_d.keys())[0]
        fcch=ForumColClassifiedHeadlines()
        fcch.name=dict_key
        fcch.headlines=[]
        for headline_d in fcch_json_d[fcch.name]:
                fcch.headlines.append(Headline(title=headline_d['title'],\
                                     trimed_title=headline_d['trimed_title'],\
                                     href=headline_d['href'],\
                                     date=headline_d['date']))
        
        return fcch
    
    def save(self):
        value=json.dumps(\
                         ForumColClassifiedHeadlines.\
                         instance_to_jsonsequence(self)\
                         )
        key=self.name
        the_redis.set(key,value)
    
    @classmethod
    def retrieve(cls,key):
        '''工厂方法 根据key创建一个实例'''
        try:
            fcch_json_d=json.loads(the_redis.get(key).\
                                   decode('utf-8'),encoding='utf-8')
            return ForumColClassifiedHeadlines.jsonsequence_to_instance(fcch_json_d)
        except:
            traceback.print_exc()
            return None
#cols=['phi','eco','law','let','his','con','int','man','lif','inf','met','mac','pha','nur','sug','wei']
#cols=['phi','eco','law','let']
cols=['met','mac']

catalog_name={'fores':'论坛预告','news':'论坛新闻'}#论坛分类信息代码对应的名称 主要用来在模板中显示
forum_cols={
    'phi':ForumColInfo(col_name='哲学与社会发展学院',href='http://www.sps.sdu.edu.cn/sps80/list_all.php?sortid=144',forum_name='爱智论坛',col='phi',catalogs=['fores','news']),
    'eco':ForumColInfo(col_name='经济学院',href='http://www.econ.sdu.edu.cn/yjslt/',forum_name='经济学院研究生系列学术论坛',col='eco',catalogs=[]),
    'law':ForumColInfo(col_name='法学院',href='http://www.law.sdu.edu.cn/header_sbjy_index.site?isDto=1&beanName=catalogsPageBean&pageIndex=1&typeCode=0508&pageSize=10',forum_name='法学院独角兽研究生学术论坛',col='law',catalogs=['news']),
    'let':ForumColInfo(col_name='文学与新闻传播学院',href='http://www.lit.sdu.edu.cn/Article/ShowClass.asp?ClassID=98',forum_name='新闻传播学前沿论坛',col='let',catalogs=['news']),
    'his':ForumColInfo(col_name='历史文化学院',href='http://www.history.sdu.edu.cn/new/cf/',forum_name='长风讲坛',col='his',catalogs=['fores','news']),
    'con':ForumColInfo(col_name='儒学高等研究院',href='http://www.rxgdyjy.sdu.edu.cn/article.php?classid=149',forum_name='尼山大讲堂',col='con',catalogs=['news']),
    'int':ForumColInfo(col_name='国际教育学院',href='http://www.cie.sdu.edu.cn/info/ShowArticle.asp?ArticleID=3685',forum_name='汉语国际教育研究生论坛',col='int',catalogs=[]),
    'man':ForumColInfo(col_name='管理学院',href='http://www.glxy.sdu.edu.cn:1503/',forum_name='管理理论前沿与研究创新研究生论坛',col='man',catalogs=['fores','news']),
    'lif':ForumColInfo(col_name='生命科学学院',href='http://www.lifestu.sdu.edu.cn/subject/yunlvtan2013/',forum_name='蕴绿潭研究生学术论坛',col='lif',catalogs=['fores','news']),
    'inf':ForumColInfo(col_name='信息科学与工程学院',forum_name='研究生学术论坛',col='inf',catalogs=['fores','news']),
    'met':ForumColInfo(col_name='材料科学与工程学院',href='http://www.mlsh.sdu.edu.cn/forum/',forum_name='求材学术论坛',col='met',catalogs=['fores','news']),
    'mac':ForumColInfo(col_name='机械工程学院',href='http://www.mech.sdu.edu.cn/articel.php?id=72',forum_name='研究生学术论坛',col='mac',catalogs=['news']),
    'pha':ForumColInfo(col_name='药学院',href='http://www.pharm.sdu.edu.cn/yjsjy/yjsxslt/',forum_name='研究生学术论坛',col='pha',catalogs=['fores','news']),
    'nur':ForumColInfo(col_name='护理学院',href='http://nc.nursing.sdu.edu.cn/yjs/bbs.asp',forum_name='研究生学术论坛',col='nur',catalogs=['fores','news']),
    'sug':ForumColInfo(col_name='国家糖工程技术研究中心',href='http://www.glycoeng.sdu.edu.cn/more_info.php?category_id=4&class_id=49',forum_name='糖科学论坛',col='sug',catalogs=['fores','news']),
    'wei':ForumColInfo(col_name='威海校区',href='http://www.grad.wh.sdu.edu.cn/yjs/xueshuluntan/index.htm',forum_name='研究生学术论坛',col='wei',catalogs=['fores','news'])
}

if __name__=='__main__':
    #字串 到 序列
    fcch_json_d=json.loads('{"col_name:catalog_name": [{"title":"题目1","trimed_title":"t...","href":"h//","date":"1970-01-01"},\
    {"title":"题目2","trimed_title":"t...","href":"h//","date":"1970-01-01"}]}')
    
    #序列 到 对象
    fcch=ForumColClassifiedHeadlines.jsonsequence_to_instance(fcch_json_d)
    print('ok')
    #对象 到 序列
    fcch_json_d=ForumColClassifiedHeadlines.instance_to_jsonsequence(fcch)
    
    #序列到字串 会编码
    json_str=json.dumps(fcch_json_d)
    #字串到序列 
    json_d=json.loads(json_str, encoding='utf-8')
    print('ok')