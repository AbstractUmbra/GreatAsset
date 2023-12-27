"""
The MIT License (MIT)

Copyright (c) 2023-present AbstractUmbra

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad

from . import CRYPTO_PASSWORD
from .utils import _from_json  # type: ignore # allowing this private usage

if TYPE_CHECKING:
    from os import PathLike

__all__ = (
    "encrypt",
    "decrypt",
)


def encrypt(path: str | PathLike[str] | Path, /) -> bytes:
    if not isinstance(path, Path):
        path = Path(path)

    with path.open("rb") as fp:
        data_to_encrypt = fp.read()

    # Generate a random IV (Initialization Vector)
    init_vector = Random.new().read(16)

    # Derive the key using PBKDF2 with SHA1 hash algorithm
    key = PBKDF2(CRYPTO_PASSWORD, init_vector, dkLen=16, count=100)

    # Create AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, init_vector)  # type: ignore # the upstream types aren't great

    # Pad the data with PKCS7 before encryption
    padded_data = pad(data_to_encrypt, AES.block_size, style="pkcs7")

    # Encrypt the data
    encrypted_data = init_vector + cipher.encrypt(padded_data)

    return encrypted_data


def decrypt(path: str | PathLike[str] | Path, /) -> Any:  # it returns the type of file we decrypt but alas
    if not isinstance(path, Path):
        path = Path(path)

    with path.open("rb") as fp:
        read_data = fp.read()

    # The initialisation vector is the first 16 bytes of the save file.
    init_vector = read_data[:16]
    # then we take the proceeding N bytes as the data
    _to_decrypt = read_data[16:]

    # create the decryption key from the provided data
    decryption_key = PBKDF2(CRYPTO_PASSWORD, init_vector, dkLen=16, count=100)

    # with the key we create the needed cipher
    cipher = AES.new(decryption_key, AES.MODE_CBC, init_vector)  # type: ignore # the upstream types aren't great

    # and now we decrypt the data
    decrypted_data = unpad(cipher.decrypt(_to_decrypt), AES.block_size, style="pkcs7")

    # and it's always UTF-8
    resolved_data = decrypted_data.decode("utf-8")

    return _from_json(resolved_data)
