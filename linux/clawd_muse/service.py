import argparse
import base64
import json
from pathlib import Path
from .musebook import Client

SPECS = {
    'clawd.status': ('Read wallet service status', {}),
    'clawd.portfolio': ('Read linked wallet balances', {}),
    'clawd.quote': ('Prepare a live swap quote in base units; never executes', {'input_mint': 'string', 'output_mint': 'string', 'amount': 'string'}),
    'clawd.chart': ('Fetch a 240x240 JPEG market chart', {'mint': 'string'}),
    'clawd.voice': ('Parse a transcript for review; never executes', {'transcript': 'string'}),
    'clawd.buy': ('Prepare a buy quote for browser approval; amount is input base units', {'input_mint': 'string', 'output_mint': 'string', 'amount': 'string'}),
    'clawd.sell': ('Prepare a sell quote for browser approval; amount is input base units', {'input_mint': 'string', 'output_mint': 'string', 'amount': 'string'}),
}

def dispatch(client, command, params):
    if command not in SPECS:
        raise ValueError('Unsupported Pocket Wallet command.')
    for key, kind in SPECS[command][1].items():
        if not isinstance(params.get(key), str):
            raise ValueError(f'{key} must be a string.')
    if command == 'clawd.status':
        return client.request('status')
    if command == 'clawd.portfolio':
        return client.request('portfolio')
    if command == 'clawd.voice':
        return client.request('voice', {'transcript': params['transcript']})
    if command == 'clawd.chart':
        image = client.chart(params['mint'], params.get('tf', '1h'))
        return {'format': 'jpeg', 'width': 240, 'height': 240, 'data_b64': base64.b64encode(image).decode()}
    quote = client.request('quote', {k: v for k, v in params.items() if k in ('input_mint', 'output_mint', 'amount', 'venue', 'slippage_bps')})
    return {'quote': quote, 'requires_wallet_approval': True,
            'next_step': 'Open Pocket Wallet on your phone to review a fresh quote and sign. This device cannot execute.'}

def main():
    parser = argparse.ArgumentParser(description='Pocket Wallet companion: data and review, no local wallet keys')
    parser.add_argument('--config', default=str(Path.home() / '.config/pocket-wallet/config.toml'))
    parser.add_argument('command', choices=SPECS)
    parser.add_argument('params', nargs='?', default='{}', help='JSON parameters')
    args = parser.parse_args()
    try:
        params = json.loads(args.params)
        if not isinstance(params, dict):
            raise ValueError('Parameters must be a JSON object.')
        print(json.dumps(dispatch(Client.from_config(args.config), args.command, params)))
    except (ValueError, KeyError, OSError) as exc:
        parser.exit(1, f'{exc}\n')

if __name__ == '__main__':
    main()
