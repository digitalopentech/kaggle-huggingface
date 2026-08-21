.PHONY: doctor lab hf-test kaggle-test freeze

# Diagnóstico completo do ambiente
doctor:
	.venv/bin/python doctor.py

# Abre o JupyterLab
lab:
	.venv/bin/jupyter lab

# Testa a API do Hugging Face
hf-test:
	.venv/bin/python examples/hf_quickstart.py

# Testa a API do Kaggle
kaggle-test:
	.venv/bin/python examples/kaggle_quickstart.py

# Status da conta Twilio (saldo + últimas mensagens)
sms-status:
	.venv/bin/python examples/twilio_sms.py --status

# Congela as versões instaladas
freeze:
	.venv/bin/python -m pip freeze > requirements.lock.txt
