from PIL import Image,ImageDraw,ImageFont
import numpy as np
from scipy import misc
import os
import cv2
import random

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

article_path_collections = [os.path.join(dirpath,filename) for dirpath, dirnames, filenames in os.walk('raw_data') for filename in filenames]
font_path_collections = [os.path.join(dirpath,filename) for dirpath, dirnames, filenames in os.walk('fonts') for filename in filenames if filename.endswith('ttf')]
background_path_collections = [os.path.join('background', filename) for filename in os.listdir('background')]

cnt = 0
for each_article_path in article_path_collections:
    with open(each_article_path, errors = 'ignore') as article:
        for each_line in article:
            res =  each_line.split()
            num_of_words = random.randint(1,10)
            sublines = chunks(res, num_of_words)
            for each_subline in sublines:
                text = ' '.join(each_subline)
                if text != '':
                    if len(text) > 100:
                        text = text[:100]
                    # randomly pick a font and height
                    ttf = random.choice(font_path_collections)
                    bg = random.choice(background_path_collections)
                    h = random.randint(10,30)
                    ttfont = ImageFont.truetype(ttf, h)
                    line_w, line_h = ttfont.getsize(text)
                    
                    # random x,y of text_area
                    x = random.randint(0,3)
                    y = random.randint(0,3)
                    # random pad
                    h_pad = random.randint(0,3)
                    w_pad = random.randint(0,3)
                    bg = misc.imread(bg, mode = 'L')
                    bg_h, bg_w = bg.shape
                    canvas_h, canvas_w = line_h+y+h_pad, line_w+x+w_pad
                    if bg_h > canvas_h and bg_w > canvas_w:
                        r_x, r_y = random.randint(0,bg_w - canvas_w - 1), random.randint(0,bg_h - canvas_h - 1)
                        canvas = bg[r_y:r_y+canvas_h, r_x:r_x+canvas_w]
                    else:
                        canvas = cv2.resize(bg, (canvas_w, canvas_h))
                    canvas = Image.fromarray(canvas)
                    d = ImageDraw.Draw(canvas)
                    d.text((x, y), text, fill = 0, font = ttfont)
                    with open('output_new/{}.txt'.format(cnt), 'w') as f:
                        f.write(text)
                        img = np.asarray(canvas)
                        misc.imsave('output_new/{}.png'.format(cnt), img)
                    cnt += 1
                    if cnt > 10000:
                        quit()
                    print(cnt)
