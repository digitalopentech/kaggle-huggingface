# 🧰 HF + Kaggle Lab

Ambiente Python especializado para trabalhar com as APIs do **Hugging Face** e do **Kaggle**.
Venv isolada (Python 3.12) com stack completo de ML/NLP e análise de sinais.

## 📓 Notebooks deste repositório

| Notebook | Tema | Onde |
|---|---|---|
| [`notebooks/eeg-analise-sinais.ipynb`](notebooks/eeg-analise-sinais.ipynb) | EEG e detecção de crises epilépticas (FFT, PSD de Welch, espectrograma, Random Forest — ROC-AUC 0.998) | local |
| [`kaggle-notebooks/neurociencia-tea/`](kaggle-notebooks/neurociencia-tea/) | Neurociência do TEA: triagem AQ-10 + conectividade cerebral DTI (ABIDE II) | [publicado no Kaggle](https://www.kaggle.com/code/leonardonunesrj/neuroci-ncia-do-tea-triagem-e-conectividade) |
| [`hf-spaces/hodgkin-huxley/`](hf-spaces/hodgkin-huxley/) | O potencial de ação: modelo de Hodgkin-Huxley do zero (spike, limiar, curva F-I, refratariedade, ciclo-limite) | [publicado no Hugging Face](https://huggingface.co/spaces/leonardovalle/hodgkin-huxley-potencial-de-acao) |
| [`hf-spaces/neurociencia-ecossistema/`](hf-spaces/neurociencia-ecossistema/) | Neurociência com o stack HF: CHB-MIT via Hub + MNE, embeddings do foundation model EEGPT, BERT biomédico e mapa semântico | [publicado no Hugging Face](https://huggingface.co/spaces/leonardovalle/neurociencia-ecossistema-huggingface) |

Complementa o material do curso aberto [Neuromatch Academy — Computational Neuroscience](https://compneuro.neuromatch.io)
(clone esparso local em `../neuromatch-compneuro`, não versionado aqui por ser conteúdo de terceiros).

## Setup em 3 passos

```bash
cd hf-kaggle-lab

# 1. Credenciais
cp .env.example .env        # preencha HF_TOKEN, KAGGLE_USERNAME, KAGGLE_KEY

# 2. Ativar (venv + credenciais de uma vez)
source activate.sh

# 3. Conferir que está tudo ok
make doctor
```

### Onde pegar as credenciais

| Serviço | Onde | O que fazer |
|---|---|---|
| Hugging Face | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) | Criar token "Read" e colar em `HF_TOKEN` |
| Kaggle | [kaggle.com/settings](https://www.kaggle.com/settings) → API → Create New Token | Colar o token `KGAT_...` em `KAGGLE_API_TOKEN` (formato antigo `username`/`key` também funciona) |

> Downloads públicos do HF funcionam **sem token**. O Kaggle exige credenciais para tudo.

## O que tem instalado

- **Hugging Face**: `transformers`, `datasets`, `huggingface_hub` (CLI `hf`), `tokenizers`, `accelerate`, `evaluate`, `sentence-transformers`, `safetensors`
- **Kaggle**: `kaggle` (CLI + API), `kagglehub` (download com 1 linha)
- **ML/Data**: `torch` + `torchvision` (com MPS/GPU do Apple Silicon), `scikit-learn`, `pandas`, `polars`, `numpy`, `scipy`, `pyarrow`
- **Viz**: `matplotlib`, `seaborn`, `plotly`
- **Notebooks**: JupyterLab + kernel registrado como **"HF-Kaggle Lab"**
- **Extras**: `gradio` (demos/Spaces), `rich`, `typer`, `httpx`, `python-dotenv`

## Comandos úteis

```bash
make doctor        # diagnóstico: versões + status de auth nas duas APIs
make lab           # abre o JupyterLab
make hf-test       # roda exemplos do Hugging Face (busca, dataset, pipeline, embeddings)
make kaggle-test   # roda exemplos do Kaggle (download, busca, competições, pandas)
make freeze        # congela versões em requirements.lock.txt
```

### CLIs direto no terminal (com a venv ativa)

```bash
# Hugging Face
hf auth login                          # login interativo
hf download meta-llama/Llama-3.2-1B    # baixar modelo
hf repo create meu-modelo              # criar repo no Hub

# Kaggle
kaggle datasets list -s titanic        # buscar datasets
kaggle datasets download -d heptapod/titanic -p data/
kaggle competitions list               # competições ativas
kaggle competitions download -c titanic -p data/
```

### Em Python

```python
# Hugging Face — carregar dataset e modelo
from datasets import load_dataset
from transformers import pipeline
ds = load_dataset("imdb", split="train[:100]")
clf = pipeline("sentiment-analysis")

# Kaggle — download com 1 linha (cacheado)
import kagglehub
path = kagglehub.dataset_download("heptapod/titanic")
```

## Estrutura

```
hf-kaggle-lab/
├── .venv/               # venv Python 3.12 (uv)
├── .env.example         # template de credenciais → copie para .env
├── activate.sh          # source activate.sh = venv + .env
├── doctor.py            # diagnóstico do ambiente
├── examples/
│   ├── hf_quickstart.py
│   └── kaggle_quickstart.py
├── data/                # downloads (git-ignored)
├── notebooks/           # seus notebooks
├── Makefile
└── requirements.txt
```
