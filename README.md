## Como Executar

Primeiro, crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv

source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### Interface textual

```bash
python main.py
```

### Interface web (Streamlit)

```bash
streamlit run streamlit_app.py
```

> Você precisa estar com o ambiente virtual ativado para executar o Streamlit, a as dependencias precisam estar instaladas.