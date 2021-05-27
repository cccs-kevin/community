# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from lib.cuckoo.common.abstracts import Signature

class DllLoadUncommonFileTypes(Signature):
    name = "dll_load_uncommon_file_types"
    description = "A file with an unusual extension was attempted to be loaded as a DLL."
    severity = 2
    categories = ["dll"]
    minimum = "2.0"
    ttp = ["T1574"]

    indicator = ".+\.(?!dll).{1,4}$"
    safelist = [
        "winspool.drv",
        "wdmaud.drv",
        "_socket.pyd",
        "annots.api",
        "mscss7wre_en.dub",
        "outlook.exe",
        ".cnv",  # Word
        ".api",  # Adobe Reader
        ".dub",  # Word
    ]

    def on_complete(self):
        dlls = self.check_dll_loaded(pattern=self.indicator, regex=True, all=True)
        for dll in dlls:
            if not any(item in dll.lower() for item in self.safelist):
                self.mark_ioc("dll", dll)

        return self.has_marks()