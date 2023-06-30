# import itertools

import boa
import pytest

MAX_COINS = 8

# TODO: ADD meta


class TestFactory:
    class TestBasic:
        @pytest.mark.parametrize("sending,receiving", [(0, 1), (1, 0)])
        def test_find_pool_for_coins(self, factory, swap, pool_tokens, sending, receiving):
            assert (
                factory.find_pool_for_coins(pool_tokens[sending].address, pool_tokens[receiving].address)
                == swap.address
            )

        def test_get_coins(self, factory, swap, pool_tokens, pool_size, zero_address):
            assert factory.get_coins(swap.address) == [pt.address for pt in pool_tokens] + [zero_address] * (
                MAX_COINS - pool_size
            )

        def test_get_decimals(self, factory, swap, decimals):
            assert factory.get_decimals(swap.address) == decimals + [0] * (MAX_COINS - len(decimals))

        def test_get_balances(self, factory, swap, pool_size):
            assert factory.get_balances(swap.address) == [swap.balances(i) for i in range(pool_size)] + [0] * (
                MAX_COINS - pool_size
            )

        @pytest.mark.only_for_pool_type(0)
        def test_get_underlying_balances(self, factory, swap):
            with boa.reverts() as e:
                factory.get_underlying_balances(swap.address)
                assert str(e) == "dev: pool is not a metapool"

        def test_get_A(self, factory, swap):
            assert factory.get_A(swap.address) == swap.A()

        def test_get_fees(self, factory, swap):
            assert factory.get_fees(swap.address) == (swap.fee(), swap.admin_fee())

        def test_get_admin_balances(self, factory, swap, pool_size):
            assert factory.get_admin_balances(swap.address) == [swap.admin_balances(i) for i in range(pool_size)] + [
                0
            ] * (MAX_COINS - pool_size)

        @pytest.mark.parametrize("sending,receiving", [(0, 1), (1, 0)])
        def test_get_coin_indices(self, factory, swap, sending, receiving, pool_tokens):
            i, j, is_underlying = factory.get_coin_indices(
                swap.address, pool_tokens[sending].address, pool_tokens[receiving].address
            )
            assert i == sending
            assert j == receiving

    # @pytest.mark.only_for_pool_type(1)
    # class TestMeta:
    #     # TODO: replace with meta implementation
    #     @pytest.fixture
    #     def new_factory_setup(
    #         self,
    #         new_factory,
    #         amm_implementation_plain,
    #         pool_size,
    #         alice,
    #         fee_receiver,
    #     ):
    #         with boa.env.prank(alice):
    #             new_factory.set_plain_implementations(pool_size, 0, amm_implementation_plain.address)
    #
    #     def test_factory(self, factory, swap):
    #         assert factory.get_meta_n_coins(swap) == [2, 4]
    #
    # def test_get_underlying_coins(self, factory, swap, underlying_coins, pool_size, zero_address):
    #     assert factory.get_underlying_coins(swap) == underlying_coins + [zero_address] * (
    #             4 - pool_size
    #     )
    #
    # def test_get_underlying_decimals(self, factory, swap, underlying_decimals):
    #     assert factory.get_underlying_decimals(swap) == underlying_decimals + [0] * (
    #             4 - len(underlying_decimals)
    #     )
    #
    # @pytest.mark.parametrize("idx", range(1, 4))
    # def test_find_pool_for_coins_underlying(self, factory, swap, underlying_coins, idx):
    #     assert factory.find_pool_for_coins(underlying_coins[0], underlying_coins[idx]) == swap
    #     assert factory.find_pool_for_coins(underlying_coins[idx], underlying_coins[0]) == swap
    #
    # def test_get_metapool_rates(self, factory, swap, base_pool):
    #     assert factory.get_metapool_rates(swap) == [10 ** 18, base_pool.get_virtual_price()]
    #
    # @pytest.mark.parametrize("sending,receiving", itertools.permutations(range(1, 4), 2))
    # def test_find_pool_underlying_base_pool_only(self, factory, underlying_coins, sending, receiving, zero_address):
    #     assert (
    #         factory.find_pool_for_coins(underlying_coins[sending], underlying_coins[receiving])
    #         == zero_address
    #     )
    #
    # @pytest.mark.parametrize("sending,receiving", itertools.permutations(range(1, 4), 2))
    # def test_get_coin_indices_underlying(factory, swap, sending, receiving, underlying_coins):
    #     i, j, is_underlying = factory.get_coin_indices(
    #         swap, underlying_coins[sending], underlying_coins[receiving]
    #     )
    #     assert i == sending
    #     assert j == receiving
    #     assert is_underlying is False
    #
    # @pytest.mark.parametrize("idx", range(1, 4))
    # def test_get_coin_indices_reverts(self, factory, swap, base_lp_token, underlying_coins, idx):
    #     with boa.reverts():
    #         factory.get_coin_indices(swap, base_lp_token, underlying_coins[idx])
    #
    # @pytest.mark.usefixtures("forked_chain")
    # @pytest.mark.only_for_pool_type(0)
    # class TestFactoryAddPools:
    #     def test_add_base_pool(self, factory, alice, fee_receiver, implementation_usd):
    #         susd_pool = "0xA5407eAE9Ba41422680e2e00537571bcC53efBfD"
    #         factory.add_base_pool(
    #             susd_pool, fee_receiver, 0, [implementation_usd] + [ZERO_ADDRESS] * 9, {"from": alice}
    #         )
    #         assert factory.base_pool_count() == 3
    #         assert factory.base_pool_list(2) == susd_pool
    #         assert factory.get_fee_receiver(susd_pool) == fee_receiver
    #
    #     def test_add_base_pool_already_exists(self, factory, base_pool, alice, fee_receiver, implementation_usd):
    #         with boa.reverts("dev: pool exists"):
    #             factory.add_base_pool(
    #                 base_pool, fee_receiver, 0, [implementation_usd] + [ZERO_ADDRESS] * 9, {"from": alice}
    #             )
    #
    #     def test_add_base_pool_only_admin(factory, base_pool, bob, fee_receiver, implementation_usd):
    #         with brownie.reverts("dev: admin-only function"):
    #             factory.add_base_pool(
    #                 "0xA5407eAE9Ba41422680e2e00537571bcC53efBfD",
    #                 fee_receiver,
    #                 0,
    #                 [implementation_usd] + [ZERO_ADDRESS] * 9,
    #                 {"from": bob},
    #             )
    #
    #     @pytest.mark.skip
    #     def test_deploy_metapool(MetaUSD, new_factory, new_factory_setup, base_pool, bob):
    #         coin = ERC20(decimals=7)
    #
    #         tx = new_factory.deploy_metapool(
    #             base_pool, "Name", "SYM", coin, 12345, 50000000, 0, {"from": bob}
    #         )
    #         assert tx.return_value == tx.new_contracts[0]
    #         swap = MetaUSD.at(tx.return_value)
    #
    #         assert swap.coins(0) == coin
    #         assert swap.A() == 12345
    #         assert swap.fee() == 50000000
    #
    #         assert new_factory.pool_count() == 1
    #         assert new_factory.pool_list(0) == swap
    #         assert new_factory.get_decimals(swap) == [7, 18, 0, 0]
    #
    #
    #     @pytest.mark.skip
    #     def test_add_existing_metapools(
    #         factory, new_factory, fee_receiver, implementation_usd, base_pool, alice
    #     ):
    #         assert new_factory.pool_count() == 0
    #         # add existing USD pools to new factory
    #         new_factory.add_base_pool(
    #             base_pool, fee_receiver, 0, [implementation_usd] + [ZERO_ADDRESS] * 9, {"from": alice}
    #         )
    #         new_factory.add_existing_metapools(
    #             ["0x5a6A4D54456819380173272A5E8E9B9904BdF41B", "0x43b4FdFD4Ff969587185cDB6f0BD875c5Fc83f8c"]
    #             + [ZERO_ADDRESS] * 8
    #         )
    #         assert new_factory.pool_count() == 2
    #         assert new_factory.pool_list(0) == "0x5a6A4D54456819380173272A5E8E9B9904BdF41B"
    #         assert new_factory.pool_list(1) == "0x43b4FdFD4Ff969587185cDB6f0BD875c5Fc83f8c"
    #         assert (
    #             new_factory.get_implementation_address("0x5a6A4D54456819380173272A5E8E9B9904BdF41B")
    #             == "0x5F890841f657d90E081bAbdB532A05996Af79Fe6"
    #         )
    #
    #
    #     @pytest.mark.skip
    #     def test_add_existing_metapools_unknown_pool(swap, new_factory):
    #         with brownie.reverts("dev: pool not in old factory"):
    #             new_factory.add_existing_metapools([swap] + [ZERO_ADDRESS] * 9)
    #
    #
    #     @pytest.mark.skip
    #     def test_add_existing_metapools_duplicate_pool(
    #         new_factory, base_pool, implementation_usd, fee_receiver, alice
    #     ):
    #         new_factory.add_base_pool(
    #             base_pool, fee_receiver, 0, [implementation_usd] + [ZERO_ADDRESS] * 9, {"from": alice}
    #         )
    #         new_factory.add_existing_metapools(
    #             ["0x5a6A4D54456819380173272A5E8E9B9904BdF41B"] + [ZERO_ADDRESS] * 9
    #         )
    #         with brownie.reverts("dev: pool already exists"):
    #             new_factory.add_existing_metapools(
    #                 ["0x5a6A4D54456819380173272A5E8E9B9904BdF41B"] + [ZERO_ADDRESS] * 9
    #             )
    #
    #
    #     def test_deploy_plain_pool(
    #         new_factory_setup, new_factory, decimals, bob, plain_basic, project, coins
    #     ):
    #
    #         tx = new_factory.deploy_plain_pool(
    #             "Test Plain",
    #             "TST",
    #             coins + [ZERO_ADDRESS] * (4 - len(coins)),
    #             12345,
    #             50000000,
    #             0,
    #             0,
    #             {"from": bob},
    #         )
    #         assert tx.return_value == tx.new_contracts[0]
    #         swap = getattr(project, plain_basic._name).at(tx.return_value)
    #
    #         assert swap.coins(0) == coins[0]
    #         assert swap.coins(1) == coins[1]
    #
    #         assert swap.A() == 12345
    #         assert swap.fee() == 50000000
    #
    #         assert new_factory.pool_count() == 1
    #         assert new_factory.pool_list(0) == swap
    #         assert new_factory.get_decimals(swap) == decimals + [0] * (4 - len(decimals))
    #
    #
    #     @pytest.mark.skip
    #     def test_pool_count(new_factory, coins, new_factory_setup, bob, base_pool):
    #
    #         tx = new_factory.deploy_plain_pool(
    #             "Test Plain", "TST", coins, 12345, 50000000, 0, 0, {"from": bob}
    #         )
    #         assert tx.return_value == tx.new_contracts[0]
    #         assert new_factory.pool_count() == 1
    #
    #         coin = ERC20(decimals=7)
    #         tx = new_factory.deploy_metapool(
    #             base_pool, "Name", "SYM", coin, 12345, 50000000, 0, {"from": bob}
    #         )
    #         assert tx.return_value == tx.new_contracts[0]
    #         assert new_factory.pool_count() == 2
    #
    #         coin = ERC20(decimals=7)
    #         pool = Contract("0x7fC77b5c7614E1533320Ea6DDc2Eb61fa00A9714")
    #         tx = new_factory.deploy_metapool(pool, "Name", "SYM", coin, 123456, 50000000, 0, {"from": bob})
    #         assert new_factory.pool_count() == 3
    #
    #
    #     @pytest.mark.skip
    #     def test_deploy_plain_pool_revert(base_pool, new_factory, new_factory_setup, bob):
    #         coin = ERC20(decimals=7)
    #         new_factory.deploy_metapool(base_pool, "Name", "SYM", coin, 12345, 50000000, 0, {"from": bob})
    #         existing_coin = base_pool.coins(0)
    #         assert new_factory.base_pool_assets(existing_coin)
    #         coins = [existing_coin, ERC20(decimals=9), ZERO_ADDRESS, ZERO_ADDRESS]
    #         # should revert because a metapool already exists for one of the coins
    #         with brownie.reverts("Invalid asset, deploy a metapool"):
    #             new_factory.deploy_plain_pool("Test Plain", "TST", coins, 12345, 50000000, {"from": bob})
