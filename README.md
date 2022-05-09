# evm-utils
Utilities for helping develop EVM compatible smart contracts. All utilities are written in Python. The repository uses [Poetry](https://python-poetry.org/) for packaging and dependency management.

## EIP191_Signer
This class represents a signer that signs data per [EIP-191 version E](https://eips.ethereum.org/EIPS/eip-191). This is useful for testing smart contracts that utilize ecrecover from a signature. Either a known private key can be given as the signer or a randomly generated signer can be used if no private key is sent to the constructor.

## Merkle_Tree_Keccak
This class builds a merkle tree using the Solidity Keccak function from [web3py](https://github.com/ethereum/web3.py). The leaves to build the tree must be HexByte values that are 32 bytes long. Ideally these are computed from data using the same Solidity Keccak function, but it is not required.

The merkle tree is built with each layer having the nodes sorted in ascending order.

## Running Tests
To run tests