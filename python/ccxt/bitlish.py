# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
from ccxt.base.errors import NotSupported


class bitlish (Exchange):

    def describe(self):
        return self.deep_extend(super(bitlish, self).describe(), {
            'id': 'bitlish',
            'name': 'Bitlish',
            'countries': ['GB', 'EU', 'RU'],
            'rateLimit': 1500,
            'version': 'v1',
            'has': {
                'CORS': False,
                'fetchTickers': True,
                'fetchOHLCV': True,
                'withdraw': True,
            },
            'timeframes': {
                '1h': 3600,
            },
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/27766275-dcfc6c30-5ed3-11e7-839d-00a846385d0b.jpg',
                'api': 'https://bitlish.com/api',
                'www': 'https://bitlish.com',
                'doc': 'https://bitlish.com/api',
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': False,
            },
            'fees': {
                'trading': {
                    'tierBased': False,
                    'percentage': True,
                    'taker': 0.3 / 100,  # anonymous 0.3%, verified 0.2%
                    'maker': 0,
                },
                'funding': {
                    'tierBased': False,
                    'percentage': False,
                    'withdraw': {
                        'BTC': 0.001,
                        'LTC': 0.001,
                        'DOGE': 0.001,
                        'ETH': 0.001,
                        'XMR': 0,
                        'ZEC': 0.001,
                        'DASH': 0.0001,
                        'EUR': 50,
                    },
                    'deposit': {
                        'BTC': 0,
                        'LTC': 0,
                        'DOGE': 0,
                        'ETH': 0,
                        'XMR': 0,
                        'ZEC': 0,
                        'DASH': 0,
                        'EUR': 0,
                    },
                },
            },
            'api': {
                'public': {
                    'get': [
                        'instruments',
                        'ohlcv',
                        'pairs',
                        'tickers',
                        'trades_depth',
                        'trades_history',
                    ],
                    'post': [
                        'instruments',
                        'ohlcv',
                        'pairs',
                        'tickers',
                        'trades_depth',
                        'trades_history',
                    ],
                },
                'private': {
                    'post': [
                        'accounts_operations',
                        'balance',
                        'cancel_trade',
                        'cancel_trades_by_ids',
                        'cancel_all_trades',
                        'create_bcode',
                        'create_template_wallet',
                        'create_trade',
                        'deposit',
                        'list_accounts_operations_from_ts',
                        'list_active_trades',
                        'list_bcodes',
                        'list_my_matches_from_ts',
                        'list_my_trades',
                        'list_my_trads_from_ts',
                        'list_payment_methods',
                        'list_payments',
                        'redeem_code',
                        'resign',
                        'signin',
                        'signout',
                        'trade_details',
                        'trade_options',
                        'withdraw',
                        'withdraw_by_id',
                    ],
                },
            },
            'commonCurrencies': {
                'DSH': 'DASH',
                'XDG': 'DOGE',
            },
        })

    def fetch_markets(self, params={}):
        response = self.publicGetPairs(params)
        result = []
        keys = list(response.keys())
        for i in range(0, len(keys)):
            key = keys[i]
            market = response[key]
            id = self.safe_string(market, 'id')
            name = self.safe_string(market, 'name')
            baseId, quoteId = name.split('/')
            base = self.safeCurrencyCode(baseId)
            quote = self.safeCurrencyCode(quoteId)
            symbol = base + '/' + quote
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'info': market,
            })
        return result

    def parse_ticker(self, ticker, market):
        timestamp = self.milliseconds()
        symbol = None
        if market is not None:
            symbol = market['symbol']
        last = self.safe_float(ticker, 'last')
        return {
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'high': self.safe_float(ticker, 'max'),
            'low': self.safe_float(ticker, 'min'),
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'ask'),
            'askVolume': None,
            'vwap': None,
            'open': self.safe_float(ticker, 'first'),
            'close': last,
            'last': last,
            'previousClose': None,
            'change': None,
            'percentage': self.safe_float(ticker, 'prc') * 100,
            'average': None,
            'baseVolume': self.safe_float(ticker, 'sum'),
            'quoteVolume': None,
            'info': ticker,
        }

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        tickers = self.publicGetTickers(params)
        ids = list(tickers.keys())
        result = {}
        for i in range(0, len(ids)):
            id = ids[i]
            market = self.safe_value(self.markets_by_id, id)
            symbol = None
            if market is not None:
                symbol = market['symbol']
            else:
                baseId = id[0:3]
                quoteId = id[3:6]
                base = self.safeCurrencyCode(baseId)
                quote = self.safeCurrencyCode(quoteId)
                symbol = base + '/' + quote
            ticker = tickers[id]
            result[symbol] = self.parse_ticker(ticker, market)
        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetTickers(params)
        marketId = market['id']
        return self.parse_ticker(response[marketId], market)

    def fetch_ohlcv(self, symbol, timeframe='1h', since=None, limit=None, params={}):
        self.load_markets()
        # market = self.market(symbol)
        now = self.seconds()
        start = now - 86400 * 30  # last 30 days
        if since is not None:
            start = int(since / 1000)
        interval = [str(start), None]
        request = {
            'time_range': interval,
        }
        return self.publicPostOhlcv(self.extend(request, params))

    def fetch_order_book(self, symbol, limit=None, params={}):
        self.load_markets()
        request = {
            'pair_id': self.market_id(symbol),
        }
        response = self.publicGetTradesDepth(self.extend(request, params))
        timestamp = None
        last = self.safe_integer(response, 'last')
        if last is not None:
            timestamp = int(last / 1000)
        return self.parse_order_book(response, timestamp, 'bid', 'ask', 'price', 'volume')

    def parse_trade(self, trade, market=None):
        side = 'buy' if (trade['dir'] == 'bid') else 'sell'
        symbol = None
        if market is not None:
            symbol = market['symbol']
        timestamp = self.safe_integer(trade, 'created')
        if timestamp is not None:
            timestamp = int(timestamp / 1000)
        price = self.safe_float(trade, 'price')
        amount = self.safe_float(trade, 'amount')
        cost = None
        if amount is not None:
            if price is not None:
                cost = price * amount
        return {
            'id': None,
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': None,
            'type': None,
            'side': side,
            'takerOrMaker': None,
            'price': price,
            'amount': amount,
            'cost': cost,
            'fee': None,
        }

    def fetch_trades(self, symbol, since=None, limit=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        response = self.publicGetTradesHistory(self.extend({
            'pair_id': market['id'],
        }, params))
        return self.parse_trades(response['list'], market, since, limit)

    def fetch_balance(self, params={}):
        self.load_markets()
        response = self.privatePostBalance(params)
        result = {'info': response}
        currencyIds = list(response.keys())
        for i in range(0, len(currencyIds)):
            currencyId = currencyIds[i]
            code = self.safeCurrencyCode(currencyId)
            account = self.account()
            balance = self.safe_value(response, currencyId, {})
            account['free'] = self.safe_float(balance, 'funds')
            account['used'] = self.safe_float(balance, 'holded')
            result[code] = account
        return self.parse_balance(result)

    def sign_in(self, params={}):
        request = {
            'login': self.login,
            'passwd': self.password,
        }
        return self.privatePostSignin(self.extend(request, params))

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        self.load_markets()
        request = {
            'pair_id': self.market_id(symbol),
            'dir': 'bid' if (side == 'buy') else 'ask',
            'amount': amount,
        }
        if type == 'limit':
            request['price'] = price
        response = self.privatePostCreateTrade(self.extend(request, params))
        id = self.safe_string(response, 'id')
        return {
            'info': response,
            'id': id,
        }

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'id': id,
        }
        return self.privatePostCancelTrade(self.extend(request, params))

    def withdraw(self, code, amount, address, tag=None, params={}):
        if code != 'BTC':
            # they did not document other types...
            raise NotSupported(self.id + ' currently supports BTC withdrawals only, until they document other currencies...')
        self.check_address(address)
        self.load_markets()
        currency = self.currency(code)
        request = {
            'currency': currency.lower(),
            'amount': float(amount),
            'account': address,
            'payment_method': 'bitcoin',  # they did not document other types...
        }
        response = self.privatePostWithdraw(self.extend(request, params))
        return {
            'info': response,
            'id': response['message_id'],
        }

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        url = self.urls['api'] + '/' + self.version + '/' + path
        if api == 'public':
            if method == 'GET':
                if params:
                    url += '?' + self.urlencode(params)
            else:
                body = self.json(params)
                headers = {'Content-Type': 'application/json'}
        else:
            self.check_required_credentials()
            body = self.json(self.extend({'token': self.apiKey}, params))
            headers = {'Content-Type': 'application/json'}
        return {'url': url, 'method': method, 'body': body, 'headers': headers}
