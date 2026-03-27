from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile

from app.core.config import settings


def _guess_extension(filename: str) -> str:
    if "." in filename:
        return filename.rsplit(".", 1)[-1].lower()
    return "bin"


def _save_local(upload: UploadFile) -> tuple[str, int]:
    target_dir = Path(settings.local_storage_path).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    extension = _guess_extension(upload.filename or "file.bin")
    stored_name = f"{uuid4().hex}.{extension}"
    target_path = target_dir / stored_name

    raw = upload.file.read()
    target_path.write_bytes(raw)
    return str(target_path), len(raw)


def _save_s3(upload: UploadFile) -> tuple[str, str, int]:
    if not settings.s3_bucket_name:
        raise HTTPException(status_code=500, detail="S3 bucket is not configured")

    try:
        import boto3
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail="boto3 is required for S3 storage") from exc

    extension = _guess_extension(upload.filename or "file.bin")
    key = f"documents/{uuid4().hex}.{extension}"
    raw = upload.file.read()

    client = boto3.client(
        "s3",
        region_name=settings.s3_region,
        endpoint_url=settings.s3_endpoint_url,
        aws_access_key_id=settings.s3_access_key_id,
        aws_secret_access_key=settings.s3_secret_access_key,
    )
    client.put_object(
        Bucket=settings.s3_bucket_name,
        Key=key,
        Body=raw,
        ContentType=upload.content_type or "application/octet-stream",
    )

    if settings.s3_endpoint_url:
        base = settings.s3_endpoint_url.rstrip("/")
        url = f"{base}/{settings.s3_bucket_name}/{key}"
    else:
        url = f"s3://{settings.s3_bucket_name}/{key}"
    return key, url, len(raw)


def save_upload(upload: UploadFile) -> dict[str, str | int]:
    backend = settings.storage_backend.lower()
    if backend == "s3":
        stored_name, url, size_bytes = _save_s3(upload)
        return {
            "storage_backend": "s3",
            "stored_name": stored_name,
            "file_url": url,
            "size_bytes": size_bytes,
        }

    path, size_bytes = _save_local(upload)
    return {
        "storage_backend": "local",
        "stored_name": Path(path).name,
        "file_url": path,
        "size_bytes": size_bytes,
    }
