from datasketch import MinHash,MinHashLSH
lsh=MinHashLSH(threshold=0.6,num_perm=50)
minhashes={}
def minhash(tweet_text):
    p=tweet_text.split()
    m=MinHash(num_perm=50)
    trigram=[]
    for i in range(len(p)-2):
        trigram.append(p[i]+p[i+1]+p[i+2])
        i=i+2
    for d in trigram:
        m.update(d.encode('UTF-8'))
    minhashes.update({tweet_text:m})
    lsh.insert("%s"%tweet_text,m)
    return m

a=minhash("really?Germanwings Airbus A320 crashes in French Alps near Digne http:\/\/t.co\/yNlWbNJmYI")

b=minhash("\u201c@BBCBreaking: Germanwings Airbus A320 crashes in French Alps near Digne http://t.co/VyfwZhDhtc\u201d another plane crash.. Oh God.")

c=minhash("\u201c@BBCBreaking: Germanwings Airbus A320 crashes in French Alps near Digne http://t.co/0RVUOUMD4z\u201d")

print(minhashes)

print("really?Germanwings Airbus A320 crashes in French Alps near Digne http:\/\/t.co\/yNlWbNJmYI" in lsh)

print("\u201c@BBCBreaking: Germanwings Airbus A320 crashes in French Alps near Digne http://t.co/VyfwZhDhtc\u201d another plane crash.. Oh God." in lsh)

print("\u201c@BBCBreaking: Germanwings Airbus A320 crashes in French Alps near Digne http://t.co/0RVUOUMD4z\u201d" in lsh)


res=lsh.query(b)

print(res)


###########output#####################
"""{'really?Germanwings Airbus A320 crashes in French Alps near Digne http:\\/\\/t.co\\/yNlWbNJmYI': <datasketch.minhash.MinHash object at 0x048CE0A8>, '“@BBCBreaking: Germanwings Airbus A320 crashes in French Alps near Digne http://t.co/VyfwZhDhtc” another plane crash.. Oh God.': <datasketch.minhash.MinHash object at 0x048CE7B0>, '“@BBCBreaking: Germanwings Airbus A320 crashes in French Alps near Digne http://t.co/0RVUOUMD4z”': <datasketch.minhash.MinHash object at 0x048CE8A0>}
True
True
True
['“@BBCBreaking: Germanwings Airbus A320 crashes in French Alps near Digne http://t.co/VyfwZhDhtc” another plane crash.. Oh God.']
"""
