import time
import sys

from playsound import playsound
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# process arg for name
name = 'computer'
if len(sys.argv) > 1:
    name = sys.argv[1]

# processing options; actions
def note(content):
    with open(f'note-{str(time.time()).split(".")[0]}.txt', 'w') as file:
        file.write(content)
def google(content):
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--incognito')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(content)
    search_box.send_keys(Keys.RETURN)
    while True:
        try:
            handles = driver.window_handles
            if not handles:
                break
        except:
            break
        time.sleep(1)
# processing options; command data
commands = []
commands.append({
    'name': 'Note',
    'phrases': ['write', 'write down', 'write down that', 'take a note to', 'note down'],
    'action': note
})
commands.append({
    'name': 'Google',
    'phrases': ['google', 'search', 'search for', 'look up'],
    'action': google
})
commands.append({
    'name': 'Exit',
    'phrases': ['exit', 'stop listening'],
    'action': lambda x: None
})

# initialize
r = sr.Recognizer()
m = sr.Microphone()
running = True
processed = False

# prepare recognizer
with m as source:
    print('(Adjusting for ambient noise)')
    r.adjust_for_ambient_noise(source, duration=3)
print('(Ready)')

# loop
while running:
    print('(Listening)')
    with m as source:
        audio = r.listen(source)
    processed = False
    print('(Processing)')
    try:
        output = r.recognize_google(audio)
        if output.lower().startswith(name) or output.lower().startswith(f'hey {name}'):
            print(f'** {output}')
            # remove name
            output = output[output.lower().index(name)+len(name):].strip()
            for command in commands:
                for phrase in sorted(command['phrases'], key=len, reverse=True):
                    if output.lower().startswith(phrase):
                        if command['name'] == 'Exit':
                            print('(Exiting)')
                            playsound('beep-off.wav')
                            exit()
                        content = output[output.lower().index(phrase)+len(phrase):].strip()
                        print(f'{command["name"]}: {content}')
                        command['action'](content)
                        processed = True
                        playsound('beep-success.wav')
                        break
                if processed:
                    break
            if not processed:
                playsound('beep-none.wav')
                print('(No command match)')
        else:
            print(f'{output}')
            
    except sr.UnknownValueError:
        print('(Could not understand!)')
