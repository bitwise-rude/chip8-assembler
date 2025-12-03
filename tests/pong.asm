; org $200
; this is a classic pong game
; written by meyan adhikari

ld v0, $02
ld v1, $02

ld v2, $05
ld v3, $05

game:
    ld i, racket
    drw v0, v1, 8 ; drawing the racket

    ld i, ball
    drw v2, v3, 2 ; drawing the ball

    jmp game




racket:
    db 11000000,11000000,11000000,11000000,11000000,11000000, 11000000, 11000000

ball: 
    db 11000000,11000000