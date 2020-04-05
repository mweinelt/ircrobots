from asyncio import Future
from typing  import Awaitable, Iterable, List, Optional, Set, Tuple
from enum    import IntEnum

from ircstates import Server, Emit
from irctokens import Line

from .params   import ConnectionParams, SASLParams

class SendPriority(IntEnum):
    HIGH   = 0
    MEDIUM = 10
    LOW    = 20
    DEFAULT = MEDIUM

class SentLine(object):
    def __init__(self, priority: int, line: Line):
        self.priority       = priority
        self.line           = line
        self.future: Future = Future()
    def __lt__(self, other: "SentLine") -> bool:
        return self.priority < other.priority

class ICapability(object):
    def available(self, capabilities: Iterable[str]) -> Optional[str]:
        pass

    def match(self, capability: str) -> Optional[str]:
        pass

    def copy(self) -> "ICapability":
        pass

class IMatchResponse(object):
    def match(self, server: "IServer", line: Line) -> bool:
        pass
class IMatchResponseParam(object):
    def match(self, server: "IServer", arg: str) -> bool:
        pass

class IServer(Server):
    params:       ConnectionParams
    desired_caps: Set[ICapability]

    async def send_raw(self, line: str, priority=SendPriority.DEFAULT):
        pass
    async def send(self, line: Line, priority=SendPriority.DEFAULT):
        pass

    def wait_for(self, response: IMatchResponse) -> Awaitable[Line]:
        pass

    def set_throttle(self, rate: int, time: float):
        pass

    async def connect(self, params: ConnectionParams):
        pass

    async def line_read(self, line: Line):
        pass
    async def line_send(self, line: Line):
        pass

    async def next_line(self) -> Tuple[Line, List[Emit]]:
        pass

    def cap_agreed(self, capability: ICapability) -> bool:
        pass
    def cap_available(self, capability: ICapability) -> Optional[str]:
        pass

    async def sasl_auth(self, sasl: SASLParams) -> bool:
        pass
