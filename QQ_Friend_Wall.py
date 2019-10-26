#Time : 2019/09/21

from urllib import request
import PIL.Image as Image
import os
import sys
import math
import shutil

# 获取文件所在的绝对路径
def get_dir(sys_arg):
	sys_arg = sys_arg.split("/")
	dir_str = ""
	count = 0
	for cur_dir in sys_arg:
		if count == 0:
			count = count + 1
		if count == len(sys_arg):
			break
		dir_str = dir_str + cur_dir + "/"
		count = count + 1
	return dir_str

# 完成好友头像的获取及下载
def get_imgs():

	# 获取当前路径信息
	curr_dir = get_dir(sys.argv[0])
	# 如果FriendImgs目录不存在就创建一个
	if not os.path.exists(curr_dir + "FriendImgs/"):
		os.mkdir(curr_dir + "FriendImgs/")

	#打开csv文件并读取邮箱信息
	my_friends = []
	try:
		file = open("QQmail.csv", 'r',encoding='utf-8')#默认编码为gbk，QQ邮箱导出为utf-8
	except FileNotFoundError:
		print('啊叻? 遇到个错误: 没有找到文件 "QQmail.csv" , 参照以下方法解决.\n')
		print('使用方法：')
		print('	Step 1 ：打开 QQ 邮箱 → 点击"通讯录" → 将 QQ 好友添加到通讯录 → 回到通讯录点击"工具" → 选择"导出联系人" → 选择"CSV"格式')
		print('	Step 2 ：将下载的 "QQmail.csv" 文件和本程序保存在同一文件夹下 → 运行本程序\n')
		print('视频演示：')
		print('	微信公众号：lguoachn')
		print('	b站：lguoachn')
		sys.exit()


	for line in file:
		line = line.strip()
		arr = line.split(",")
		qq_num = arr[3]
		my_friends.append(qq_num)

	# 获取好友头像信息并存储在FriendImgs目录中
	print("开始获取头像文件")
	n = 0
	for friend in my_friends:
		qq_num1 = friend.split("@")

		if qq_num1[0].isdigit() : #判断是否为数字字符串
			url = "http://q.qlogo.cn/g?b=qq&nk=" + str(qq_num1[0]) + "&s=100"
			request.urlretrieve(url=url, filename=curr_dir + "FriendImgs/" + qq_num1[0] + ".jpg")
			print("您的第 "+str(n+1)+" 个好友："+str(qq_num1[0]))
			n = n + 1

	return n

# 用于制作生成照片墙
def to_Photo_Wall():

	# 获取下载的头像文件
	curr_dir = get_dir(sys.argv[0])
	ls = os.listdir(curr_dir + 'FriendImgs')
	n = len(ls)
	print("共获取到 " + str(n) + " 个头像文件")

	#获取尺寸边长
	x_line = math.floor(math.sqrt(n))
	y_line = math.floor(math.sqrt(n))
	than_num = n - x_line * y_line
	if than_num > 0 and than_num <= x_line:
		x_line += 1
	if than_num > x_line:
		x_line += 2

	# 准备生成微信好友头像墙的尺寸
	each_size = 100
	image = Image.new("RGB", (x_line * each_size, y_line * each_size))

	# 定义初始图片的位置
	x = 0
	y = 0

	# 遍历文件夹的图片
	print("正在生成 ……")
	for file_names in ls:
		try:
			# 依次打开图片
			img = Image.open(curr_dir + "FriendImgs/" + file_names)
		except IOError:
			continue
		else:
			# 重新设置图片的大小
			img = img.resize((each_size, each_size), Image.ANTIALIAS)
			# 将图片粘贴到最终的照片墙上
			image.paste(img, (x * each_size, y * each_size))
			# 设置每一行排x_line个图像
			x += 1
			if x == x_line:
				x = 0
				y += 1
	# 保存图片为WeChat_Friends.jpg		
	img = image.save(curr_dir + "QQ好友墙.jpg")

	#把生成的图片文件夹删除
	try:
		shutil.rmtree(curr_dir + "FriendImgs/")
	except FileNotFoundError:
		print("遇到个小错误：未删除文件夹")

if __name__=='__main__':
	print("开始运行 ……\n")
	get_imgs()
	to_Photo_Wall()
	print("生成完毕")
	print("请查看该目录下的 “QQ头像墙.jpg” 文件")
	print("\n工具作者：@lguoachn")
	print("公众号：lguoachn")
	print("Beta 1.0")
	print("2019/09/21")