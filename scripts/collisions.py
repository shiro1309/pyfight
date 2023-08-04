import pygame as pg

def slow_collision(rect, rect2):
    collide_list = []
    if rect.colliderect(rect2):
        collide_list.append(rect2)
    return collide_list

def move(rect, movment, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    #rect.x += movment[0]
    
    
    hit_list = slow_collision(rect, tiles)
    for tile in hit_list:
        if movment[0] < 0:
            rect.right = tile.left
            collision_types['right'] = True
        if movment[0] > 0:
            rect.left = tile.right
            collision_types['left'] = True
            
    rect.y += movment[1]
    hit_list = slow_collision(rect, tiles)
    for tile in hit_list:
        if movment[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        if movment[1] < 0: 
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types