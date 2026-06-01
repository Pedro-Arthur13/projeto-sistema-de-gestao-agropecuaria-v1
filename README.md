# Sistema de Gestao Agropecuaria — Fazenda Sertao (Etapa 2)

Sistema procedural modular para gestao de fazenda, com persistencia SQLite, dashboards com seaborn, recibos PDF (fpdf2) e integracao ViaCEP + Open-Meteo.

## Estrutura

```
main.py                 # menu principal
config/settings.py      # constantes e permissoes
persistence/memoria.py  # listas de dicionarios em RAM (runtime)
persistence/database.py # sqlite3 (persistencia ao disco)
app/
  auth.py               # login, usuarios, SUPERUSUARIO
  fazenda.py            # rebanho, leite, produtos
  compras.py            # compras e agendamentos
  dashboard.py          # relatorios e exportacao
  api.py                # ViaCEP e Open-Meteo
  pdf.py                # recibos fpdf2
  utils.py              # validacoes centralizadas
```

## Dados em memoria (RT1)

Ao iniciar, o SQLite carrega tudo para listas de dicionarios em `persistence/memoria.py`:

- `USUARIOS`, `ANIMAIS`, `PRODUTOS`, `ESTOQUE_LEITE`, `COMPRAS`, `AGENDAMENTOS`, etc.
- Sets auxiliares: `EMAILS_USUARIOS`, `IDS_ANIMAIS`
- Toda operacao le/escreve primeiro na memoria; o banco e atualizado em seguida

## Instalacao

```bash
pip install -r requirements.txt
python main.py
```

## Acesso padrao SUPERUSUARIO

- E-mail: `super@fazendasertao.com.br`
- Senha: `super123`

## Pacotes externos

- **fpdf2** — recibos PDF de compra/retirada
- **seaborn** — graficos do dashboard (PNG)
- **requests** — APIs ViaCEP e Open-Meteo (sem chave)

## Validacoes

- Data de retirada: formato DD/MM/AAAA, nao anterior a 11/05/2026 e nao retroativa em relacao ao momento atual
- CEP: 8 digitos numericos, consulta ViaCEP quando disponivel

