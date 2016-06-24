# -*- coding: utf-8 -*-

import requests
import json
import time
import csv

# # 小影
# urlA = "http://mail.emotibot.com.cn:808/api/APP/chat2.php"

# # 范儿盒
# urlA = "http://mail.emotibot.com.cn:8009/api/APP/chat2.php"

# 小竹子
urlA = "http://mail.emotibot.com.cn:8010/api/APP/chat2.php"

payload = {'wechatid': 'o7WYos9rD62Dx72mXgHE3rCXv31k', 'type': 'text'}

# CU Result json
url = "http://192.168.1.27:8081/cu?UniqueID=123&UserID=Test&Text1="

i = 0
# 测试文件需命名为Test.txt
test_file = 'Test.txt'
# 测试结果文件为Output.csv
output_file = 'TestOutput.csv'

with open(test_file) as f:
    with open(output_file, 'w') as out:
        writer = csv.writer(out, dialect='excel')
        for line in f:
            Input = line.strip()
            payload['text'] = Input
            rA = requests.get(urlA, params=payload)
            rAtext = rA.text.strip().replace('\n', '\\n').replace('\r', '')
            try:
                jdata = json.loads(rAtext)
                reply = jdata.get("answer").encode('utf8')
            except Exception as e:
                reply = rAtext.encode("utf8")
            inputUrl = url + Input
            r = requests.get(inputUrl)
            normText = r.text.strip().replace('\n', '\\n').replace('\r', '')
            jdata = json.loads(normText)
            memory = jdata.get("memory")
            i += 1
            print i, ".", line
            time.sleep(0.5)
            rowList = [Input, reply]
            for j in range(len(memory)):
                print "---Output %d:---" % (j + 1)
                print "type: %s" % memory[j]["type"]
                print "subject: %s" % memory[j]["subject"]
                print "relation: %s" % memory[j]["relation"]
                print "entity: %s" % memory[j]["entity"]
                print "score: %s" % memory[j]["score"]
                print "candidateAnswer: %s" % memory[j]["candidateAnswer"]
                print "conflict: %s" % memory[j]["conflict"]
                extractor = "type: %s\n" % memory[j]["type"]
                extractor += "subject: %s\n" % memory[j]["subject"]
                extractor += "relation: %s\n" % memory[j]["relation"]
                if memory[j]["entity"] is None:
                    extractor += "entity: %s\n" % memory[j]["entity"]
                else:
                    extractor += "entity: %s\n" % memory[j]["entity"]
                extractor += "score: %s\n" % memory[j]["score"]
                if memory[j]["candidateAnswer"] is None:
                    extractor += "candidateAnswer: %s\n" % memory[j]["candidateAnswer"]
                else:
                    extractor += "candidateAnswer: %s\n" % memory[j]["candidateAnswer"]
                extractor += "conflict: %s\n" % memory[j]["conflict"]
                rowList.append(extractor.encode('utf8'))
            writer.writerow(rowList)
