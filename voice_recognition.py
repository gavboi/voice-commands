import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print('Adjusting for ambient noise...')
    r.adjust_for_ambient_noise(source, duration=3)
    print('Say something!')
    audio = r.listen(source)

try:
    output = r.recognize_google(audio)
    print(f'You said: {output}')
except sr.UnknownValueError:
    print('Could not understand')
