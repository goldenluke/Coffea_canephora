import os

EXTENSOES = {
    '.py', '.html', '.js', '.jsx', '.ts', '.tsx',
    '.css', '.astro', '.sh', '.md',
    '.yml', '.yaml'
}

PASTAS_IGNORADAS = {
    'venv', '.venv', 'env', '__pycache__', '.git',
    'node_modules', '.mypy_cache', '.pytest_cache',
    'dist', 'build', '.next', '.nuxt', '.output', 'metaenv'
}

ARQUIVOS_IGNORADOS = (
    '.lock', '.log', '.min.js', '.map',
    '.geojson', '.topojson'
)

CAMINHOS_IGNORADOS = (
    'frontend/public/geojson_uf/',
    'frontend/metaenv/'
)


def juntar_arquivos(
    pasta='.',
    saida='codigo_completo.txt',
    tamanho_max_mb=2
):
    tamanho_max = tamanho_max_mb * 1024 * 1024
    caminho_saida = os.path.abspath(saida)
    caminho_script = os.path.abspath(__file__) if '__file__' in globals() else None

    total = 0

    with open(saida, 'w', encoding='utf-8') as out:
        for raiz, dirs, files in os.walk(pasta):
            # filtra pastas
            dirs[:] = [d for d in dirs if d not in PASTAS_IGNORADAS and not d.startswith('.')]

            for nome in files:
                if not nome.endswith(tuple(EXTENSOES)):
                    continue

                if nome.endswith(ARQUIVOS_IGNORADOS):
                    continue

                caminho = os.path.join(raiz, nome)
                caminho_abs = os.path.abspath(caminho)
                caminho_rel = os.path.relpath(caminho)

                if caminho_abs in (caminho_saida, caminho_script):
                    continue

                if any(p in caminho_rel for p in CAMINHOS_IGNORADOS):
                    continue

                try:
                    if os.path.getsize(caminho) > tamanho_max:
                        continue

                    with open(caminho, encoding='utf-8', errors='ignore') as f:
                        conteudo = f.read()

                except Exception:
                    continue

                out.write(f"\n\n{'='*80}\nARQUIVO: {caminho_rel}\n{'='*80}\n\n")
                out.write(conteudo)

                total += 1

    print(f"✔ {total} arquivos agregados em {saida}")


if __name__ == "__main__":
    juntar_arquivos()
