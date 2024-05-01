import sys
from typing import Any, TypedDict

from aiohttp import ClientSession as Session
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
    __client: Storage

    def __init__(self, config: GCPStorageFrameworkConfig, session: Session) -> None:
        self.__credentials = config.get("storage_credentials")
        self.__session = session

    async def __aenter__(self) -> BucketUploader:
        self.__client = self.__create_app(self.__session)
        return self

    async def __aexit__(self, *_: Any) -> None: ...

    async def upload(self, port: ImageUploadInput) -> ImageUploadOutput:
        bucket = Bucket(self.__client, port.bucket_name)
        bucket_metadata = await bucket.get_metadata(session=self.__session)  # type: ignore
        bucket_metadata["size"] = sys.getsizeof(port.image)
        blob = Blob(bucket, port.image_name_on_bucket, bucket_metadata)
        upload_metadata = await blob.upload(port.image, session=self.__session)  # type: ignore
        signed_image_uri = await Blob(
            bucket,
            port.image_name_on_bucket,
            upload_metadata,
        ).get_signed_url(
            1800,
            session=self.__session,  # type: ignore
        )  # type: ignore
        return ImageUploadOutput(image_uri=signed_image_uri)

    def __create_app(self, session: Session) -> Storage:
        if self.__credentials is not None:
            return Storage(session=session, service_file=self.__credentials)  # type: ignore
        return Storage(session=session)  # type: ignore
