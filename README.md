# ESPNet tts demo in Ubuntu

Work in progress.

## Setup

Assume `espnet` https://github.com/espnet/espnet is cloned into `../espnet`.

```
+-+- espnet
  +- espnet-tts
```

building kaldi in espnet is not required.

Assume (mini)conda is installed.
Create conda env for ESPNet.

```
$ conda create -n espnet-tts python=3.7
$ conda activate espnet-tts
```

## Japanese TTS

### Install python modules

```
$ pip install numpy cython
$ pip install editdistance
$ pip install parallel_wavegan PyYaml unidecode ConfigArgparse g2p_en nltk
$ pip install chainer
```

### Build dependencies

```
$ ./build-jp-deps.sh
```

### Download models

```
# download pretrained models(both for Tacotron2 and Transformer)
../espnet/utils/download_from_google_drive.sh \
    https://drive.google.com/open?id=1OwrUQzAmvjj1x9cDhnZPp6dqtsEqGEJM downloads tar.gz
../espnet/utils/download_from_google_drive.sh \
    https://drive.google.com/open?id=1kp5M4VvmagDmYckFJa78WGqh1drb_P9t downloads tar.gz
../espnet/utils/download_from_google_drive.sh \
    https://drive.google.com/open?id=1mEnZfBKqA4eT6Bn0eRZuP6lNzL-IL3VD downloads tar.gz
```

### Run inference

Set LD_LIBRARY_PATH to libopenjtalks(`dist/lib`), then run python code.

```
$ export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:./dist/lib
$ python run-ja-tts-inference.py
```
