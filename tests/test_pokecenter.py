"""contract.cairo test file."""
import os

import pytest
from signers import MockSigner
from utils import (
    str_to_felt, compile_starknet_files, to_uint
)
from starkware.starknet.testing.starknet import Starknet

PIP_PATH = "/Users/apemon/.pyenv/versions/3.7.13/lib/python3.7/site-packages"

# The path to the contract source code.
CONTRACT_FILE = os.path.join('contracts', 'pokecenter.cairo')
NFT_FILE = os.path.join('contracts', 'erc721.cairo')
ACCOUNT_FILE = os.path.join(PIP_PATH, 'openzeppelin/account/Account.cairo')

TOKENS = [to_uint(0), to_uint(1)]
TOKEN = TOKENS[0]

signer = MockSigner(123456789987654321)


# The testing library uses python's asyncio. So the following
# decorator and the ``async`` keyword are needed.
@pytest.mark.asyncio
async def test_constructor():
    # Create a new Starknet class that simulates the StarkNet
    # system.
    starknet = await Starknet.empty()

    account_cls = compile_starknet_files(
        files=[ACCOUNT_FILE],
        debug_info=True
    )
    account1 = await starknet.deploy(
        contract_class=account_cls,
        constructor_calldata=[signer.public_key]
    )
    # deploy nft
    nft = await starknet.deploy(
        source=NFT_FILE,
        constructor_calldata=[
            str_to_felt("Mock NFT for Hackathon"),
            str_to_felt("MOCK"),
            account1.contract_address
        ]
    )
    # Deploy the contract.
    contract = await starknet.deploy(
        source=CONTRACT_FILE,
        constructor_calldata=[]
    )
    await signer.send_transaction(
        account1, contract.contract_address, 'create_post', [str_to_felt('hello world')]
    )
    execution_info = await contract.post(TOKENS[0]).invoke()
    assert execution_info.result.post.issuer == account1.contract_address

    # mint nft
    await signer.send_transaction(
        account1, nft.contract_address, 'mint', [account1.contract_address, *TOKENS[1]]
    )
    # post with attestion
    await signer.send_transaction(
        account1, contract.contract_address, 'create_post_with_attestion', [str_to_felt('hello world'), nft.contract_address, *TOKENS[1]]
    )
    execution_info = await contract.post_attestion(TOKENS[1]).invoke()
    assert execution_info.result.attestion.nft_address == nft.contract_address
    # post comment
    await signer.send_transaction(
        account1, contract.contract_address, 'create_comment', [*TOKENS[0], str_to_felt('hello world')]
    )
    execution_info = await contract.comment(TOKENS[0], TOKENS[0]).invoke()
    print (execution_info.result)
    assert execution_info.result.comment.data == str_to_felt('hello world')

    await signer.send_transaction(
        account1, contract.contract_address, 'create_comment_with_attestion', [*TOKENS[1], str_to_felt('hello world'), nft.contract_address, *TOKENS[1]]
    )
    execution_info = await contract.comment(TOKENS[1], TOKENS[0]).invoke()
    print (execution_info.result)
    assert execution_info.result.comment.data == str_to_felt('hello world')
    execution_info = await contract.comment_attestion(TOKENS[1],TOKENS[0]).invoke()
    assert execution_info.result.attestion.nft_address == nft.contract_address

