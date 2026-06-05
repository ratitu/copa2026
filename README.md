# 🏆 Copa do Mundo FIFA 2026 — Simulador

App interativo em **Streamlit** que exibe a tabela da Copa do Mundo 2026 (Canadá, México e EUA) e permite simular os resultados da fase de grupos e mata-mata.

## Funcionalidades

- **12 grupos** (A–L) com as 48 seleções
- **72 jogos** da fase de grupos com datas oficiais
- **Tabelas dinâmicas** — classificação (P, J, V, E, D, GP, GC, SG) é recalculada a cada alteração de placar
- **Inserção manual** de resultados jogo a jogo
- **Simulação automática** com distribuição realista de gols
- **Classificação geral** com ranking de todos os times e os 8 melhores terceiros colocados
- **Fase eliminatória** — 32 avos (oitavas) com simulação
- **Tema escuro** com código de cores (verde = classificado, vermelho = eliminado)

## Como usar

```bash
pip install -r requirements.txt
streamlit run app.py
```

O app abre em `http://localhost:8501`.

## Dados

Grupos e times baseados no sorteio oficial da FIFA para a Copa do Mundo de 2026.
