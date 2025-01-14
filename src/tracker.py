import time

import requests

from loguru import logger

from src.models.pairs.service import Service as PairService
from src.models.prices.service import Service as PriceService

from src.models.pairs.dto import PairView
from src.models.prices.dto import PriceView

pair_service = PairService()
price_service = PriceService()


class Tracker:
    async def run(self):
        while True:
            # TODO: делать выборку selected_pair каждые 5 минут
            selected_pair = await self.get_selected_pair()

            time.sleep(1.1)
            try:
                current_price = self.get_current_price(pair=selected_pair.text)
                print(current_price)
                await price_service.create(
                    PriceView(
                        value=current_price,
                        timestamp=int(time.time()),
                        pair_id=selected_pair.id
                    )
                )
            except Exception as e:
                logger.error(e)

    async def get_selected_pair(self) -> PairView:
        pair = await pair_service.read_selected()
        if pair:
            return pair
        else:
            return None

    def get_current_price(self, pair: str, category: str = 'spot') -> float:
        url = 'https://api.bybit.com/v5/market/tickers'
        params = f'?category={category}&symbol={pair}'
        response = requests.get(f'{url}{params}')

        if response and 'result' in response.json() and response.json()['result']:
            return float(response.json()['result']['list'][0]['lastPrice'])
        else:
            raise Exception(response.json()['retMsg'])
