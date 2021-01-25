# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# encoding=utf-8
import math
import jieba

#将爬虫得到的评论（无新闻内容）规格化并分词，参数为第x月，返回列表（索引为日期-第几条评论，例如jan[1][1]表示一月一日第一条评论
#未进行文件读写操作
def simplify(x):
    name = str(x) + "yue.txt"
    f = open(name, "r", encoding='utf-8')
    content = f.readlines()
    con = []
    for each in content:
        each = each.split("{\"comment_info\": \"：")
        each.pop(0)
        if len(each) != 0:
            each = each[0].split("\", \"comment_time\": \"")
            each[1] = each[1][7:9]
            con.append(each)
    con.reverse()
    res = []
    i = 0
    while i <= 31:
        newl = []
        res.append(newl)
        i += 1
    res[0] = 1
    for comment in con:
        x = int(comment[1])
        if x != -1:
            res[x].append(comment[0])
    jieba.load_userdict("positive.txt")
    jieba.load_userdict("negative.txt")
    jieba.load_userdict("not.txt")
    Res = []
    i = 0
    while i <= 32:
        newl = []
        Res.append(newl)
        i = i + 1
    stop = open("chineseStopWords.txt")
    stop_data = []
    for i in stop.readlines():
        stop_data.append(i.strip())
    i = 1
    for a in res:
        if a != 1:
            for sentence in a:
                seg_list = jieba.cut(sentence)
                l = []
                for seg in seg_list:
                    if seg in stop_data:
                        continue
                    else:
                        l.append(seg)
                Res[i].append(l)
            i = i + 1
    return Res#

#按list第二项（list[1])从大到小排序
def sort(list, len):
    i = 0
    while i < len:
        j = 0
        while j < len - 1 - i:
            if float(list[j][1]) < float(list[j + 1][1]):
                l = list[j]
                list[j] = list[j + 1]
                list[j + 1] = l
            j += 1
        i += 1

#分别提取月份或各阶段（有st-mon决定）的emothionalwords并写入相应txt文件
def screenEmotionalWords(st_mon):
    pos = open("positive.txt", encoding='utf-8')
    neg = open("negative.txt", encoding='utf-8')
    posWords = []
    negWords = []
    for each in pos.readlines():
        posWords.append(each.strip())
    for each in neg.readlines():
        negWords.append(each.strip())
    i = 1
    if st_mon == 'month':
        data=create_month_data()
        for month in data:
            if month != 0:
                namePos = str(i) + 'yuePositiveWords.txt'
                nameNeg = str(i) + 'yueNegativeWords.txt'
                pFile = open(namePos, 'w')
                nFile = open(nameNeg, 'w')
                p = []
                n = []
                for day in month:
                    for comment in day:
                        for eachWord in comment:
                            if eachWord in posWords:
                                k = 0
                                for a in p:
                                    if eachWord in a:
                                        a[1] += 1
                                        k = 1
                                        break
                                if k == 0:
                                    l = [eachWord, 1]
                                    p.append(l)
                            if eachWord in negWords:
                                k = 0
                                for a in n:
                                    if eachWord in a:
                                        a[1] += 1
                                        k = 1
                                        break
                                if k == 0:
                                    l = [eachWord, 1]
                                    n.append(l)
                i = i + 1
                sort(p, len(p))
                sort(n, len(n))
                for each in p:
                    pFile.write(each[0])
                    space = 10 - len(each[0])
                    while space > 0:
                        space -= 1
                        pFile.write(' ')
                    pFile.write(str(each[1]) + '\n')

                for each in n:
                    nFile.write(each[0])
                    space = 10 - len(each[0])
                    while space > 0:
                        space -= 1
                        nFile.write(' ')
                    nFile.write(str(each[1]) + '\n')
                pFile.close()
                nFile.close()

    if st_mon == 'stage':
        data=create_stage_data()
        for stage in data:
            namePos = 'stage' + str(i) + 'PositiveWords.txt'
            nameNeg = 'stage' + str(i) + 'NegativeWords.txt'
            pFile = open(namePos, 'w')
            nFile = open(nameNeg, 'w')
            p = []
            n = []
            for day in stage:
                for comment in day:
                    for eachWord in comment:
                        if eachWord in posWords:
                            k = 0
                            for a in p:
                                if eachWord in a:
                                    a[1] += 1
                                    k = 1
                                    break
                            if k == 0:
                                l = [eachWord, 1]
                                p.append(l)
                        if eachWord in negWords:
                            k = 0
                            for a in n:
                                if eachWord in a:
                                    a[1] += 1
                                    k = 1
                                    break
                            if k == 0:
                                l = [eachWord, 1]
                                n.append(l)
            i = i + 1
            sort(p, len(p))
            sort(n, len(n))
            for each in p:
                pFile.write(each[0])
                space = 10 - len(each[0])
                while space > 0:
                    space -= 1
                    pFile.write(' ')
                pFile.write(str(each[1]) + '\n')

            for each in n:
                nFile.write(each[0])
                space = 10 - len(each[0])
                while space > 0:
                    space -= 1
                    nFile.write(' ')
                nFile.write(str(each[1]) + '\n')
            pFile.close()
            nFile.close()

#返回存储第i阶段分词的列表
def month2stage(i):
    data=create_month_data()
    filename = 'stage' + str(i) + '.txt'
    stFile = open(filename, 'w', encoding='utf-8')
    if i == 1:
        stage = data[1][:23]
        for day in stage:
            for comment in day:
                for word in comment:
                    stFile.write(str(word))
                    stFile.write('  ')
                stFile.write('\n')
    if i == 2:
        stage = data[1][23:]
        for each in data[2][1:8]:
            stage.append(each)

        for day in stage:
            for comment in day:
                for word in comment:
                    stFile.write(str(word))
                    stFile.write('  ')
                stFile.write('\n')
    if i == 3:
        stage = data[2][10:14]
        for day in stage:
            for comment in day:
                for word in comment:
                    stFile.write(str(word))
                    stFile.write('  ')
                stFile.write('\n')
    if i == 4:
        stage = data[3][10:]
        for month in data[4:]:
            for day in month:
                stage.append(day)

        for day in stage:
            for comment in day:
                for word in comment:
                    stFile.write(str(word))
                    stFile.write('  ')
                stFile.write('\n')
    stFile.close()
    return stage

#对每一条评论的所有单词打分（积极/消极为1/-1，乘以对应的degree和not），并按日为单位将rank写入txt文件（rank.txt
def rank(data):
    degree2f = open("degree2.txt", encoding='utf-8')
    degree2 = []
    for each in degree2f.readlines():
        degree2.append(each.strip())
    degree2f.close()
    degree1_5f = open("degree1.5.txt", encoding='utf-8')

    degree1_5 = []
    for each in degree1_5f.readlines():
        degree1_5.append(each.strip())
    degree1_5f.close()

    degree1_25f = open("degree1.25.txt", encoding='utf-8')
    degree1_25 = []
    for each in degree1_25f.readlines():
        degree1_25.append(each.strip())
    degree1_25f.close()

    degree1_2f = open("degree1.2.txt", encoding='utf-8')
    degree1_2 = []
    for each in degree1_2f.readlines():
        degree1_2.append(each.strip())
    degree1_2f.close()

    degree0_8f = open("degree0.8.txt", encoding='utf-8')
    degree0_8 = []
    for each in degree0_8f.readlines():
        degree0_8.append(each.strip())
    degree0_8f.close()

    degree0_5f = open("degree0.5.txt", encoding='utf-8')
    degree0_5 = []
    for each in degree0_5f.readlines():
        degree0_5.append(each.strip())
    degree0_5f.close()

    reversef = open("not.txt", encoding='utf-8')
    reverse = []
    for each in reversef:
        reverse.append(each.strip())
    reversef.close()

    rankRes = open("rank.txt", 'w')

    pf = open("positive.txt", encoding='utf-8')
    nf = open("negative.txt", encoding='utf-8')
    p = []
    n = []
    for each in pf.readlines():
        p.append(each.strip())
    for each in nf.readlines():
        n.append(each.strip())
    pf.close()
    nf.close()
    i = 0
    for month in data:
        maxRank = [0, 0, 0, 0]
        minRank = [0, 0, 0, 0]
        if month != 0:
            i += 1
            j = 0
            for day in month:
                if len(day) != 0:
                    j += 1
                    day_rank = 0
                    x = 0
                    for comment in day:
                        w = 1
                        x += 1
                        comment_rank = 0
                        for word in comment:
                            if word in reverse:
                                if w != 1:
                                    w = w * -1 * 2  # 程度词+否定词
                                else:
                                    w = w * -1
                            if word in degree0_5:
                                if w != 1:
                                    w = w * 0.5 * 0.5  # 否定词+程度词
                                else:
                                    w = w * 0.5
                            if word in degree0_8:
                                if w != 1:
                                    w = w * 0.5 * 0.8
                                else:
                                    w = w * 0.8
                            if word in degree1_5:
                                if w != 1:
                                    w = w * 0.5 * 1.5
                                else:
                                    w = w * 1.5
                            if word in degree1_25:
                                if w != 1:
                                    w = w * 0.5 * 1.25
                                else:
                                    w = w * 1.25
                            if word in degree1_5:
                                if w != 1:
                                    w = w * 0.5 * 1.5
                                else:
                                    w = w * 1.5
                            if word in degree2:
                                if w != 1:
                                    w = w * 0.5 * 2
                                else:
                                    w = w * 2
                            if word in p:
                                day_rank += w
                                comment_rank += w
                                w = 1
                            if word in n:
                                day_rank -= w
                                comment_rank += w
                                w = 1
                    date = str(i) + '月' + str(j) + '日'
                    rankRes.write(date + ':   ' + str(day_rank) + '\n')
    rankRes.close()

#对各阶段的每一条评论的所有单词进行细化打分，按阶段为单位写入txt（rankInStage.txt
def rankInStage(data):
    degree2f = open("degree2.txt", encoding='utf-8')
    degree2 = []
    for each in degree2f.readlines():
        degree2.append(each.strip())
    degree2f.close()
    degree1_5f = open("degree1.5.txt", encoding='utf-8')

    degree1_5 = []
    for each in degree1_5f.readlines():
        degree1_5.append(each.strip())
    degree1_5f.close()

    degree1_25f = open("degree1.25.txt", encoding='utf-8')
    degree1_25 = []
    for each in degree1_25f.readlines():
        degree1_25.append(each.strip())
    degree1_25f.close()

    degree1_2f = open("degree1.2.txt", encoding='utf-8')
    degree1_2 = []
    for each in degree1_2f.readlines():
        degree1_2.append(each.strip())
    degree1_2f.close()

    degree0_8f = open("degree0.8.txt", encoding='utf-8')
    degree0_8 = []
    for each in degree0_8f.readlines():
        degree0_8.append(each.strip())
    degree0_8f.close()

    degree0_5f = open("degree0.5.txt", encoding='utf-8')
    degree0_5 = []
    for each in degree0_5f.readlines():
        degree0_5.append(each.strip())
    degree0_5f.close()

    reversef = open("not.txt", encoding='utf-8')
    reverse = []
    for each in reversef:
        reverse.append(each.strip())
    reversef.close()

    rankRes = open("rankInStage.txt", 'w')

    pf2 = open("positive_rank2.txt", encoding='utf-8').readlines()
    pf1=open("positive_rank1.txt", encoding='utf-8').readlines()
    nf1 = open("negative_rank1.txt", encoding='utf-8').readlines()
    nf2 = open("negative_rank2.txt", encoding='utf-8').readlines()
    r1=pf1[0].split()
    r2=pf2[0].split()
    h1=pf1[1].split()
    h2=pf2[1].split()
    c1=pf1[2].split()
    c2=pf2[2].split()
    p1 = nf1[0].split()
    p2 = nf2[0].split()
    a1 = nf1[1].split()
    a2 = nf2[1].split()
    i = 0
    for stage in data:
        rationalRank=0
        cheerfulRank=0
        hopefulRank=0
        angerRank=0
        panicRank=0
        if stage==0:
            continue
        i += 1
        for day in stage:
            if len(day) != 0:
                for comment in day:
                    w = 1
                    for word in comment:
                        if word in reverse:
                            if w != 1:
                                w = w * -1 * 2  # 程度词+否定词
                            else:
                                w = w * -1
                        if word in degree0_5:
                            if w != 1:
                                w = w * 0.5 * 0.5  # 否定词+程度词
                            else:
                                w = w * 0.5
                        if word in degree0_8:
                            if w != 1:
                                w = w * 0.5 * 0.8
                            else:
                                 w = w * 0.8
                        if word in degree1_5:
                            if w != 1:
                                w = w * 0.5 * 1.5
                            else:
                                w = w * 1.5
                        if word in degree1_25:
                            if w != 1:
                                w = w * 0.5 * 1.25
                            else:
                                w = w * 1.25
                        if word in degree1_5:
                            if w != 1:
                                w = w * 0.5 * 1.5
                            else:
                                w = w * 1.5
                        if word in degree2:
                            if w != 1:
                                w = w * 0.5 * 2
                            else:
                                w = w * 2
                        if word in a2:
                            angerRank+=w*2
                            w=1
                        elif word in a1:
                            angerRank+=w
                            w=1
                        elif word in p1:
                            panicRank+=w
                            w=1
                        elif word in p2:
                            panicRank += 2*w
                            w=1
                        elif word in c2:
                            cheerfulRank += 2*w
                            w=1
                        elif word in h2:
                            hopefulRank += 2*w
                            w=1
                        elif word in r2:
                            rationalRank += 2*w
                            w=1
                        elif word in c1:
                            cheerfulRank+=w
                            w=1
                        elif word in h1:
                            hopefulRank +=  w
                            w = 1
                        elif word in r1:
                            rationalRank += 1*w
                            w=1
        rankRes.write('stage'+str(i)+':\n')
        rankRes.write("rationalRank =" + str(rationalRank) + '\n')
        rankRes.write("hopefulRank =" + str(hopefulRank) + '\n')
        rankRes.write("cheerfulRank ="+str(cheerfulRank )+'\n')
        rankRes.write("angerRank =" + str(angerRank) + '\n')
        rankRes.write("panicRank =" + str(panicRank) + '\n')
    rankRes.close()

#选出每个阶段积极消极频率最高的50个word，合并后写入相应文件（positiveInstage.txt/negativeInstage.txt，每一行前面为单词，后面为频数
def chooesTop50():
    i = 0
    pos = open("positiveInstage.txt", 'w')
    neg = open("negativeInstage.txt", 'w')
    lpos = []
    lneg = []
    while i < 4:
        i += 1
        namePos = 'stage' + str(i) + 'PositiveWords.txt'
        nameNeg = 'stage' + str(i) + 'NegativeWords.txt'
        pFile = open(namePos)
        nFile = open(nameNeg)
        index = 0
        while index < 50:
            index += 1
            p = pFile.readline().split()
            n = nFile.readline().split()
            k = 0
            for each in lpos:
                if p[0] in each:
                    k = 1
                    each[1] = int(p[1]) + int(each[1])
            if k == 0:
                lpos.append(p)
            k = 0
            for each in lneg:
                if n[0] in each:
                    k = 1
                    each[1] = int(n[1]) + int(each[1])
            if k == 0:
                lneg.append(n)
    sort(lpos, len(lpos))
    sort(lneg, len(lneg))
    for each in lpos:
        pos.write(each[0])
        space = 10 - len(each[0])
        while space > 0:
            space -= 1
            pos.write(' ')
        pos.write(str(each[1]) + '\n')

    for each in lneg:
        neg.write(each[0])
        space = 10 - len(each[0])
        while space > 0:
            space -= 1
            neg.write(' ')
        neg.write(str(each[1]) + '\n')
    pos.close()
    neg.close()


def create_month_data():
    jan=simplify(1)
    feb=simplify(2)
    mar=simplify(3)
    apr=simplify(4)
    may=simplify(5)
    jun=simplify(6)
    return [0,jan,feb,mar,apr,may,jun]


def create_stage_data():
    data=create_month_data()
    stage_data=[0]
    for i in range(1,5):
        stage_data.append(month2stage(data,i))
    return stage_data

#读取各阶段情绪词并返回
def getWords(x):
    name='stage'+str(x)+'PositiveWords.txt'
    stage=[]
    for eachword in open(name).readlines():
        l=eachword.split()
        stage.append(l)
    name='stage'+str(x)+'NegativeWords.txt'
    for eachword in open(name) .readlines():
        l=eachword.split()
        stage.append(l)
    return stage

#统计各阶段tf-idf前20并写入txt（TF_IDFtop20.txt
def getITF_IDFInStage():
    f=open('TF_IDFtop20.txt','w')
    stage1=getWords(1)
    stage2=getWords(2)
    stage3=getWords(3)
    stage4=getWords(4)
    data=[stage1,stage2,stage3,stage4]
    for stage in data:
        sum=0
        for word in stage:
            sum+=int(word[1])
        for word in stage:
            idf=0
            for st in data:
                for w in st:
                   if word[0]==w[0]:
                        idf+=1
                        break
            idf=math.log(4/idf)
            tf=float(word[1])/sum
            word[1]=idf*tf
    sort(stage1,len(stage1))
    sort(stage2,len(stage2))
    sort(stage3,len(stage3))
    sort(stage4,len(stage4))
    i=0
    while i<4:
        f.write('stage'+str(i+1)+':\n')
        j=0
        while j<20:
            f.write(data[i][j][0]+'   ')
            f.write(str(data[i][j][1]))
            f.write('\n')
            j+=1
        i+=1
    f.close()

getITF_IDFInStage()