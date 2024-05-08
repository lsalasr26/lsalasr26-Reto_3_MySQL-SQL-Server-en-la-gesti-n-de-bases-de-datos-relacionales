from textblob import TextBlob
from deep_translator import GoogleTranslator


text = 'Una manzana'

transTex = GoogleTranslator(source='spanish', target='english').translate(text)

print(transTex)