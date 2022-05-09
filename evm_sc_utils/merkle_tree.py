"""Module containing Merkle Tree implementations"""
# pylint: disable=no-value-for-parameter
from typing import List, Dict
from hexbytes import HexBytes
from eth_typing import HexStr
from web3 import Web3


class MerkleTreeKeccak:
    """Class for computing a sorted Merkle Tree using Keccak hashing algorithm"""

    def __init__(self, leaves: List[HexBytes]):
        MerkleTreeKeccak.__check_input(leaves)
        self.tree = MerkleTreeKeccak.__compute_tree(leaves)

    @staticmethod
    def __check_input(leaves: List[HexBytes]):
        if not isinstance(leaves, list):
            raise ValueError("MerkleTreeKeccak: Leaves are not a list")

        if len(leaves) == 0:
            raise ValueError("MerkleTreeKeccak: Leaves are an empty list")

        for leaf in leaves:
            if not isinstance(leaf, HexBytes):
                raise TypeError(f"MerkleTreeKeccak: {leaf!r} not of HexBytes type")
            if len(leaf) != 32:
                raise ValueError(
                    f"MerkleTreeKeccak: {leaf!r} is not a valid 32 byte hash"
                )

    @staticmethod
    def __compute_tree(leaves: List[HexBytes]):
        tree: Dict = {}
        leaves.sort()
        tree[0] = leaves
        node_level = 0
        while len(tree[node_level]) != 1:
            nodes = tree[node_level]
            next_nodes: List[HexBytes] = []
            num_of_nodes = len(nodes)
            is_odd = num_of_nodes % 2 != 0
            if is_odd:
                for i in range(0, num_of_nodes - 1, 2):
                    next_nodes.append(
                        Web3.solidityKeccak(
                            ["bytes32", "bytes32"], [nodes[i], nodes[i + 1]]
                        )
                    )
                next_nodes.append(nodes[-1])
            else:
                for i in range(0, num_of_nodes, 2):
                    next_nodes.append(
                        Web3.solidityKeccak(
                            ["bytes32", "bytes32"], [nodes[i], nodes[i + 1]]
                        )
                    )
            # sort in place
            next_nodes.sort()
            tree[node_level + 1] = next_nodes
            node_level = len(tree.keys()) - 1
        return tree

    @property
    def root_hash(self) -> HexStr:
        """Returns the merkle root hash"""
        return self.tree[len(self.tree.keys()) - 1][0].hex()

    def get_proof(self, leaf: HexBytes) -> List[HexStr]:
        """Function to get the merkle proof for an input leaf"""
        if not isinstance(leaf, HexBytes):
            raise TypeError(f"MerkleTreeKeccak: {leaf!r} not of HexBytes type")
        if len(leaf) != 32:
            raise ValueError(f"MerkleTreeKeccak: {leaf!r} is not a valid 32 byte hash")

        if self.tree[0].index(leaf) < 0:
            print(self.tree[0].index(leaf))
            return []

        proof: List[HexStr] = []
        num_of_nodes: int = len(self.tree.keys()) - 1  # don't need the root hash
        lookup_val: HexBytes = leaf
        for i in range(num_of_nodes):
            loc: int = 0
            for (node, j) in zip(self.tree[i], range(len(self.tree[i]))):
                if node.hex() == lookup_val.hex():
                    loc = j
                    break
            if loc % 2 == 0 and loc != len(self.tree[i]) - 1:
                proof.append(self.tree[i][loc + 1].hex())
                lookup_val = Web3.solidityKeccak(
                    ["bytes32", "bytes32"],
                    [self.tree[i][loc], self.tree[i][loc + 1]],
                )
            elif loc % 2 == 0 and loc == len(self.tree[i]) - 1:
                pass
            else:
                proof.append(self.tree[i][loc - 1].hex())
                lookup_val = Web3.solidityKeccak(
                    ["bytes32", "bytes32"],
                    [self.tree[i][loc - 1], self.tree[i][loc]],
                )
        return proof
