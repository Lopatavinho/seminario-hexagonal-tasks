Para Testar o Sistema em Sua Máquina:

Pré-Requisitos: Python 3.8+ (Recomendado Python 3.10 ou superior) e Git (Para clonar o repositório)

1. Clone o Repositório.

2. Crie o Ambiente Virtual: python -m venv venv

3. Ative o Ambiente Virtual: venv\Scripts\activate (Windows) / source venv/bin/activate (macOS/Linux).

4. Instale as Dependências: pip install -r requirements.txt

5. Execute Servidor FastAPI: python -m uvicorn src.adapters.api.main:app --reload

6. Teste o Sistema: http://127.0.0.1:8000/docs
