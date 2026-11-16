# Gotham Gecesi 🦇

Claude Code masaüstü ve mobil uygulaması için karanlık, Gotham havasında sarı-lacivert bir tema.

- Gece laciverdi yüzeyler, sarı (`#ffd400`) vurgu
- Hareketli arka plan: yağmurlu şehir silueti, titreyen pencereler, uzak şimşekler
- Gökyüzünü tarayan projektör ve ışığın içinde yarasa silüeti
- Ara sıra sağdan sola uçan yarasa sürüleri
- Katmanların farklı hızda kaydığı yavaş kamera hareketi

Tema yalnızca masaüstü ve mobil uygulamada çizilir; terminal görünümü değişmez.

## Kurulum

Bir terminal oturumunun komut satırında:

```
/plugin install gotham-gecesi --marketplace mertmozmen/gotham-gecesi
```

`Add marketplace?` sorusuna `y`, ardından kapsamı Enter ile seç.

Kabuktan:

```bash
claude plugin install gotham-gecesi --marketplace mertmozmen/gotham-gecesi
```

Masaüstü uygulamasında (`/plugin` orada çalışmaz): komut kutusunun yanındaki **+** → **Plugins** → **Add marketplace** ile `mertmozmen/gotham-gecesi`, ardından **Add plugin**.

## Sahneyi düzenlemek

Sahne `tools/build-scene.py` ile üretilir:

```bash
python3 tools/build-scene.py
```

Bu komut `hooks/scene.ts` dosyasını yeniden yazar. Renkler `hooks/register.tsx` içinde.

Gökyüzüne kendi arma ya da logonu koymak için bir SVG ver:

```bash
python3 tools/build-scene.py --logo assets/logom.svg
```

Depoda logo yoktur; `assets/` klasörü git dışında tutulur. Kullandığın logonun haklarına dikkat et.

Yarasa çizimleri özgündür; herhangi bir markanın logosu değildir.
