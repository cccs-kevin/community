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

class ApiHammering(Signature):
    name = "api_hammering"
    description = "Makes an unusually high volume of API calls, possibly in the attempt to crash the sandbox."
    severity = 1
    categories = ["anti-sandbox"]
    minimum = "2.0"
    ttp = ["T1106", "T1497"]

    def on_complete(self):
        apistats = self.get_results("behavior", {}).get("apistats", {})
        for pid in apistats:
            process_apistats = apistats[pid]
            for api_call in process_apistats:
                process_api_call_count = process_apistats[api_call]
                if process_api_call_count > 10000:
                    description = "Process %s made the call %s %d times" % (pid, api_call, process_api_call_count)
                    self.mark(description=description)
        return self.has_marks()

