import pytest
from evm_utils.signers import EIP191Signer
from eth_account.messages import SignableMessage
from eth_account import Account
from web3 import Web3


@pytest.fixture
def random_signer():
    return EIP191Signer()


@pytest.fixture(scope="module")
def acc():
    return Account.create()


@pytest.fixture
def known_signer(acc):
    return EIP191Signer(private_key=acc.key.hex())


class Test_Random_Signer:
    # test sending empty lists to sign
    def test_empty_abi_types(self, random_signer):
        with pytest.raises(ValueError):
            random_signer.sign([], [1])

    def test_empty_values(self, random_signer):
        with pytest.raises(ValueError):
            random_signer.sign(["uint256"], [])

    def test_not_list_abi_types(self, random_signer):
        with pytest.raises(ValueError):
            random_signer.sign("uint256", [])

    def test_not_list_values(self, random_signer):
        with pytest.raises(ValueError):
            random_signer.sign([], 1)

    def test_not_equal_lengths(self, random_signer):
        with pytest.raises(ValueError):
            random_signer.sign(["uint256"], [1, 2])

    # Recover random_signer from a message
    def test_uint256_pair(self, random_signer):
        msg: SignableMessage = random_signer.get_signable_message(
            ["uint256", "uint256"], [1, 2]
        )
        sig: SignedMessage = random_signer.sign(["uint256", "uint256"], [1, 2])
        assert (
            Account.recover_message(msg, signature=sig.signature)
            == random_signer.address
            and Web3.solidityKeccak(
                ["string", "uint256", "uint256"],
                ["\x19Ethereum Signed Message:\n64", 1, 2],
            )
            == sig.messageHash
        )


class Test_Known_Signer:
    # test sending empty lists to sign
    def test_empty_abi_types(self, known_signer):
        with pytest.raises(ValueError):
            known_signer.sign([], [1])

    def test_empty_values(self, known_signer):
        with pytest.raises(ValueError):
            known_signer.sign(["uint256"], [])

    def test_not_list_abi_types(self, known_signer):
        with pytest.raises(ValueError):
            known_signer.sign("uint256", [])

    def test_not_list_values(self, known_signer):
        with pytest.raises(ValueError):
            known_signer.sign([], 1)

    def test_not_equal_lengths(self, known_signer):
        with pytest.raises(ValueError):
            known_signer.sign(["uint256"], [1, 2])

    # Recover known_signer from a message
    def test_uint256_pair(self, known_signer):
        msg: SignableMessage = known_signer.get_signable_message(
            ["uint256", "uint256"], [1, 2]
        )
        sig: SignedMessage = known_signer.sign(["uint256", "uint256"], [1, 2])
        assert (
            Account.recover_message(msg, signature=sig.signature)
            == known_signer.address
            and Web3.solidityKeccak(
                ["string", "uint256", "uint256"],
                ["\x19Ethereum Signed Message:\n64", 1, 2],
            )
            == sig.messageHash
        )
