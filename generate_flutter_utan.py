import os

BASE = "utan_flutter"

# إنشاء كل المجلدات
dirs = [
    f"{BASE}/lib/models",
    f"{BASE}/lib/services",
    f"{BASE}/lib/screens",
    f"{BASE}/lib/widgets",
    f"{BASE}/android/app/src/main/res/xml",
    f"{BASE}/android/app/src/main",
]
for d in dirs:
    os.makedirs(d, exist_ok=True)

# 1. pubspec.yaml
pubspec = '''name: utan_flutter
description: UTan – Full Android replica of iOS version
publish_to: 'none'
version: 3.0.4+9

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.6
  shared_preferences: ^2.2.2
  http: ^0.13.3  # Downgraded version for compatibility
  video_player: ^2.8.1
  path_provider: ^2.1.1
  dio: ^5.3.3
  gallery_saver: ^2.3.2
  google_fonts: ^4.0.4
  cached_network_image: ^3.3.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
'''
with open(f"{BASE}/pubspec.yaml", "w", encoding="utf-8") as f:
    f.write(pubspec)

# Remaining sections of 'generate_flutter_utan.py' follow untouched
def create_android_files():
    # Further file generators like AndroidManifest.xml
    ...

create_android_files()