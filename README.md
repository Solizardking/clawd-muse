# Pocket Wallet — with Muse and Clawd inside 🦞

**Pocket Wallet** is a pocket trading gadget for Musebook — with Muse and
Clawd inside — built on Meta's open-source [muse-gadget-sdk](https://github.com/facebookincubator/muse-gadget-sdk)
(Apache 2.0). Get an SDK token and see the supported boards at
[gadgets.muse.ai](https://gadgets.muse.ai/).

A handheld ESP32 device with a color AMOLED touchscreen, microphone, and
speaker. It pairs with the Muse app, connects to Musebook, shows live charts,
takes **voice trading commands** ("buy 10 $CLAWD"), and lets you **confirm
trades with a physical press** instead of squinting at a phone.

```
┌─────────────────────────────────────────────────────────┐
│                      Pocket Wallet                      │
│  ┌──────────┐   ┌──────────────┐   ┌──────────────────┐  │
│  │ ESP32-S3 │   │ Raspberry Pi │   │ Musebook backend │  │
│  │ AMOLED   │◄─►│ companion    │◄─►│  (musebook.trade)│  │
│  │ mic+spk  │   │ (linux SDK)  │   │  /api/gadget/*   │  │
│  └──────────┘   └──────────────┘   └──────────────────┘  │
│       │                 │                     │          │
│       └──── BLE ──► Muse app ◄── sign-in ─────┘          │
│              (spins up your Muse at launch)              │
└─────────────────────────────────────────────────────────┘
```

## Three layers

| Layer | What it is | Code |
|---|---|---|
| **Device** | ESP32-S3 firmware: trading UI, charts, voice loop, physical trade confirm | `firmware/` |
| **Companion** | Raspberry Pi service (linux device SDK): voice trading brain, chart rendering, trade orchestration | `linux/` |
| **Backend** | Musebook worker endpoints the gadget talks to: auth, portfolio, quotes, chart PNGs, trade intents | `api/` |

## Two modes

- **Sign-in mode** (default, safest): the gadget holds a scoped Musebook API key
  (`mbk_live_*`). It builds trade intents and shows exact terms on its screen;
  you sign in your phone's browser like always. The gadget never touches a key.
- **Wallet mode** (opt-in): the gadget holds a scoped local Solana keypair with
  hard caps (per-trade + per-day), created with your explicit approval. A trade
  only executes when you physically press confirm on the device.

See [docs/SECURITY.md](docs/SECURITY.md) for the full threat model.

## Quickstart

1. Buy the parts — [BOM.md](BOM.md).
2. Flash the firmware — [firmware/README.md](firmware/README.md).
3. Set up the Pi companion — [linux/README.md](linux/README.md).
4. Pair with the Muse app (Settings > Devices, Developer mode on) using your
   [SDK token](https://gadgets.muse.ai/settings/sdk-tokens).
5. Sign in to Musebook on the gadget, or enable wallet mode.

## Docs

- [ARCHITECTURE.md](ARCHITECTURE.md) — how the pieces fit
- [BOM.md](BOM.md) — parts list with links (reference board + alternatives)
- [docs/PAIRING.md](docs/PAIRING.md) — pairing + first boot
- [docs/SECURITY.md](docs/SECURITY.md) — auth modes, key handling, caps
- [docs/VOICE.md](docs/VOICE.md) — voice trading flow
- [api/OPENAPI.md](api/OPENAPI.md) — backend endpoint contract

## Upstream SDK

Pocket Wallet builds on Meta's official SDKs, not a fork:

- **ESP32 Device SDK** — `facebookincubator/muse-gadget-sdk`, `esp32/` directory.
  Firmware builds with ESP-IDF; per-board settings live in
  `esp32/devices/sdkconfig.*`. Pairing needs a personal SDK token from
  [gadgets.muse.ai](https://gadgets.muse.ai/settings/sdk-tokens) (review the
  Gadget SDK Terms when you create one).
- **Linux Device SDK** — same repo, `linux/` directory. Custom Muse commands
  via its executor; the Pi companion registers `clawd.*` commands there.

The reference board (Waveshare ESP32-S3-Touch-AMOLED-1.75C) is one of Meta's
featured example devices on gadgets.muse.ai and ships a first-class SDK
overlay (`devices/sdkconfig.muse-waveshare-s3-175c`), so the stock firmware
builds for it with no porting work.

## License

Apache-2.0, matching the upstream gadget SDK. See [LICENSE](LICENSE).
