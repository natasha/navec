
<img src="i/logo.svg" height="85">

[![Build Status](https://travis-ci.org/natasha/navec.svg?branch=master)](https://travis-ci.org/natasha/navec) [![Coverage Status](https://coveralls.io/repos/github/natasha/navec/badge.svg?branch=master)](https://coveralls.io/github/natasha/navec?branch=master)

`navec` is a library of pretrained word embeddings for russian language. It shows competitive or better results than <a href="http://rusvectores.org">RusVectores</a>, loads ~10 times faster (~1 sec), takes ~10 times less space (~50Mb).

> Navec = large russian text datasets + vanila GloVe + quantization

## Downloads

How to read model filename:
```
navec_hudlit_v1_12B_500K_300d_100q.tar
                 |    |    |    |
                 |    |    |     ---- 100 dimentions after quantization
                 |    |     --------- original vectors have 300 dimentions
                 |     -------------- vocab size is 500 000 words + 1 for <unk>
                  ------------------- dataset of 12 billion tokens was used
```

Currently two models are published:
<table>

<tr>
<th>Model</th>
<th>Size</th>
<th>Description</th>
<th>Sources</th>
</tr>

<tr>
<td>
  <a href="https://github.com/natasha/navec/releases/download/v0.0.0/navec_hudlit_v1_12B_500K_300d_100q.tar"><code>navec_hudlit_v1_12B_500K_300d_100q.tar</code></a>
</td>
<td>50Mb</td>
<td>
  Should be used by default. Shows best results on <a href="#evaluation">intrinsic evaluations</a>. Model was trained on large corpus of russian literature (~150Gb).
</td>
<td>
  <a href="https://github.com/natasha/corus#load_librusec"><code>librusec</code></a>
</td>
</tr>

<tr>
<td>
<a href="https://github.com/natasha/navec/releases/download/v0.0.0/navec_news_v1_1B_250K_300d_100q.tar"><code>navec_news_v1_1B_250K_300d_100q.tar</code></a>
</td>
<td>25Mb</td>
<td>
  Try to use this model to news texts. It is two times smaller than `hudlit` but covers same 98% of words in news articles.
</td>
<td>
  <a href="//github.com/natasha/corus#load_lenta"><code>lenta</code></a>
  <a href="//github.com/natasha/corus#load_ria"><code>ria</code></a>
  <a href="//github.com/natasha/corus#load_taiga_fontanka"><code>taiga_fontanka</code></a>
  <a href="//github.com/natasha/corus#load_buriy_news"><code>buriy_news</code></a>
  <a href="//github.com/natasha/corus#load_buriy_webhose"><code>buriy_webhose</code></a>
  <a href="//github.com/natasha/corus#load_ods_gazeta"><code>ods_gazeta</code></a>
  <a href="//github.com/natasha/corus#load_ods_interfax"><code>ods_interfax</code></a>
</td>
</tr>

</table>

## Install

`navec` supports Python 2.7+, 3.4+ и PyPy 3. PyPy 2 is excluded since it is hard to install `numpy` for PyPy 2.

```bash
$ pip install navec
```

## Usage

First download `hudlit` emdeddings (see the table above):
```bash
wget https://github.com/natasha/navec/releases/download/v0.0.0/navec_hudlit_v1_12B_500K_300d_100q.tar
```

Load tar-archive with `Navec.load`, it takes ~1s and ~100Mb of RAM:
```python
>>> from navec import Navec

>>> path = 'hudlit_12B_500K_300d_100q.tar'
>>> navec = Navec.load(path)
```

Then `navec` can be used as a dict object:
```python
>>> navec['навек']
array([ 0.3955571 ,  0.11600914,  0.24605067, -0.35206917, -0.08932345,
        0.3382279 , -0.5457616 ,  0.07472657, -0.4753835 , -0.3330848 ,
        ...

>>> 'нааавееек' in navec
False

>>> navec.get('нааавееек')
None
```

To get an index of word, use `navec.vocab`:
```python
>>> navec.vocab['навек']
225823

>>> navec.vocab.get('наааавеeeк', navec.vocab.unk_id)
500000   # == navec.vocab['<unk>']
```

## Evaluation

Let's compore Navec to top 5 RusVectores models (based on `simlex` and `hj` eval datasets). In each column top 3 results are highlighted.

* `init` — time it takes to load model file to RAM. `tayga_upos_skipgram_300_2_2019` word2vec binary file takes 14.5 seconds to load with `gensim.KeyedVectors.load_word2vec_format`. `tayga_none_fasttextcbow_300_10_2019` fastText large 910.6Mb file takes 3.4 seconds. Navec `hudlit` with vocab 2 times larger than previous two takes 1 second.
* `get` — time is takes to query embedding vector for a single word. Word2vec models win here, to fetch a vector they basically do `dict.get`. FastText and Navec for every query do extra computation. FastText extracts and sums word ngrams, Navec unpacks vector from quantization table. In practice query to embeddings table is small compared to all other computation in network.
* `disk` — model file size. It is convenient for deployment and distribution to have small models. Notice that `hudlit` model is 4-20 times smaller with vocab size 2 times bigger.
* `ram` — space model takes in RAM after loading. It is convenient to have small memory footprint to fit more computation on single server.
* `vocab` — number of words in vocab, number of embedding vectors. Since Navec vectors table takes less space we can have larger vocab. With 500K vocab `hudlit` model has ~2% OVV rate on average.

<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>type</th>
      <th>init, s</th>
      <th>get, µs</th>
      <th>disk, mb</th>
      <th>ram, mb</th>
      <th>vocab</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>ruscorpora_upos_cbow_300_20_2019</th>
      <td>w2v</td>
      <td>11.9</td>
      <td><b>5.1</b></td>
      <td><b>220.6</b></td>
      <td><b>236.1</b></td>
      <td>189K</td>
    </tr>
    <tr>
      <th>ruwikiruscorpora_upos_skipgram_300_2_2019</th>
      <td>w2v</td>
      <td>19.7</td>
      <td><b>5.0</b></td>
      <td>290.0</td>
      <td>309.4</td>
      <td>248K</td>
    </tr>
    <tr>
      <th>tayga_upos_skipgram_300_2_2019</th>
      <td>w2v</td>
      <td>20.5</td>
      <td><b>6.6</b></td>
      <td>290.7</td>
      <td>310.9</td>
      <td><b>249K</b></td>
    </tr>
    <tr>
      <th>tayga_none_fasttextcbow_300_10_2019</th>
      <td>fasttext</td>
      <td><b>3.7</b></td>
      <td>16.3</td>
      <td>910.6</td>
      <td>909.7</td>
      <td>192K</td>
    </tr>
    <tr>
      <th>araneum_none_fasttextcbow_300_5_2018</th>
      <td>fasttext</td>
      <td>5.9</td>
      <td>12.6</td>
      <td>945.3</td>
      <td>926.5</td>
      <td>195K</td>
    </tr>
    <tr>
      <th>hudlit_12B_500K_300d_100q</th>
      <td>navec</td>
      <td><b>1.5</b></td>
      <td>22.1</td>
      <td><b>50.6</b></td>
      <td><b>95.3</b></td>
      <td><b>500K</b></td>
    </tr>
    <tr>
      <th>news_1B_250K_300d_100q</th>
      <td>navec</td>
      <td><b>0.7</b></td>
      <td>18.5</td>
      <td><b>25.4</b></td>
      <td><b>47.7</b></td>
      <td><b>250K</b></td>
    </tr>
  </tbody>
</table>

Now let's look at intrinsic evaluation scores. Navec `hudlit` model does not show best results on all datasets but it is usually in top 3. We'll use 6 datasets, they are all available in <a href="data/eval">data/eval</a>:

* `simlex965`, `hj` — two small datasets (965 and 398 tests respectively) used by RusVectores, see the <a href="https://arxiv.org/abs/1801.06407">their paper</a> for more info. Metric is spearman correlation, other datasets use average precision.
* `rt`, `ae`, `ae2` — large datasets (114066, 22919, 86772 tests) from RUSSE workshop, see <a href="https://russe.nlpub.org/downloads/">the description</a> for more.
* `lrwc` — relatively new dataset by Yandex.Toloka, see <a href="https://research.yandex.com/datasets/toloka">their page</a>.

<table border="0" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>type</th>
      <th>simlex</th>
      <th>hj</th>
      <th>rt</th>
      <th>ae</th>
      <th>ae2</th>
      <th>lrwc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>ruscorpora_upos_cbow_300_20_2019</th>
      <td>w2v</td>
      <td><b>0.359</b></td>
      <td>0.685</td>
      <td><b>0.852</b></td>
      <td>0.758</td>
      <td><b>0.896</b></td>
      <td>0.602</td>
    </tr>
    <tr>
      <th>ruwikiruscorpora_upos_skipgram_300_2_2019</th>
      <td>w2v</td>
      <td>0.321</td>
      <td><b>0.723</b></td>
      <td>0.817</td>
      <td><b>0.801</b></td>
      <td>0.860</td>
      <td><b>0.629</b></td>
    </tr>
    <tr>
      <th>tayga_upos_skipgram_300_2_2019</th>
      <td>w2v</td>
      <td><b>0.429</b></td>
      <td><b>0.749</b></td>
      <td><b>0.871</b></td>
      <td>0.771</td>
      <td><b>0.899</b></td>
      <td><b>0.639</b></td>
    </tr>
    <tr>
      <th>tayga_none_fasttextcbow_300_10_2019</th>
      <td>fasttext</td>
      <td><b>0.370</b></td>
      <td>0.643</td>
      <td>0.792</td>
      <td>0.695</td>
      <td>0.809</td>
      <td>0.533</td>
    </tr>
    <tr>
      <th>araneum_none_fasttextcbow_300_5_2018</th>
      <td>fasttext</td>
      <td>0.349</td>
      <td>0.670</td>
      <td>0.804</td>
      <td>0.717</td>
      <td>0.796</td>
      <td>0.578</td>
    </tr>
    <tr>
      <th>hudlit_12B_500K_300d_100q</th>
      <td>navec</td>
      <td>0.310</td>
      <td><b>0.707</b></td>
      <td><b>0.842</b></td>
      <td><b>0.931</b></td>
      <td><b>0.923</b></td>
      <td><b>0.604</b></td>
    </tr>
    <tr>
      <th>news_1B_250K_300d_100q</th>
      <td>navec</td>
      <td>0.230</td>
      <td>0.590</td>
      <td>0.784</td>
      <td><b>0.866</b></td>
      <td>0.861</td>
      <td>0.589</td>
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

Notice! All commands belows use code from `navec/train`, it is not under CI, it works only with python3, it is expected user is familiar with source code. We use Yandex.Cloud EC2 and S3.

Create remote worker

To compute cooc (large HDD, 1Tb for librusec).
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

navec-train s3 download news_pq.bin pq.bin
navec-train s3 download news_vocab.txt vocab.txt

navec-train vocab pack < vocab.txt > vocab.bin

navec-train pack vocab.bin pq.bin hudlit_v1_12B_500K_300d_100q
navec-train s3 upload navec_hudlit_v1_12B_500K_300d_100q.tar packs/navec_hudlit_v1_12B_500K_300d_100q.tar

navec-train pack vocab.bin pq.bin news_v1_1B_250K_300d_100q
navec-train s3 upload navec_news_v1_1B_250K_300d_100q.tar packs/navec_news_v1_1B_250K_300d_100q.tar
```

Publish
```
navec-train s3 download packs/navec_hudlit_v1_12B_500K_300d_100q.tar
navec-train s3 download packs/navec_news_v1_1B_250K_300d_100q.tar
```
