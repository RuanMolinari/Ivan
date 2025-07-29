🧨 Projeto Ivan (RDS-220)
Scanner de Tokens + Scanner de Vulnerabilidades (Token Migration Hijack)

"Inspirado na bomba mais poderosa já criada, Ivan é um projeto que detecta alvos com precisão e revela falhas críticas no ecossistema DeFi."

🔍 Visão Geral
O Projeto Ivan é uma ferramenta dupla composta por:

Token Hunter: Scanner que varre DEXs em busca de tokens recentes e potencialmente vulneráveis com base em liquidez baixa.

Token Checker: Validador que analisa tokens identificados e detecta se são vulneráveis ao ataque de Token Migration Hijack, uma falha crítica em contratos proxy upgradeáveis.

🛠️ Funcionalidades
🔹 Scanner de Tokens
Consulta diversas DEXs (Uniswap, PancakeSwap, etc.).

Detecta tokens novos com base em pools pequenos (potencial alvo de exploits).

Armazena os tokens encontrados em tokens_found.json.

🔹 Scanner de Vulnerabilidades
Lê os tokens detectados pelo Token Hunter.

Verifica presença de funções sensíveis: upgradeTo, upgrade, migrate.

Detecta contratos com owner ainda ativo e permissões de atualização.

Gera tokens_vulnerables.json.

💥 Estratégia de Ataque (Estudo Experimental)
Embora este projeto seja apenas educacional, ele explora o vetor Token Migration Hijack, que pode permitir controle total do contrato caso certas funções não estejam protegidas.


📁 Estrutura do Projeto

ivan-rds220/

├── token_hunter.py            # Scanner de tokens

├── token_checker_migration.py # Scanner de vulnerabilidades

├── tokens_found.json          # Tokens detectados (gerado pelo token_hunter.py)

├── tokens_vulnerables.json    # Tokens vulneráveis identificados (gerado pelo token_checker_migration.py)

├── README.md

⚠️ Aviso Legal
Este projeto é para fins educacionais e de pesquisa de segurança. Não incentive nem apoie o uso para atividades maliciosas. O uso indevido pode ser crime.

🧠 Autor
Ruan Vinicius dos Anjos Molinari
💼 Pesquisador em segurança blockchain, MEV e arbitragem.
🚀 Em busca de vulnerabilidades esquecidas no espaço DeFi.

