class Post:
    def __init__(self, dic):
        self.id = dic["id"] if "id" in dic else None
        self.caption = dic["caption"] if "caption" in dic else None
        self.media_url = dic["media_url"] if "media_url" in dic else None
        self.media_type = dic["media_type"] if "media_type" in dic else None
