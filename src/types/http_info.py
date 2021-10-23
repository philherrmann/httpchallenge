from dataclasses import dataclass


@dataclass(frozen=True)
class HTTPInfo:

    method: str  # make it an enum
    host: str
    path: str
    content_length: int

    def extract_section(self):
        return self.host + self.path.rsplit('/', 1)[0]
