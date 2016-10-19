def accept_input(eventlist, Camera):
    #Events.
    for event in events:

        #Exit.
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            return "quit"
        
        elif event.type == KEYDOWN:
            #Rotation
            if event.key == K_j: #+Y
                ROTATING[1] = 1
            if event.key == K_i: #+X
                ROTATING[0] = 1
            if event.key == K_l: #-Y
                ROTATING[1] = -1
            if event.key == K_k: #-X
                ROTATING[0] = -1
            if event.key == K_o: #+Z
                ROTATING[2] = 1
            if event.key == K_p: #-Z
                ROTATING[2] = -1

            if event.key == K_m: #Reset z rotation.
                Camera.look((Camera.angle[0],
                             Camera.angle[1],
                             0))
                
            #Translation
            if event.key == K_w: #Forward
                MOVING[2] = 1
            if event.key == K_s: #Backward
                MOVING[2] = -1
            if event.key == K_d: #Right
                MOVING[0] = 1
            if event.key == K_a: #Left
                MOVING[0] = -1
                
        if event.type == KEYUP:
            
            #Stop rotation
            if event.key == K_j:
                ROTATING[1] = 0
            if event.key == K_i:
                ROTATING[0] = 0
            if event.key == K_l:
                ROTATING[1] = 0
            if event.key == K_k:
                ROTATING[0] = 0
            if event.key == K_o:
                ROTATING[2] = 0
            if event.key == K_p:
                ROTATING[2] = 0
                
            #Stop Moving.
            if event.key == K_w:
                MOVING[2] = 0
            if event.key == K_s:
                MOVING[2] = 0
            if event.key == K_d:
                MOVING[0] = 0
            if event.key == K_a:
                MOVING[0] = 0
                
    #Rotate the camera.
    if ROTATING[0] == 1:
        Camera.angle[0] += 1
    elif ROTATING[0] == -1:
        Camera.angle[0] -= 1
    if ROTATING[1] == 1:
        Camera.angle[1] += 1
    elif ROTATING[1] == -1:
        Camera.angle[1] -= 1
    if ROTATING[2] == 1:
        Camera.angle[2] += 1
    elif ROTATING[2] == -1:
        Camera.angle[2] -= 1

    #Translate the camera.
    if MOVING[0] == 1:
        CAMERA_VELOCITY = (1,0,0)
        Camera.move(CAMERA_VELOCITY)
    elif MOVING[0] == -1:
        CAMERA_VELOCITY = (-1,0,0)
        Camera.move(CAMERA_VELOCITY)
    if MOVING[2] == 1:
        CAMERA_VELOCITY = (0,0,1)
        Camera.move(CAMERA_VELOCITY)
    elif MOVING[2] == -1:
        CAMERA_VELOCITY = (0,0,-1)
        Camera.move(CAMERA_VELOCITY)

    return "nope"
