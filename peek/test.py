from asciimatics.screen import Screen


def demo(screen):
    while True:
        screen.print_at('Hello world!', 0, 0)
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return
        if ev in (ord('B'), ord('b')):
            screen.print_at('Bubba!', 10, 0)
            screen.refresh()
        screen.refresh()

Screen.wrapper(demo)
