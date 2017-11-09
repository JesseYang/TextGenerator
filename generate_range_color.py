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
raw_data_dir = '2000_txt'
dictionary = [" ", "\"", "$", "%", "&", "'", "(", ")", "*",
            "-", ".", "/", "0", "1", "2", "3", "4", "5",
            "6", "7", "8", "9", ":", "<", ">", "?", "[",
            "]", "a", "b", "c", "d", "e", "f", "g", "h",
            "i", "j", "k", "l", "m", "n", "o", "p", "q",
            "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "{", "}", 'A', 'B', 'C', 'D', 'E', 'F', 'G',
            'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
            'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
            'Z', ';', ',', '!', '=', '|', '_', '#', '~', '+']
article_path_collections = [os.path.join(dirpath,filename) for dirpath, dirnames, filenames in os.walk(raw_data_dir) for filename in filenames if filename.endswith('txt')]
font_path_collections = [os.path.join(dirpath,filename) for dirpath, dirnames, filenames in os.walk('more_fonts') for filename in filenames if filename.endswith('ttf') or filename.endswith('TTF')]
# font_path_collections = ['more_fonts/Adobe Garamond/Adobe Garamond Bold Expert.ttf']
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
                    filtered_text = ''.join(i for i in text if i in dictionary)
                    if filtered_text != '':
                        # randomly pick a font and height
                        ttf = random.choice(font_path_collections)
                        fg, bg = random.sample(background_path_collections, 2)
                        h = random.randint(10,30)
                        ttfont = ImageFont.truetype(ttf, h)
                        line_w, line_h = ttfont.getsize(filtered_text)
                        
                        # random x,y of text_area
                        x = random.randint(0,3)
                        y = random.randint(0,3)
                        # random pad
                        h_pad = random.randint(0,3)
                        w_pad = random.randint(0,3)

                        fg = misc.imread(fg, mode = 'L')
                        fg = fg // 5
                        bg = misc.imread(bg, mode = 'L')
                        bg_h, bg_w = bg.shape
                        canvas_h, canvas_w = line_h+y+h_pad, line_w+x+w_pad
                        if canvas_w <= 0 or canvas_h <= 0:
                            continue
                        if bg_h > canvas_h and bg_w > canvas_w:
                            r_x, r_y = random.randint(0,bg_w - canvas_w - 1), random.randint(0,bg_h - canvas_h - 1)
                            canvas = bg[r_y:r_y+canvas_h, r_x:r_x+canvas_w]
                        else:
                            canvas = cv2.resize(bg, (canvas_w, canvas_h))
                        fg = cv2.resize(fg, (canvas_w, canvas_h))
                        blank = Image.fromarray(np.zeros((canvas_h, canvas_w)) + 255)
                        d = ImageDraw.Draw(blank)
                        d.text((x, y), filtered_text, fill = 0, font = ttfont)
                        boolean_mask = np.array(blank) == 0
                        canvas[boolean_mask] = fg[boolean_mask]
                        with open('output/{}.txt'.format(cnt), 'w') as f:
                            f.write(filtered_text)
                            img = np.asarray(canvas)
                            misc.imsave('output/{}.png'.format(cnt), img)
                        cnt += 1
                        if cnt > 799999:
                            quit()
                        print(cnt)
