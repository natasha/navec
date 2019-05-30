
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

To compute cooc (large HDD)
```bash
yc compute instance create \
    --name worker \
    --zone ru-central1-a \
    --network-interface subnet-name=default,nat-ip-version=ipv4 \
    --create-boot-disk image-folder-id=standard-images,image-family=ubuntu-1804,type=network-hdd,size=2000 \
    --memory 8 \
    --cores 1 \
    --core-fraction 100 \
    --ssh-key ~/.ssh/id_rsa.pub \
    --folder-name default
```

To fit embedings (multiple cores)
```bash
    --create-boot-disk image-folder-id=standard-images,image-family=ubuntu-1804,type=network-hdd,size=500 \
    --memory 10 \
    --cores 10 \
    --core-fraction 100
```

Setup machine
```bash
yc compute instance list --folder-name default
ssh yc-user@123.123.123.123

sudo apt-get update
sudo apt-get install -y language-pack-ru python3-pip screen unzip git pv cmake

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
sudo -H pip3 install -r navec/requirements-dev.txt 

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

Share text data
```bash
navec-train s3 upload ~/path/to/librusec_fb2.plain.gz librusec.gz
navec-train s3 download librusec.gz 
```

Text to tokens
```bash
navec-train corpus librusec librusec.gz | pv \
	| navec-train tokenize \
	> tokens.txt

pv tokens.txt | gzip > tokens.txt.gz
navec-train s3 upload tokens.txt.gz librusec_tokens.txt.gz
```

Tokens to vocab
```bash
pv tokens.txt \
	| navec-train vocab count \
	> full_vocab.txt

pv full_vocab.txt \
	| navec-train vocab quantile

cat full_vocab.txt \
	| head -500000 \
	| LC_ALL=C sort \
	> vocab.txt

navec-train s3 upload vocab.txt librusec_vocab.txt
```

Compute coocurence pairs
```bash
# Warning! Default limit on max number of open files is 1024, merge
# fails if number of chunks is large

ulimit -n  # 1024
sudo nano /etc/security/limits.conf

# * soft     nofile         65535
# * hard     nofile         65535

# relogin
ulimit -n  # 65535

pv tokens.txt \
	| navec-train cooc count vocab.txt --memory 7 --window 10 \
	> cooc.bin

# Monitor
tail -c 16 cooc.bin | navec-train cooc parse

navec-train s3 upload cooc.bin librusec_cooc.bin
```

Compute embedings
```bash
navec-train s3 download librusec_vocab.txt vocab.txt
navec-train s3 download librusec_cooc.bin cooc.bin

pv cooc.bin \
	| navec-train cooc shuffle --memory 9 \
	> shuf_cooc.bin

# Search dim with best score
for i in 100 200 300 400 500 600;
	do navec-train emb shuf_cooc.bin vocab.txt emb_${i}d.txt --dim $i --threads 10 --iterations 2;
done

# 300 has ok score. 400, 500 are a bit better, but too heavy
navec-train emb shuf_cooc.bin vocab.txt emb_300d.txt --dim 300 --threads 10 --iterations 10

navec-train s3 upload emb_300d.txt librusec_12B_500k_300d.txt
```

Quantize
```
# Search for best compression that has still ok score
for i in 300 150 100 75 60 50 30;
	do navec-train quantize emb_300d.txt quant_300d_${i}q.tar $i --sample 100000 --iterations 10;
done

# Select 100
navec-train quantize emb_300d.txt quant_300d_100q.tar 100 --sample 100000 --iterations 10

navec-train s3 upload quant_300d_100q.tar librusec_12B_500k_300d_100q.tar
```
