# -*- coding: utf-8 -*-
import functools
import re
from aip import AipNlp

from util import listutils

any_backspaces = re.compile("\b+")

_BAIDU_ACCOUNTS = [
    {'app_id': '15428255', 'api_key':	't2OOUBpi0rREk2fXirNYp4G7', 'secret_key': 'gmvQVV0gllz2ICkWQUpMkzEsUumOGXax'},
    {'app_id': '15428373', 'api_key':	'tt0AepbE391GfGw4bzZnLt3i', 'secret_key': 'vXRxjuB0vCZYvuDmnlRPxq7Z93yLrzAp'},
    {'app_id': '15457807', 'api_key':	'9poNFltyjRNXULRYx7v50qD6', 'secret_key': '3Lexv9vkXkMgGo9SK16sE5kQdxfAOMzF'},
    {'app_id': '15457866', 'api_key':	'QvBt8Ghv82phGXO8gr6COtuE', 'secret_key': 'mDifAvCtTG9YyDjoYyYyVwtGXTE2Wl3g'},
    {'app_id': '15457932', 'api_key':	'5FUUSa9PSpSeGWfduFuCr908', 'secret_key': 'sPhwSynOoeAah1zZP7YI9GC9rqxhRetT'},
    {'app_id': '15458058', 'api_key':	'At1TkFUfeOkt4bm9BuKMeQNz', 'secret_key': 'gsurUGRixcfgksNNmncjdkVkWb3e5RBa'},
    {'app_id': '15458141', 'api_key':	'G108AmHG1EZrQOb3IGiPHMF3', 'secret_key': 'WFnQHkqndb3UlDLheHSSCq3lgjAsTd8s'},
    {'app_id': '15458224', 'api_key':	'DGj4ApzN5ENwxQg53ExIUjaH', 'secret_key': 'LGxSxrPjBNtSYdqOInEBzNjhWjw4P3Wz'},
    {'app_id': '15458285', 'api_key':	'5DDoGQlZOng6pFlGffMKQAbH', 'secret_key': 'hczWHLdiNRXzTe3ak3cyEr6Dwd4B31CP'},
    {'app_id': '15458333', 'api_key':	'yTFh9kdS8Vl8DPVTmYfgGGQi', 'secret_key': '0YYjcFm9UhwuPM4O9SNdKKPGm7WwN14Q'},
    {'app_id': '15458414', 'api_key':	'hw2kPI2pCNAZePumGZYyQzzI', 'secret_key': '2FfIfsk7X7AH9WEKvThbmc2PhlhkXh1R'},
    {'app_id': '15458460', 'api_key':	'j20jM8vAVne3vdOlKVGGo5q2', 'secret_key': 'GGID8wvKDlkLdj0KaHqh1KTn0y6kK70z'},
    {'app_id': '15458500', 'api_key':	'UDyyKMT0E2NTuII5dLD3CLn5', 'secret_key': 'MlywXXfkNSA6LOrk4ffqdplUGsOeVCB0'},
    {'app_id': '15458536', 'api_key':	'bDIPCmRtxID3be9EYz92hSo6', 'secret_key': 'KU0elddpDeiTG87oLRgx1fuFGzNzktXg'},
    {'app_id': '15458562', 'api_key':	'FLO1sjwme5ZrFfhnzdRi5RBK', 'secret_key': 'qwZYkxZDRIIb4DTxzKFRuqDPFZuU3WLK'},
    {'app_id': '15458610', 'api_key':	'PFXz6Nw0H9W2oGOfqFtmSdX6', 'secret_key': 'irdL4dgfw4w1ymU2kPnw3VVMv9pukm6q'},
    {'app_id': '15458626', 'api_key':	'6lYWnuEPDMABWrlb2AIbzwG4', 'secret_key': 'kvkBC6YvpgtS6evBVH4xT14WRGyQIyAy'},
    {'app_id': '15458693', 'api_key':	'Te8obDQ1WOntx8yUT5iUWIHj', 'secret_key': 'gGhCETndRplSovfvxaEL3sY5F8irlW2R'},
    {'app_id': '15458720', 'api_key':	'8KaaBEbZwQLj7dLCGwDzgdWu', 'secret_key': 'IRfijMcwH6MHqsw5f5bkVHUjqTUXCGSq'},
    {'app_id': '15459015', 'api_key':	'hBQFFXCyC9pSREfbBt8rGF1s', 'secret_key': 'y87DrDMpg5tPHDObWtI3S1FIqfi2jeHQ'},
]
BAIDU_ACCOUNTS = listutils.cycle(_BAIDU_ACCOUNTS)

ORG_QUALIFIED = [
    "宣布.*盈利",
    "宣布.*裁员",
    "宣布.*计划",
    "进入",
    "加盟",
    "加入",
    "当上",
    "先后任",
    "担任",
    "晋升",
    "改任",
    "调往",
    "启动",
    "位居",
    "月任",
    "升任",
    "任职",
    "回归",
    "出任",
    "当学徒",
    "接掌",
    "接替",
    "执导",
    "率领",
    "聘为",
    "聘任",
    "现任",
    "聘请",
    "投身",
    "供职",
    "被任命",
    "就职于",
    "离开",
    "辞去",
    "辞职",
    "离职",
    "创办",
    "ALL IN",
    "创立",
    "建立",
    "成立",
    "创建",
    "自立门户",
    "共同成立",
    "开始.*创业",
    "二次创业",
    "共同创建",
    "独立创业",
    "连续创业",
    "推出",
    "负责",
    "年任",
    "曾在.*工作",
    "创始",
    "历任",
    "创立",
    "曾任",
    "大学.*主任",
    "大学.*教授",
    "CEO",
    "董事长",
    "联合.*创建",
    "联合.*创办",
    "拥有.*经验",
    "曾在.*担任",
    "曾在.*担当",
    "曾在.*经验",
    "工作",
    "管理",
    "合伙人",
    "创始人",
    "员工",
    "从业",
    "从事",
    "创立",
    "副总裁",
    "带领",
    "总裁",
    "主管",
    "首席",
    "总监",
    "董事",
    "专家",
    "leader",
    "总经理",
    "工程师",
    "产品经理",
    "产品设计师",
    "经理",
    "进入",
    "CEO",
    "CTO",
    "COO",
    "CFO",
    "CMO",
    "CSO",
    "科学家",
    "一职",
    "法人",
    "取得.*学位",
    "就读",
    "毕业",
    "考上",
    "获.*博士",
    "获.*硕士",
    "获.*学位",
    "保送",
    "免试",
    "攻读",
    "获得.*学历",
    "获得.*学位",
    "休学",
    "大学.*硕士",
    "大学.*博士",
    "大学.*MBA",
    "校友",
    "大学.*本科",
    "拥有.*学位",
    "拥有.*硕士",
    "拥有.*博士",
    "拥有.*学士",
    "拥有.*本科",
    "大学.*EMBA",
    "学院.*EMBA",
    "学院.*MBA",
    "考入",
    "深造",
    "本科",
    "学士",
    "硕士",
    "博士",
    "硕博",
    "求学",
    "学位",
    "大学.*专业",
    "学院.*专业",
    "加盟",
]


ORG_BLACK_LIST = {"公司", "毕业后", "新媒体", "投资银行部", "中国共产党", "生产部经理", "薪酬委员会", "提名委员会", "首家", "审计员", "北京分公司", "国际会计师行", "任有限公司", "资产管理部",
                  "市场部", "综合管理部", "监事会", "联交所主板上市公司", "汽车行业", "技术部", "人事部", "审计部", "世界500强企业", "总经办", "惠州", "历任有限公司", "科技部", "北京办事处",
                  "零售行业", "财务部门", "企业银行", "联交所主板上市之公司", "会计员", "有资产", "跨国", "惠州市", "中华", "有多", "中央政策组", "科技控股", "从一", "上海分所", "中共",
                  "金融服务业", "资产经营", "智慧城市", "品牌运营", "党群工作部", "餐饮连锁", "公司证券部", "深圳分公司", "公司办公室", "资产经营部", "校董会", "北京分行", "财务部", "北京分所",
                  "宣传部", "财务审计部", "深圳分行", "我的", "投资银行事业部", "广州分公司", "医院管理局", "共青团", "进入有限公司", "行政人事部", "航空工业", "联交所创业板上市之公司", "大公司",
                  "企业信息化", "PE投资", "服务总监", "于新华社", "市委", "初创公司", "创新科技", "钢铁研究总院", "财务委员会", "世界500强公司", "方向投资", "移动互联", "职业生涯", "服务过",
                  "主持", "制片", "导演", "核心成员", "副总", "效力", "主任", "毕业后", "公司", "金融学", "一九八八", "Science", "生物工程", "黄博士", "INSEAD", "电信",
                  "博士后流动站", "民商法学", "香港政府", "金融学院", "金融博士", "薪酬委员会", "百度", "恒辉企业控股有限公司", "商学", "腾讯", "铭源医疗发展有限公司", "神通电信服务",
                  "神通机器人教育集团有限公司", "华为", "精密仪器系", "电视广播有限公司", "机电工程系", "新媒体", "提名委员会", "香港特许秘书公会", "香港会计师公会", "移动互联", "永保林业控股有限公司",
                  "新南", "开明投资有限公司", "IBM", "香港铁路有限公司", "香港特许行政管理协会", "阿里巴巴", "网易", "播音主持专业", "微软亚洲研究院", "宝洁", "天网", "Google",
                  "Chelsea", "高盛", "马博士", "联想", "清华校友TMT协会", "搜狐", "传媒专业", "中国财政部", "Clark", "BiMBA", "钱先生", "道路与铁道工程", "磐霖资本", "熊先生",
                  "新浪", "新华社", "北大国际", "世界500强企业", "SMBA", "Kansas", "Intel", "211", "香港大学公司", "高分子化学与物理", "香港工程师学会",
                  "香港中文大学校友会联会教育基金会", "香港上海汇丰银行有限公司", "金融商学", "谷歌", "航空工业", "联想集团", "美图公司", "精密仪器与机械", "科技大学", "理工大学", "环球", "测绘专业",
                  "永利澳门有限公司", "毕马威", "普华永道", "教育部", "戴尔", "州立大学", "基础建设", "名牌大学", "北京研究生部", "冶金工程", "农校", "中国电信", "中共", "一化控股(中国)有限公司",
                  "SAP", "IBM中国研发中心", "GMBA", "Austin", "Columbia", "鲲鹏资本", "驻港", "马国际控股有限公司", "香港银行学会", "香港金山公司", "香港科技大学合办",
                  "香港理工大学公司", "香港摩根士丹利私人财富管理部", "香港工业总会", "陶氏化学公司", "阿里云事业部", "金融界", "金融学系", "辉煌科技（控股）有限公司", "超图软件", "财政部", "贝塔斯曼集团",
                  "薇蜜", "腾讯公司", "胜利油田", "美国优质服务科学协会", "红筹企业", "红杉资本", "省委党校", "澳门特别行政区政府", "澳洲证券交易所", "澳洲会计师公会", "深圳润迅通讯发展有限公司", "海尔",
                  "水木清华创新理事会", "毕马威会计师事务所", "欧唯特公司", "格力电器", "校董会", "柏毅证券公司", "智能交通", "新进科技集团有限公司", "新加坡证券交易所有限公司", "新媒体协会", "摩根士丹利",
                  "摩托罗拉", "搜狗", "德邦物流", "微电子院", "微电子所", "康佰控股有限公司", "应用科学学院", "平安集团", "师范专科", "师范专科学校", "巴克莱德胜投资公司", "工业设计系", "尼尔森",
                  "寰亚矿业有限公司", "富士康", "威尔斯特许会计师公会", "大学函授", "复星国际有限公司", "在商", "圣丰", "卫生部", "从一", "乐天集团", "乐天集团金融部", "MBA", "EMBA", "进修"}


def strip_to_none(text: str):
    if text is None:
        return None
    text = text.strip()
    text = re.sub(any_backspaces, '', text)
    if len(text) == 0:
        return None
    if text == 'None':
        return None
    return text


def get_client():
    account = next(BAIDU_ACCOUNTS)
    app_id = account.get('app_id')
    api_key = account.get('api_key')
    secret_key = account.get('secret_key')
    return AipNlp(app_id, api_key, secret_key)


def convert_encoding(f):
    @functools.wraps(f)
    def wrapper(sentence, *args, **kwargs):
        text = strip_to_none(sentence)
        if text is None or len(text) > 700:
            return list()
        text = text.encode('gbk', 'ignore').decode('gbk')
        times = 2
        while times > 0:
            try:
                result = f(text, *args)
                times = 0
                return result
            except Exception as err:
                times -= 1

    return wrapper


@convert_encoding
def cut(text: str) -> list:
    result = get_client().lexer(text)
    error_msg = result.get('error_msg')
    if error_msg is not None:
        msg = f"{error_msg}: '{text}'"
        # notifier.notify(msg)
        return []
    items = result.get('items')
    if items is None:
        return []
    return [item.get('item') for item in items]


@convert_encoding
def named_entities(text: str, debug=False) -> list:
    text = strip_to_none(text)
    if text is None:
        return []
    result = get_client().lexerCustom(text)
    error_msg = result.get('error_msg')
    if error_msg is not None:
        msg = f"{error_msg}: '{text}'"
        return []
    items = result.get('items')
    if items is None:
        return []
    tags = list()
    for item in items:
        word = item.get('item')
        if len(word) < 2:
            continue
        ne = item.get('ne').lower()
        if ne.startswith('org'):
            ne = 'org'
        elif ne.startswith('per'):
            ne = 'per'
        tags.append((word, ne))
    return tags


@convert_encoding
def lexer(text: str, debug=False) -> list:
    text = strip_to_none(text)
    if text is None:
        return []
    result = get_client().lexerCustom(text)
    error_msg = result.get('error_msg')
    if error_msg is not None:
        msg = f"{error_msg}: '{text}'"
        return []
    items = result.get('items')
    if items is None:
        return []
    return items


@convert_encoding
def original_lexer(text: str, debug=False) -> list:
    text = strip_to_none(text)
    if text is None:
        return []
    result = get_client().lexer(text)
    error_msg = result.get('error_msg')
    if error_msg is not None:
        msg = f"{error_msg}: '{text}'"
        return []
    items = result.get('items')
    if items is None:
        return []
    return items


@convert_encoding
def dependency(text: str):
    """
    1.定中关系ATT
    如：工人/n师傅/n（工人/n ← 师傅/n）。

    2. 数量关系QUN（quantity）
    如：三/m天/q（三/m ← 天/q）。

    3.并列关系COO（coordinate）
    如：奔腾/v咆哮/v的怒江激流（奔腾/v → 咆哮/v）。

    4.同位关系APP（appositive）
    如：我们大家 （我们 → 大家）。

    5.附加关系ADJ（adjunct）
    如：约/d 二十/m 多/m 米/q 远/a 处/n （二十/m → 多/m，米/q → 远/a）。

    6.动宾关系VOB（verb-object）
    如：历时/v 三/m 天/q 三/m夜/q（历时/v → 天/q）。

    7.介宾关系POB（preposition-object）
    如：距/p球门/n（距/p → 球门/n）。

    8.主谓关系SBV（subject-verb）
    如：父亲/n 逝世/v １０/m 周年/q 之际/nd（父亲/n ← 逝世/v）。

    9.比拟关系SIM（similarity）
    如：炮筒/n 似的/u 望远镜/n（炮筒/n ← 似的/u）。

    10.时间关系TMP（temporal）
    如：十点以前到公司（以前 ← 到）。

    11.处所关系LOC（locative）
    如：在公园里玩耍（在 ← 玩耍）。

    12.“的”字结构DE
    如：上海/ns 的/u 工人/n（上海/ns ← 的/u，的/u ← 工人/n）。

    13.“地”字结构DI
    如： 方便/a 地/u 告诉/v 计算机/n（方便/a ← 地/u，地/u ← 告诉/v）。

    14.“得”字结构DEI
    如：讲/v 得/u 很/d 对/a（讲/v → 得/u，得/u → 对/a）。

    15.“所”字结构SUO
    如：机电/b 产品/n 所/u 占/v 比重/n 稳步/d 上升/v（所/u ← 占/v）。

    16.“把”字结构BA
    如：我们把豹子打死了（把/p → 豹子/n）。

    17.“被”字结构BEI
    如：豹子被我们打死了（豹子/n ← 被/p）。

    18.状中结构ADV（adverbial）
    如：连夜/d 安排/v 就位/v（连夜/d ← 安排/v）。

    19.动补结构CMP（complement）
    如：做完了作业（做/v → 完）。

    20.兼语结构DBL（double）
    如：[7]曾经/d [8]使/v [9]多少/r [10]旅游/n [11]人/n [12]隔/v [13]岸/n [14]惊叹/v [15]！/wp（使 → 人/n ，/v使/v → 惊叹/v）。

    21.关联词CNJ（conjunction）
    如：只要他请客，我就来。（只要 ← 请 ，就 ← 来）。

    22.关联结构 CS(conjunctive structure)
    如：只要他请客，我就来。（请 ← 来）。

    23.语态结构MT（mood-tense）
    如： [12]答应/v [13]孩子/n [14]们/k [15]的/u [16]要求/n [17]吧/u [18]，/wp [19]他们/r [20]这/r [21]是/v [22]干/v [23]事业/n [24]啊/u [25]！/wp（[12]答应/v ← [17]吧/u，[21]是/v ← [24]啊/u）。

    24.连谓结构VV（verb-verb）
    如：美国总统来华访问。（来华/v → 访问/v）。

    25.核心HED（head）
    如：这/r 就是/v恩施/ns最/d]便宜/a的/u出租车/n，/wp相当于/v北京/ns的/u “/wp 面的/n ”/wp 。/wp <EOS>/<EOS>（就是/v ← <EOS>/<EOS>）

    26.前置宾语FOB（fronting object）
    如：他什么书都读（书/n ← 读/v）。

    27.双宾语DOB（double object）
    如：我送她一束花。（送/v → 她/r，送/v → 花/n）。

    28.主题TOP（topic）
    如：西直门，怎么走？（西直门 ← 走）。

    29.独立结构IS（independent structure）
    如：事情明摆着，我们能不管吗？

    30.独立分句IC（independent clause）
    如：我是中国人，我们爱自己的祖国。（是 → 爱）

    31.依存分句DC（dependent clause）
    如：大家/r叫/v 它/r “/wp 麻木/a 车/n ”/wp ，/wp 听/v起来/v 怪怪的/a 。/wp（叫/v → 听/v）。

    32.叠词关系VNV （verb-no-verb or verb-one-verb)
    如“是 不 是”、“看一看”，那么这几个词先合并在一起，然后预存到其他词上，叠词的内部关系定义为：(是1→不；不→是2） 。

    33.一个词YGC
    当专名或者联绵词等切散后，他们之间本身没有语法关系，应该合起来才是一个词。如：百 度。

    34.标点 WP
    大部分标点依存于其前面句子的核心词上，依存关系WP。
    """
    result = get_client().depParser(text)
    items = result.get('items')
    if items is None:
        return None
    results = {}
    for item in items:
        _id = item.get('id')
        word = item.get('word')
        postag = item.get('postag')
        head = item.get('head')
        deprel = item.get('deprel')
        results[_id] = (word, postag, head, deprel)
    return results


@convert_encoding
def dependency_relations(text: str, persons: list):
    result = get_client().depParser(text)
    items = result.get('items')
    if items is None:
        return None
    results = {}
    for item in items:
        word = item.get('word')
        if word not in persons:
            continue
        results[word] = item.get('deprel')
    return results


@convert_encoding
def dependency_test(text):
    return get_client().depParser(text)


@convert_encoding
def get_dependency(text):
    result = get_client().depParser(text)
    items = result.get('items')
    if items is None:
        return None
    return items


def pos_tags_of_sub_sentence(sentence, sub_sentence, pos_tags):
    start = sentence.find(sub_sentence)
    end = start + len(sub_sentence)
    index = 0
    sub_pos_tags = list()
    idx = 0
    for item in pos_tags:
        word = item.get('item')
        index += len(word)
        if start >= index:
            idx += 1
        elif index <= end:
            sub_pos_tags.append(item)
    return sub_pos_tags, idx
