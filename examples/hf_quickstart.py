"""Exemplos rápidos com a API do Hugging Face.

Uso: python examples/hf_quickstart.py
Funciona sem token (modelos/datasets públicos).
"""

from dotenv import load_dotenv

load_dotenv()


def buscar_modelos() -> None:
    """Busca modelos no Hub via API."""
    from huggingface_hub import list_models

    print("── Top 5 modelos de sentiment-analysis ──")
    for model in list_models(pipeline_tag="text-classification", sort="downloads", limit=5):
        print(f"  {model.id}  ({model.downloads:,} downloads)")


def baixar_dataset() -> None:
    """Carrega um dataset direto do Hub."""
    from datasets import load_dataset

    ds = load_dataset("imdb", split="train[:100]")
    print(f"\n── Dataset IMDB (amostra) ── {ds}")
    print("Exemplo:", ds[0]["text"][:120], "...")


def rodar_pipeline() -> None:
    """Roda inferência local com um modelo pequeno."""
    from transformers import pipeline

    clf = pipeline(
        "sentiment-analysis",
        model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
    )
    frases = ["I love this course!", "This homework is terrible."]
    print("\n── Inferência local ──")
    for frase, resultado in zip(frases, clf(frases)):
        print(f"  {frase!r} -> {resultado['label']} ({resultado['score']:.3f})")


def embeddings() -> None:
    """Gera embeddings de sentenças (útil para RAG / similaridade)."""
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("all-MiniLM-L6-v2")
    vecs = model.encode(["machine learning", "aprendizado de máquina", "banana"])
    sim = model.similarity(vecs, vecs)
    print("\n── Similaridade de embeddings ──")
    print(f"  'machine learning' vs 'aprendizado de máquina': {sim[0][1]:.3f}")
    print(f"  'machine learning' vs 'banana':                 {sim[0][2]:.3f}")


if __name__ == "__main__":
    buscar_modelos()
    baixar_dataset()
    rodar_pipeline()
    embeddings()
