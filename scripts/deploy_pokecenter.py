def run(nre):
    #print("Compiling contract…")
    nre.compile(["contracts/pokecenter.cairo"]) # we compile our contract first
    #print("Deploying contract…")
    params = []
    address, abi = nre.deploy("pokecenter", params, alias="pokecenter")
    print(f"ABI: {abi},\nContract address: {address}")
    # mint nft
    # tokenId = to_uint(1)
    # nre.invoke(address, 'mint', [admin, from_uint(tokenId)])

# Auxiliary functions
def str_to_felt(text):
    b_text = bytes(text, "ascii")
    return int.from_bytes(b_text, "big")
def uint(a):
    return(a, 0)
def to_uint(a):
    """Takes in value, returns uint256-ish tuple."""
    return (a & ((1 << 128) - 1), a >> 128)
def from_uint(uint):
    """Takes in uint256-ish tuple, returns value."""
    return uint[0] + (uint[1] << 128)
