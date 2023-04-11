from certbot import interfaces
from certbot.plugins import common
from certbot.compat import os
from certbot import errors

from typing import Any
from typing import Callable

import shutil

class Installer(common.Plugin, interfaces.Installer):

    description = ('Install certificates by copying them to a specified '
                   'directory. Copies whole file contents, not just '
                   'symbolic links')

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.target_dir = None 

    @classmethod
    def add_parser_arguments(cls, add: Callable[..., None]) -> None:
        super().add_parser_arguments(add)
        add('destination', help='Destination directory for certificates')

    def more_info(self) -> str:
        return ('Install certificates by copying them to a directory. '
               'This may be useful for exporting the certificate file '
               'contents is desired, not just the "live" directory '
               'whose contents are symlinks to other files.')

    def config_test(self) -> None:
        destination = self.conf('destination')
        if not os.path.isdir(destination):
            raise errors.MisconfigurationError(
                f'Destination "{destination}" does not exist.')

    def deploy_cert(self, domain: str, cert_path: str, key_path: str,
            chain_path: str, fullchain_path: str) -> None:
        destination = self.conf('destination')

        for source in [cert_path, key_path, chain_path, fullchain_path]:
            source_filename = os.path.basename(source)
            dest_path = os.path.join(destination, source_filename)
            shutil.copy2(cert_path, dest_path)
