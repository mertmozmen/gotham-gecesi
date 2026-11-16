# Gotham sahnesini üretir → hooks/scene.ts   (python3 tools/build-scene.py)
import random, json, os
random.seed(7)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'hooks', 'scene.ts')

def bat_half():
    # Özgün yarasa silüeti, sağ yarı: kulak, parmak kemikli kanat, dalgalı alt kenar.
    return ('M-1,-12 L0,-12 L5,-26 L9,-11 L20,-13 Q48,-40 78,-34 Q92,-34 104,-22 '
            'Q90,-14 86,2 Q74,-8 62,4 Q52,-4 42,14 Q32,6 22,20 L10,18 L4,30 L0,26 L-1,26 Z')

def bat(attrs=''):
    h = bat_half()
    return f'<g {attrs}><path d="{h}"/><path transform="scale(-1,1)" d="{h}"/></g>'


SC = 'transform="scale(%s)"'
EMB = bat('class="emb" transform="translate(1180,82) scale(1.35,1.2)" fill="#050607" filter="url(#sb)"')

# Şehir
bld=[];x=-90
while x<1700:
    w=random.randint(40,110);h=random.randint(120,420)
    bld.append(f'<rect x="{x}" y="{900-h}" width="{w}" height="{h+80}"/>')
    if random.random()<.25: bld.append(f'<rect x="{x+w//2-3}" y="{900-h-40}" width="6" height="40"/>')
    x+=w+random.randint(-6,4)
far=[];x=-120
while x<1740:
    w=random.randint(50,130);h=random.randint(200,560)
    far.append(f'<rect x="{x}" y="{900-h}" width="{w}" height="{h+80}"/>');x+=w-8
win=[]
for i in range(160):
    wx=random.randint(0,1580);wy=random.randint(560,880)
    win.append(f'<rect class="w w{i%8}" x="{wx}" y="{wy}" width="4" height="6"/>')
rain=''.join(f'<line x1="{(rx:=random.randint(-100,1700))}" y1="{(ry:=random.randint(-900,0))}" x2="{rx-12}" y2="{ry+38}"/>' for _ in range(140))

# Otomatik kamera kayması: her katman kendi genliğinde yavaşça salınır (derinlik hissi).
LAYERS={'p-sky':10,'p-cl':22,'p-far':34,'p-near':60,'p-fly':80}
rules=''.join(
    f'.{L}{{animation:{L} 38s ease-in-out infinite}}'
    f'@keyframes {L}{{0%,100%{{transform:translate({k}px,{k*.3:.0f}px)}}'
    f'25%{{transform:translate(0px,{-k*.3:.0f}px)}}50%{{transform:translate({-k}px,0px)}}'
    f'75%{{transform:translate(0px,{k*.3:.0f}px)}}}}'
    for L,k in LAYERS.items())
zones=[]

# Ara sıra sağdan sola uçan yarasalar (style özniteliği ve CSS değişkeni yok)
flock=[];flyrules=[]
groups=[([(0,0,.75),(120,-50,.55),(230,35,.65)], 22, 1, 150),
        ([(0,0,.5),(90,40,.42)], 29, 11, 240),
        ([(0,0,1.0)], 37, 19, 190)]
for gi,(bats,dur,delay,y) in enumerate(groups):
    inner=''.join(
        f'<g transform="translate({dx},{dy})"><g class="flap f{(gi+j)%3}">{bat(SC % s_)}</g></g>'
        for j,(dx,dy,s_) in enumerate(bats))
    flock.append(f'<g class="fl g{gi}">{inner}</g>')
    flyrules.append(
        f'.g{gi}{{transform:translate(1900px,{y}px);animation:fly{gi} {dur}s linear {delay}s infinite}}'
        f'@keyframes fly{gi}{{0%{{transform:translate(1900px,{y}px)}}10%{{transform:translate(1300px,{y-50}px)}}'
        f'20%{{transform:translate(700px,{y+15}px)}}30%{{transform:translate(100px,{y-55}px)}}'
        f'38%,100%{{transform:translate(-500px,{y-20}px)}}}}')
flock=''.join(flock);flyrules=''.join(flyrules)

svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice">
<style>
{rules}
.w{{fill:#e6b422;animation-name:wf;animation-iteration-count:infinite;animation-timing-function:steps(1)}}{''.join(f'.w{i}{{{{animation-duration:{3+i*.9:.1f}s;animation-delay:-{i*.7:.1f}s}}}}' for i in range(8))}
@keyframes wf{{0%{{opacity:.75}}40%{{opacity:.15}}70%{{opacity:.6}}}}
.beam{{transform-origin:1180px 900px;animation:sw 22s ease-in-out infinite alternate}}
@keyframes sw{{from{{transform:rotate(-14deg)}}to{{transform:rotate(10deg)}}}}
.cl{{animation:dr 90s linear infinite}}
@keyframes dr{{from{{transform:translateX(0)}}to{{transform:translateX(-800px)}}}}
.rn{{animation:rf .9s linear infinite}}
@keyframes rf{{from{{transform:translate(0,0)}}to{{transform:translate(-30px,900px)}}}}
.lt{{animation:lg 17s infinite}}
@keyframes lg{{0%,93%,100%{{opacity:0}}94%{{opacity:.35}}95%{{opacity:0}}96%{{opacity:.2}}}}
.emb{{animation:pu 6s ease-in-out infinite}}
@keyframes pu{{0%,100%{{opacity:.85}}50%{{opacity:.65}}}}
.fl{{fill:#000;stroke:#f2c84b;stroke-opacity:.7;stroke-width:3;paint-order:stroke}}
{flyrules}
.flap{{transform-box:fill-box;transform-origin:center;animation:fp .28s ease-in-out infinite alternate}}.f1{{animation-duration:.24s}}.f2{{animation-duration:.33s}}
@keyframes fp{{from{{transform:scaleY(1)}}to{{transform:scaleY(-.45)}}}}
@media (max-aspect-ratio:1/1){{.bw{{transform:translateX(-300px)}}}}
</style>
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05070a"/><stop offset=".7" stop-color="#11151b"/><stop offset="1" stop-color="#1a1d22"/></linearGradient>
<linearGradient id="bm" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#f2c84b" stop-opacity=".35"/><stop offset="1" stop-color="#f2c84b" stop-opacity="0"/></linearGradient>
<radialGradient id="spot"><stop offset="0" stop-color="#f7d97a" stop-opacity=".7"/><stop offset=".55" stop-color="#e6b422" stop-opacity=".35"/><stop offset="1" stop-color="#e6b422" stop-opacity="0"/></radialGradient>
<filter id="bl"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="sb"><feGaussianBlur stdDeviation="1.6"/></filter>
</defs>
<rect width="1600" height="900" fill="url(#sky)"/>
<rect class="lt" width="1600" height="900" fill="#9fb3c8"/>
{''.join(zones)}
<g class="p-sky"><g class="bw"><g class="beam"><polygon points="1170,900 1190,900 1300,30 1060,30" fill="url(#bm)" filter="url(#bl)"/>
<ellipse cx="1180" cy="82" rx="200" ry="110" fill="url(#spot)"/>
{EMB}</g></g></g>
<g class="p-cl"><g class="cl" fill="#1c2128" opacity=".7" filter="url(#bl)">
<ellipse cx="200" cy="120" rx="260" ry="50"/><ellipse cx="700" cy="80" rx="320" ry="60"/><ellipse cx="1300" cy="140" rx="280" ry="45"/>
<ellipse cx="1000" cy="120" rx="260" ry="50"/><ellipse cx="1500" cy="80" rx="320" ry="60"/><ellipse cx="2100" cy="140" rx="280" ry="45"/></g></g>
<g class="p-fly">{flock}</g>
<g class="p-far" fill="#0d1014">{''.join(far)}</g>
<g class="p-near"><g fill="#07090b">{''.join(bld)}</g><g>{''.join(win)}</g></g>
<g stroke="#8a97a6" stroke-opacity=".22" stroke-width="1.2"><g class="rn">{rain}</g><g class="rn" transform="translate(0,900)">{rain}</g></g>
</svg>'''
assert len(svg) < 131072, len(svg)
open(OUT,'w').write('export const SCENE = '+json.dumps(svg)+'\n')
open(os.path.join(HERE,'preview.svg'),'w').write(svg)
print('ok', len(svg))
