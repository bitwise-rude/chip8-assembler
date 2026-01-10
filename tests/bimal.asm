ld v0, 8
ld v1, 14

ld v7, 120

main:
    cls
    call draw_bimal
    call sleep
    jmp main


draw_bimal:
    ld i, B
    drw v0, v1, 5
    add v0, 6

    ld i, letter_i
    drw v0, v1, 5
    add v0, 6

    ld i, M
    drw v0, v1, 5
    add v0, 6

    ld i, A
    drw v0, v1, 5
    add v0, 6

    ld i, L
    drw v0, v1, 5

    ret

; -------------------------
; sleep + beep
; -------------------------
sleep:
    ld dt, v7
    ld st, v7
wait:
    ld v6, dt
    se v6, 00
    jmp wait
    ret

; -------------------------
; Sprites (5 bytes each)
; -------------------------

B:
    db %11110,%10001,%11110,%10001,%11110

letter_i:
    db %11111,%00100,%00100,%00100,%11111

M:
    db %10001,%11011,%10101,%10001,%10001

A:
    db %01110,%10001,%11111,%10001,%10001

L:
    db %10000,%10000,%10000,%10000,%11111

bimal:
