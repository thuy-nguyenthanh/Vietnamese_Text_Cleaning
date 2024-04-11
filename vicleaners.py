# -*- coding: utf-8 -*-
from pyvi import ViTokenizer
import re

# flatten = lambda *n: (e for a in n for e in (flatten(*a) if isinstance(a, (tuple, list)) else (a,)))
# _whitespace_re = re.compile(r'\s+')


#Chuẩn hóa các ký tự đặc biệt
def _specChar(text):
	try:
		if len(text) == 1:
			return _spec_char[text]
		else:
			for char in _spec_char:
				if char in text:
					text = text.replace(char,u" " + _spec_char[char] + u" ")
   
			result = []
			for char in text.split():
				print("in processing: ",char)
				char=_unit_(char)
				# char = c_unit(char)
				# char = d_unit(char)
				# char = w_unit(char)
				print("out: ",char)
				result.append(char)
			return cleaners.join_str(result)
	except:
		return text

class cleaners(object):
	def __init__(self, text=None):
		if text == None:
			print("Text not None!")
			return
		self.str = text
		self.raw = text
		self.word_sent = []
		self.result = []

	def split_word_sent(self, text):
		self.word_sent = ViTokenizer.tokenize(text).split()
		return self.word_sent

	#Chuẩn hóa từ đặc biệt
	@staticmethod
	def _spec_char_(text):
		d = _spec_char()
		try:
			return d[text]
		except:
			return text

	#Chuẩn hóa từ viết tắt
	@staticmethod
	def _short_dict(text):
		d = short_dict()
		try:
			return d[text]
		except:
			return text

	#Xóa dấu cách
	@staticmethod
	def collapse_whitespace(text):
		return re.sub(_whitespace_re, ' ', text)

	#Chuẩn hóa giá trị số
	@staticmethod
	def normalize_numbers(text):
		text = re.compile(r'[0-9]+(\/[0-9]+)+').sub('', text)	#Xóa phân số
		text = re.compile(r'[0-9]+').sub('', text)				#Xóa số
		text = re.compile(r'[0-9]+(\.|\,)[0-9]+').sub('', text)	#Xóa số thập phân
		return text

	#Xóa dấu câu
	@staticmethod
	def normalize_punctuation(text):
		punctuation_re = re.compile(r'[.,?!;:(){}\[\]\'"<>]')
		return punctuation_re.sub('', text)

	@staticmethod
	def lower(text):
		return str(text).lower()
	
	def do(self):
		text = self.collapse_whitespace(self.str)  #Xóa các ký tự trắng thừa
		text = text.lower()	#Chuyển chữ hoa sang chữ thường
		# ws = self.split_word_sent(text)	#Tách từ
		
		text = self.normalize_numbers(text)
		text = self.normalize_punctuation(text)
		# text = self._normalize_commmas_(text)
  
		ws = text.split()
		result=[]
		for chars in ws:
			# if "_" in chars:
			# 	chars = chars.split("_")
			# else:
			# 	chars = [chars]
			chars = [chars]
   
			for char in chars:
				char = self._short_dict(char)
				# char = _normalize_numbers(char)
				char = _specChar(char)
				# char = c_unit(char)
				# char = d_unit(char)
				# char = w_unit(char)   
			
			result.append(char)
    	
		strResult=self.join_str(flatten(result))		
		self.result = self.split_word_sent(strResult)	#Tách từ
		return cleaners.join_str(flatten(self.result))

	def strip(self):
		self.str = self.str.strip()
		return self.str

	@staticmethod
	def join_str(list_str):
		return " ".join(list_str)


if __name__ == "__main__":
	with open("input.txt", mode="r", encoding="utf-8") as f:
		for line in f:
			print("Input:\n[%s]" % (line))
			# ret = cleaners(line).do()
			ret=_specChar(line)
			print("\nOutput:\n[%s]" % ret)
			input()
