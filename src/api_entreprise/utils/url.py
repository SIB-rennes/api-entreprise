def join_fragments(*args):
    """Assemble plusieurs fragments d'url

    Returns:
        _type_: Une url assemblée
    """
    return "/".join(s.strip("/") for s in args)
