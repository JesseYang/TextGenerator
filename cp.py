import shutil
import os
filenames = os.listdir('output')
cnt = 0
for filename in filenames:
    if filename.endswith('txt'):
        input_path = os.path.join('output', filename)
        output_path = os.path.join('data', filename)
        shutil.copy(input_path, output_path)
        print(cnt)
        cnt += 1
