; prints the key you just pressed

; coordinates 
ld va, 10
ld vb, 10

; main loop
to_loop:

    ld v0, k ; store the key 
    ld f, v0 ; get the location for the image
    cls ; clear the screen
    drw va, vb, 5
     
    jmp to_loop
    
    