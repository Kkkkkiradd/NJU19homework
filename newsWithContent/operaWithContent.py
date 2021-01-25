import jieba
#将爬虫得到的评论（无新闻内容）规格化并分词，参数为第x月，返回列表（例如jan[1][1][1]表示一月一日第一条新闻，新闻内容存在jan[1][1][1][0]
#未进行文件读写操作
def simpWithContent(x):
    name = str(x) + "月.txt"
    f = open(name, "r", encoding='utf-8')
    content = f.readlines()
    con = []
    i=0
    for each in content:
        if each.startswith('{"main_body": '):
            index=i+1
            next=content[index]
            while not next.startswith('{"comment_info":'):
                each+=next
                index+=1
                next=content[index]
            con.append([each,0])
        else:
            each = each.split("{\"comment_info\": \"：")
            each.pop(0)
            if len(each) != 0:
                each = each[0].split("\", \"comment_time\": \"")
                each[1] = each[1][7:9]
                con.append(each)
    month = []
    i = 0
    while i <= 31:
        day=[]
        month.append(day)
        i+=1
    length=len(con)
    for i in range(0,length):
        comment=[]
        curday=0
        if (con[i][1])==0:
            comment.append(con[i][0])
            i+=1
            curday=con[i][1]
            while con[i][1]!=0:
                comment.append(con[i][0])
                i+=1
                if i>=length:
                    break
        if len(comment)!=0:
            month[int(curday)].append(comment)

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
    for day in month:
        if len(day)!=0:
            for new in day:
                j=0
                ll=[]
                for sentence in new:
                    if j==0:
                        ll.append(sentence)
                        j+=1
                        continue
                    seg_list = jieba.cut(sentence)
                    l = []
                    for seg in seg_list:
                        if seg in stop_data:
                            continue
                        else:
                            l.append(seg)
                    ll.append(l)
                    j+=1
                Res[i].append(ll)
            i = i + 1
    return Res

def month2stage(data, i):
    filename = 'stage_with_content' + str(i) + '.txt'
    stFile = open(filename, 'w', encoding='utf-8')
    if i == 1:
        stage = data[1][:23]
        for day in stage:
            for news in day:
                j = 0
                for comment in news:
                    if j == 0:
                        stFile.write(comment + '\n')
                        j += 1
                        continue
                    for word in comment:
                        stFile.write(str(word))
                        stFile.write('  ')
                    stFile.write('\n')
                    j += 1
    if i == 2:
        stage = data[1][23:]
        for each in data[2][1:8]:
            stage.append(each)

        for day in stage:
            for news in day:
                j = 0
                for comment in news:
                    if j == 0:
                        stFile.write(comment + '\n')
                        j += 1
                        continue
                    for word in comment:
                        stFile.write(str(word))
                        stFile.write('  ')
                    stFile.write('\n')
                    j += 1
    if i == 3:
        stage = data[2][10:14]
        for day in stage:
            for news in day:
                j = 0
                for comment in news:
                    if j == 0:
                        stFile.write(comment + '\n')
                        j += 1
                        continue
                    for word in comment:
                        stFile.write(str(word))
                        stFile.write('  ')
                    stFile.write('\n')
                    j += 1
    if i == 4:
        stage = data[3][10:]
        for day in stage:
            for news in day:
                j=0
                for comment in news:
                    if j==0:
                        stFile.write(comment+'\n')
                        j+=1
                        continue
                    for word in comment:
                        stFile.write(str(word))
                        stFile.write('  ')
                    stFile.write('\n')
                    j += 1
    stFile.close()
    if len(stage[0])!=0:
        stage.insert(0,[]) #保证索引x指的是阶段的第x天
    return stage

#给各阶段评分并打印出典型新闻（阶段中评分极值
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

    rankRes = open("rank_with_content.txt", 'w')

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
    i=0
    for stage in data:
        stage_rank=0
        maxRank = [0, 0, 0,0]
        minRank = [0, 0, 0,0]
        if stage != 0:
            i += 1
            j = 0
            for day in stage:
                if len(day)!=0:
                    j+=1
                    x = -1   #新闻条数从第零条开始
                    for new in day:
                        w = 1
                        x += 1
                        cnt=0
                        new_rank=0
                        for comment in new:
                            if cnt==0:
                                cnt+=1
                                continue
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
                                    new_rank += w
                                    stage_rank += w
                                    w = 1
                                if word in n:
                                    new_rank -= w
                                    stage_rank -= w
                                    w = 1
                        if new_rank>maxRank[0]:
                            maxRank[0]=new_rank
                            maxRank[1]=i
                            maxRank[2]=j
                            maxRank[3]=x
                        if new_rank<minRank[0]:
                            minRank[0]=new_rank
                            minRank[1]=i
                            minRank[2]=j
                            minRank[3]=x
        if maxRank[1]!=0:
            date = 'stage'+str(i)
            rankRes.write(date + ':   ' + str(stage_rank) + '\n')
            print('stage'+str(i)+':\n')
            print(maxRank[0])
            print(data[maxRank[1]][maxRank[2]][maxRank[3]])
            print(minRank[0])
            print(data[minRank[1]][minRank[2]][minRank[3]])
            print('\n')
    rankRes.close()


jan=simpWithContent(1)
feb=simpWithContent(2)
mar=simpWithContent(3)
data=[0,jan,feb,mar]
stage1=month2stage(data,1)
stage2=month2stage(data,2)
stage3=month2stage(data,3)
stage4=month2stage(data,4)

stage_data=[0,stage1,stage2,stage3,stage4]
rank(stage_data)
