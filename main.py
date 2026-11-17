import cv2
import numpy as np
import pygame


pygame.init()


class Window:
    w = 500
    h = 500


class Body:
    m = 1   # [kg]
    x = 0
    y = 0

    def __init__(self, x:float = 0, y:float = 0, m:float = 1):
        self.x = x
        self.y = y
        self.m = m

    def draw(self):
        cv2.circle(
            canvas,
            (round(self.x), round(self.y)),
            4,
            (250, 150, 200),
            1
        )


def getQTPathFromPos(x:int, y:int, precision:int = 1):
    width, height = Window.w, Window.h

    out = []
    for i in range(precision):
        width /= 2
        height /= 2

        b0, b1 = 0, 0
        if width < x:
            x -= width
            b0 = 1
        if height < y:
            y -= height
            b1 = 1

        out.append(b0 + 2*b1)

    return out


def renderQTSegment(img, qtpath:list[int]):
    width, height = Window.w, Window.h
    p1 = [0, 0]
    for num in qtpath:
        width /= 2
        height /= 2

        if num not in (0, 1, 2, 3):
            raise Exception("QTpath can only contain indices from 0 through 4.")

        b1, b0 = divmod(num, 2)

        p1[0] += b0 * width
        p1[1] += b1 * height

    p2 = [round(p1[0] + width), round(p1[1] + height)]
    p1 = [round(p1[0]), round(p1[1])]

    cv2.rectangle(img,
                  p1,
                  p2,
                  (200, 100, 50),
                  1)


def renderQTSegmentRecursive(img, qtpath:list[int]):
    for i in range(1, len(qtpath) + 1):
        renderQTSegment(img, qtpath[:i])


qtpath = []
def mouse_callback():
    global qtpath
    x, y = pygame.mouse.get_pos()
    qtpath = getQTPathFromPos(x, y, 6)


canvas = None
def numpy_to_surface():
    global canvas
    arr_rgb = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)
    return pygame.surfarray.make_surface(arr_rgb.swapaxes(0, 1))

screen_ref = None
def try_init_screen():
    global screen_ref
    if pygame.get_init():
        screen_ref = pygame.display.set_mode((Window.w, Window.h))
    else:
        raise Exception("Pygame not initialized!")













def main():
    global qtpath, canvas

    try_init_screen()

    bodies = []
    bodies.append(Body(Window.w//2 - 100, Window.h//2 + 70))
    bodies.append(Body(Window.w//2 + 130, Window.h//2 + 200))

    canvas = np.zeros((Window.w, Window.h, 3), dtype=np.uint8)
    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(30) / 1000.0

        canvas = np.zeros((Window.w, Window.h, 3), dtype=np.uint8)
        canvas[:] = (25, 25, 25)

        # cv2.putText(canvas, "This is a demo", (100, 200), cv2.FONT_HERSHEY_PLAIN, 3,
        #             (200, 0, 0), 1)

        mouse_callback()
        renderQTSegmentRecursive(canvas, qtpath)

        for body in bodies:
            body.draw()
            qtpath = getQTPathFromPos(body.x, body.y, 6)
            renderQTSegmentRecursive(canvas, qtpath)

        screen_ref.blit(numpy_to_surface(), (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False


if __name__=="__main__":
    main()
