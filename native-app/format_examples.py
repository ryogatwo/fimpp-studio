"""Indent bundled letters without changing their statements or string contents."""
import re


def indent_letter(source):
    depth = 0
    quoted = False
    result = []
    for raw in source.splitlines():
        line = raw.lstrip()
        # Leading whitespace on a continuation of a literal is program data.
        if quoted:
            result.append(raw)
        elif not line:
            result.append('')
        else:
            lower = line.lower()
            if lower.startswith(('dear princess', 'your faithful student', "that's about")):
                depth = 0
            elif lower.startswith(('i learned', 'today i learned')):
                depth = 0
            elif lower.startswith(("that's what i did", 'in the end, i did this instead', "it didn't work, but i knew why")):
                depth = max(0, depth - 1)
            result.append('    ' * depth + line)
            if lower.startswith(('i learned', 'today i learned', 'when ', 'in the end, i did this instead', "it didn't work, but i knew why")) or re.match(r'i did this(?:\s|[.!:])', lower):
                depth += 1
        # The bundled examples use paired straight quotes, with no escape syntax.
        if raw.count('"') % 2:
            quoted = not quoted
    return '\n'.join(result) + '\n'
