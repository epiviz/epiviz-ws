from fastapi import HTTPException, Request, Header, status
from fastapi.security.utils import get_authorization_scheme_param

from app.models import User

from typing import List, Optional
from pydantic import BaseModel

import requests
from jose import jwt, jwk
from jose.utils import base64url_decode

import time

# From sebastian's documentation on KeyCloak and Authentication
# cache certificates from Keycload, so we don't query Keycloak for each token
# verification.
CERTS = {}

def get_public_key_data(kid):
    global CERTS
    key_data = CERTS.get(kid)
    if not key_data:
        # the URL comes from "jwks_uri" in the .well-known endpoint
        # https://restst.gene.com/auth/realms/gene/.well-known/openid-configuration
        certs_uri = "http://restst.gene.com/auth/realms/gene/protocol/openid-connect/certs"
        response = requests.get(certs_uri)
        assert response.status_code == 200
        result = response.json()
        for data in result["keys"]:
            CERTS[data["kid"]] = data
        # now it should work
        key_data = CERTS.get(kid)
        assert key_data, "Couldn't find kid %s" % kid
    
    return key_data

def is_token_valid(token:str):
    # print("in is token valid")
    # print(token)
    global CERTS
    # get the kid from the headers prior to verification
    headers = jwt.get_unverified_headers(token)

    kid = headers['kid']
    # use that kid to get the public key from keycloak
    key_data = get_public_key_data(kid)

    # construct the public key
    public_key = jwk.construct(key_data)

    # get the last two sections of the token,
    # message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit('.', 1)

    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))

    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        raise HTTPException(
            status_code=400,
            detail="Invalid token, {}".format("failed signature"),
            headers={"WWW-Authenticate": "Bearer"},
        )        

    # since we passed the verification, we can now safely
    # use the unverified claims
    claims = jwt.get_unverified_claims(token)
    # print(claims)

    # additionally we can verify the token expiration
    if time.time() > claims['exp']:  # time() returns epoch (UTC)
        print('Token has expired')

    return User(username=claims.get("preferred_username"), 
                    email=claims.get("email"), 
                    full_name=claims.get("name"))

def get_user_from_header(*, authorization: str = Header(None)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    scheme, token = get_authorization_scheme_param(authorization)

    if scheme.lower() != "bearer":
        raise credentials_exception

    try:
        tokenuser = is_token_valid(token)
        return tokenuser
    except Exception as e:
        raise credentials_exception