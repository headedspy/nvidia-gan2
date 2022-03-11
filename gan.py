import requests, re, shutil, os, base64, random, string
from argparse import ArgumentParser
from threading import Thread
from time import sleep

parser = ArgumentParser()
parser.add_argument('-s', '--style', dest='style')
parser.add_argument('-t', '--threads', dest='threads')
args = parser.parse_args()

style = args.style
threads = args.threads

def getUrl():
	print('Getting server address...')
	r = requests.get('http://54.187.79.102/gaugan2/demo.js')
	urls = re.findall(r'\'(http.*?://.*?/)\'', re.search(r'urls=.*?;', r.text)[0])
	return urls[0]
    
url = getUrl()
i = 0
print(f'THREADS: {threads}')

def processImage(threadName, img):
	global i
	global processed_images
	processed_images += 1
	print(f'Processing image \'{img}\'')
	style_img = True

	if str(style).isdigit():
		style_img = False

	# get b64 encoded image
	with open('./in/' + img, "rb") as f:
		imgb64 = 'data:image/png;base64,' + str(base64.b64encode(f.read()))[2:-1]

	if style_img:
		with open(str(style), "rb") as f:
			imgb64_style = 'data:image/png;base64,' + str(base64.b64encode(f.read()))[2:-1]

	# generate name for requests
	name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

	while True:
		try:
			if style_img:
				POSTdata = {
					'name': name,
					'file': imgb64_style
				}
				requests.post(url + 'gaugan2_receive_style_image', data = POSTdata, stream = True)
			
				# send map img to server
				POSTdata = {
					'name': name,
					'masked_segmap': imgb64,
					'masked_edgemap': '',
					'masked_image': '',
					'style_name': 'custom',
					'caption': '',
					'enable_seg': 'true',
					'enable_edge': 'false',
					'enable_caption': 'false',
					'enable_image': 'false',
					'use_model12': 'false'
				}
			else:
				POSTdata = {
					'name': name,
					'masked_segmap': imgb64,
					'masked_edgemap': '',
					'masked_image': '',
					'style_name': str(style),
					'caption': '',
					'enable_seg': 'true',
					'enable_edge': 'false',
					'enable_caption': 'false',
					'enable_image': 'false',
					'use_model12': 'false'
				}
            
			requests.post(url + 'gaugan2_infer', data = POSTdata)
			# get generated img from server
			POSTdata = {
				'name': name
			}
			r = requests.post(url + 'gaugan2_receive_output', data = POSTdata, stream = True)
			break
		except:
			url = getUrl() # if there is an error getting the image get a new server URL and try again

	r.raw.decode_content = True

	# write image to out folder
	with open('Out/' + img.split('.')[0] + '.jpg','wb') as f:
		shutil.copyfileobj(r.raw, f)

	i -= 1

list = [None] * int(threads)
processed_images = 0
img_list = os.listdir('./In/')
print(len(img_list))

while processed_images != len(img_list):
	if i == 0:
		for thread in range(int(threads)):
			try:
				list[i] = Thread(target = processImage, args = (str(i), img_list[processed_images]))
				list[i].start()
				i += 1
			except:
				print("No more images")
