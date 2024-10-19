import random
import pyfiglet

def generate_random_ascii_art():
    text = random.choice(["Hello", "World", "GitHub Actions", "ASCII Art"])
    ascii_art = pyfiglet.figlet_format(text)
    return ascii_art

if __name__ == "__main__":
    print(generate_random_ascii_art())
