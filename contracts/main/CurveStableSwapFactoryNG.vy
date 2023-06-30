# @version 0.3.9
"""
@title CurveStableswapFactoryNG
@author Curve.Fi
@license Copyright (c) Curve.Fi, 2023 - all rights reserved
@notice Permissionless pool deployer and registry
"""

struct PoolArray:
    base_pool: address
    implementation: address
    liquidity_gauge: address
    coins: address[MAX_COINS]
    decimals: uint256[MAX_COINS]
    n_coins: uint256
    asset_type: uint256

struct BasePoolArray:
    implementations: address[10]
    lp_token: address
    fee_receiver: address
    coins: address[MAX_COINS]
    is_rebasing: bool[MAX_COINS]
    decimals: uint256
    n_coins: uint256
    asset_type: uint256


interface AddressProvider:
    def admin() -> address: view

interface ERC20:
    def balanceOf(_addr: address) -> uint256: view
    def decimals() -> uint256: view
    def totalSupply() -> uint256: view
    def approve(_spender: address, _amount: uint256): nonpayable

interface CurvePool:
    def A() -> uint256: view
    def fee() -> uint256: view
    def admin_fee() -> uint256: view
    def balances(i: uint256) -> uint256: view
    def admin_balances(i: uint256) -> uint256: view
    def get_virtual_price() -> uint256: view
    def initialize(
        _name: String[32],
        _symbol: String[10],
        _coin: address,
        _rate_multiplier: uint256,
        _A: uint256,
        _fee: uint256,
    ): nonpayable
    def exchange(  # TODO: change this!
        i: int128,
        j: int128,
        dx: uint256,
        min_dy: uint256,
        _receiver: address,
    ) -> uint256: nonpayable

interface CurveFactoryMetapool:
    def coins(i :uint256) -> address: view
    def decimals() -> uint256: view


event BasePoolAdded:
    base_pool: address

event PlainPoolDeployed:
    coins: address[MAX_COINS]
    A: uint256
    fee: uint256
    deployer: address

event MetaPoolDeployed:
    coin: address
    base_pool: address
    A: uint256
    fee: uint256
    deployer: address

event LiquidityGaugeDeployed:
    pool: address
    gauge: address

WETH20: public(immutable(address))

MAX_COINS: constant(uint256) = 8
ADDRESS_PROVIDER: constant(address) = 0x0000000022D53366457F9d5E68Ec105046FC4383
OLD_FACTORY: constant(address) = 0x0959158b6040D32d04c301A72CBFD6b39E21c9AE

admin: public(address)
future_admin: public(address)

pool_list: public(address[4294967296])   # master list of pools
pool_count: public(uint256)              # actual length of pool_list
pool_data: HashMap[address, PoolArray]

base_pool_list: public(address[4294967296])   # master list of pools
base_pool_count: public(uint256)         # actual length of pool_list
base_pool_data: public(HashMap[address, BasePoolArray])

# asset -> is used in a metapool?
base_pool_assets: public(HashMap[address, bool])

# number of coins -> implementation addresses
# for "plain pools" (as opposed to metapools), implementation contracts
# are organized according to the number of coins in the pool
plain_implementations: public(HashMap[uint256, address[10]])

# fee receiver for plain pools
fee_receiver: address

gauge_implementation: public(address)

# mapping of coins -> pools for trading
# a mapping key is generated for each pair of addresses via
# `bitwise_xor(convert(a, uint256), convert(b, uint256))`
markets: HashMap[uint256, address[4294967296]]
market_counts: HashMap[uint256, uint256]


@external
def __init__(_fee_receiver: address, _owner: address, _weth: address):

    self.fee_receiver = _fee_receiver
    self.admin = _owner

    WETH20 = _weth


# <--- Factory Getters --->

@view
@external
def metapool_implementations(_base_pool: address) -> address[10]:
    """
    @notice Get a list of implementation contracts for metapools targetting the given base pool
    @dev A base pool is the pool for the LP token contained within the metapool
    @param _base_pool Address of the base pool
    @return List of implementation contract addresses
    """
    return self.base_pool_data[_base_pool].implementations


@view
@external
def find_pool_for_coins(_from: address, _to: address, i: uint256 = 0) -> address:
    """
    @notice Find an available pool for exchanging two coins
    @param _from Address of coin to be sent
    @param _to Address of coin to be received
    @param i Index value. When multiple pools are available
            this value is used to return the n'th address.
    @return Pool address
    """
    key: uint256 = (convert(_from, uint256) ^ convert(_to, uint256))
    return self.markets[key][i]


# <--- Pool Getters --->

@view
@external
def get_base_pool(_pool: address) -> address:
    """
    @notice Get the base pool for a given factory metapool
    @param _pool Metapool address
    @return Address of base pool
    """
    return self.pool_data[_pool].base_pool


@view
@external
def get_n_coins(_pool: address) -> (uint256):
    """
    @notice Get the number of coins in a pool
    @param _pool Pool address
    @return Number of coins
    """
    return self.pool_data[_pool].n_coins


@view
@external
def get_meta_n_coins(_pool: address) -> (uint256, uint256):
    """
    @notice Get the number of coins in a metapool
    @param _pool Pool address
    @return Number of wrapped coins, number of underlying coins
    """
    base_pool: address = self.pool_data[_pool].base_pool
    return 2, self.base_pool_data[base_pool].n_coins + 1


@view
@external
def get_coins(_pool: address) -> address[MAX_COINS]:
    """
    @notice Get the coins within a pool
    @param _pool Pool address
    @return List of coin addresses
    """
    return self.pool_data[_pool].coins


@view
@external
def get_underlying_coins(_pool: address) -> address[MAX_COINS]:
    """
    @notice Get the underlying coins within a pool
    @dev Reverts if a pool does not exist or is not a metapool
    @param _pool Pool address
    @return List of coin addresses
    """
    coins: address[MAX_COINS] = empty(address[MAX_COINS])
    base_pool: address = self.pool_data[_pool].base_pool
    assert base_pool != empty(address)  # dev: pool is not metapool
    coins[0] = self.pool_data[_pool].coins[0]
    for i in range(1, MAX_COINS):
        coins[i] = self.base_pool_data[base_pool].coins[i - 1]
        if coins[i] == empty(address):
            break

    return coins


@view
@external
def get_decimals(_pool: address) -> uint256[MAX_COINS]:
    """
    @notice Get decimal places for each coin within a pool
    @param _pool Pool address
    @return uint256 list of decimals
    """
    if self.pool_data[_pool].base_pool != empty(address):
        decimals: uint256[MAX_COINS] = empty(uint256[MAX_COINS])
        decimals = self.pool_data[_pool].decimals
        decimals[1] = 18
        return decimals
    return self.pool_data[_pool].decimals


@view
@external
def get_underlying_decimals(_pool: address) -> uint256[MAX_COINS]:
    """
    @notice Get decimal places for each underlying coin within a pool
    @param _pool Pool address
    @return uint256 list of decimals
    """
    # decimals are tightly packed as a series of uint8 within a little-endian bytes32
    # the packed value is stored as uint256 to simplify unpacking via shift and modulo
    pool_decimals: uint256[MAX_COINS] = empty(uint256[MAX_COINS])
    pool_decimals = self.pool_data[_pool].decimals
    decimals: uint256[MAX_COINS] = empty(uint256[MAX_COINS])
    decimals[0] = pool_decimals[0]
    base_pool: address = self.pool_data[_pool].base_pool
    packed_decimals: uint256 = self.base_pool_data[base_pool].decimals

    for i in range(MAX_COINS):

        unpacked: uint256 = (packed_decimals >> 8 * i) % 256
        if unpacked == 0:
            break
        decimals[i+1] = unpacked

    return decimals


@view
@external
def get_metapool_rates(_pool: address) -> uint256[2]:
    """
    @notice Get rates for coins within a metapool
    @param _pool Pool address
    @return Rates for each coin, precision normalized to 10**18
    """
    rates: uint256[2] = [10**18, 0]
    rates[1] = CurvePool(self.pool_data[_pool].base_pool).get_virtual_price()
    return rates


@view
@external
def get_balances(_pool: address) -> uint256[MAX_COINS]:
    """
    @notice Get balances for each coin within a pool
    @dev For pools using lending, these are the wrapped coin balances
    @param _pool Pool address
    @return uint256 list of balances
    """
    balances: uint256[MAX_COINS] = empty(uint256[MAX_COINS])

    if self.pool_data[_pool].base_pool != empty(address):
        balances[0] = CurvePool(_pool).balances(0)
        balances[1] = CurvePool(_pool).balances(1)
        return balances

    n_coins: uint256 = self.pool_data[_pool].n_coins
    for i in range(MAX_COINS):
        if i < n_coins:
            balances[i] = CurvePool(_pool).balances(i)
        else:
            balances[i] = 0

    return balances


@view
@external
def get_underlying_balances(_pool: address) -> uint256[MAX_COINS]:
    """
    @notice Get balances for each underlying coin within a metapool
    @param _pool Metapool address
    @return uint256 list of underlying balances
    """

    base_pool: address = self.pool_data[_pool].base_pool
    assert base_pool != empty(address)  # dev: pool is not a metapool

    underlying_balances: uint256[MAX_COINS] = empty(uint256[MAX_COINS])
    underlying_balances[0] = CurvePool(_pool).balances(0)

    base_total_supply: uint256 = ERC20(self.pool_data[_pool].coins[1]).totalSupply()
    if base_total_supply > 0:
        underlying_pct: uint256 = CurvePool(_pool).balances(1) * 10**36 / base_total_supply
        n_coins: uint256 = self.base_pool_data[base_pool].n_coins
        for i in range(MAX_COINS):
            if i == n_coins:
                break
            underlying_balances[i + 1] = CurvePool(base_pool).balances(i) * underlying_pct / 10**36

    return underlying_balances


@view
@external
def get_A(_pool: address) -> uint256:
    """
    @notice Get the amplfication co-efficient for a pool
    @param _pool Pool address
    @return uint256 A
    """
    return CurvePool(_pool).A()


@view
@external
def get_fees(_pool: address) -> (uint256, uint256):
    """
    @notice Get the fees for a pool
    @dev Fees are expressed as integers
    @return Pool fee and admin fee as uint256 with 1e10 precision
    """
    return CurvePool(_pool).fee(), CurvePool(_pool).admin_fee()


@view
@external
def get_admin_balances(_pool: address) -> uint256[MAX_COINS]:
    """
    @notice Get the current admin balances (uncollected fees) for a pool
    @param _pool Pool address
    @return List of uint256 admin balances
    """
    n_coins: uint256 = self.pool_data[_pool].n_coins
    admin_balances: uint256[MAX_COINS] = empty(uint256[MAX_COINS])
    for i in range(MAX_COINS):
        if i == n_coins:
            break
        admin_balances[i] = CurvePool(_pool).admin_balances(i)
    return admin_balances


@view
@external
def get_coin_indices(
    _pool: address,
    _from: address,
    _to: address
) -> (int128, int128, bool):
    """
    @notice Convert coin addresses to indices for use with pool methods
    @param _pool Pool address
    @param _from Coin address to be used as `i` within a pool
    @param _to Coin address to be used as `j` within a pool
    @return int128 `i`, int128 `j`, boolean indicating if `i` and `j` are underlying coins
    """
    coin: address = self.pool_data[_pool].coins[0]
    base_pool: address = self.pool_data[_pool].base_pool
    if coin in [_from, _to] and base_pool != empty(address):
        base_lp_token: address = self.pool_data[_pool].coins[1]
        if base_lp_token in [_from, _to]:
            # True and False convert to 1 and 0 - a bit of voodoo that
            # works because we only ever have 2 non-underlying coins if base pool is empty(address)
            return convert(_to == coin, int128), convert(_from == coin, int128), False

    found_market: bool = False
    i: uint256 = 0
    j: uint256 = 0
    for x in range(MAX_COINS):
        if base_pool == empty(address):
            if x >= MAX_COINS:
                raise "No available market"
            if x != 0:
                coin = self.pool_data[_pool].coins[x]
        else:
            if x != 0:
                coin = self.base_pool_data[base_pool].coins[x-1]
        if coin == empty(address):
            raise "No available market"
        if coin == _from:
            i = x
        elif coin == _to:
            j = x
        else:
            continue
        if found_market:
            # the second time we find a match, break out of the loop
            break
        # the first time we find a match, set `found_market` to True
        found_market = True

    return convert(i, int128), convert(j, int128), True


@view
@external
def get_gauge(_pool: address) -> address:
    """
    @notice Get the address of the liquidity gauge contract for a factory pool
    @dev Returns `empty(address)` if a gauge has not been deployed
    @param _pool Pool address
    @return Implementation contract address
    """
    return self.pool_data[_pool].liquidity_gauge


@view
@external
def get_implementation_address(_pool: address) -> address:
    """
    @notice Get the address of the implementation contract used for a factory pool
    @param _pool Pool address
    @return Implementation contract address
    """
    return self.pool_data[_pool].implementation


@view
@external
def is_meta(_pool: address) -> bool:
    """
    @notice Verify `_pool` is a metapool
    @param _pool Pool address
    @return True if `_pool` is a metapool
    """
    return self.pool_data[_pool].base_pool != empty(address)


@view
@external
def get_pool_asset_type(_pool: address) -> uint256:
    """
    @notice Query the asset type of `_pool`
    @dev 0 = USD, 1 = ETH, 2 = BTC, 3 = Other
    @param _pool Pool Address
    @return Integer indicating the pool asset type
    """
    base_pool: address = self.pool_data[_pool].base_pool
    if base_pool == empty(address):
        return self.pool_data[_pool].asset_type
    else:
        return self.base_pool_data[base_pool].asset_type


@view
@external
def get_fee_receiver(_pool: address) -> address:
    base_pool: address = self.pool_data[_pool].base_pool
    if base_pool == empty(address):
        return self.fee_receiver
    else:
        return self.base_pool_data[base_pool].fee_receiver


# <--- Pool Deployers --->

@external
def deploy_plain_pool(
    _name: String[32],
    _symbol: String[10],
    _coins: address[MAX_COINS],
    _A: uint256,
    _fee: uint256,
    _ma_exp_time: uint256,
    _method_ids: bytes4[MAX_COINS] = empty(bytes4[MAX_COINS]),
    _oracles: address[MAX_COINS] = empty(address[MAX_COINS]),
    _asset_type: uint256 = 0,
    _implementation_idx: uint256 = 0,
    _is_rebasing: bool[MAX_COINS] = empty(bool[MAX_COINS])
) -> address:
    """
    @notice Deploy a new plain pool
    @param _name Name of the new plain pool
    @param _symbol Symbol for the new plain pool - will be
                   concatenated with factory symbol
    @param _coins List of addresses of the coins being used in the pool.
    @param _A Amplification co-efficient - a lower value here means
              less tolerance for imbalance within the pool's assets.
              Suggested values include:
               * Uncollateralized algorithmic stablecoins: 5-10
               * Non-redeemable, collateralized assets: 100
               * Redeemable assets: 200-400
    @param _fee Trade fee, given as an integer with 1e10 precision. The
                the maximum is 1% (100000000).
                50% of the fee is distributed to veCRV holders.
    @param _ma_exp_time Averaging window of oracle. Set as time_in_seconds / ln(2)
                        Example: for 10 minute EMA, _ma_exp_time is 600 / ln(2) ~= 866
    @param _method_ids Array of first four bytes of the Keccak-256 hash of the function signatures
                       of the oracle addresses that gives rate oracles.
                       Calculated as: keccak(text=event_signature.replace(" ", ""))[:4]
    @param _oracles Array of rate oracle addresses.
    @param _asset_type Asset type for pool, as an integer
                       0 = USD, 1 = ETH, 2 = BTC, 3 = Other
    @param _implementation_idx Index of the implementation to use. All possible
                implementations for a pool of N_COINS can be publicly accessed
                via `plain_implementations(N_COINS)`
    @param _is_rebasing If any of the coins rebases, then this should be set to True.
    @return Address of the deployed pool
    """
    assert _fee <= 100000000, "Invalid fee"

    n_coins: uint256 = MAX_COINS
    rate_multipliers: uint256[MAX_COINS] = empty(uint256[MAX_COINS])
    decimals: uint256[MAX_COINS] = empty(uint256[MAX_COINS])

    for i in range(MAX_COINS):

        coin: address = _coins[i]

        if coin == empty(address):
            assert i > 1, "Insufficient coins"
            n_coins = i
            break

        decimals[i] = ERC20(coin).decimals()
        assert decimals[i] < 19, "Max 18 decimals for coins"

        rate_multipliers[i] = 10 ** (36 - decimals[i])

        for x in range(i, i + MAX_COINS):
            if x+1 == MAX_COINS:
                break
            if _coins[x+1] == empty(address):
                break
            assert coin != _coins[x+1], "Duplicate coins"

    implementation: address = self.plain_implementations[n_coins][_implementation_idx]
    assert implementation != empty(address), "Invalid implementation index"
    pool: address = create_from_blueprint(
        implementation,
        _name,
        _symbol,
        _coins,
        rate_multipliers,
        _A,
        _fee,
        WETH20,
        _ma_exp_time,
        _method_ids,
        _oracles,
        _is_rebasing,
        code_offset=3
    )

    length: uint256 = self.pool_count
    self.pool_list[length] = pool
    self.pool_count = length + 1
    self.pool_data[pool].decimals = decimals
    self.pool_data[pool].n_coins = n_coins
    self.pool_data[pool].base_pool = empty(address)
    self.pool_data[pool].implementation = implementation
    if _asset_type != 0:
        self.pool_data[pool].asset_type = _asset_type

    for i in range(MAX_COINS):
        coin: address = _coins[i]
        if coin == empty(address):
            break
        self.pool_data[pool].coins[i] = coin
        raw_call(
            coin,
            concat(
                method_id("approve(address,uint256)"),
                convert(pool, bytes32),
                convert(max_value(uint256), bytes32)
            )
        )
        for j in range(MAX_COINS):
            if i < j:
                swappable_coin: address = _coins[j]
                key: uint256 = (convert(coin, uint256) ^ convert(swappable_coin, uint256))
                length = self.market_counts[key]
                self.markets[key][length] = pool
                self.market_counts[key] = length + 1

    log PlainPoolDeployed(_coins, _A, _fee, msg.sender)
    return pool


@external
def deploy_metapool(
    _base_pool: address,
    _name: String[32],
    _symbol: String[10],
    _coin: address,
    _A: uint256,
    _fee: uint256,
    _ma_exp_time: uint256,
    _method_id: bytes4 = empty(bytes4),
    _oracle: address = empty(address),
    _implementation_idx: uint256 = 0,
    _is_rebasing: bool = False
) -> address:
    """
    @notice Deploy a new metapool
    @param _base_pool Address of the base pool to use
                      within the metapool
    @param _name Name of the new metapool
    @param _symbol Symbol for the new metapool - will be
                   concatenated with the base pool symbol
    @param _coin Address of the coin being used in the metapool
    @param _A Amplification co-efficient - a higher value here means
              less tolerance for imbalance within the pool's assets.
              Suggested values include:
               * Uncollateralized algorithmic stablecoins: 5-10
               * Non-redeemable, collateralized assets: 100
               * Redeemable assets: 200-400
    @param _fee Trade fee, given as an integer with 1e10 precision. The
                the maximum is 1% (100000000).
                50% of the fee is distributed to veCRV holders.
    @param _implementation_idx Index of the implementation to use. All possible
                implementations for a BASE_POOL can be publicly accessed
                via `metapool_implementations(BASE_POOL)`
    @param _is_rebasing If _coin rebases, then this should be set to True.
    @return Address of the deployed pool
    """
    assert not self.base_pool_assets[_coin], "Invalid asset: Cannot pair base pool asset with base pool's LP token"
    assert _fee <= 100000000, "Invalid fee"

    implementation: address = self.base_pool_data[_base_pool].implementations[_implementation_idx]
    assert implementation != empty(address), "Invalid implementation index"

    # things break if a token has >18 decimals
    decimals: uint256 = ERC20(_coin).decimals()
    assert decimals < 19, "Max 18 decimals for coins"

    # combine _coins's _is_rebasing and basepool coins _is_rebasing:
    base_pool_is_rebasing: bool[MAX_COINS] = self.base_pool_data[_base_pool].is_rebasing
    is_rebasing: bool[MAX_COINS] = empty(bool[MAX_COINS])
    is_rebasing[0] = _is_rebasing
    for i in range(MAX_COINS):

        if i+1 == MAX_COINS:
            break

        is_rebasing[i+1] = base_pool_is_rebasing[i]

    pool: address = create_from_blueprint(
        implementation,
        _name,
        _symbol,
        _coin,
        10 ** (36 - decimals),  # rate multiplier for _coin
        _A,
        _fee,
        _ma_exp_time,
        _method_id,
        _oracle,
        _is_rebasing,
        _base_pool,
        self.base_pool_data[_base_pool].lp_token,
        self.base_pool_data[_base_pool].coins,
        code_offset=3
    )

    ERC20(_coin).approve(pool, max_value(uint256))

    # add pool to pool_list
    length: uint256 = self.pool_count
    self.pool_list[length] = pool
    self.pool_count = length + 1

    base_lp_token: address = self.base_pool_data[_base_pool].lp_token

    self.pool_data[pool].decimals = [decimals, 0, 0, 0, 0, 0, 0, 0]
    self.pool_data[pool].n_coins = 2
    self.pool_data[pool].base_pool = _base_pool
    self.pool_data[pool].coins[0] = _coin
    self.pool_data[pool].coins[1] = self.base_pool_data[_base_pool].lp_token
    self.pool_data[pool].implementation = implementation

    is_finished: bool = False
    for i in range(MAX_COINS):
        swappable_coin: address = self.base_pool_data[_base_pool].coins[i]
        if swappable_coin == empty(address):
            is_finished = True
            swappable_coin = base_lp_token

        key: uint256 = (convert(_coin, uint256) ^ convert(swappable_coin, uint256))
        length = self.market_counts[key]
        self.markets[key][length] = pool
        self.market_counts[key] = length + 1
        if is_finished:
            break

    log MetaPoolDeployed(_coin, _base_pool, _A, _fee, msg.sender)
    return pool


@external
def deploy_gauge(_pool: address) -> address:
    """
    @notice Deploy a liquidity gauge for a factory pool
    @param _pool Factory pool address to deploy a gauge for
    @return Address of the deployed gauge
    """
    assert self.pool_data[_pool].coins[0] != empty(address), "Unknown pool"
    assert self.pool_data[_pool].liquidity_gauge == empty(address), "Gauge already deployed"
    implementation: address = self.gauge_implementation
    assert implementation != empty(address), "Gauge implementation not set"

    gauge: address = create_from_blueprint(self.gauge_implementation, _pool, code_offset=3)
    self.pool_data[_pool].liquidity_gauge = gauge

    log LiquidityGaugeDeployed(_pool, gauge)
    return gauge


# <--- Admin / Guarded Functionality --->

@external
def add_base_pool(
    _base_pool: address,
    _base_lp_token: address,
    _fee_receiver: address,
    _coins: address[MAX_COINS],
    _asset_type: uint256,
    _n_coins: uint256,
    _is_rebasing: bool[MAX_COINS],
    _implementations: address[10],
):
    """
    @notice Add a base pool to the registry, which may be used in factory metapools
    @dev Only callable by admin
    @param _base_pool Pool address to add
    @param _fee_receiver Admin fee receiver address for metapools using this base pool
    @param _asset_type Asset type for pool, as an integer  0 = USD, 1 = ETH, 2 = BTC, 3 = Other
    @param _is_rebasing Array of booleans: _is_rebasing[i] is True if basepool coin[i] is rebasing
    @param _implementations List of implementation addresses that can be used with this base pool
    """
    assert msg.sender == self.admin  # dev: admin-only function
    assert self.base_pool_data[_base_pool].coins[0] == empty(address)  # dev: pool exists
    assert _n_coins < MAX_COINS  # dev: base pool can only have (MAX_COINS - 1) coins.

    # add pool to pool_list
    length: uint256 = self.base_pool_count
    self.base_pool_list[length] = _base_pool
    self.base_pool_count = length + 1
    self.base_pool_data[_base_pool].lp_token = _base_lp_token
    self.base_pool_data[_base_pool].n_coins = _n_coins
    self.base_pool_data[_base_pool].fee_receiver = _fee_receiver
    if _asset_type != 0:
        self.base_pool_data[_base_pool].asset_type = _asset_type

    for i in range(10):
        implementation: address = _implementations[i]
        if implementation == empty(address):
            break
        self.base_pool_data[_base_pool].implementations[i] = implementation

    decimals: uint256 = 0
    coins: address[MAX_COINS] = _coins
    for i in range(MAX_COINS):
        if i == _n_coins:
            break
        coin: address = coins[i]
        self.base_pool_data[_base_pool].coins[i] = coin
        self.base_pool_data[_base_pool].is_rebasing[i] = _is_rebasing[i]
        self.base_pool_assets[coin] = True
        decimals += (ERC20(coin).decimals() << i*8)
    self.base_pool_data[_base_pool].decimals = decimals

    log BasePoolAdded(_base_pool)


@external
def set_metapool_implementations(
    _base_pool: address,
    _implementations: address[10],
):
    """
    @notice Set implementation contracts for a metapool
    @dev Only callable by admin
    @param _base_pool Pool address to add
    @param _implementations Implementation address to use when deploying metapools
    """

    # TODO: ensure only one implementation can be set at a time

    assert msg.sender == self.admin  # dev: admin-only function
    assert self.base_pool_data[_base_pool].coins[0] != empty(address)  # dev: base pool does not exist

    for i in range(10):
        new_imp: address = _implementations[i]
        current_imp: address = self.base_pool_data[_base_pool].implementations[i]
        if new_imp == current_imp:
            if new_imp == empty(address):
                break
        else:
            self.base_pool_data[_base_pool].implementations[i] = new_imp


@external
def set_plain_implementations(
    _n_coins: uint256,
    _implementation_index: uint256,
    _implementation: address,
):
    assert msg.sender == self.admin  # dev: admin-only function
    self.plain_implementations[_n_coins][_implementation_index] = _implementation


@external
def set_gauge_implementation(_gauge_implementation: address):
    assert msg.sender == self.admin  # dev: admin-only function

    self.gauge_implementation = _gauge_implementation


@external
def batch_set_pool_asset_type(_pools: address[32], _asset_types: uint256[32]):
    """
    @notice Batch set the asset type for factory pools
    @dev Used to modify asset types that were set incorrectly at deployment
    """
    assert msg.sender in [self.admin]  # dev: admin-only function

    for i in range(32):
        if _pools[i] == empty(address):
            break
        self.pool_data[_pools[i]].asset_type = _asset_types[i]


@external
def commit_transfer_ownership(_addr: address):
    """
    @notice Transfer ownership of this contract to `addr`
    @param _addr Address of the new owner
    """
    assert msg.sender == self.admin  # dev: admin only

    self.future_admin = _addr


@external
def accept_transfer_ownership():
    """
    @notice Accept a pending ownership transfer
    @dev Only callable by the new owner
    """
    _admin: address = self.future_admin
    assert msg.sender == _admin  # dev: future admin only

    self.admin = _admin
    self.future_admin = empty(address)


@external
def set_fee_receiver(_base_pool: address, _fee_receiver: address):
    """
    @notice Set fee receiver for base and plain pools
    @param _base_pool Address of base pool to set fee receiver for.
                      For plain pools, leave as `empty(address)`.
    @param _fee_receiver Address that fees are sent to
    """
    assert msg.sender == self.admin  # dev: admin only
    if _base_pool == empty(address):
        self.fee_receiver = _fee_receiver
    else:
        self.base_pool_data[_base_pool].fee_receiver = _fee_receiver


@external
def convert_metapool_fees() -> bool:
    """
    @notice Convert the fees of a metapool and transfer to
            the metapool's fee receiver
    @dev All fees are converted to LP token of base pool
    """
    base_pool: address = self.pool_data[msg.sender].base_pool
    assert base_pool != empty(address)  # dev: sender must be metapool
    coin: address = self.pool_data[msg.sender].coins[0]

    amount: uint256 = ERC20(coin).balanceOf(self)
    receiver: address = self.base_pool_data[base_pool].fee_receiver

    CurvePool(msg.sender).exchange(0, 1, amount, 0, receiver)
    return True
