
def bg(r, g, b):
    return f"\033[48;2;{r};{g};{b}m"


THEMES = {
    "Default": {
        "wall":    bg(220, 220, 220),
        "passage": bg(10, 10, 10),
        "entry":   bg(180, 0, 220),
        "exit":    bg(200, 30, 30),
        "number":  bg(180, 180, 180),
    },
    "Ocean": {
        "wall":    bg(0, 80, 120),
        "passage": bg(0, 20, 40),
        "entry":   bg(0, 200, 180),
        "exit":    bg(255, 100, 0),
        "number":  bg(0, 120, 160),
    },
    "Earthy": {
        "wall":    bg(47, 147, 1),
        "passage": bg(94, 67, 39),
        "entry":   bg(180, 220, 50),
        "exit":    bg(200, 80, 30),
        "number":  bg(0, 224, 228),
    },
    "Lava": {
        "wall":    bg(205, 49, 5),
        "passage": bg(40, 5, 5),
        "entry":   bg(255, 200, 0),
        "exit":    bg(0, 0, 0),
        "number":  bg(255, 173, 5),
    },
    "BENFICA SLB GLORIOSO": {
        "wall":    bg(210, 0, 0),
        "passage": bg(20, 5, 0),
        "entry":   bg(250, 220, 0),
        "exit":    bg(255, 255, 255),
        "number":  bg(255, 255, 255),
    },
    "PORTUGAL SELACAO DAS QUINAS CAMPEOES DO MUNDIAL 2026": {
        "wall":    bg(215, 5, 5),
        "passage": bg(40, 152, 20),
        "entry":   bg(250, 220, 0),
        "exit":    bg(255, 255, 255),
        "number":  bg(250, 246, 62),
    },
    "ZAPORTING": {
        "wall":    bg(3, 251, 62),
        "passage": bg(255, 255, 255),
        "entry":   bg(250, 220, 0),
        "exit":    bg(0, 0, 0),
        "number":  bg(250, 220, 0),
    },
}
