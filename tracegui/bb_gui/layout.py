layout_abs = {'mot': {'CTX': (2, 2), 'STR': (2, 3), 'GPi': (2, 4), 'THL': (2, 5), 'STN': (1, 4)},
              'cog': {'CTX': (4, 2), 'STR': (4, 3), 'GPi': (4, 4), 'THL': (4, 5), 'STN': (5, 4)},
              'ass': {'CTX': (3, 2), 'STR': (3, 3)}}

layout_links = {(('CTX', 'mot'), ('STN', 'mot')): (( -30, 0), (   0, -100)),
                (('CTX', 'mot'), ('THL', 'mot')): ((-200, 0), (-250,    0))}


layout_posx = {1: 200, 2: 300, 3: 400, 4: 500, 5:600}
layout_posy = {1: 200, 2: 300, 3: 400, 4: 500, 5:600}

def generate_pos(x_offset, y_offset):
    global layout_posx, layout_posy

    layout_posx = {i+1: this.width//2  + (i-2)*x_offset for i in range(5)}
    layout_posy = {i+1: this.height//2 + (i-2)*y_offset for i in range(5)}
