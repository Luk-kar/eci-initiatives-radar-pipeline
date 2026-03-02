def wrap_card(inner_html: str, extra_class: str = "") -> str:
    cls = f"card {extra_class}".strip()
    return f'''<div class="{cls}">\n{inner_html}\n</div>'''
