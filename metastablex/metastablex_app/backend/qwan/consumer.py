import json
import torch
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

class QWANConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

        self.N = 64
        self.field = torch.randn((self.N,self.N))*0.1

        asyncio.create_task(self.loop())

    def evolve(self, x):
        lap = (
            -4*x
            + torch.roll(x,1,0)
            + torch.roll(x,-1,0)
            + torch.roll(x,1,1)
            + torch.roll(x,-1,1)
        )

        return x + 0.05*(lap - x**3 + x)

    def metrics(self, x):
        mean = x.mean()
        var = ((x-mean)**2).mean()

        Phi = (x**2).mean()

        # Lyapunov approx simples
        lyap = torch.log(var + 1e-6)

        return {
            "Phi": float(Phi),
            "lyapunov": float(lyap)
        }

    async def loop(self):
        while True:
            self.field = self.evolve(self.field)

            m = self.metrics(self.field)

            await self.send(text_data=json.dumps({
                "field": self.field.tolist(),
                **m
            }))

            await asyncio.sleep(0.03)
