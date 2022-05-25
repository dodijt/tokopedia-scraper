import requests, json, os
from bs4 import BeautifulSoup as bs
import csv

class tokopedia():
	def __init__(self, namatoko):
		self.tokourl = 'https://tokopedia.com/'+namatoko
		self.namatoko = namatoko
		self.headerbrowser = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'}
		self.getid()
	
	def getid(self):
		try:
			req = requests.post(self.tokourl, headers=self.headerbrowser, timeout=3.000)
			if req.status_code == 200:
				sup = bs(req.text, 'html.parser')
				for i in sup.find_all('meta', attrs={'name':'branch:deeplink:$android_deeplink_path'}):
					self.idToko = i.get('content')[5:]
				self.scrapJson()
			else:
				print('Toko Tidak ditemukan')
		except:
			print('Toko tidak valid')

	def scrapJson(self):
		urlJson = 'https://ace.tokopedia.com/search/product/v3?shop_id={}&rows=80&start=0&full_domain=www.tokopedia.com&scheme=https&device=desktop&source=shop_product'.format(self.idToko)
		req = requests.get(urlJson, headers=self.headerbrowser)
		self.hasilReq = req.json()
		if not os.path.isdir(self.namatoko):
			os.mkdir(self.namatoko)
		with open('{}/{}_[detail].json'.format(self.namatoko,self.namatoko), 'w') as fileW:
			json.dump(self.hasilReq, fileW)
		self.showData()

	def showData(self, path='data_products.csv'):
		self.jumlahProduk = len(self.hasilReq['data']['products'])
		self.fullProduk = []
		for num,i in enumerate(self.hasilReq['data']['products']):
			self.fullProduk += [{'name':i['name'], 'harga':i['price'], 'link':i['url'], 'image':i['image_url'],'category':i['category_name']}]

		with open(path, 'w') as file:
			writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
			writer.writerow(['name', 'harga', 'link', 'image', 'category'])
			index = 0
			for data in self.fullProduk:
				writer.writerow([index, self.fullProduk[index]['name'], self.fullProduk[index]['harga'], self.fullProduk[index]['link'], self.fullProduk[index]['image'], self.fullProduk[index]['category']])
				index = index+1
			print(f"Data saved to `{path}`")

	def saveProduk(self):
		with open('{}/{}_[produk].json'.format(self.namatoko,self.namatoko), 'w') as fileW:
			json.dump(self.fullProduk, fileW)

inputLink = input('Nama Toko : https://tokopedia.com/')
actionToko = tokopedia(inputLink)



