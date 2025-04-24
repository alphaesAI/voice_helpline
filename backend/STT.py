# import speech_recognition as sr

# def listen():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("listening...")
#         audio = recognizer.listen(source)
#     try:
#         return recognizer.recognize_google(audio)
#     except sr.UnknownValueError:
#         return "sorry, i couldn't understand"
#     except sr.RequestError:
#         return "couldn't request results"