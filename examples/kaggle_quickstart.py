"""Exemplos rápidos com a API do Kaggle.

Uso: python examples/kaggle_quickstart.py
Requer credenciais (KAGGLE_USERNAME/KAGGLE_KEY no .env ou ~/.kaggle/kaggle.json).
"""

from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path(__file__).parent.parent / "data"


def baixar_com_kagglehub() -> None:
    """kagglehub: jeito moderno — baixa e cacheia datasets com 1 linha."""
    import kagglehub

    path = kagglehub.dataset_download("heptapod/titanic")
    print(f"── Dataset baixado via kagglehub ──\n  {path}")
    for f in Path(path).iterdir():
        print(f"  - {f.name}")


def buscar_datasets() -> None:
    """API clássica: busca datasets por palavra-chave."""
    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    api.authenticate()
    print("\n── Busca: 'cybersecurity' ──")
    for ds in api.dataset_list(search="cybersecurity")[:5]:
        print(f"  {ds.ref}")


def listar_competicoes() -> None:
    """Lista competições ativas."""
    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    api.authenticate()
    print("\n── Competições recentes ──")
    resp = api.competitions_list(sort_by="latestDeadline")
    for comp in resp.competitions[:5]:
        print(f"  {comp.ref}  (deadline: {comp.deadline})")


def carregar_em_pandas() -> None:
    """Baixa um dataset e abre direto em pandas."""
    import kagglehub
    import pandas as pd

    path = kagglehub.dataset_download("heptapod/titanic")
    csv = next(Path(path).glob("*.csv"))
    df = pd.read_csv(csv)
    print(f"\n── {csv.name} em pandas ── shape={df.shape}")
    print(df.head(3))


if __name__ == "__main__":
    baixar_com_kagglehub()
    buscar_datasets()
    listar_competicoes()
    carregar_em_pandas()
