import time
from datetime import timedelta

import requests

from loguru import logger

from src.models.pairs.service import Service as PairService
from src.models.prices.service import Service as PriceService

from src.models.pairs.dto import PairView
from src.models.prices.dto import PriceView

pair_service = PairService()
price_service = PriceService()


class Tracker:
    selected_pair: PairView
    pair_check_interval_min: int = 1

    async def run(self):
        start_time = time.time()
        self.selected_pair = await self.get_selected_pair()

        while True:
            current_time = time.time()
            if int(current_time - start_time) >= self.pair_check_interval_min * 60:
                self.selected_pair = await self.get_selected_pair()
                start_time = time.time()

            time.sleep(1.1)
            try:
                current_price = self.get_current_price(pair=self.selected_pair.text)
                logger.info(f'{self.selected_pair.text}: {current_price}')
                await price_service.create(
                    PriceView(
                        value=current_price,
                        timestamp=int(time.time()),
                        pair_id=self.selected_pair.id
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
