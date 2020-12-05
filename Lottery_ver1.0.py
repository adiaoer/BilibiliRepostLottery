from urllib.request import *
import json
import random
import re

class User:
	def __init__(self, uid, name, comment):
		self.uid = uid
		self.name = name
		self.comment = comment

	def __eq__(self, rhs):
		return self.uid == rhs.uid

	def __hash__(self):
		return int(self.uid)

	def DispInfo(self):
		print(f'中奖用户信息：\nUID：{self.uid}\n昵称：{self.name}\n附加信息：{self.comment}')
		print(f'中奖用户个人空间：https://space.bilibili.com/{self.uid}/')

class RepostLuckyDog:
	def __init__(self):
		self.totalCount = 0
		self.jsonText = None
		self.userList = []

	def GetString(self, original: str, beg, end) -> str:
		begIndex = original.index(beg)
		if begIndex >= 0:
			begIndex += len(beg)
		endIndex = original.index(end)
		return original[begIndex:endIndex]

	def GetUserCount(self, dynamicID):
		url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id=' + str(dynamicID)
		self.jsonText = json.loads(urlopen(url).read())
		self.totalCount = self.jsonText['data']['card']['desc']['repost']

	def GetUserList(self, dynamicID):
		dynamicAPI = 'https://api.live.bilibili.com/dynamic_repost/v1/dynamic_repost/view_repost?dynamic_id=' + str(dynamicID) + '&offset='
		cnt = 0
		while cnt < self.totalCount:
			tmpAPI = dynamicAPI + str(cnt)
			try:
				self.jsonText = json.loads(self.GetString(urlopen(tmpAPI).read(), b'comments\":', b',\"total'))
				for tmpDict in self.jsonText:
					uid = tmpDict['uid']
					name = tmpDict['uname']
					comment = tmpDict['comment']
					self.userList.append(User(uid, name, comment))
			except:
				break
			cnt += 20
		return self.userList

	def GetDynamicID(self, url):
		return re.findall(r'\d+', url)[0]

	def GenerateLuckyDog(self, sz):
		if sz == 0:
			print('未抓取到转发信息')
			return
		self.userList = list(set(self.userList))
		sz = len(self.userList)
		luckyNum = random.randint(0, sz-1)
		return self.userList[luckyNum]	

	def Run(self, url):
		dynamicID = self.GetDynamicID(url)
		self.GetUserCount(dynamicID)
		print(f'共有转发信息{self.totalCount}条，开始获取转发用户数据......')
		self.userList = self.GetUserList(dynamicID)
		luckyDog = self.GenerateLuckyDog(len(self.userList))
		print(f'获取数据完成')
		if luckyDog:
			luckyDog.DispInfo()

if __name__ == '__main__':
	url = input('请在电脑端打开bilibili，进入动态界面，将连接粘贴到下面：\n')
	while True:
		print('----------------------------------------')
		RepostLuckyDog().Run(url)
		print('----------------------------------------')
		ok = input('继续抽取吗(Y/N)？').lower()
		if ok == 'n':
			break




