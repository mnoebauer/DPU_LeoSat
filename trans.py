import transmission
import asyncio

tranObj = transmission.Transmission()
asyncio.run(tranObj.transmit())
