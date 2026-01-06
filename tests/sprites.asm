ld v0, 30
ld v1, 14

loop:
    ld i, SPRITE
    cls
    drw v0, v1, 5
    jmp loop

SPRITE:
    db 255,255,255,255,255