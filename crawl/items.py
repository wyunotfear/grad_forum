# -*- coding: utf-8 -*-
'''
Created on 2013年12月17日

字典 forum_cols 键值学院代码 值是一个col_forum_info对象
列表 cols 按序存储学院代码 为forum_cols排序显示

对象 col_forum_info 有3个属性：学院名 学院论坛名 学院论坛链接
对象 headline 存储 每条新闻的 标题 和发布日期 
 

@author: User
'''
def serialize_fch(fch):#fch:ForumColsHeadlines
    fch_jsonable=dict.fromkeys(fch.__dict__,None)#创建返回用的字典
    #print(fch_jsonable)
    #In [149]: dd=dict.fromkeys(fch.__dict__,[]) 浅拷贝 会出错
    #In [150]: dd
    #Out[150]: 
    #{'con': [], 'eco': [], 'his': [], 'inf': [], 'int': [], 'law': [], 'let': [], 'lif': [], 'mac': [], 'man': [], 'met': [], 'nur': [], 'pha': [], 'phi': [], 'sug': [], 'wei': []}
    for col in cols:
        if len(getattr(fch,col))>0:
            col_headlines=getattr(fch,col)
            for headline in col_headlines:
                temp_headlines=fch_jsonable[col]
                if temp_headlines==None:
                    temp_headlines=[]
                temp_headlines.append(headline.__dict__)
                fch_jsonable[col]=temp_headlines

                #print(fch_jsonable)
    return fch_jsonable

class ForumColInfo():
    '''一个学院论坛信息 学院名 论坛名 论坛地址'''
    def __init__(self,forum_name='',col_name='',href=''):
        self.col_name=col_name
        self.forum_name=forum_name
        self.href=href

class Headline():
    '''存储一条新闻的信息：标题 日期 连接'''
    def __init__(self,title='',trimed_title='',href='',date='1970-01-01'):
        self.title=title
        self.trimed_title=trimed_title
        self.href=href
        self.date=date
class ForumColsHeadlines():
    '''工厂 对象包含所有学院每个学院下需要显示的信息
    多个对象可能存放同一个学院下不同的信息'''
    def __init__(self):
        self.phi=[]
        self.eco=[]
        self.law=[]
        self.let=[]
        self.his=[]
        self.con=[]
        self.int=[]
        self.man=[]
        self.lif=[]
        self.inf=[]
        self.met=[]
        self.mac=[]
        self.pha=[]
        self.nur=[]
        self.sug=[]
        self.wei=[]

cols=['phi','eco','law','let','his','con','int','man','lif','inf','met','mac','pha','nur','sug','wei']
        
forum_cols={
    'phi':ForumColInfo(col_name='哲学与社会发展学院',href='http://www.sps.sdu.edu.cn/sps80/list_all.php?sortid=144',forum_name='爱智论坛'),\
    'eco':ForumColInfo(col_name='经济学院',href='http://www.econ.sdu.edu.cn/yjslt/',forum_name='经济学院研究生系列学术论坛'),\
    'law':ForumColInfo(col_name='法学院',href='http://www.law.sdu.edu.cn/header_sbjy_index.site?isDto=1&beanName=catalogPageBean&pageIndex=1&typeCode=0508&pageSize=10',forum_name='法学院独角兽研究生学术论坛'),\
    'let':ForumColInfo(col_name='文学与新闻传播学院',href='http://www.lit.sdu.edu.cn/Article/ShowClass.asp?ClassID=98',forum_name='新闻传播学前沿论坛'),\
    'his':ForumColInfo(col_name='历史文化学院',href='http://www.history.sdu.edu.cn/new/cf/',forum_name='长风讲坛'),\
    'con':ForumColInfo(col_name='儒学高等研究院',href='http://www.rxgdyjy.sdu.edu.cn/article.php?classid=149',forum_name='尼山大讲堂'),\
    'int':ForumColInfo(col_name='国际教育学院',href='http://www.cie.sdu.edu.cn/info/ShowArticle.asp?ArticleID=3685',forum_name='汉语国际教育研究生论坛'),\
    'man':ForumColInfo(col_name='管理学院',href='http://219.218.118.142:1503/',forum_name='管理理论前沿与研究创新研究生论坛'),\
    'lif':ForumColInfo(col_name='生命科学学院',href='http://www.lifestu.sdu.edu.cn/',forum_name='蕴绿潭研究生学术论坛'),\
    'inf':ForumColInfo(col_name='信息科学与工程学院',forum_name='研究生学术论坛'),\
    'met':ForumColInfo(col_name='材料科学与工程学院',href='http://www.mlsh.sdu.edu.cn/forum/',forum_name='求材学术论坛'),\
    'mac':ForumColInfo(col_name='机械工程学院',href='http://www.mech.sdu.edu.cn/articel.php?id=72',forum_name='研究生学术论坛'),\
    'pha':ForumColInfo(col_name='药学院',href='http://www.pharm.sdu.edu.cn/yjsjy/yjsxslt/',forum_name='研究生学术论坛'),\
    'nur':ForumColInfo(col_name='护理学院',href='http://nc.nursing.sdu.edu.cn/yjs/bbs.asp',forum_name='研究生学术论坛'),\
    'sug':ForumColInfo(col_name='国家糖工程技术研究中心',href='http://www.glycoeng.sdu.edu.cn/more_info.php?category_id=4&class_id=49',forum_name='糖科学论坛'),\
    'wei':ForumColInfo(col_name='威海校区',href='http://www.grad.wh.sdu.edu.cn/yjs/xueshuluntan/index.htm',forum_name='研究生学术论坛')
}