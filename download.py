f = open('/Users/Lavector/dataset/classification/artwork.txt', 'r')
lines = f.readlines()
f.close()

f = open('/Users/Lavector/dataset/classification/artwork.sh', 'w')
prefix = 'artwork_'
for i, line in enumerate(lines):
    f.write('curl -o '+prefix+'%04d.jpg'%i+' --connect-timeout 20 -m 40 --insecure '+line.strip()+' --socks5-hostname 127.0.0.1:1080\n')
f.close()