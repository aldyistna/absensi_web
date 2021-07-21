from app import bucket_app


def upload_file(dest, path):
    blob = bucket_app.blob(dest)
    blob.upload_from_filename(path)
    blob.make_public()

    return blob.public_url
