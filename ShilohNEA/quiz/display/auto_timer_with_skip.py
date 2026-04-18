import time


def auto_timer_with_skip():
    try:
        answer = input("You have 10 minutes to revise. Type 's' to skip, or press Enter to start: ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nRevision timer skipped.")
        return True

    if answer == 's':
        print("Timer skipped!")
        return True

    print("Revision timer running. Press Ctrl+C at any time to skip.\n")
    try:
        for remaining in range(600, 0, -1):
            print(f"\rTime left: {remaining}s", end="")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nTimer skipped!")
        return True

    print("\nTime's up!")
    return False
