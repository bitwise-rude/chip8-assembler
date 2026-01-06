; Prints out natural number

; coordinates (middle of the screen)
ld v0, 30 
ld v1, 14

; natural number storage
ld v2, 1

; how many second  to hold, 60 means 1 second
ld v3, 60


loop:
    ld f, v2
    cls
    drw v0,v1,5
    add v2, 1

    sne v2,15
    call reset

    call sleep

    jmp loop

sleep:
    ld dt, v3
    loop2:
        ld v4, dt
        se v4, 00
        jmp loop2
    ret

reset:
    ld v2, 1
    ret
