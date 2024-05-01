from abc import ABCMeta, abstractmethod
from typing import Any, NamedTuple


class ImageUploadInput(NamedTuple):
    image: bytes
    bucket_name: str
    image_name_on_bucket: str


class ImageUploadOutput(NamedTuple):
    image_uri: str


class BucketUploader(metaclass=ABCMeta):
    @abstractmethod
    async def upload(self, port: ImageUploadInput) -> ImageUploadOutput: ...


class BucketProvider(metaclass=ABCMeta):
    @abstractmethod
    async def __aenter__(self) -> BucketUploader: ...

    @abstractmethod
    async def __aexit__(self, *_: Any) -> None: ...
