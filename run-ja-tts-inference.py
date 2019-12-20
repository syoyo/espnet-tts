import sys

# Edit path if required.
sys.path.append("../espnet")

# define device
import torch

use_cuda = torch.cuda.is_available()
device = torch.device('cuda' if use_cuda else 'cpu')

# Transformer version
dict_path = "downloads/data/lang_1phn/train_no_dev_units.txt"
model_path = "downloads/exp/train_no_dev_pytorch_train_pytorch_transformer_phn/results/model.last1.avg.best"
vocoder_path = "downloads/jsut.parallel_wavegan.v1/checkpoint-400000steps.pkl"
vocoder_conf = "downloads/jsut.parallel_wavegan.v1/config.yml"

# define E2E-TTS model
from argparse import Namespace
from espnet.asr.asr_utils import get_model_conf
from espnet.asr.asr_utils import torch_load
from espnet.utils.dynamic_import import dynamic_import
idim, odim, train_args = get_model_conf(model_path)
model_class = dynamic_import(train_args.model_module)
model = model_class(idim, odim, train_args)
torch_load(model_path, model)
model = model.eval().to(device)
inference_args = Namespace(**{"threshold": 0.5, "minlenratio": 0.0, "maxlenratio": 10.0})

# define neural vocoder
import yaml
from parallel_wavegan.models import ParallelWaveGANGenerator
with open(vocoder_conf) as f:
    config = yaml.load(f, Loader=yaml.Loader)
vocoder = ParallelWaveGANGenerator(**config["generator_params"])
vocoder.load_state_dict(torch.load(vocoder_path, map_location="cpu")["model"]["generator"])
vocoder.remove_weight_norm()
vocoder = vocoder.eval().to(device)

# define text frontend
import pyopenjtalk
with open(dict_path) as f:
    lines = f.readlines()
lines = [line.replace("\n", "").split(" ") for line in lines]
char_to_id = {c: int(i) for c, i in lines}
def frontend(text):
    """Clean text and then convert to id sequence."""
    text = pyopenjtalk.g2p(text, kana=False)
    print(f"Cleaned text: {text}")
    charseq = text.split(" ")
    idseq = []
    for c in charseq:
        if c.isspace():
            idseq += [char_to_id["<space>"]]
        elif c not in char_to_id.keys():
            idseq += [char_to_id["<unk>"]]
        else:
            idseq += [char_to_id[c]]
    idseq += [idim - 1]  # <eos>
    return torch.LongTensor(idseq).view(-1).to(device)

frontend("初回の辞書のインストールが必要です")
print("Now ready to synthesize!")

# ----------------------------------

import time
input_text = "日本語で好きな文章を入力してください"

with torch.no_grad():
    start = time.time()
    x = frontend(input_text)
    c, _, _ = model.inference(x, inference_args)
    z = torch.randn(1, 1, c.size(0) * config["hop_size"]).to(device)
    c = torch.nn.ReplicationPad1d(config["generator_params"]["aux_context_window"])(c.unsqueeze(0).transpose(2, 1))
    y = vocoder(z, c).view(-1)
rtf = (time.time() - start) / (len(y) / config["sampling_rate"])
print(f"RTF = {rtf:5f}")

from scipy.io.wavfile import write
write("output.wav", config["sampling_rate"],  y.view(-1).cpu().numpy())
#from IPython.display import display, Audio
#display(Audio(y.view(-1).cpu().numpy(), rate=config["sampling_rate"]))

