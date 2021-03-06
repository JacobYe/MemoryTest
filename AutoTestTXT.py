# -*- coding: utf-8 -*-

import requests
import json
import time

# 小影
urlA = "http://mail.emotibot.com.cn:808/api/APP/chat2.php"
payload = {'wechatid': 'Test'}

# 小竹子
# url = "http://mail.emotibot.com.cn:8009/Emotibot/api/APP/chat2.php"
# payload = {'wechatid': 'Test', 'type':'text'}

# createTime = time.strftime("%Y%m%d%H%M%S", time.localtime(int(time.time())))

# CU Result json
url = "http://192.168.1.27:8081/cu?UniqueID=123&UserID=Test&Text1="

i = 0
test_file = 'Test.txt'
output_file = 'Output_%s' % test_file

with open(test_file) as f:
    with open(output_file, 'w') as out:
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
            out.write("==================================================\n")
            out.write('%s: %s\n' % (i, Input))
            print reply
            out.write('Answer: %s\n' % reply)
            for j in range(len(memory)):
                print "---Output %d:---" % (j + 1)
                print "type: %s" % memory[j]["type"]
                print "subject: %s" % memory[j]["subject"]
                print "relation: %s" % memory[j]["relation"]
                print "entity: %s" % memory[j]["entity"]
                print "score: %s" % memory[j]["score"]
                print "candidateAnswer: %s" % memory[j]["candidateAnswer"]
                print "conflict: %s" % memory[j]["conflict"]
                out.write("---Output %d:---\n" % (j + 1))
                out.write("type: %s\n" % memory[j]["type"])
                out.write("subject: %s\n" % memory[j]["subject"])
                out.write("relation: %s\n"
                          % memory[j]["relation"].encode("utf8"))
                if memory[j]["entity"] is None:
                    out.write("entity: %s\n" % memory[j]["entity"])
                else:
                    out.write("entity: %s\n"
                              % memory[j]["entity"].encode("utf8"))
                out.write("score: %s\n" % memory[j]["score"])
                if memory[j]["candidateAnswer"] is None:
                    out.write("candidateAnswer: %s\n"
                              % memory[j]["candidateAnswer"])
                else:
                    out.write("candidateAnswer: %s\n"
                              % memory[j]["candidateAnswer"].encode("utf8"))
                out.write("conflict: %s\n" % memory[j]["conflict"])
