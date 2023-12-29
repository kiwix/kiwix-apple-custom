from glob import glob

for f in glob('./**/info.json', recursive=True):
    print(f)