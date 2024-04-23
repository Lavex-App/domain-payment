from typing import TypedDict

import aiofiles
import aiohttp
from gcloud.aio.storage import Storage

from domain_payment.adapters.interface_adapters.interfaces import (
    BucketProvider,
    BucketUploader,
    ImageUploadInput,
    ImageUploadOutput,
)


class GCPStorageFrameworkConfig(TypedDict):
    storage_credentials: str | None


class GCPStorageManager(BucketProvider, BucketUploader):
    def __init__(self, config: GCPStorageFrameworkConfig, session: aiohttp.ClientSession) -> None:
        self.__credentials = config.get("storage_credentials")
        self.__session = session
        self.__client = None

    async def __aenter__(self) -> BucketUploader:
        self.__client = self.__create_app(self.__session)
        return self

    async def __aexit__(self, *_) -> None: ...

    async def upload(self, port: ImageUploadInput) -> ImageUploadOutput:
        async with aiofiles.open(port.path2image, mode="rb") as f:
            output = await f.read()
            result = await self.__client.upload(port.bucket_name, port.image_name_on_bucket, output)
            return ImageUploadOutput(image_uri=result["selfLink"])

    def __create_app(self, session: aiohttp.ClientSession) -> Storage:
        if self.__credentials is not None:
            return Storage(session=session, service_file=self.__credentials)
        return Storage(session=session)
