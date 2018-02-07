from unittest import TestCase
from peregrine.async_build_markets import build_all_collections, build_specific_collections, build_collections
import ccxt.async as ccxt


class TestCollectionBuilder(TestCase):

    def test_exchange_length(self):
        collections = build_all_collections(write=False)
        for exchange_list in collections.values():
            # check that all collections are at least one exchange long
            self.assertGreater(len(exchange_list), 1)


class TestCollectionBuilders(TestCase):

    def test_errors_raised(self):
        with self.assertRaises(ValueError):
            # note the misspelling of "countries" as "contries"
            build_specific_collections(contries='US')

    def test_whitelist_blacklist(self):
        us_exchanges = build_specific_collections(countries='US')
        confirmed_us_exchanges = []
        for exchange_list in us_exchanges.values():
            for exchange_name in exchange_list:
                # so each exchange is only checked once.
                if exchange_name in confirmed_us_exchanges:
                    continue
                exchange = getattr(ccxt, exchange_name)()
                self.assertIn('US', exchange.countries)
                confirmed_us_exchanges.append(exchange_name)

        not_us_exchanges = build_specific_collections(countries='US', blacklist=True)
        confirmed_not_us_exchanges = []
        for exchange_list in not_us_exchanges.values():
            for exchange_name in exchange_list:
                # so each exchange is only checked once.
                if exchange_name in confirmed_not_us_exchanges:
                    continue
                exchange = getattr(ccxt, exchange_name)()
                self.assertNotIn('US', exchange.countries)
                confirmed_not_us_exchanges.append(exchange_name)

    def test_kwargs_with_dict_as_rule(self):
        specific_collections = build_specific_collections(has={'fetchOrderBook': True, 'createOrder': True})
        # exchanges which are confirmed to meet the given criteria (.hasFetchOrderBook and .hasCreateOrder)
        confirmed_exchanges = []
        for exchange_list in specific_collections.values():
            for exchange_name in exchange_list:
                if exchange_name in confirmed_exchanges:
                    continue
                exchange = getattr(ccxt, exchange_name)()
                self.assertTrue(exchange.hasFetchOrderBook and exchange.hasCreateOrder)
                confirmed_exchanges.append(exchange_name)

    def test_build_collections(self):
        collections = build_collections(write=False)
        confirmed_exchanges = []
        for exchange_list in collections.values():
            for exchange_name in exchange_list:
                if exchange_name in confirmed_exchanges:
                    continue
                exchange = getattr(ccxt, exchange_name)()
                self.assertTrue(exchange.has['fetchOrderBook'])
                confirmed_exchanges.append(exchange_name)