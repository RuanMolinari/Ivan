from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import json

API_KEY = "SUA_APY_KEY_THEGRAPH"

DEX_ENDPOINTS = {
    "UniswapV3": {
        "url": f"https://gateway.thegraph.com/api/{API_KEY}/subgraphs/id/HMuAwufqZ1YCRmzL2SfHTVkzZovC9VL2UAKhjvRqKiR1",
        "link_prefix": "https://app.uniswap.org/pools/"
    },
    "PancakeSwapV3": {
        "url": f"https://gateway.thegraph.com/api/{API_KEY}/subgraphs/id/A1fvJWQLBeUAggX2WQTMm3FKjXTekNXo77ZySun4YN2m",
        "link_prefix": "https://pancakeswap.finance/v3/pool/"
    }
}

QUERY_FACTORIES = gql("""
{
  factories(first: 1) {
    id
    poolCount
    txCount
    totalVolumeUSD
  }
}
""")

QUERY_POOLS = gql("""
{
  pools(first: 1000, orderBy: volumeUSD, orderDirection: desc) {
    id
    token0 {
      id
      symbol
      name
    }
    token1 {
      id
      symbol
      name
    }
    volumeUSD
    liquidity
    feeTier
  }
}
""")

def fetch_v3_data(dex_name, dex_info):
    print(f"\n🔎 Consultando {dex_name}")
    try:
        transport = RequestsHTTPTransport(url=dex_info["url"], verify=True, retries=3)
        client = Client(transport=transport, fetch_schema_from_transport=False)

        res_factory = client.execute(QUERY_FACTORIES)
        res_pools = client.execute(QUERY_POOLS)

        factory = res_factory.get("factories", [])[0]
        pools = res_pools.get("pools", [])

        print(f"📊 Factory {factory['id']}: {factory['poolCount']} pools, {factory['txCount']} txs, volume USD: ${float(factory['totalVolumeUSD']):,.2f}")

        # Inverter a ordem: começamos pelos menores volumes
        pools_sorted = sorted(pools, key=lambda p: float(p["volumeUSD"]))

        analyzed_pools = []

        for p in pools_sorted:
            s0 = p['token0']['symbol']
            s1 = p['token1']['symbol']
            vol = float(p['volumeUSD'])
            liq = float(p['liquidity'])
            fee = int(p['feeTier'])

            warnings = []
            if vol < 10_000:
                warnings.append("⚠️ volume baixo")
            if liq < 5_000:
                warnings.append("⚠️ liquidez baixa")
            if fee not in (500, 3000, 10000):
                warnings.append("⚠️ fee incomum")

            analyzed_pools.append({
                "pair": f"{s0}/{s1}",
                "token0": {
                    "address": p['token0']['id'],
                    "symbol": s0,
                    "name": p['token0']['name']
                },
                "token1": {
                    "address": p['token1']['id'],
                    "symbol": s1,
                    "name": p['token1']['name']
                },
                "volumeUSD": vol,
                "liquidity": liq,
                "feeTier": fee,
                "pool_id": p['id'],
                "link": dex_info["link_prefix"] + p['id'],
                "warnings": warnings
            })

        return {
            "dex_name": dex_name,
            "analyzed_pools": analyzed_pools
        }

    except Exception as e:
        print(f"❌ Erro ao consultar {dex_name}: {e}")
        return None

def print_report(results):
    for dex_data in results:
        print(f"\n📘 Resultados para {dex_data['dex_name']}")
        for pool in dex_data["analyzed_pools"]:
            if pool["warnings"]:
                print(f"🔍 {pool['pair']}: ${pool['volumeUSD']:,.2f} vol | {pool['liquidity']:,.2f} liq | fee {pool['feeTier']} -> {', '.join(pool['warnings'])}")
                print(f"   🔗 {pool['link']}")

def salvar_vulnerabilidades(resultados, caminho="tokens_found.json"):
    vulneraveis = []

    for dex_data in resultados:
        for pool in dex_data['analyzed_pools']:
            if pool["warnings"]:
                vulneraveis.append({
                    "dex": dex_data["dex_name"],
                    "pair": pool["pair"],
                    "volumeUSD": pool["volumeUSD"],
                    "liquidity": pool["liquidity"],
                    "feeTier": pool["feeTier"],
                    "token0": pool["token0"],
                    "token1": pool["token1"],
                    "pool_id": pool["pool_id"],
                    "link": pool["link"],
                    "warnings": pool["warnings"]
                })

    with open(caminho, "w") as f:
        json.dump(vulneraveis, f, indent=2)
    print(f"\n✅ Pools suspeitos salvos em: {caminho}")

if __name__ == "__main__":
    results = []
    for dex, info in DEX_ENDPOINTS.items():
        data = fetch_v3_data(dex, info)
        if data:
            results.append(data)

    print_report(results)
    salvar_vulnerabilidades(results)
