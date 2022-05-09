"""Module containing signer classes."""
# pylint: disable=no-value-for-parameter
from typing import List
from eth_typing import Address
from eth_account import Account
from eth_account.messages import encode_defunct, SignableMessage
from eth_account.datastructures import SignedMessage
from hexbytes import HexBytes


class EIP191Signer:
    """Signer for EIP-191 messages"""

    def __init__(self, private_key: Address = None) -> None:
        if private_key is None:
            self.acc = Account.create()
        else:
            if len(HexBytes(private_key)) == 32:
                self.acc = Account.from_key(private_key)
            else:
                raise ValueError("EIP191Signer: private_key not a 20 byte address")

    @staticmethod
    def __check_inputs(abi_types: List[str], values: List) -> None:
        if not isinstance(abi_types, list) or len(abi_types) == 0:
            raise ValueError(
                "EIP191Signer:sign abi_types cannot be None or an empty list"
            )

        if not isinstance(values, list) or len(values) == 0:
            raise ValueError("EIP191Signer:sign values cannot be None or an empty list")

        if len(abi_types) != len(values):
            raise ValueError(
                "EIP191Signer:sign length mismatch between abi_types and values"
            )

    @staticmethod
    def __pack_data(abi_types: List[str], values: List) -> bytearray:
        data: bytearray = bytearray()
        length: int = 0
        val: int = 0
        for abi_type, value in zip(abi_types, values):
            if "int8" in abi_type.lower():
                length = 1
                val = value
            elif "int16" in abi_type.lower():
                length = 2
                val = value
            elif "int32" in abi_type.lower():
                length = 4
                val = value
            elif "int64" in abi_type.lower():
                length = 8
                val = value
            elif "int128" in abi_type.lower():
                length = 16
                val = value
            elif "int256" in abi_type.lower():
                length = 32
                val = value
            elif "bytes32" in abi_type.lower():
                length = 32
                val = int(value, 16)
            elif "address" in abi_type.lower():
                length = 20
                val = int(value, 16)
            elif "string" in abi_type.lower():
                length = len(value)
                data.extend(value.encode("utf-8"))  # extend in place

            if isinstance(val, int):
                data.extend(bytearray(val.to_bytes(length=length, byteorder="big")))

        return data

    def sign(self, abi_types: List[str], values: List) -> SignedMessage:
        """Function to sign pack and sign the data supplied according to
        the ABI types and EIP-191 version 0x45"""
        EIP191Signer.__check_inputs(abi_types, values)
        msg: SignableMessage = self.get_signable_message(abi_types, values)
        return Account.sign_message(msg, private_key=self.acc.key)

    @staticmethod
    def get_signable_message(abi_types: List[str], values: List) -> SignableMessage:
        """Function to get the signable message by packing the data according to abi types"""
        EIP191Signer.__check_inputs(abi_types, values)
        data: bytearray = EIP191Signer.__pack_data(abi_types, values)
        return encode_defunct(data)

    @property
    def address(self) -> str:
        """Returns the public key of the signer"""
        return self.acc.address
