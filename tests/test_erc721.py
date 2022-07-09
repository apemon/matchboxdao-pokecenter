# """contract.cairo test file."""
# import os

# import pytest
# from signers import MockSigner
# from utils import (
#     str_to_felt, compile_starknet_files, to_uint
# )
# from starkware.starknet.testing.starknet import Starknet

# PIP_PATH = "/Users/apemon/.pyenv/versions/3.7.13/lib/python3.7/site-packages"

# # The path to the contract source code.
# CONTRACT_FILE = os.path.join('contracts', 'erc721.cairo')
# ACCOUNT_FILE = os.path.join(PIP_PATH, 'openzeppelin/account/Account.cairo')

# TOKENS = [to_uint(1)]
# TOKEN = TOKENS[0]

# signer = MockSigner(123456789987654321)


# # The testing library uses python's asyncio. So the following
# # decorator and the ``async`` keyword are needed.
# @pytest.mark.asyncio
# async def test_constructor():
#     # Create a new Starknet class that simulates the StarkNet
#     # system.
#     starknet = await Starknet.empty()

#     account_cls = compile_starknet_files(
#         files=[ACCOUNT_FILE],
#         debug_info=True
#     )
#     account1 = await starknet.deploy(
#         contract_class=account_cls,
#         constructor_calldata=[signer.public_key]
#     )
#     # Deploy the contract.
#     contract = await starknet.deploy(
#         source=CONTRACT_FILE,
#         constructor_calldata=[
#             str_to_felt("Sandbox Land"),
#             str_to_felt("SAND"),
#             account1.contract_address
#         ]
#     )
#     execution_info = await contract.name().invoke()
#     assert execution_info.result == (str_to_felt("Sandbox Land"),)

#     await signer.send_transaction(
#         account1, contract.contract_address, 'mint', [account1.contract_address, *TOKENS[0]]
#     )
#     execution_info = await contract.ownerOf(TOKENS[0]).invoke()
#     assert execution_info.result == (account1.contract_address,)

#     execution_info = await contract.ownerTimestamp(TOKENS[0]).invoke()
#     print (execution_info)
