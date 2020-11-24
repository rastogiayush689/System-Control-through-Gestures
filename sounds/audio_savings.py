from gtts import gTTS
import os

text = 'Voice control is paused'
lang = 'en'

obj = gTTS(text = text, lang = lang, slow = False)

obj.save('pause_voice.mp3')
os.system("pause_voice.mp3")
