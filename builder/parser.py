def parse_docksmithfile(context):

    instructions = []

    path = context + "/Docksmithfile"

    with open(path) as f:

        for line in f:

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split(" ",1)

            instruction = parts[0]
            argument = parts[1] if len(parts) > 1 else ""

            instructions.append((instruction,argument))

    return instructions
