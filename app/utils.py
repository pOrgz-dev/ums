# -*- encoding: utf-8 -*-

import time
import hashlib

from app import (
    # for info block logging
    __version__,
    PROJECT_ENVIRON
)

class ResponseFormatter(object):
    """Format any CRUD Operation to a Standard API Response"""

    def get_small_message(self, code : int) -> str:
        """Define Status Codes for API Response"""

        return {
            200 : "OK",
            201 : "Created",
            204 : "No Content",
            400 : "Bad Request",
            401 : "Unauthorized",
            403 : "Forbidden",
            404 : "Not Found",
            500 : "Internal Server Error"
        }.get(code, 502) # 502 > Bad Gateway
    

    def get_code_category(self, code : int) -> str:
        """Get the High-Level Category for a Status Code"""

        code_ = int(str(code)[0]) # get first digit of status code
        return {
            1 : "informational",
            2 : "success",
            3 : "redirection",
            4 : "client error",
            5 : "server error"
        }.get(code_, "NONE: UNDEFINED: API Utility Error")
    

    def _message_defination_(self, code : int, err : str, msg_desc : str, request_type : str = "get") -> dict:
        """
        The Message Format for any Outbound APIs

        The core structure of message is defined here, such that any
        of the outbound function calls can be controlled using one
        single type of message, and thus all the message have a same
        type of "JSON" structure.

        Additional information specific to a message, like `data`
        block in a `get` request etc. are appended in their
        respective function and the structure is updated accordingly.
        """

        return {
            "status" : {
                # provide general information about request
                "code" : code, # https://www.restapitutorial.com/httpstatuscodes.html
                "desc" : {
                    # provide information about `code`
                    "category" : self.get_code_category(code), # provide type of response
                    "information" : self.get_small_message(code) # code reference message
                },

                # the next two is an optional block for error message
                "error" : str(err) if err else err, # this error can be logged
                "message" : msg_desc # long message description (for UI/UX)
            },

            "info" : {
                # provide information about api, call request
                # this block can be typically used for logging and dev-ops
                "api_version" : __version__,
                "project_env" : PROJECT_ENVIRON,

                "request_summary" : {
                    # summarizes the request information
                    "type" : request_type,
                    "time" : time.ctime()
                }
            }
        }


    def get(self, data : list, err : str = None, code : int = 200, msg_desc : str = None) -> dict:
        """Format O/P of all GET Response"""

        return self._message_defination_(code, err, msg_desc) | {"data" : data}


    def post(self, data : list, err : str = None, code : int = 200, msg_desc : str = None) -> dict:
        """Format O/P of all GET Response"""

        return self._message_defination_(code, err, msg_desc, request_type = "post")

def encrypt_password(password : str) -> str:
    """
    Encrypt a RAW Password using `hashlib` Module

    Currently, the function encrypts the password as a
    `hashlib.sha512` string and is stored into database.

    TODO: Create a methodology of using "salting" method
    """

    return hashlib.sha512(password.encode()).hexdigest()


def validate_password(password : str, encoded_password : str) -> bool:
    """
    Validates an Encrypted SHA-512 Password String

    SHA-512 encoded string is created and returns <bool> upon
    password validation.
    """

    password = hashlib.sha512(password.encode()).hexdigest()
    return password == encoded_password
