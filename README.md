# ESPNet tts demo in Ubuntu

Work in progress.

## Japanese TTS

### Setup

Assume (mini)conda is installed.
Create conda env for ESPnet.

```
$ conda create -n espnet-tts python=3.7
$ conda activate espnet-tts
```

### Install python modules

```
$ pip install numpy cython
```

### Build dependencies

```
$ ./build-jp-deps.sh
```

