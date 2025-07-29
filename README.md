# 💣 Ivan — Token Vulnerability Scanner & Exploiter

> Nomeado em homenagem à **Tsar Bomba**, o projeto **Ivan** é uma estrutura modular para **detecção e exploração automatizada de vulnerabilidades críticas em tokens ERC20/Proxy via DeFi**, com foco em **Token Migration Hijack** e execução potencial via **flash loans e automação DeFi**.

---

## ⚠️ Aviso Legal

Este projeto tem **fins exclusivamente educacionais e de pesquisa de segurança**.  
**Nunca utilize em contratos reais sem autorização.**  
Abusos podem configurar crime. Responsabilize-se eticamente.

---

## 🧠 Visão Geral

**Ivan** é dividido em 3 componentes:

1. **Scanner de tokens (`token_scanner.py`)**  
   🔎 Explora diversas DEXs e fábricas de contratos para identificar tokens que utilizam padrões proxies (ERC1967, UUPS, etc.).

2. **Validador de vulnerabilidades (`token_checker_migration.py`)**  
   🛠️ Verifica se os contratos encontrados têm funções críticas acessíveis (`upgradeTo`, `migrate`, etc.) controladas diretamente por um owner externo.

3. **Executor DeFi (em desenvolvimento)**  
   ⚙️ Monta um ataque via **DSProxy** (DeFi Saver), simulando execução automatizada através de **flash loans** e bundles DeFi.

---

## 🧬 Vulnerabilidade: Token Migration Hijack

Tokens construídos sobre **proxy patterns** (como `TransparentUpgradeableProxy` ou `ERC1967`) podem ser vulneráveis se:

- O owner do contrato não estiver renunciado.
- As funções `upgradeTo`, `migrate`, `upgrade`, etc., estiverem **publicamente expostas**.
- A nova implementação puder ser maliciosa (reentrância, rug pull, dreno de fundos).

---

## 🛠️ Estrutura do Projeto

```bash
├── token_scanner.py             # Busca tokens em DEXs/fábricas (UniswapV2, PancakeSwap, etc.)
├── token_checker_migration.py   # Valida se os tokens são vulneráveis a hijack
├── tokens_found.json            # Tokens encontrados no scanner
├── tokens_vulnerables.json      # Tokens confirmadamente vulneráveis
├── executor/                    # Scripts para execução DeFi (em desenvolvimento)
│   └── dsproxy_attack.py        # Exemplo de ataque via DSProxy (DeFi Saver)
├── contracts/
│   └── MaliciousImplementation.sol  # Contrato para hijack (substitui implementação legítima)
├── .env                         # Contém sua chave privada e provider URL


🚀 Como Usar
1. Configure o ambiente

git clone https://github.com/seuusuario/ivan.git
cd ivan
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Crie um arquivo .env com:

PRIVATE_KEY=0x...
RPC_URL=https://...

2. Execute o Scanner

python token_scanner.py
Resultado: tokens_found.json

3. Verifique vulnerabilidades

python token_checker_migration.py
Resultado: tokens_vulnerables.json

4. (Opcional) Ataque simulado
Em desenvolvimento

python executor/dsproxy_attack.py

🧪 Teste e Simulação
Você pode simular o ataque com tokens na Goerli ou Sepolia Testnet, modificando os contratos para representar proxies vulneráveis.

📌 Requisitos Técnicos

Python 3.10+

Web3.py

dotenv

Acesso a um nó RPC confiável (Alchemy, Infura, etc.)

Chave privada para simulações

Conhecimento básico de contratos inteligentes

👨‍💻 Contribuindo

Pull requests são bem-vindos!
Ideias para novos scanners (reentrância, fee drain, honeypots) também.

🧠 Inspirado por:

Furucombo

DeFi Saver

OpenZeppelin Proxy Patterns

Real-world DeFi exploits

🧨 Nome: Ivan
O projeto recebe seu nome em referência à Tsar Bomba, a maior bomba nuclear já detonada, codinome "Ivan", refletindo o potencial devastador de falhas de segurança ignoradas em contratos DeFi.

