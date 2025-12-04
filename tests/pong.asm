;========================
; CHIP-8 PONG GAME
;========================
; Memory map:
; 0x200: program start
; 0x300: ball sprite (1 byte)
; 0x310: paddle sprite (4 bytes)
;========================

org 0x200

;------------------------
; Initialization
;------------------------
ld v0, 12       ; paddle1 Y position (middle)
ld v1, 12       ; paddle2 Y position
ld v2, 30       ; ball X
ld v3, 14       ; ball Y
ld v4, 1        ; ball X velocity (1 = right, 255 = left)
ld v5, 1        ; ball Y velocity (1 = down, 255 = up)

; Main loop
loop:
    cls                     ; clear screen

    ; Draw paddles
    ld f, v0
    drw 0, v0, 4            ; paddle1 at X=0, Y=V0
    ld f, v1
    drw 60, v1, 4           ; paddle2 at X=60, Y=V1

    ; Draw ball
    ld f, v2
    drw v2, v3, 1           ; ball sprite is 1 byte

    ;------------------------
    ; Input handling (simplified)
    ;------------------------
    ; Paddle1 Up (key 1)
    skp 1
    add v0, 255              ; subtract 1 modulo 256
    ; Paddle1 Down (key 2)
    skp 2
    add v0, 1
    ; Paddle2 Up (key 3)
    skp 3
    add v1, 255
    ; Paddle2 Down (key 4)
    skp 4
    add v1, 1

    ;------------------------
    ; Ball movement
    ;------------------------
    add v2, v4               ; ball X += velocity
    add v3, v5               ; ball Y += velocity

    ; Wall collision
    se v3, 0
    ld v5, 1                 ; bounce down
    se v3, 28
    ld v5, 255               ; bounce up (255 ≡ -1)

    ; Paddle collision
    se v2, 1                 ; ball at paddle1 X=0
    se v3, v0
    ld v4, 1                 ; bounce right
    se v2, 58                ; ball at paddle2 X=60
    se v3, v1
    ld v4, 255               ; bounce left

    ;------------------------
    ; Delay for visible movement
    ld dt, 10
delay:
    ld v7, dt
    se v7, 0
    jmp delay

    jmp loop

;------------------------
; Sprites
;------------------------
org 0x300
ball:   db %10000000        ; 1x1 ball
paddle: db %1111            ; 1x4 paddle

