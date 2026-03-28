import requests

def explicar(contexto, tendencia=None, volatilidade=None, alerta=None):
    try:
        prompt = f"""
        Analise os dados:

        {contexto}

        Tendência: {tendencia}
        Volatilidade: {volatilidade}
        Alerta: {alerta}

        Gere uma interpretação epidemiológica.
        """

        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",  # use leve
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 200,
                    "temperature": 0.3
                }
            },
            timeout=120
        )

        data = r.json()

        # 🔥 LOG PARA DEBUG
        print("DEBUG OLLAMA:", data)

        # ✅ CASOS POSSÍVEIS
        if "response" in data:
            return data["response"]

        if "message" in data and "content" in data["message"]:
            return data["message"]["content"]

        if "error" in data:
            return f"Erro do modelo: {data['error']}"

        return f"Resposta inesperada: {data}"

    except Exception as e:
        return f"Erro no LLM: {e}"
