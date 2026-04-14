import threading
import time
import sys

# Non-blocking input for Windows
try:
    import msvcrt
    def getch():
        return msvcrt.getch().decode('utf-8')
except ImportError:
    import sys, tty, termios
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def auto_timer_with_skip():
    print("You have 10 minutes to revise... (press 's' then Enter to skip)")
    start = time.time()
    skip = False

    def check_skip():
        nonlocal skip
        while not skip:
            ch = sys.stdin.readline().strip().lower()
            if ch == 's':
                skip = True
                break

    t = threading.Thread(target=check_skip, daemon=True)
    t.start()

    while True:
        elapsed = time.time() - start
        remaining = 600 - elapsed
        print(f"\rTime left: {int(remaining)}s", end="")
        if skip:
            print("\nTimer skipped!")
            return True
        if elapsed > 600:
            print("\nTime's up!")
            return False
        time.sleep(1)
