import json
import os
from web3 import Web3
from web3.exceptions import ContractLogicError

# Configuração RPC (defina seu RPC ou use variável de ambiente)
RPC_URL = os.getenv("RPC_URL", "https://bsc-dataseed.binance.org/")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# ABI simplificada com funções proxy comuns e owner
UPGRADE_ABI = [
    {
        "inputs": [{"internalType": "address","name": "newImplementation","type": "address"}],
        "name": "upgradeTo",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address","name": "newImplementation","type": "address"}],
        "name": "upgrade",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address","name": "newImplementation","type": "address"}],
        "name": "migrate",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address","name": "","type": "address"}],
        "stateMutability": "view",
        "type": "function"
    }
]

def load_tokens(file_path="tokens_found.json"):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao ler {file_path}: {e}")
        return []

def get_proxy_implementation(address):
    # Slot padrão do EIP-1967 para implementação proxy
    # slot = bytes32(uint256(keccak256('eip1967.proxy.implementation')) - 1)
    slot_hash = Web3.keccak(text="eip1967.proxy.implementation")
    slot_int = int.from_bytes(slot_hash, byteorder='big') - 1
    slot_hex = hex(slot_int)

    try:
        raw = w3.eth.get_storage_at(address, slot_hex)
        # Últimos 20 bytes representam o endereço
        impl_address_bytes = raw[-20:]
        impl_address = Web3.to_checksum_address(impl_address_bytes.hex())
        if impl_address != "0x0000000000000000000000000000000000000000":
            return impl_address
    except Exception:
        pass
    return None

def check_token_migration(token_address):
    token_address = w3.to_checksum_address(token_address)
    contract = w3.eth.contract(address=token_address, abi=UPGRADE_ABI)
    vulnerability = {
        "upgradeTo": False,
        "upgrade": False,
        "migrate": False,
        "owner": None,
        "proxy_implementation": None
    }

    vulnerability["proxy_implementation"] = get_proxy_implementation(token_address)

    try:
        vulnerability["owner"] = contract.functions.owner().call()
    except (ContractLogicError, ValueError):
        vulnerability["owner"] = None
    except Exception:
        vulnerability["owner"] = None

    for func_name in ["upgradeTo", "upgrade", "migrate"]:
        try:
            func = getattr(contract.functions, func_name)
            vulnerability[func_name] = True
        except AttributeError:
            vulnerability[func_name] = False
        except Exception:
            vulnerability[func_name] = False

    return vulnerability

def main():
    tokens = load_tokens()
    results = []

    print(f"Tokens para analisar: {len(tokens)}")

    for entry in tokens:
        for token_key in ["token0", "token1"]:
            token_data = entry.get(token_key)
            if not token_data:
                continue
            symbol = token_data.get("symbol")
            address = token_data.get("address")

            if not address:
                continue

            print(f"Analisando {symbol} - {address}")
            mig = check_token_migration(address)
            owner = mig.get("owner")
            impl = mig.get("proxy_implementation")

            # FILTRO MAIS RIGOROSO
            if (mig["upgradeTo"] or mig["upgrade"] or mig["migrate"]) \
               and owner and owner.lower() != "0x0000000000000000000000000000000000000000" \
               and impl:
                print(f"⚠️ {symbol} potencialmente vulnerável a token migration hijack!")
                print(f"   Owner: {owner}")
                print(f"   Proxy Implementation: {impl}")
                results.append({
                    "token": symbol,
                    "address": address,
                    "owner": owner,
                    "proxy_implementation": impl,
                    "vulnerable_to_migration": True,
                    "details": mig
                })

    with open("tokens_vulnerable_migration.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Análise concluída. Tokens vulneráveis salvos em tokens_vulnerable_migration.json")

if __name__ == "__main__":
    main()
