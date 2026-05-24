def deduplicate(articles):
    seen = set()
    unique = []

    for a in articles:
        key = a.title.lower()

        if key not in seen:
            seen.add(key)
            unique.append(a)

    return unique