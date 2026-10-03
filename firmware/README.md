# Pocket Wallet — Firmware

Target: **Waveshare ESP32-S3-Touch-LCD-1.28** (1.28" round 240×240 capacitive
touch LCD), ESP-IDF v6.0.1.

> The muse-gadget-sdk does not ship a stock overlay for this board — the
> firmware needs a custom board overlay (GC9A01 round LCD + touch
> controller, ESP32-S3R8, 16MB flash / 8MB PSRAM). Start from the closest
> upstream overlay (`devices/sdkconfig.muse-waveshare-s3-175c`) and swap the
> display driver + touch config.

## Build the upstream firmware first

```sh
git clone https://github.com/Solizardking/muse-gadget-sdk /tmp/mgs
cd /tmp/mgs/esp32
# install ESP-IDF v6.0.1, then:
. ~/esp/esp-idf-v6/export.sh
# create your overlay from the 175c one, replacing the display/touch driver
# set your SDK token:
#   CONFIG_GADGET_SDK_TOKEN=<redacted>  (via idf.py menuconfig, never commit it)
idf.py build
idf.py -p /dev/ttyUSB0 flash monitor
```

Pair in the Muse app: Settings > Devices (Developer mode on), look for
`MuseGadget…`.

## Pocket Wallet customizations (`devices/`)

Planned overlays/screens on top of stock firmware — see
[`devices/OVERLAY.md`](devices/OVERLAY.md):

- `pocket_boot` — Pocket Wallet splash + Musebook session bring-up
- `pocket_home` — portfolio snapshot screen (round-layout)
- `pocket_chart` — full-screen chart PNG viewer (tap = token/timeframe)
- `pocket_voice` — push-to-talk UI with waveform
- `pocket_confirm` — exact-terms trade confirmation w/ 10s countdown

All screens are designed round-first for the 1.28" circular display.

## Audio — add-on modules (required for voice)

The 1.28" board has no onboard mic or speaker. Wire:

| Module | ESP32-S3 pins (suggested) | Notes |
|---|---|---|
| INMP441 mic | BCK 4, WS 5, SD 6, 3V3/GND | I2S RX |
| MAX98357A amp | BCK 4, WS 5, SD 7, 3V3/GND | I2S TX, shares BCK/WS with mic |

> I2S sharing BCK/WS between mic (RX) and amp (TX) is the standard ESP32
> voice-assistant wiring. Verify against your exact board revision.

## Power

The board has a 3.7V MX1.25 LiPo header and charges over USB-C. Use a LiPo
with the MX1.25 2-pin plug — JST-PH (2.0mm) will not fit without an adapter.
