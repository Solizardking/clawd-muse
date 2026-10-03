# Pocket Wallet — Muse + Clawd

A wallet companion for a small round-screen gadget, with a browser dashboard
for live balances, swap quotes and wallet-approved transactions. Built against
the Muse Gadget SDK reference in `/Users/8bit/Untitled`.

The browser and API run now. The Linux companion registers read-only Muse
commands in an isolated copy of the upstream SDK. The firmware confirmation
core is host-tested; the 1.28-inch hardware port, flashing and BLE pairing
still require device validation. See [verification](docs/VERIFICATION.md).

## Start on your computer

Requires Node 22.12+ and Python 3.11+ for the companion.

```sh
npm ci
cp .env.example .env.local  # skip this if .env.local already contains your credentials
chmod 600 .env.local
npm run api
```

In a second terminal:

```sh
npm run dev
```

Open **http://localhost:5173**. Connect an installed Solana wallet, then press
**Sign in to Pocket Wallet** to sign a short-lived challenge. Balances load
from your configured RPC. Choose SOL/USDC, enter an amount, get a quote,
review the minimum receive and fees, then approve in your wallet. Cancel or
let the review expire to discard it. Signing and submission spend real funds.

On Android Chrome, select **Use Installed Wallet**. Desktop Wallet Standard
extensions are also supported. For iOS, open the dashboard inside a compatible
wallet's browser. Android wallet/Seeker device tests are still outstanding.

## Server configuration

Put credentials in `.env.local`. Provider keys and the RPC URL never enter
the browser bundle. Restart `npm run api` after changing them.

| Variable | Purpose |
|---|---|
| `RPC_URL` | Standard Solana mainnet RPC, including Alchemy; takes precedence |
| `ALCHEMY_API_KEY` | Builds an Alchemy mainnet endpoint when `RPC_URL` is unset |
| `HELIUS_RPC_URL` / `HELIUS_API_KEY` | Alternative mainnet RPC |
| `BIRDEYE_API_KEY` | Live price candles and 240×240 JPEG/PNG/RGB565 charts |
| `JUPITER_API_KEY` | Jupiter Swap V2 order and user-signed execution |
| `DFLOW_API_KEY` | DFlow synchronous swap order and RPC submission |
| `OPENROUTER_API_KEY` | Text/voice-transcript interpretation; never executes |
| `META_API_KEY` | Meta Model API credential; separate from the Gadget SDK token |
| `GADGET_API_KEY` | Muse Gadget SDK token (`mgst_…`), configured in upstream pairing/build |
| `APP_ORIGIN` | Exact browser origin, default `http://localhost:5173` |
| `VITE_SEEKER_RELAY_DOMAIN` | Optional public Seeker Connect relay domain you are authorized to use |

The local API reports which credentials are configured without revealing their
values. Missing providers return an actionable error rather than sample data.

## Add the Linux companion

Follow [linux/README.md](linux/README.md). The browser's **Pair Linux companion**
button downloads a one-hour config with a device token. Device tokens can read
data and prepare quotes; they cannot submit transactions. Muse pairing uses
the upstream SDK's BLE/Noise implementation and SDK token.

## Handheld

See [BOM.md](BOM.md), [firmware/README.md](firmware/README.md) and the
[vendor pin map](firmware/devices/board-waveshare-s3-128.json).
The ESP32-S3-Touch-LCD-1.28 has **2 MB quad PSRAM**, GC9A01A LCD and CST816S
touch. Do not flash a 1.75-inch AMOLED profile to this board. The original
GPIO 4–7 audio suggestion conflicted with onboard peripherals; the corrected
proposal uses free expansion GPIOs and needs electrical verification.

## Checks and docs

```sh
npm run check
python3 scripts/prepare-linux-sdk.py --output build/muse-linux
uv run --project build/muse-linux --with pytest --with ./linux pytest build/muse-linux/tests -q
```

- [Architecture](ARCHITECTURE.md) · [API contract](api/OPENAPI.md)
- [Pairing](docs/PAIRING.md) · [Security](docs/SECURITY.md) · [Voice](docs/VOICE.md)
- [Mobile integration](docs/MOBILE.md) · [Verification](docs/VERIFICATION.md)
- [Reference manifest](docs/reference-manifest.json)

Apache-2.0. Upstream Muse code retains Meta's copyright and license notices.
No hardware purchase, deployment, wallet creation or funded trade has been performed.
