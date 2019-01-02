from aip import AipSpeech
# import mp3play
import time
import datetime
import os
import re
import random
import sqlite3
import pypinyin
import threading
import logging


logger = logging.getLogger('django')
errlog = logging.getLogger('error')

class AipClient(object):
    def __init__(self,appId,apiKey,secretKey):
        self.appId = appId
        self.apiKey = apiKey
        self.secretKey = secretKey
        self.lang = 'zh' #语言选择,填写zh
        self.ctp = 1 #客户端类型选择，web端填写1
        self.voiceCfg = {}
        self.client = AipSpeech(appId, apiKey, secretKey)
        self.setVoiceCfg()

    def setVoiceCfg(self, voiceSet=None):
        if voiceSet == None:
            self.voiceCfg['spd'] = 2 # 语速，取值0-9，默认为5中语速
            self.voiceCfg['pit'] = 5 # 音调，取值0-9，默认为5中语调
            self.voiceCfg['vol'] = 12 # 音量，取值0-15，默认为5中音量
            self.voiceCfg['per'] = 0 # 发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女
        else:
            self.voiceCfg = voiceSet

    def getVoice(self, tex, voiceCfg=None):
        if voiceCfg == None:
            voiceCfg = self.voiceCfg
        voice = self.client.synthesis(tex, self.lang, self.ctp, voiceCfg)
        if not isinstance(voice, dict):
            return voice
        else:
            print(('make voice error:%s' % voice['err_msg']))
            return None

class ListenWord(object):
    def __init__(self, word, voiceSet, aipClient):
        self.word = word
        self.voiceSet = voiceSet
        self.pinyin = None
        self.wordNum = len(word)
        self.voiceFile = None
        self.aipClient = aipClient
        # self.sleepSeconds = len(word) / 3 * 2
        self.sleepSeconds = len(word) * 2
        self.testResult = 0
        # self.wordKey = word.decode('utf-8').encode('unicode_escape').replace('\\u','')
        self.wordKey = word.encode('unicode_escape').replace(b'\\u',b'').decode()
        self.makePinyin()

    def prepareVoice(self):
        self.voiceFile = 'voice/%s_%d%d%d%d.mp3' % (self.wordKey, self.voiceSet['per'], self.voiceSet['pit'], self.voiceSet['spd'], self.voiceSet['vol'])
        if os.path.isfile(self.voiceFile):
            return self.voiceFile
        voice = self.aipClient.getVoice(self.word, self.voiceSet)
        if voice is None:
            print(('can not make voice of "%s"' % self.word))
            self.voiceFile = None
            return None
        with open(self.voiceFile, 'wb') as f:
            f.write(voice)
        f.close()
        return self.voiceFile

    def makePinyin(self):
        # uword = self.word.decode('utf-8')
        uword = self.word
        self.pinyin = pypinyin.pinyin(uword)
        self.wordNum = len(self.pinyin)
        self.sleepSeconds = self.wordNum * 2

class VoiceBuilder(object):
    APP_ID = '10568246'
    API_KEY = '6cFFqOMdPr3EIYx4uEpYsD4s'
    SECRET_KEY = '6e2c9e550e3358d1e6fd85030115ae36'
    ANNOUNCEVOICE = [['1', '开始听写'], ['2', '听写完毕']]

    def __init__(self, path):
        self.announceSet = {}
        self.dictateSet = {}
        self.vioceSet()
        self.voicePath = path
        self.client = AipClient(VoiceBuilder.APP_ID, VoiceBuilder.API_KEY, VoiceBuilder.SECRET_KEY)

    def vioceSet(self):
        # announcerSet
        self.announceSet['spd'] = 5  # 语速，取值0-9，默认为5中语速
        self.announceSet['pit'] = 5  # 音调，取值0-9，默认为5中语调
        self.announceSet['vol'] = 12  # 音量，取值0-15，默认为5中音量
        self.announceSet['per'] = 3  # 发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女
        # listenSet
        self.dictateSet['spd'] = 2  # 语速，取值0-9，默认为5中语速
        self.dictateSet['pit'] = 5  # 音调，取值0-9，默认为5中语调
        self.dictateSet['vol'] = 12  # 音量，取值0-15，默认为5中音量
        self.dictateSet['per'] = 0  # 发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女

    def builderVoice(self, aWords, voiceSet=None):
        if not voiceSet:
            voiceSet = self.dictateSet
        for aWd in aWords:
            logger.info('builde voice for %s', aWd)
            word = aWd[1]
            if len(aWd) > 3 and aWd[3]:
                continue
            aWd.append(self.makePinyin(word))

            wordKey = word.encode('unicode_escape').replace(b'\\u', b'').decode()
            voiceFile = '%s_%d%d%d%d.mp3' % (wordKey, voiceSet['per'], voiceSet['pit'], voiceSet['spd'], voiceSet['vol'])
            fullFile = os.path.join(self.voicePath, voiceFile)
            if os.path.isfile(fullFile):
                voiceReqPath = '/static/dictation/voice/%s' % voiceFile
                aWd.append(voiceReqPath)
                # aWd.append(voiceFile)
                continue
            if not self.prepareVoice(word, fullFile, voiceSet):
                aWd.append(None)
            else:
                voiceReqPath = '/static/dictation/voice/%s' % voiceFile
                aWd.append(voiceReqPath)
        return aWords

    def buildeAnnouncer(self):
        return self.builderVoice(self.ANNOUNCEVOICE, self.announceSet)

    def prepareVoice(self, word, voiceFile, voiceSet=None):
        if not voiceSet:
            voiceSet = self.dictateSet
        voice = self.client.getVoice(word, voiceSet)
        if voice is None:
            print(('can not make voice of "%s"' % word))
            return None
        with open(voiceFile, 'wb') as f:
            f.write(voice)
        f.close()
        return voiceFile

    def getVoice(self, aWords):
        for aWd in aWords:
            print(aWd)
            word = aWd[1]
            aWd.append(self.makePinyin(word))
            if len(aWd) > 3 and aWd[3]:
                continue
            wordKey = word.encode('unicode_escape').replace(b'\\u', b'').decode()
            voiceFile = '%s_%d%d%d%d.mp3' % (wordKey, self.dictateSet['per'], self.dictateSet['pit'], self.dictateSet['spd'], self.dictateSet['vol'])
            fullFile = os.path.join(self.voicePath, voiceFile)
            i = 0
            fileOk = True
            while not os.path.isfile(fullFile):
                i += 1
                if i>10:
                    fileOk = False
                    break
                time.sleep(1)
            if fileOk:
                aWd.append(voiceFile)
            else:
                aWd.append(None)
        return aWords

    def builderPinyin(self, aWords):
        for aWd in aWords:
            print(aWd)
            word = aWd[1]
            aWd.append(self.makePinyin(word))
        return aWords

    def makePinyin(self, word):
        # uword = self.word.decode('utf-8')
        uword = word
        pinyin = pypinyin.pinyin(uword)
        return pinyin

