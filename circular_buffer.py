movement=[];

import functools as f

index = 0
cb_size=3

movement=[]

def add_new_movement(v):
    global movement, index
    movement.append(v)
    if len(movement) > cb_size:
        movement = movement[1:]

add_new_movement(True)
add_new_movement(True)
add_new_movement(True)
add_new_movement(False)
add_new_movement(False)
add_new_movement(False)
add_new_movement(False)

print(movement)
# movement=[True,True,True]



def any_movement():
    for m in movement:
        if m:
            return True
    return False 
print(any_movement())