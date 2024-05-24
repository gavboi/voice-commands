import time
import sys

import speech_recognition as sr


# process arg for name
name = 'computer'
if len(sys.argv) > 1:
    name = sys.argv[1]

# processing options
commands = []
def note(content):
    with open(f'note-{str(time.time()).split(".")[0]}.txt', 'w') as file:
        file.write(content)
commands.append({
    'name': 'Note',
    'phrases': ['write', 'write down', 'write down that', 'take a note to'],
    'action': note
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
                        content = output[output.lower().index(phrase)+len(phrase):].strip()
                        print(f'{command["name"]}: {content}')
                        command['action'](content)
                        processed = True
                        break
                if processed:
                    break
        else:
            print(f'{output}')
            
    except sr.UnknownValueError:
        print('(Could not understand!)')
    finally:
        print('(Listening)')
