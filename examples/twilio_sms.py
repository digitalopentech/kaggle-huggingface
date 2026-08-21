"""Envio de SMS com a API do Twilio.

Uso:
    python examples/twilio_sms.py --to +5521999999999 --texto "Pipeline concluído"
    python examples/twilio_sms.py --status            # lista mensagens recentes e saldo

Requer TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN e TWILIO_FROM_NUMBER no .env.
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv(Path(__file__).parent.parent / ".env")
console = Console()


def cliente():
    """Cria o client autenticado, com mensagem clara se faltar credencial."""
    from twilio.rest import Client

    sid = os.getenv("TWILIO_ACCOUNT_SID")
    token = os.getenv("TWILIO_AUTH_TOKEN")
    if not (sid and token):
        console.print("[red]❌ Faltam credenciais.[/red] Preencha no .env:")
        console.print("   TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN e TWILIO_FROM_NUMBER")
        console.print("   (pegue em https://console.twilio.com)")
        sys.exit(1)
    return Client(sid, token)


def enviar(destino: str, texto: str) -> None:
    """Envia um SMS. O número deve estar em formato E.164 (+55DDDNNNNNNNNN)."""
    remetente = os.getenv("TWILIO_FROM_NUMBER")
    if not remetente:
        console.print("[red]❌ Defina TWILIO_FROM_NUMBER no .env[/red] (seu número Twilio)")
        sys.exit(1)

    from twilio.base.exceptions import TwilioRestException

    try:
        msg = cliente().messages.create(body=texto, from_=remetente, to=destino)
    except TwilioRestException as exc:
        console.print(f"[red]❌ Twilio recusou o envio (HTTP {exc.status}, código {exc.code})[/red]")
        console.print(f"   {exc.msg}")
        DICAS = {
            21408: "Habilite a região do destino em Console → Messaging → Settings → Geo Permissions.",
            21608: "Conta trial: o número de destino precisa ser verificado no console.",
            21606: "O número remetente não é seu ou não envia SMS. Confira TWILIO_FROM_NUMBER.",
            21211: "Número inválido — use o formato E.164, ex.: +5521999999999.",
        }
        if exc.code in DICAS:
            console.print(f"   [yellow]→ {DICAS[exc.code]}[/yellow]")
        sys.exit(1)

    console.print(f"✅ Enviado para [bold]{destino}[/bold]")
    console.print(f"   SID: {msg.sid} | status: {msg.status}")
    if msg.error_message:
        console.print(f"   [yellow]aviso: {msg.error_message}[/yellow]")


def status(limite: int = 10) -> None:
    """Mostra saldo da conta e as últimas mensagens enviadas."""
    api = cliente()
    conta = api.api.accounts(os.environ["TWILIO_ACCOUNT_SID"]).fetch()
    console.print(f"Conta: [bold]{conta.friendly_name}[/bold] | tipo: {conta.type} | status: {conta.status}")
    try:
        saldo = api.balance.fetch()
        console.print(f"Saldo: {saldo.balance} {saldo.currency}")
    except Exception:
        pass

    tabela = Table(title=f"Últimas {limite} mensagens")
    for col in ("Data", "Para", "Status", "Texto"):
        tabela.add_column(col)
    for m in api.messages.list(limit=limite):
        tabela.add_row(
            str(m.date_sent)[:16] if m.date_sent else "-",
            m.to or "-",
            m.status,
            (m.body or "")[:40],
        )
    console.print(tabela)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Envio de SMS via Twilio")
    p.add_argument("--to", help="destino em E.164, ex: +5521999999999")
    p.add_argument("--texto", default="Mensagem de teste do hf-kaggle-lab")
    p.add_argument("--status", action="store_true", help="mostra saldo e histórico")
    args = p.parse_args()

    if args.status:
        status()
    elif args.to:
        enviar(args.to, args.texto)
    else:
        p.print_help()
