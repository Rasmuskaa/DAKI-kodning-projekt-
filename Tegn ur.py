import math
import pygame
import sys
from datetime import datetime  # Tidspunkt lige nu

pygame.init()  # Kalder alle pygames moduler
SKÆRM_BREDDE = 600
SKÆRM_HØJDE = 600


RØD = (255, 000, 000)
SORT = (0, 0, 0)
ORANGE = (255, 165, 0)

# Opretter vinduet
screen = pygame.display.set_mode((SKÆRM_BREDDE, SKÆRM_HØJDE))
pygame.display.set_caption("Ur")
clock = pygame.time.Clock()

# centrum og radius (afstand fra centrum til endepunktet)
cx, cy, r = 300, 300, 250

# 2 * pi er en hel cirkel, dermed når man dividere med 12 får man steppet for timemarkeringerne
step = 2 * math.pi / 12
lille_step = 2 * math.pi / 60


# main loop - et loop der bliver ved med at køre ind til man lukker programmet
while True:
    # Event handling:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # bruger kan trykke på kryds, og programmet vil lukke
            pygame.quit()
            sys.exit()

    # Tegner baggrund
    screen.fill(SORT)

    # Tegner en fyldt orange cirkel som ur baggrund (første lag)
    pygame.draw.circle((screen), (ORANGE), (cx, cy), (251), width=0)

    # Laver sekund/minut-markeringer for uret
    for i in range(60):
        theta = i * lille_step  # vinkel i radianer
        x = cx + r * math.cos(theta)  # x-koordinaten for endepunktet
        y = cy + r * math.sin(theta)  # y-koordinaten for endepunktet

        # tegn en linje fra centrum (cx, cy) til (x, y)
        pygame.draw.line(screen, (0, 0, 0), (cx, cy), (int(x), int(y)), 2)

        # Indre cirkel (anden lag)
        pygame.draw.circle((screen), (ORANGE), (cx, cy), (240), width=0)

    # Laver time-markeringer for uret:
    for i in range(12):
        theta = i * step  # vinkel i radianer
        x = cx + r * math.cos(theta)
        y = cy + r * math.sin(theta)

        # tegner en linje fra centrum (cx, cy) til (x, y)
        pygame.draw.line(screen, (0, 0, 0), (cx, cy), (int(x), int(y)), 5)
        # Indre cirkel (tredje lag)
        pygame.draw.circle((screen), (ORANGE), (cx, cy), (220), width=0)

    # VISERNE:
    now = datetime.now()  # Henter nuværende tid
    h = now.hour % 12   # bruger % 12, da man importere timer med 24
    m = now.minute
    s = now.second

    # Sekundviser
    # 6 grader pr. sekund, da 360/60 = 6 og - 90 grader, da vi roterer til kl 12
    ang_sec = math.radians(s * 6 - 90)
    Ls = int(r * 0.95)  # Længde på sekundviser
    # lægger cx og cy til, flytter du den fra (0,0) til ures centrum (cos/sin fungere i en enhedscirkel)
    # Bruger her formlen for at konvertere retning og afstand for viseren: (x, y) = (cx + r * cos(vinkel), cy + r * sin(vinkel))
    sx = cx + Ls * math.cos(ang_sec)
    sy = cy + Ls * math.sin(ang_sec)
    # Kan nu tegne viseren
    pygame.draw.line(screen, (200, 0, 0), (cx, cy), (int(sx), int(sy)), 2)

    # Minutviser (glider med sekunder)
    # 6° pr. minut plus de resterende sekunder, så viseren glider med
    ang_min = math.radians((m + s/60) * 6 - 90)
    Lm = int(r * 0.75)                            # længde på minutviser
    mx = cx + Lm * math.cos(ang_min)
    my = cy + Lm * math.sin(ang_min)
    pygame.draw.line(screen, (0, 0, 0), (cx, cy), (int(mx), int(my)), 4)

    # Timeviser (glider med min + sekunder)
    # 30° pr. time plus de resterende minutter, så viseren glider med
    ang_hour = math.radians((h + m/60 + s/3600) * 30 - 90)
    Lh = int(r * 0.5)  # længde på timevise
    hx = cx + Lh * math.cos(ang_hour)
    hy = cy + Lh * math.sin(ang_hour)
    pygame.draw.line(screen, (0, 0, 0), (cx, cy), (int(hx), int(hy)), 6)

    # tager alle forandringerne lavet i objektet og tegner det
    pygame.display.update()

    # While loopet vil programmet køres max 15 gange i sekundet
    clock.tick(15)
