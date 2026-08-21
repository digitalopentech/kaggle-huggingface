"""Diagnóstico do ambiente: versões instaladas e status de autenticação nas APIs.

Uso: python doctor.py
"""

import importlib.metadata as md
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv(Path(__file__).parent / ".env")
console = Console()


def check_versions() -> None:
    table = Table(title="Pacotes principais")
    table.add_column("Pacote")
    table.add_column("Versão", style="green")
    for pkg in [
        "torch", "transformers", "datasets", "huggingface_hub",
        "sentence-transformers", "accelerate", "kaggle", "kagglehub",
        "scikit-learn", "pandas", "polars", "jupyterlab", "gradio", "twilio",
    ]:
        try:
            table.add_row(pkg, md.version(pkg))
        except md.PackageNotFoundError:
            table.add_row(pkg, "[red]não instalado[/red]")
    console.print(table)

    import torch
    console.print(f"Python: {sys.version.split()[0]}")
    console.print(f"PyTorch MPS (GPU Apple Silicon): {torch.backends.mps.is_available()}")


def check_huggingface() -> None:
    console.rule("Hugging Face")
    from huggingface_hub import HfApi

    token = os.getenv("HF_TOKEN") or None
    try:
        user = HfApi(token=token).whoami()
        console.print(f"✅ Autenticado como [bold]{user['name']}[/bold]")
    except Exception:
        console.print("❌ Sem autenticação. Defina HF_TOKEN no .env ou rode: hf auth login")
        console.print("   (downloads públicos funcionam mesmo sem token)")


def check_kaggle() -> None:
    console.rule("Kaggle")
    has_token = os.getenv("KAGGLE_API_TOKEN")
    has_env = os.getenv("KAGGLE_USERNAME") and os.getenv("KAGGLE_KEY")
    has_file = (Path.home() / ".kaggle" / "kaggle.json").exists()
    if not (has_token or has_env or has_file):
        console.print("❌ Sem credenciais. Preencha KAGGLE_API_TOKEN no .env (token KGAT_...)")
        console.print("   ou salve o kaggle.json em ~/.kaggle/ (baixe em kaggle.com/settings)")
        return
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi

        api = KaggleApi()
        api.authenticate()
        datasets = api.dataset_list(search="titanic")
        console.print(f"✅ API autenticada (teste de busca ok: {datasets[0].ref})")
    except Exception as exc:
        console.print(f"❌ Credenciais presentes mas a API falhou: {exc}")


def check_twilio() -> None:
    console.rule("Twilio (SMS)")
    sid, token = os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN")
    if not (sid and token):
        console.print("❌ Sem credenciais. Preencha TWILIO_ACCOUNT_SID/TWILIO_AUTH_TOKEN no .env")
        console.print("   (opcional — só necessário para enviar SMS)")
        return
    try:
        from twilio.rest import Client

        conta = Client(sid, token).api.accounts(sid).fetch()
        console.print(f"✅ Conta [bold]{conta.friendly_name}[/bold] ({conta.type}, {conta.status})")
        if not os.getenv("TWILIO_FROM_NUMBER"):
            console.print("   [yellow]⚠️  defina TWILIO_FROM_NUMBER para conseguir enviar[/yellow]")
    except Exception as exc:
        console.print(f"❌ Credenciais presentes mas a API falhou: {str(exc)[:120]}")


if __name__ == "__main__":
    check_versions()
    check_huggingface()
    check_kaggle()
    check_twilio()
