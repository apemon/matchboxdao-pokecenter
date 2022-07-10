# MatchboxDAO Hackathon - PokeCenter
PokeCenter is Starknet contract for social media gaming. You can create post, comment on post, upvote/downvote content. Moreover, you can attach something like attestion (proof of ownership of some nft) to increase your creditability.


## Testnet Contracts (Goerli)


|    Contract  | Address |
| ----------- | ----------- |
| Mock NFT      | [0x05f8e9e261bc538ef82b4a6f409bf518571d826ec4c117b1f2c17c8eb8a10894](https://goerli.voyager.online/contract/0x05f8e9e261bc538ef82b4a6f409bf518571d826ec4c117b1f2c17c8eb8a10894)       |
| PokeCenter   | [0x02fe58b9bab7948690772da752812c9b4cc333181fa9943ba97df5cf2afeade0](https://goerli.voyager.online/contract/0x02fe58b9bab7948690772da752812c9b4cc333181fa9943ba97df5cf2afeade0)        |

## Usages
```
nile install
pytest tests
```

## Limitation
- voyager explorer only support for felt only and does not support Uint256 yet. You may need to use cli or script to interact with the contracts
- post and comment data can contain only 31 characters because lack of string supported in Cairo. We may implement String if we have enough time 😛