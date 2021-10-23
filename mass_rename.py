from common import TMC_FOLDER
import pyperclip
import subprocess

lines = pyperclip.paste().splitlines()

renames = []
for line in lines:
    arr = line.split(',')
    if len(arr) == 2:
        print(f'Renaming {arr[0]} to {arr[1]}')
        renames.append((arr[0], arr[1]))

print('Really rename? y/n')
answer = input()
if answer.strip() == 'y':
    with open('/tmp/replacements.sed', 'w') as file:
        for arr in renames:
            file.write(f's/{arr[0]}/{arr[1]}/g\n')

    print('Renaming...')
    subprocess.check_call(f'find {TMC_FOLDER} \( -type d -name .git -o -name build -o -name tools -o -name translations \) -prune -o -type f \( -iname \*.s -o -iname \*.c -o -iname \*.yaml -o -iname \*.ld \) -print0| xargs -0 sed -i -f /tmp/replacements.sed', shell=True)
    print('Done')
else:
    print('Did not rename anything')