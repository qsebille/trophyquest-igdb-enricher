def get_image_url(image_id: str, size: str = "t_cover_big") -> str:
    return f"https://images.igdb.com/igdb/image/upload/{size}/{image_id}.jpg"
