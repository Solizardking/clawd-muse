# Verification — 2026-10-03

## Verified software

- `npm run check`: 10 API/provider tests, 7 Python companion tests, firmware
  confirmation state checks and Muse request-format C checks pass. C checks use
  warnings-as-errors and AddressSanitizer/UndefinedBehaviorSanitizer.
- `npm run build`: Vite production dashboard builds successfully.
- Prepared Muse Linux SDK: 137 upstream tests pass with the command extension.
- Alchemy live RPC: getBalance and getTokenAccountsByOwner for both SPL Token
  and Token-2022 pass. RPC credentials stay server-side.
- DFlow live order: 0.01 SOL → USDC returns a synchronous v0 unsigned
  transaction, integer output and minimum receive, and block-height expiry.
- Jupiter V2: live endpoint accepts the key and returns insufficient-funds
  rejection for an ephemeral unfunded taker. A funded executable order has not
  been tested.
- Browser: Wallet Standard test wallet connection, genuine Ed25519 challenge
  signing, live Alchemy balance loading, DFlow exact-terms review, unsigned
  intent preparation and cancellation pass. No signing/submission of a swap.
- Mobile viewport: 390×844, no horizontal overflow.
- Production dashboard at localhost:8790: zero browser console errors/warnings.
- `node --env-file=.env.local scripts/check-secrets.mjs`: no configured provider
  secrets found in the built dashboard.

The browser test wallet was generated solely for testing, was unfunded, and
was registered through Wallet Standard. This is not real MWA/Seed Vault proof.
Generated chart JPEG/RGB565 formats were checked with fixture candles; live
Birdeye charts are not yet proven.

## Outstanding

- `BIRDEYE_API_KEY` and `GADGET_API_KEY` are missing from `.env.local`.
- No ESP-IDF v6.0.1 installation was available; no full 1.28-inch board port,
  firmware link/build, flash, boot log or physical touch/audio check.
- No real Muse BLE/Noise pairing, Pi service registration, Android Chrome/MWA,
  Seeker Connect relay or Seed Vault wallet test.
- No funded swap or on-chain receipt. Submission validation is tested against
  fixtures, while quotes and balances use live read-only providers.
- No deployed public dashboard or Musebook Worker route installation.
- No device audio capture, Opus/WAV server STT or TTS playback.
- Local dependency audit: 17 upstream findings (13 high, 4 moderate), mostly
  inherited Solana/Mobile SDK toolchain dependencies. Sharp was upgraded to
  0.35.5. A release requires dependency review and real-device validation.

The checked-in firmware pin map corrects the initial PSRAM and audio wiring
assumptions. The portable review core does not prove the handheld is functional.
