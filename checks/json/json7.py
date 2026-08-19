# checks/json/json7.py
assert settings["theme"] == "dark", f"Expected settings['theme'] to be 'dark', got {settings.get('theme')!r}"
assert encoded == '{"font_size": 12, "theme": "dark"}', f"Expected encoded JSON string '{{\"font_size\": 12, \"theme\": \"dark\"}}', got {encoded!r}"
print("json7 ok")
