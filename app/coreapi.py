# CORE_ENDPOINT: Url of the CORE API server your connecting to. Must not have a trailing '/', usually points to /api on the deployed domain
# CORE_APP_ID: The ID of your registered application on the application management page in Core
# CORE_PRIVATE_KEY: Your applications Private ECDSA Key as generated in the check_app(app) function
# CORE_CORE_PUBLIC_KEY: The Core API server's Public ECDSA Key, printed in HEX on the application management page.

import textwrap

from binascii import unhexlify
from hashlib import sha256

from ecdsa.keys import SigningKey, VerifyingKey
from ecdsa.curves import NIST256p

from braveapi.client import API

class CoreAPI:
    required_config_variables_ = ['CORE_ENDPOINT', 'CORE_APP_ID', 'CORE_PRIVATE_KEY', \
        'CORE_CORE_PUBLIC_KEY', 'CORE_VIEW_PERMISSION', 'CORE_EDIT_PERMISSION']
    
    def __init__(self, app):
        self.endpoint = app.config['CORE_ENDPOINT']
        self.app_id = app.config['CORE_APP_ID']
        self.private_key_string = app.config['CORE_PRIVATE_KEY']
        self.core_public_key_string = app.config['CORE_CORE_PUBLIC_KEY']
        
        self.private_key = SigningKey.from_string(unhexlify(self.private_key_string), curve=NIST256p, hashfunc=sha256)
        self.core_public_key = VerifyingKey.from_string(unhexlify(self.core_public_key_string), curve=NIST256p, hashfunc=sha256)
        
        self.view_perm = app.config['CORE_VIEW_PERMISSION']
        self.edit_perm = app.config['CORE_EDIT_PERMISSION']

    @staticmethod
    def check_app(app):
        try:
            for var in CoreAPI.required_config_variables_:
                app.config[var]
        except KeyError as e:
            private = SigningKey.generate(NIST256p, hashfunc=sha256)

            error_message =  "\n================================================================================\n"

            error_message += "Core Service API identity, public, or private key missing.\n\n"

            error_message += "Here's a new private key; update the api.private setting to reflect this.\n" + \
                             "%s \n\n" % private.to_string().encode('hex')

            error_message += "Here's that key's public key; this is what you register with Core.\n" + \
                             "%s \n\n" % private.get_verifying_key().to_string().encode('hex')

            error_message += textwrap.fill("After registering, make sure to populate all of the following in config.py: {0}" \
                                 .format(", ".join(CoreAPI.required_config_variables_)))
                             
            error_message += "\n================================================================================\n\n"
        
            print error_message
            raise
    
    def get_api(self):
        return API(self.endpoint, self.app_id, self.private_key, self.core_public_key)
        
    def get_session(self, token):
        info = self.get_api().core.info(token=token)
        return CoreSession(self, info)
            
    def check_logged_in(self):
        return
        
    
class CoreSession:
    def __init__(self, coreapi, info):
        self.info = info
        self.coreapi = coreapi
        
    def has_perm(self, perm):
        return perm in self.info.perms

    def has_view_perm(self):
        return self.has_perm(self.coreapi.view_perm)
        
    def has_edit_perm(self):
        return self.has_perm(self.coreapi.edit_perm)
        
    def get_user(self):
        alliance = None
        if 'alliance' in self.info:
            alliance = self.info.alliance.name
        return User(self.info.character.name,
                    self.info.corporation.name,
                    alliance)

class User:
    def __init__(self, character, corporation, alliance):
        self.character = character
        self.corporation = corporation
        self.alliance = alliance
