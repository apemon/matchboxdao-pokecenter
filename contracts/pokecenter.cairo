%lang starknet

from starkware.cairo.common.cairo_builtins import HashBuiltin, BitwiseBuiltin
from starkware.cairo.common.alloc import alloc
from starkware.cairo.common.uint256 import Uint256
from starkware.starknet.common.syscalls import get_caller_address

from openzeppelin.security.safemath import SafeUint256
from openzeppelin.token.erc721.interfaces.IERC721 import IERC721

#
# Structs
#

struct Post:
    member issuer : felt
    member data : felt
end

struct Comment:
    member post_id : Uint256
    member issuer : felt
    member data : felt
end

struct Attestion:
    member nft_address : felt
    member token_id : Uint256
end

@storage_var
func Poke_posts(post_id : Uint256) -> (post : Post):
end

@storage_var
func Poke_post_attestions(post_id : Uint256) -> (attestion : Attestion):
end

@storage_var
func Poke_last_post_id() -> (id : Uint256):
end

@storage_var
func Poke_comments(post_id : Uint256, comment_id : Uint256) -> (comment : Comment):
end

@storage_var
func Poke_comment_attestions(post_id : Uint256, comment_id : Uint256) -> (attestion : Attestion):
end

@storage_var
func Poke_last_comment_id(post_id : Uint256) -> (id : Uint256):
end

@constructor
func constructor{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}():
    Poke_last_post_id.write(Uint256(0, 0))
    return ()
end

@external
func create_post{pedersen_ptr : HashBuiltin*, syscall_ptr : felt*, range_check_ptr}(data : felt):
    let (caller) = get_caller_address()
    # check owner

    let (post_id) = Poke_last_post_id.read()
    let post = Post(issuer=caller, data=data)
    Poke_posts.write(post_id, post)
    let (new_post_id) = SafeUint256.add(post_id, Uint256(1, 0))
    Poke_last_post_id.write(new_post_id)
    return ()
end

@external
func create_post_with_attestion{pedersen_ptr : HashBuiltin*, syscall_ptr : felt*, range_check_ptr}(
    data : felt, nftAddress : felt, tokenId : Uint256
):
    let (caller) = get_caller_address()
    # check owner
    let (token_owner) = IERC721.ownerOf(contract_address=nftAddress, tokenId=tokenId)

    with_attr error_message("nft doesn't belong to the caller"):
        assert caller = token_owner
    end

    let (post_id) = Poke_last_post_id.read()
    let post = Post(issuer=caller, data=data)
    Poke_posts.write(post_id, post)
    let attestion = Attestion(nft_address=nftAddress, token_id=tokenId)
    Poke_post_attestions.write(post_id, attestion)
    let (new_post_id) = SafeUint256.add(post_id, Uint256(1, 0))
    Poke_last_post_id.write(new_post_id)
    return ()
end

@external
func create_comment{pedersen_ptr : HashBuiltin*, syscall_ptr : felt*, range_check_ptr}(
    postId : Uint256, data : felt
):
    let (caller) = get_caller_address()
    let (comment_id) = Poke_last_comment_id.read(postId)
    let comment = Comment(post_id=postId, issuer=caller, data=data)
    Poke_comments.write(postId, comment_id, comment)
    let (new_comment_id) = SafeUint256.add(comment_id, Uint256(1, 0))
    Poke_last_comment_id.write(postId, new_comment_id)
    return ()
end

@external
func create_comment_with_attestion{
    pedersen_ptr : HashBuiltin*, syscall_ptr : felt*, range_check_ptr
}(postId : Uint256, data : felt, nftAddress : felt, tokenId : Uint256):
    let (caller) = get_caller_address()

    # check owner
    let (token_owner) = IERC721.ownerOf(contract_address=nftAddress, tokenId=tokenId)

    with_attr error_message("nft doesn't belong to the caller"):
        assert caller = token_owner
    end

    let (comment_id) = Poke_last_comment_id.read(postId)
    let comment = Comment(post_id=postId, issuer=caller, data=data)
    Poke_comments.write(postId, comment_id, comment)
    let attestion = Attestion(nft_address=nftAddress, token_id=tokenId)
    Poke_comment_attestions.write(postId, comment_id, attestion)
    let (new_comment_id) = SafeUint256.add(comment_id, Uint256(1, 0))
    Poke_last_comment_id.write(postId, new_comment_id)
    return ()
end

@view
func post{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(post_id : Uint256) -> (
    post : Post
):
    let (post) = Poke_posts.read(post_id)
    return (post)
end

@view
func post_attestion{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
    post_id : Uint256
) -> (attestion : Attestion):
    let (attestion) = Poke_post_attestions.read(post_id)
    return (attestion)
end

@view
func comment{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
    post_id : Uint256, comment_id : Uint256
) -> (comment : Comment):
    let (comment) = Poke_comments.read(post_id, comment_id)
    return (comment)
end

@view
func comment_attestion{syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
    post_id : Uint256, comment_id : Uint256
) -> (attestion : Attestion):
    let (attestion) = Poke_comment_attestions.read(post_id, comment_id)
    return (attestion)
end
