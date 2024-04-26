from certbot import interfaces
from certbot.plugins import common
from certbot.compat import os
from certbot import errors

import shutil

from typing import Any
from typing import Callable
from typing import Iterable
from typing import List
from typing import Optional
from typing import Union

class CopyInstaller(common.Plugin, interfaces.Installer):

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

    def prepare(self) -> None:
        pass

    def more_info(self) -> str:
        return ('Install certificates by copying them to a directory. '
               'This may be useful for exporting the certificate file '
               'contents is desired, not just the "live" directory '
               'whose contents are symlinks to other files.')

    def get_all_names(self) -> Iterable[str]:
        return []

    def deploy_cert(self, domain: str, cert_path: str, key_path: str,
            chain_path: str, fullchain_path: str) -> None:
        destination = self.conf('destination')

        for source_symlink in [cert_path, key_path, chain_path, fullchain_path]:
            source_filename = os.path.basename(source_symlink)
            source_realpath = os.path.realpath(source_symlink)
            dest_path = os.path.join(destination, source_filename)
            shutil.copy2(source_realpath, dest_path)

    def enhance(self, domain: str, enhancement: str, 
                options: Optional[Union[List[str], str]] = None) -> None:
        pass

    def supported_enhancements(self) -> List[str]:
        return []

    def save(self, title: Optional[str] = None,
             temporary: bool = False) -> None:
        pass

    def rollback_checkpoints(self, rollback: int = 1) -> None:
        pass

    def recovery_routine(self) -> None:
        pass

    def config_test(self) -> None:
        destination = self.conf('destination')
        if not os.path.isdir(destination):
            raise errors.MisconfigurationError(
                f'Destination "{destination}" does not exist.')

    def restart(self) -> None:
        pass
