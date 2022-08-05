from typing import List
from eth_typing import Hash32
from evm_sc_utils.merkle_tree import MerkleTreeKeccak
from web3 import Web3

"""
@dev testing values computed by the library against merkletreejs and keccak256 javascript libraries
"""


def test_three_addresses():
    leaves: List[str] = [
        "0x807c47A89F720fe4Ee9b8343c286Fc886f43191b",
        "0x844ec86426F076647A5362706a04570A5965473B",
        "0x46C0a5326E643E4f71D3149d50B48216e174Ae84"
    ]
    hashed_leaves: List[Hash32] = [
        Web3.solidityKeccak(["address"], [leaf]) for leaf in leaves
    ]
    mt = MerkleTreeKeccak(hashed_leaves)
    assert (
        mt.root_hash
        == "0x1d8c3fe103f58db27a9a8e824b1af9ec98a7fb3434ea37750f6206c0da288903"
        and mt.get_proof(hashed_leaves[0])
        == [
            "0x50ba2086958d320d73135728ff30eae03ef09b45fea302102d844697eb2f4b6d",
            "0xf9e19de495b8998dfee29352ebd3bfe146263e1f8b3223187244cf38e03ab9c5",
        ]
        and mt.get_proof(hashed_leaves[1])
        == [
            "0x344d536da52f2f25e5f9e89b357952f4ed7fdf6a74025f4a9098dc355396695a",
            "0xf9e19de495b8998dfee29352ebd3bfe146263e1f8b3223187244cf38e03ab9c5",
        ]
        and mt.get_proof(hashed_leaves[2])
        == ["0xe9c363ac8b15db69db1f132015672432dae2ca766a668862d5371379ce145d38"]
    )
