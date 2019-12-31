from bs4 import BeautifulSoup
import numpy as np
import cv2
import os
from MakeTreeDir import MAKETREEDIR
import pytesseract
import pandas as pd

class TessToDict:
	def __init__(self):
		pass
	def tess2dict(self,image,outname,outpath='.',config=''):
		"""Function to call tesseract in hocr mode and get word level dataframe

		Args:
			image (np.ndarray): input image
			outname (str): output name
			outpath (str): directory to save the .hocr output
			config (str): tesseract configuration params
		Returns:
			dict: word_dict containing coordinates and content of each word

		Examples
			>>> import cv2
			>>> from tesseract2dict import TessToDict
			>>> td=TessToDict()
			>>> inputImage=cv2.imread('path/to/image.jpg')
			>>> word_dict=td.tess2dict(inputImage,'out','outfolder')

		"""
		try:
			### temp file creation for tesseract call
			directory=MAKETREEDIR()
			directory.makedir('tmp')
			cv2.imwrite('tmp/hocr.jpg',image)
			if outpath not in ['.','']:
				directory.makedir(outpath)
			###call tesseract to get hocr out
			pytesseract.pytesseract.run_tesseract(
			'tmp/hocr.jpg', '{}'.format(os.path.join(outpath,outname)),
			extension='.html', lang='eng', config="hocr {}".format(config))
			### removing temp files
			os.remove("tmp/hocr.jpg")
			os.rmdir('tmp')

			### hocr to word_dict
			word_dict= self.hocr2dict(outpath,outname)
		except Exception as e:
			print(e)
			word_dict=pd.DataFrame(columns=['x','y','w','h','text','conf'])
		return word_dict

	def hocr2dict(self,outpath,name):
		"""parse hocr and return word dictionary

		Args:
			outpath (str):  path in which hocr out is saved
			name (str): hocr name

		Returns:
			dict: word_dict containing coordinates and content of each word
		"""
		try:
			### read hocr
			with open(os.path.join(outpath,name+'.hocr'),mode='r',encoding="utf8") as f:
				hout=f.read()

			### parsing and converting to word dict
			parsed_html = BeautifulSoup(hout,"html.parser")
			words=parsed_html.body.find_all('span',attrs={'class':'ocrx_word'})
			word_dict=pd.DataFrame()

			for index,word in enumerate(words):
				bbox,conf=word['title'].split(';')
				x,y,x2,y2=bbox.split(' ')[1:]
				confidence=conf.split(' ')[-1]
				text=word.text
				w=int(x2)-int(x)
				h=int(y2)-int(y)
				word_dict.loc[index,'x']=int(x)
				word_dict.loc[index,'y']=int(y)
				word_dict.loc[index,'w']=int(w)
				word_dict.loc[index,'h']=int(h)
				word_dict.loc[index,'text']=text
				word_dict.loc[index,'conf']=int(confidence)
		except Exception as e:
			print(e)
			word_dict=pd.DataFrame(columns=['x','y','w','h','text','conf'])
		return word_dict
