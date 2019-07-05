
# navec

`navec` is a library of pretrained word embeddings for russian language. It shows competitive or better results than RusVectores, loads ~10 times faster (~1 sec), takes ~10 times less space (~50Mb).

> navec = huge datasets + vanila GloVe + quantization

## Evaluation

<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>init, s</th>
      <th>get, µs</th>
      <th>disk, mb</th>
      <th>ram, mb</th>
      <th>simlex965, spearman | support</th>
      <th>hj, spearman</th>
      <th>rt, prec</th>
      <th>ae, prec</th>
      <th>ae2, prec</th>
      <th>lrwc, prec</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>ruscorpora_upos_cbow_300_20_2019</th>
      <td>12.6</td>
      <td>4.6</td>
      <td>220.6</td>
      <td>236.1</td>
      <td>0.359|961</td>
      <td>0.685|378</td>
      <td>0.852|61428</td>
      <td>0.758|16213</td>
      <td>0.896|49895</td>
      <td>0.602|6234</td>
    </tr>
    <tr>
      <th>ruwikiruscorpora_upos_skipgram_300_2_2019</th>
      <td>15.9</td>
      <td>4.5</td>
      <td>290.0</td>
      <td>309.4</td>
      <td>0.321|961</td>
      <td>0.723|376</td>
      <td>0.817|66197</td>
      <td>0.801|17067</td>
      <td>0.860|54479</td>
      <td>0.629|6173</td>
    </tr>
    <tr>
      <th>tayga_upos_skipgram_300_2_2019</th>
      <td>15.5</td>
      <td>4.4</td>
      <td>290.7</td>
      <td>310.9</td>
      <td>0.429|959</td>
      <td>0.749|382</td>
      <td>0.871|65091</td>
      <td>0.771|17372</td>
      <td>0.899|54082</td>
      <td>0.639|6297</td>
    </tr>
    <tr>
      <th>tayga_none_fasttextcbow_300_10_2019</th>
      <td>3.3</td>
      <td>14.3</td>
      <td>910.6</td>
      <td>909.7</td>
      <td>0.370|965</td>
      <td>0.643|398</td>
      <td>0.792|114066</td>
      <td>0.695|22907</td>
      <td>0.809|86772</td>
      <td>0.533|10596</td>
    </tr>
    <tr>
      <th>araneum_none_fasttextcbow_300_5_2018</th>
      <td>4.5</td>
      <td>11.1</td>
      <td>945.3</td>
      <td>926.5</td>
      <td>0.349|965</td>
      <td>0.670|398</td>
      <td>0.804|114066</td>
      <td>0.717|22910</td>
      <td>0.796|86771</td>
      <td>0.578|10596</td>
    </tr>
    <tr>
      <th>navec_librusec_12B_500k_300d_100q</th>
      <td>1.0</td>
      <td>64.7</td>
      <td>49.5</td>
      <td>95.3</td>
      <td>0.309|958</td>
      <td>0.704|390</td>
      <td>0.842|81408</td>
      <td>0.932|21698</td>
      <td>0.923|71667</td>
      <td>0.604|6733</td>
    </tr>
  </tbody>
</table>

## Development

Test
```bash
make test
```

Package:
```bash
make version
git push
git push --tags

make clean wheel upload
```

Create remote worker

To compute cooc (large HDD, 1Tb for librusec). We use instance from Yandex.Cloud
```bash
yc compute instance create \
    --name worker \
    --zone ru-central1-a \
    --network-interface subnet-name=default,nat-ip-version=ipv4 \
    --create-boot-disk image-folder-id=standard-images,image-family=ubuntu-1804,type=network-hdd,size=1000 \
    --memory 8 \
    --cores 1 \
    --core-fraction 100 \
    --ssh-key ~/.ssh/id_rsa.pub \
    --folder-name default \
    --preemptible  # in case computation takes <24h
```

To fit embedings (multiple cores). HDD should be > cooc.bin * 3 (for suffle + tmp)
```bash
yc compute instance create \
    --name worker \
    --zone ru-central1-a \
    --network-interface subnet-name=default,nat-ip-version=ipv4 \
    --create-boot-disk image-folder-id=standard-images,image-family=ubuntu-1804,type=network-hdd,size=700 \
    --memory 16 \
    --cores 16 \
    --core-fraction 100 \
    --ssh-key ~/.ssh/id_rsa.pub  \
    --folder-name default \
    --preemptible
```

Setup machine
```bash
yc compute instance list --folder-name default
ssh yc-user@123.123.123.123

sudo locale-gen en_US.UTF-8
sudo timedatectl set-timezone Europe/Moscow
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y language-pack-ru python3-pip screen unzip git pv cmake

wget https://nlp.stanford.edu/software/GloVe-1.2.zip
unzip GloVe-1.2.zip
rm GloVe-1.2.zip
mv GloVe-1.2 glove
cd glove
make
cd ..

export GLOVE_DIR=~/glove/build

git clone https://github.com/natasha/navec.git
sudo -H pip3 install -e navec
sudo -H pip3 install -r navec/requirements/train.txt

screen
ctrl a d
```

Remove instance
```bash
yc compute instance list --folder-name default
yc compute instance delete xxxxxxxxx
````

Env, used by `navec-train s3|vocab|cooc|emb`
```bash
export S3_KEY=_XxXXXxxx_XXXxxxxXxxx
export S3_SECRET=XXxxx_XXXXXXxxxxxxXXXXxxXXx-XxxXXxxxX
export S3_BUCKET=XXXXXXX
export GLOVE_DIR=~/path/to/glove/build
```

Notice! All commands belows use code from navec/train, it is not under CI, it works only with python3, it expects user is familiar with source code.

Share text data (see corus)
```bash
navec-train s3 upload librusec_fb2.plain.gz sources/librusec.gz
navec-train s3 upload taiga/proza_ru.zip sources/taiga_proza.zip

navec-train s3 upload ruwiki-latest-pages-articles.xml.bz2 sources/wiki.xml.bz2

navec-train s3 upload lenta-ru-news.csv.gz sources/lenta.csv.gz
navec-train s3 upload ria.json.gz sources/ria.json.gz
navec-train s3 upload taiga/Fontanka.tar.gz sources/taiga_fontanka.tar.gz
navec-train s3 upload buriy/news-articles-2014.tar.bz2 sources/buriy_news1.tar.bz2
navec-train s3 upload buriy/news-articles-2015-part1.tar.bz2 sources/buriy_news2.tar.bz2
navec-train s3 upload buriy/news-articles-2015-part2.tar.bz2 sources/buriy_news3.tar.bz2
navec-train s3 upload buriy/webhose-2016.tar.bz2 sources/buriy_webhose.tar.bz2
navec-train s3 upload ods/gazeta_v1.csv.zip sources/ods_gazeta.csv.zip
navec-train s3 upload ods/interfax_v1.csv.zip sources/ods_interfax.csv.zip

navec-train s3 download sources/librusec.gz
navec-train s3 download sources/taiga_proza.zip

navec-train s3 download sources/wiki.xml.bz2

navec-train s3 download sources/lenta.csv.gz
navec-train s3 download sources/ria.json.gz
navec-train s3 download sources/taiga_fontanka.tar.gz
navec-train s3 download sources/buriy_news1.tar.bz2
navec-train s3 download sources/buriy_news2.tar.bz2
navec-train s3 download sources/buriy_news3.tar.bz2
navec-train s3 download sources/buriy_webhose.tar.bz2
navec-train s3 download sources/ods_gazeta.csv.zip
navec-train s3 download sources/ods_interfax.csv.zip
```

Text to tokens
```bash
navec-train corpus librusec librusec.gz | pv | navec-train tokenize > tokens.txt  # ~12B words
navec-train corpus taiga_proza taiga_proza.zip | pv | navec-train tokenize > tokens.txt  # ~3B

navec-train corpus wiki wiki.xml.bz2 | pv | navec-train tokenize > tokens.txt  # ~0.5B

navec-train corpus lenta lenta.csv.gz | pv | navec-train tokenize >> tokens.txt
navec-train corpus ria ria.json.gz | pv | navec-train tokenize >> tokens.txt
navec-train corpus taiga_fontanka taiga_fontanka.tar.gz | pv | navec-train tokenize >> tokens.txt
navec-train corpus buriy_news buriy_news1.tar.bz2 | pv | navec-train tokenize >> tokens.txt
navec-train corpus buriy_news buriy_news2.tar.bz2 | pv | navec-train tokenize >> tokens.txt
navec-train corpus buriy_news buriy_news3.tar.bz2 | pv | navec-train tokenize >> tokens.txt
navec-train corpus buriy_webhose buriy_webhose.tar.bz2 | pv | navec-train tokenize >> tokens.txt
navec-train corpus ods_gazeta ods_gazeta.csv.zip | pv | navec-train tokenize >> tokens.txt
navec-train corpus ods_interfax ods_interfax.csv.zip | pv | navec-train tokenize >> tokens.txt  # ~1B

pv tokens.txt | gzip > tokens.txt.gz
navec-train s3 upload tokens.txt.gz librusec_tokens.txt.gz

navec-train s3 upload tokens.txt taiga_proza_tokens.txt
navec-train s3 upload tokens.txt news_tokens.txt
navec-train s3 upload tokens.txt wiki_tokens.txt
```

Tokens to vocab
```bash
pv tokens.txt \
	| navec-train vocab count \
	> full_vocab.txt

pv full_vocab.txt \
	| navec-train vocab quantile

# librusec
# ...
# 0.970      325 882
# 0.980      511 542
# 0.990    1 122 624
# 1.000   22 129 654

# taiga_proza
# ...
# 0.960      229 906
# 0.970      321 810
# 0.980      517 647
# 0.990    1 224 277
# 1.000   14 302 409

# wiki
# ...
# 0.950     380 134
# 0.960     519 817
# 0.970     757 561
# 0.980   1 223 201
# 0.990   2 422 265
# 1.000   6 664 630

# news
# ...
# 0.970    163 833
# 0.980    243 903
# 0.990    462 361
# 1.000  3 744 070

# threashold at ~0.98
# librusec 500000
# taiga_proza 500000
# wiki 750000
# news 250000

cat full_vocab.txt \
	| head -500000 \
	| LC_ALL=C sort \
	> vocab.txt

navec-train s3 upload full_vocab.txt librusec_full_vocab.txt
navec-train s3 upload vocab.txt librusec_vocab.txt

navec-train s3 upload full_vocab.txt taiga_proza_full_vocab.txt
navec-train s3 upload vocab.txt taiga_proza_vocab.txt

navec-train s3 upload full_vocab.txt wiki_full_vocab.txt
navec-train s3 upload vocab.txt wiki_vocab.txt

navec-train s3 upload full_vocab.txt news_full_vocab.txt
navec-train s3 upload vocab.txt news_vocab.txt
```

Compute coocurence pairs
```bash
# Default limit on max number of open files is 1024, merge fails if
# number of chunks is large

ulimit -n  # 1024
sudo nano /etc/security/limits.conf

* soft     nofile         65535
* hard     nofile         65535

# relogin
ulimit -n  # 65535

pv tokens.txt \
	| navec-train cooc count vocab.txt --memory 7 --window 10 \
	> cooc.bin

# Monitor
ls /tmp/cooc_*
tail -c 16 cooc.bin | navec-train cooc parse

navec-train s3 upload cooc.bin librusec_cooc.bin
navec-train s3 upload cooc.bin taiga_proza_cooc.bin
navec-train s3 upload cooc.bin wiki_cooc.bin
navec-train s3 upload cooc.bin news_cooc.bin
```

Merge (did not give much boost compared to plain librusec, so all_vocab.txt, all_cooc.bin not used below)
```bash
for i in librusec taiga_proza wiki news; do
	navec-train s3 download $i_vocab.txt;
	navec-train s3 download $i_cooc.bin;
done

navec-train merge vocabs \
	librusec_vocab.txt \
	taiga_proza_vocab.txt \
	wiki_vocab.txt \
	news_vocab.txt \
	| pv > vocab.txt

navec-train merge coocs vocab.txt \
	librusec_cooc.bin:librusec_vocab.txt \
	taiga_proza_cooc.bin:taiga_proza_vocab.txt \
	wiki_cooc.bin:wiki_vocab.txt \
	news_cooc.bin:news_vocab.txt \
	| pv > cooc.bin

navec-train s3 upload vocab.txt all_vocab.txt
navec-train s3 upload cooc.bin all_cooc.bin
```

Compute embedings
```bash
navec-train s3 download librusec_vocab.txt vocab.txt
navec-train s3 download librusec_cooc.bin cooc.bin

navec-train s3 download wiki_vocab.txt vocab.txt
navec-train s3 download wiki_cooc.bin cooc.bin

navec-train s3 download news_vocab.txt vocab.txt
navec-train s3 download news_cooc.bin cooc.bin

pv cooc.bin \
	| navec-train cooc shuffle --memory 15 \
	> shuf_cooc.bin

# Search dim with best score
for i in 100 200 300 400 500 600;
	do navec-train emb shuf_cooc.bin vocab.txt emb_${i}d.txt --dim $i --threads 10 --iterations 2;
done

# 300 has ok score. 400, 500 are a bit better, but too heavy
navec-train emb shuf_cooc.bin vocab.txt emb.txt --dim 300 --threads 16 --iterations 15

navec-train s3 upload emb.txt librusec_emb.txt
navec-train s3 upload emb.txt wiki_emb.txt
navec-train s3 upload emb.txt news_emb.txt
```

Quantize
```bash
navec-train s3 download librusec_emb.txt emb.txt
navec-train s3 download wiki_emb.txt emb.txt
navec-train s3 download news_emb.txt emb.txt

# Search for best compression that has still ok score
for i in 150 100 75 60 50;
	do pv emb.txt | navec-train pq $i --sample 100000 --iterations 15 > pq_${i}q.bin;
done

# 100 is <1% worse on eval but much lighter
pv emb.txt | navec-train pq 100 --sample 100000 --iterations 20 > pq.bin

navec-train s3 upload pq.bin librusec_pq.bin
navec-train s3 upload pq.bin wiki_pq.bin
navec-train s3 upload pq.bin news_pq.bin
```

Pack
```
navec-train s3 download librusec_pq.bin pq.bin
navec-train s3 download librusec_vocab.txt vocab.txt

navec-train s3 download wiki_pq.bin pq.bin
navec-train s3 download wiki_vocab.txt vocab.txt

navec-train s3 download news_pq.bin pq.bin
navec-train s3 download news_vocab.txt vocab.txt

navec-train vocab pack < vocab.txt > vocab.bin

navec-train pack vocab.bin pq.bin librusec_12B_500K_300d_100q
navec-train s3 upload librusec_12B_500K_300d_100q.tar packs/hudlit_12B_500K_300d_100q.tar

navec-train pack vocab.bin pq.bin wiki_500M_750K_300d_100q
navec-train s3 upload wiki_500M_750K_300d_100q.tar packs/wiki_500M_750K_300d_100q.tar

navec-train pack vocab.bin pq.bin news_1B_250K_300d_100q
navec-train s3 upload news_1B_250K_300d_100q.tar packs/news_1B_250K_300d_100q.tar
```

Publish
```
navec-train s3 download packs/hudlit_12B_500K_300d_100q.tar
navec-train s3 download packs/wiki_500M_750K_300d_100q.tar
navec-train s3 download packs/news_1B_250K_300d_100q.tar
```
