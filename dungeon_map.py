from PIL import Image

def render_map():
    path = '/home/octorock/git/tmc/build/tmc/assets/assets/unknown_248.bin'

    data = None
    with open(path, 'rb') as f:
        data = f.read()

    colors = [
        (0,0,0,0xff),
        (255,0,0,0xff),
        (0,255,0,0xff),
        (0,0,255,0xff),
    ]

    chars = [' ', '#', '.', '-']

    print('Possible sizes:')
    sizes = []
    for width in range(1, len(data)//2):
        height = len(data)/width
        print(f'{width * 4 } x {int(height)}')
        sizes.append((width * 4, int(height)))

    def render_map(path, data, image_width, image_height):
        print('\n\n\n')
        bytes_per_row = (image_width+3)//4
        room_image = Image.new("RGBA", (image_width, image_height), (255, 255, 255, 0))
        pixels = room_image.load()
        for y in range(image_height):
            for x in range(0, image_width, 4):
                offset = y*bytes_per_row + x//4
                byte = data[offset]

                for i in range(4):
                    color_type = (byte >> (6 - i*2)) & 0x03
                    if color_type != 0:
                        pixels[x,y] = colors[color_type]
                        print(chars[color_type], end='')
                #   if color_type == 2:
                #     color_type = 3
                #   elif color_type == 3:
                #     color_type = 7

                #   if color_type != 0:
                #     color = palette[color_type]
                #     pixels[x,y] = color

                    x += 1
            print()
        room_image.save(path)

    for (w, h) in sizes:
        image_path = f'/tmp/map_{w}x{h}.png'
        render_map(image_path, data, w, h)

    print('done')

map_lines = '''DUNGEON MAP 0x84e7770 24x17
DUNGEON MAP 0x84e7404 20x15
DUNGEON MAP 0x84e3d0c 20x15
DUNGEON MAP 0x84e4024 28x15
DUNGEON MAP 0x84e4324 24x15
DUNGEON MAP 0x84e45cc 20x15
DUNGEON MAP 0x84e47e0 20x10
DUNGEON MAP 0x84e4b5c 20x25
DUNGEON MAP 0x84e5058 32x25
DUNGEON MAP 0x84e5424 20x25
DUNGEON MAP 0x84e5694 20x12
DUNGEON MAP 0x84e58d0 20x13
DUNGEON MAP 0x84e5bd0 24x17
DUNGEON MAP 0x84e5f60 24x17
DUNGEON MAP 0x84e627c 24x17
DUNGEON MAP 0x84e6588 28x15
DUNGEON MAP 0x84e6864 24x15
DUNGEON MAP 0x84e6eac 32x25
DUNGEON MAP 0x84e7174 20x18'''

def find_maps():
    for line in map_lines.split('\n'):
        print(line)

render_map()
#find_maps()