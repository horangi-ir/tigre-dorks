headers = {
    "user-agent": "Horangi OSINT"
}


def is_match(_filter, text, url):
    for f in _filter:
        if any([
            (f[0] == "url" and f[1] in url),
            (f[0] == "file" and url.lower().endswith(f[1])),
            (f[0] == "summary" and f[1] == text[:len(f[1])])
        ]):
            return True
    return False


def get_unique(obj, items):
    hashes = [
        hash(frozenset(x.items())) for x in obj
    ]

    for i in reversed(range(len(items))):
        if hash(frozenset(items[i].items())) in hashes:
            items.pop(i)

    return items
