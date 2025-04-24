# from gtts import gTTS
# from io import BytesIO
# import pygame

# def speak(text: str):
#     tts = gTTS(text=text, lang='en')
#     mp3_fp = BytesIO()
#     tts.write_to_fp(mp3_fp)
#     mp3_fp.seek(0)

#     pygame.mixer.init()
#     pygame.mixer.music.load(mp3_fp, 'mp3')
#     pygame.mixer.music.play()

#     while pygame.mixer.music.get_busy():
#         continue