
def bg(r: int, g: int, b: int) -> str:
    return f"\033[48;2;{r};{g};{b}m"


THEMES = {
    "Default": {
        "wall":    bg(220, 220, 220),
        "passage": bg(10, 10, 10),
        "entry":   bg(180, 0, 220),
        "exit":    bg(200, 30, 30),
        "number":  bg(180, 180, 180),
        "path":    bg(0, 200, 100),
    },
    "Ocean": {
        "wall":    bg(0, 80, 120),
        "passage": bg(0, 20, 40),
        "entry":   bg(0, 200, 180),
        "exit":    bg(255, 100, 0),
        "number":  bg(0, 120, 160),
        "path":    bg(0, 255, 220),
    },
    "Earthy": {
        "wall":    bg(47, 147, 1),
        "passage": bg(94, 67, 39),
        "entry":   bg(180, 220, 50),
        "exit":    bg(200, 80, 30),
        "number":  bg(0, 224, 228),
        "path":    bg(255, 220, 80),
    },
    "Benfica": {
        "wall":    bg(210, 0, 0),
        "passage": bg(20, 5, 0),
        "entry":   bg(140, 198, 253),
        "exit":    bg(255, 255, 255),
        "number":  bg(255, 255, 255),
        "path":    bg(255, 220, 0),
    },
    "BubbleGum": {
        "wall":    bg(255, 198, 246),
        "passage": bg(255, 254, 246),
        "entry":   bg(210, 0, 0),
        "exit":    bg(140, 198, 253),
        "number":  bg(140, 198, 253),
        "path":    bg(255, 211, 158),
    },
}
