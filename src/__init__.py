import logging

logging.getLogger('asyncio').disabled = True
logging.getLogger('hypercorn.error').disabled = True
