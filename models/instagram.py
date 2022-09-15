from dateutil import parser


class Post:
    def __init__(self, dic):
        self.id = dic["id"] if "id" in dic else None
        self.caption = dic["caption"] if "caption" in dic else None
        self.media_url = dic["media_url"] if "media_url" in dic else None
        self.media_type = dic["media_type"] if "media_type" in dic else None
        self.timestamp = dic["timestamp"] if "timestamp" in dic else None

    def get_offset_naive_timestamp(self):
        return parser.parse(self.timestamp).replace(tzinfo=None)


class Cursors:
    def __init__(self, dic):
        self.before = dic["before"] if "before" in dic else None
        self.after = dic["after"] if "after" in dic else None

    def __str__(self):
        return f"before: {self.before}, after: {self.after}"

    def has_next(self):
        return self.after is not None


class Paging:
    def __init__(self, dic):
        self.cursors = Cursors(dic["cursors"]) if "cursors" in dic else None
        self.next = dic["next"] if "next" in dic else None
        self.previous = dic["previous"] if "previous" in dic else None

    def __str__(self):
        return f"cursors: {self.cursors}, next: {self.next}, previous: {self.previous}"

    def has_next_cursor(self):
        return self.cursors.has_next()
