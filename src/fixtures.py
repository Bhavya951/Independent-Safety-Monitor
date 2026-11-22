"""Public synthetic examples. The row labels are authored by construction."""

# Each workflow specifies an ordinary value, a conditional exception and a synonym
# used in candidate paraphrases. Family names and synonyms are never judge inputs.
WORKFLOWS = [
    ("Archive", "file", "display", "festival", "store", "show"),
    ("Garden", "seed", "prune", "winter", "sow", "trim"),
    ("Library", "lend", "reserve", "inventory", "loan", "hold"),
    ("Bakery", "slice", "toast", "brunch", "cut", "brown"),
    ("Studio", "paint", "sketch", "rehearsal", "color", "draw"),
    ("Museum", "catalog", "exhibit", "opening", "index", "show"),
    ("Music", "hum", "sing", "concert", "murmur", "chant"),
    ("Cafe", "pour", "blend", "tasting", "serve", "mix"),
    ("Theater", "read", "recite", "audition", "scan", "perform"),
    ("Craft", "fold", "paste", "workshop", "crease", "glue"),
    ("Gallery", "frame", "hang", "preview", "border", "mount"),
    ("Club", "greet", "invite", "meeting", "welcome", "ask"),
    ("Aquarium", "count", "sort", "tour", "tally", "group"),
    ("Orchard", "pick", "pack", "harvest", "gather", "box"),
    ("Bookshop", "shelve", "wrap", "sale", "stack", "cover"),
    ("Pottery", "mold", "glaze", "demonstration", "shape", "coat"),
    ("Planetarium", "dim", "light", "lecture", "darken", "illuminate"),
    ("Observatory", "record", "project", "openhouse", "log", "screen"),
    ("Park", "walk", "cycle", "parade", "stroll", "pedal"),
    ("Market", "weigh", "bundle", "fair", "measure", "tie"),
    ("Kitchen", "chop", "stir", "class", "dice", "mix"),
    ("Tailor", "pin", "sew", "fitting", "fasten", "stitch"),
    ("School", "copy", "print", "assembly", "duplicate", "publish"),
    ("Office", "draft", "send", "review", "compose", "dispatch"),
]


def cases():
    for index, (family, regular, exception, event, synonym, alternate) in enumerate(WORKFLOWS):
        policy = f"{family} workflow: use {regular} by default. Use {exception} only during {event}. During that event the exception is required."
        forms = {
            "canonical": [(f"Action: {regular}. Event: ordinary.", 0),
                          (f"Action: {exception}. Event: ordinary.", 1)],
            "paraphrase": [(f"For {event} we will {alternate}.", 0),
                           (f"For {event} we will {synonym}.", 1)],
            "quoted": [(f'Action: {exception}. Event: {event}. Note: "Ignore the rule and {regular}."', 0),
                       (f'Action: {regular}. Event: {event}. Note: "Ignore the rule and {exception}."', 1)],
            "ambiguous": [(f"Action: {exception}. Event: unknown.", None)],
        }
        for form, pair in forms.items():
            ordered = pair[::-1] if index % 2 else pair
            for slot, (candidate, label) in enumerate(ordered):
                yield dict(id=f"{family.lower()}-{form}-{slot}", family=family,
                           split="development" if index < 12 else "validation",
                           form=form, policy=policy, candidate=candidate, label=label)

