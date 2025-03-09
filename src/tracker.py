import time

import requests
from loguru import logger

from src.models.pairs.dto import PairView
from src.models.pairs.service import Service as PairService
from src.models.prices.dto import PriceView
from src.models.prices.service import Service as PriceService

pair_service = PairService()
price_service = PriceService()


class Tracker:
    selected_pairs: list[PairView]
    pair_check_interval_min: int = 1

    async def run(self):
        start_time = time.time()
        self.selected_pairs = await self.get_selected_pairs()

        while True:
            current_time = time.time()
            if int(current_time - start_time) >= self.pair_check_interval_min * 60:
                self.selected_pairs = await self.get_selected_pairs()
                start_time = time.time()

            time.sleep(1.3)

            for selected_pair in self.selected_pairs:
                try:
                    current_price = self.get_current_price(pair=selected_pair.text)
                    if not current_price:
                        continue

                    logger.info(f'{selected_pair.text}: {current_price}')
                    await price_service.create(
                        PriceView(
                            value=current_price,
                            timestamp=int(time.time()),
                            pair_id=selected_pair.id
                        )
                    )
                except Exception as e:
                    logger.error(e)

    async def get_selected_pairs(self) -> list[PairView]:
        pairs = await pair_service.read_selected()
        if pairs:
            return pairs
        else:
            return []

    def get_current_price(self, pair: str, category: str = 'spot') -> float | None:
        url = 'https://api.bybit.com/v5/market/tickers'
        params = f'?category={category}&symbol={pair}'
        try:
            response = requests.get(f'{url}{params}', timeout=5)

            if response and 'result' in response.json() and response.json()['result']:
                return float(response.json()['result']['list'][0]['lastPrice'])
            else:
                raise Exception(response.json()['retMsg'])
        except requests.exceptions.Timeout:
            logger.info('TIMED OUT')
            return None
