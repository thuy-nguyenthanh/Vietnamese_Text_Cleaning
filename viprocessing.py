# -*- coding: utf-8 -*-
# from pyvi import ViTokenizer
import re

# flatten = lambda *n: (e for a in n for e in (flatten(*a) if isinstance(a, (tuple, list)) else (a,)))

_whitespace_re = re.compile(r'\s+')
_string_ascii_re = re.compile(r'[a-z]+')

# Ky tu dac biet
_spec_char 	= {	u'&': u'và',u'@': u'a còng', u'^': u'mũ', u'$': u'đô la', 
					u'%': u'phần_trăm', u'*' : u'sao', u'+': u'cộng', u'>': u'dấu_lớn', 
					u'<': u'dấu_bé', u'=': u'bằng', u'/': u'trên'}

# Chu so
_number 		= {	0: u'không', 1: u'một', 2: u'hai', 3: u'ba', 4: u'bốn', 5: u'năm', 6: u'sáu', 7: u'bảy', 8: u'tám', 9: u'chín', 10: u'mười'}


# Don vi tien te
_currency 	= {	u'vnd': u'việt_nam_đồng', u'usd': 'đô_la_mỹ', u'eur': u'ơ_rô'}


# Don vi do luong
_d_unit 		= {	u'km': u'ki_lô_mét', u'cm': u'xen_ti_mét', u'dm': u'đề_xi_mét', u'mm': u'mi_li_mét', u'nm':u'na_nô_mét', 
					u'm2' : u'mét_vuông', u'm3' : u'mét_khối',
					u'hz' : u'héc', u'm' : u'mét',
					u'h': u'giờ', u'p': u'phút', u's': u'giây'
					} 


# Don vi can nang
_w_unit 		= {u'kg': u'ki_lô_gam', u'g': 'gam'}

#############################################################################################
### Các phương thức xử lý dữ liệu ###########################################################
#############################################################################################

# Tu dien viet tat
def short_dict():
	d = {}
	with open("short_dict.txt", encoding="utf-8") as f:
		for line in f:
			(key, val) = line.split(",")
			d[str(key).lower()] = str(val).lower()
	return d 

#Chuẩn hóa các ký tự đặc biệt
def remove_specChar(text):
	try:
		if len(text) == 1:
			return _spec_char[text]
		else:
			for char in _spec_char:
				if char in text:
					text = text.replace(char,u" " + _spec_char[char] + u" ")
			return text	
	except:
		return text

#Chuyển số thành chuổi 
def num_to_text(nInteger, flag):
	try:
		num = int(nInteger)
		if num <= 10: 
			if flag == 0:
				return _number[num]
			return u"linh " + _number[num]
		if num//1000000000 > 0:
			if num%1000000000 == 0: 
				return num_to_text(num//1000000000, 0) + u" tỷ"
			if num%1000000000 != 0: 
				return num_to_text(num//1000000000, 0) + u" tỷ " + num_to_text(num%1000000000, 1)
		if num//1000000 > 0:
			if num%1000000 == 0: 
				return num_to_text(num//1000000, 0) + u" triệu"
			if num%1000000 != 0: 
				return num_to_text(num//1000000, 0) + u" triệu " + num_to_text(num%1000000, 2)
		else:
			if flag == 1:
				return num_to_text(num//1000000, 0) + u" triệu " + num_to_text(num%1000000, 2)
		if num//1000 > 0:
			if num%1000 == 0: 
				return num_to_text(num//1000, 0) + u" nghìn"
			if num%1000 != 0: 
				return num_to_text(num//1000, 0) + u" nghìn " + num_to_text(num%1000, 3)
		else:
			if flag == 2:
				return num_to_text(num//1000, 0) + u" nghìn " + num_to_text(num%1000, 3)
		if num//100 > 0:
			if num%100 == 0: 
				return num_to_text(num//100, 0) + u" trăm"
			if num%100 != 0: 
				return num_to_text(num//100, 0) + u" trăm " + num_to_text(num%100, 4)
		else:
			if flag == 3:
				return num_to_text(num//100, 0) + u" trăm " + num_to_text(num%100, 4)
		if num//10 > 0:
			if num >= 20:
				if num%10 != 0:
					if num%10 == 1:
						return num_to_text(num//10, 0) + u" mươi mốt"
					if num%10 == 5:
						return num_to_text(num//10, 0) + u" mươi lăm"
					return num_to_text(num//10, 0) + u" mươi " + num_to_text(num%10, 0)
				else:
					return num_to_text(num//10, 0) + u" mươi"
			else:
				if num == 15: 
					return u"mười lăm"
				return u"mười " + num_to_text(num%10, 0)
	except:
		return nInteger

#Chuẩn hóa số
def normalize_numbers(word):
	try:
		if len(word) > 1:
			output = u''
			splitChar = ''
			res = [word]

			if ',' in word:
				res = word.split(',')
				splitChar =','

			if '.' in word:
				res = word.split('.')
				splitChar = '.'

			if '/' in word:
				res = word.split('/')
				splitChar = '/'

			if len(res) > 1:
				if splitChar in ['.', ',']:
					for i, map in enumerate(res):
						if i < len(res) - 1:
							output += num_to_text(map, 0) + u" phẩy "
						else: 
							output += num_to_text(map, 0)

				# if splitChar in ['/']:
				# 	if len(res) == 3:
				# 		if int(res[0]) <=31 and int(res[1]) <=12 and len(res[2]) == 4:
				# 			return u"ngày " + num_to_text(res[0], 0) + u" tháng " + num_to_text(res[1], 0) + u" năm " + num_to_text(res[2], 0)
				# 	elif len(res) == 2:
				# 		if int(res[0]) <= 31 and int(res[1]) <= 12:
				# 			return u"ngày " + num_to_text(res[0], 0) + u" tháng " + num_to_text(res[1], 0)
				# 		elif int(res[0]) <= 12 and len(res[1]) == 4:
				# 			return u"tháng " + num_to_text(res[0], 0) + u" năm " + num_to_text(res[1], 0)
							
					for i, map in enumerate(res):
						if i < len(res) - 1:
							output += num_to_text(map, 0) + u" phần "
						else: 
							output += num_to_text(map, 0)

				if str(word).isdigit():
					return num_to_text(word, 0).split()
				
				return output
			else:
				return num_to_text(word,0)
    
		return word
	except:
		return word

#Chuẩn hóa ngày tháng năm
def normalize_date(word):
	try:
		if len(word) > 1:
			output = u''
			splitChar = ''
			res = [word]

			if '/' in word:
				res = word.split('/')
				splitChar = '/'

			if len(res) > 1:
				if splitChar in ['/']:
					if len(res) == 3:
						if int(res[0]) <=31 and int(res[1]) <=12 and len(res[2]) == 4:
							return u"ngày " + num_to_text(res[0], 0) + u" tháng " + num_to_text(res[1], 0) + u" năm " + num_to_text(res[2], 0)
					elif len(res) == 2:
						if int(res[0]) <= 31 and int(res[1]) <= 12:
							return u"ngày " + num_to_text(res[0], 0) + u" tháng " + num_to_text(res[1], 0)
						elif int(res[0]) <= 12 and len(res[1]) == 4:
							return u"tháng " + num_to_text(res[0], 0) + u" năm " + num_to_text(res[1], 0)

				if str(word).isdigit():
					return num_to_text(word, 0).split()
				
				return output
			else:
				return num_to_text(word,0)
    
		return word
	except:
		return word

#Chuẩn hóa đơn vị đo lường các loại 
class Units:
	def __init__(self, word=None):
		if word == None:
			print("Text not None!")
			return
		self.word = word

   #Chuẩn hóa đơn vị tiền tệ
	@staticmethod
	def c_unit(word):
		try:
			return _currency[word]
		except:
			return word    

	#Chuẩn hóa đơn vị cân nặng
	@staticmethod
	def w_unit(word):
		try:
			return _w_unit[word]
		except:
			return word

	#Chuẩn hóa đơn vị khoảng cách
	@staticmethod 
	def d_unit(word):
		try:
			return _d_unit[word]
		except:
			return word  

	def all_units(self):
		rerult =self.c_unit(self.word)
		rerult =self.w_unit(rerult)  
		rerult =self.d_unit(rerult)
		return rerult
def normalize_units(word):
   _unit=Units(word)
   return _unit.allUnit()