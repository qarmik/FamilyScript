import re
from pprint import pprint


class FamilyScriptLexer:
    def __init__(self):
        self.symbols = {}  # Track declared variables

    def canonical_name(self, name):
        """
        Convert:
        Tommy's allowance → tommy_allowance
        The total → total
        """
        name = name.lower()
        name = name.replace("'s", "")
        name = name.replace("the ", "")
        name = name.replace(" ", "_")
        return name.strip()

    def parse_line(self, line):
        line = line.strip()

        if not line:
            return None

        # 1️⃣ Variable Declaration
        match = re.match(r"(.+?) is (.+)", line)
        if match and "If " not in line:
            left = match.group(1)
            right = match.group(2)

            canonical = self.canonical_name(left)
            self.symbols[canonical] = True

            return {
                "type": "assign",
                "target": canonical,
                "value": right
            }

        # 2️⃣ Add to variable
        match = re.match(r"Add (.+?) to (.+)", line)
        if match:
            value = match.group(1)
            target = self.canonical_name(match.group(2))

            return {
                "type": "increment",
                "target": target,
                "value": value
            }

        # 3️⃣ For Each Loop
        match = re.match(r"For each (.+?) in (.+):", line)
        if match:
            item = match.group(1)
            list_name = self.canonical_name(match.group(2))

            return {
                "type": "loop_each",
                "item": item,
                "list": list_name
            }

        # 4️⃣ If Condition (basic > comparison)
        match = re.match(r"If (.+?) is more than (.+):", line)
        if match:
            left = self.canonical_name(match.group(1))
            right = match.group(2)

            return {
                "type": "if",
                "condition": {
                    "left": left,
                    "operator": ">",
                    "right": right
                }
            }

        # 5️⃣ Say Output
        match = re.match(r"Say:\s*\"(.+)\"", line)
        if match:
            message = match.group(1)
            return {
                "type": "output",
                "message": message
            }

        return {
            "type": "unknown",
            "raw": line
        }

    def parse_file(self, filename):
        results = []
        with open(filename, "r") as f:
            for line in f:
                parsed = self.parse_line(line)
                if parsed:
                    results.append(parsed)
        return results


if __name__ == "__main__":
    lexer = FamilyScriptLexer()
    result = lexer.parse_file("sample.fs")
    pprint(result)