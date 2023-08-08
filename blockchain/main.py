"""main program for the blockchain

Usage:
    main [--log-level=L] [--port=N]

Options:
    --log-level=L       the log level [default: info]
    --port=N            the port number to be used [default: 3001]
"""
import logging

import uvicorn
from docopt import docopt

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    args = docopt(__doc__)
    log_level = args['--log-level']
    port = int(args['--port'])
    logging.info(f"Params {{ 'port':{port}, 'log_level'={log_level} }}")

    uvicorn.run('blockchain_api:app', port=port, log_level=log_level, reload=True)
