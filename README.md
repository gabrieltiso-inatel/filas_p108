### Instruções

Crie um `virtualenv` para facilitar o processo de gerenciamento de dependências e o isolamento 
entre diferentes projetos:
```bash
python -m venv .venv # Criação
source .venv/bin/activate # Ativação
pip install -r requirements.txt # Instalação das dependências
```

#### Executar a aplicação

```bash
python main.py
```

#### Executar os testes

```bash
PYTHONPATH=. pytest
```