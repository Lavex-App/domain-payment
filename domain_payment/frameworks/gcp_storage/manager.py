import sys
from pathlib import Path
from typing import TypedDict

import aiofiles
import aiohttp
from gcloud.aio.storage import Storage
from gcloud.aio.storage.blob import Blob
from gcloud.aio.storage.bucket import Bucket

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
            bucket = Bucket(self.__client, port.bucket_name)
            bucket_metadata = await bucket.get_metadata(session=self.__session)
            bucket_metadata["size"] = sys.getsizeof(output)
            blob = Blob(bucket, port.image_name_on_bucket, bucket_metadata)
            upload_metadata = await blob.upload(output, session=self.__session)
            signed_image_uri = await Blob(
                bucket,
                port.image_name_on_bucket,
                upload_metadata,
            ).get_signed_url(
                1800,
                session=self.__session,
            )
        Path(port.path2image).unlink(missing_ok=True)
        return ImageUploadOutput(image_uri=signed_image_uri)

    def __create_app(self, session: aiohttp.ClientSession) -> Storage:
        if self.__credentials is not None:
            return Storage(session=session, service_file=self.__credentials)
        return Storage(session=session)
