# Pressed

A coin-launch browser landing page with live market charts and a Phantom wallet connection. It is one static file, `public/index.html`: no server and no build step.

## What is in it

- **A working price-curve model** in the hero. Drag it, or use the slider, and the headline word "pressed" and the top bar squeeze with it. It uses example constant-product numbers (30 SOL virtual start, 1B supply, 793M for sale, before fees). It is an illustration, not a quote.
- **Markets.** Charts (24h, 7d, 30d, 90d) for the major coins and the high-cap memecoins, with price, market cap and 24h change. A search box finds any coin and saves it to a "Mine" list on the device. Prices and history come from CoinGecko's public API.
- **Phantom wallet.** Connect, see your shortened address and SOL balance, copy the address, disconnect. The page only reads your address and balance. It contains no code that signs messages or sends transactions.
- **Trade.** The trade button opens Jupiter in a new tab with the coin pre-filled, and you approve the swap in your own wallet there. The Solana address of each coin is looked up from the price data and shown so you can check it before you trade. Coins that are not Solana tokens (Bitcoin, Ethereum and so on) get a chart and an explanation instead of a swap button.
- A sign-up form, an X link in the header, a FAQ and a risk notice. Light on dependencies: no framework, no build.

## Configure

Near the top of the main script in `public/index.html`:

```
var CONFIG={signupUrl:''};
```

- `signupUrl`: where beta sign-ups are sent (a form service or your own endpoint, expecting `POST {email}`). Left empty, the form is switched off and says so.
- Optional `CONFIG.api` (price service address) and `CONFIG.rpc` (Solana RPC address). The defaults are the public CoinGecko API and the public Solana RPC, which are rate-limited. For real traffic use your own key, a small caching proxy and your own RPC provider.

## Hosting

Static hosting only. **Live prices and the wallet need the page to be on your own domain.** Sandboxed previews usually block requests to other sites and do not inject wallet extensions.

- **Vercel:** import the repo. `vercel.json` serves `public/`.
- **GitHub Pages:** Settings > Pages > Source: GitHub Actions. `.github/workflows/pages.yml` deploys `public/`.

## Tests

```
pip install -r tests/requirements-test.txt && playwright install chromium
python3 tests/test_page.py       # 21 checks: layout, the curve model, accessibility, sign-up form
python3 tests/test_markets.py    # 56 checks: lists, charts, search, trade links, wallet states, errors, phones
python3 tests/test_xlink.py      # 6 checks: the X link in the header
```

The tests run in Chromium with a stand-in for the price service and a stand-in Phantom wallet. They have not been run against the real services, real wallets, real phones, Safari or Firefox.

## Honest notes

- **Pressed is a placeholder name**; it has not been checked for availability or trademarks.
- The wording describes features like "we never hold your funds". Keep only what your product really does.
- Nothing here is financial advice. New coins are extremely volatile, and the page says so.
- Add a `LICENSE` file if you want others to reuse the code.
