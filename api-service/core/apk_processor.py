import subprocess
import os
from pathlib import Path
import xml.etree.ElementTree as ET


KEYSTORE_PASS = os.environ.get("KEYSTORE_PASS", "changeit")
KEY_ALIAS = os.environ.get("KEY_ALIAS", "mobile-morpher")


class APKProcessor:
    def __init__(self, work_dir: Path):
        self.work_dir = work_dir
        self.apk_path = work_dir / "original.apk"
        self.decompiled_dir = work_dir / "decompiled"

    def decompile(self):
        subprocess.run(
            ["apktool", "d", "-f", str(self.apk_path), "-o", str(self.decompiled_dir)],
            check=True, capture_output=True, text=True,
        )

    def get_package_name(self) -> str:
        manifest_path = self.decompiled_dir / "AndroidManifest.xml"
        if not manifest_path.exists():
            raise FileNotFoundError(f"AndroidManifest.xml not found at {manifest_path}")

        tree = ET.parse(manifest_path)
        root = tree.getroot()
        package = root.get("package")

        if not package:
            raise ValueError("Package name not found in AndroidManifest.xml")
        return package

    def get_app_name(self) -> str:
        manifest_path = self.decompiled_dir / "AndroidManifest.xml"
        if not manifest_path.exists():
            return "Unknown"

        tree = ET.parse(manifest_path)
        root = tree.getroot()

        app = root.find("application")
        if app is not None:
            label = app.get("{http://schemas.android.com/apk/res/android}label", "")
            if label.startswith("@string/"):
                string_name = label.split("/")[1]
                strings_path = self.decompiled_dir / "res" / "values" / "strings.xml"
                if strings_path.exists():
                    strings_tree = ET.parse(strings_path)
                    for string in strings_tree.findall("string"):
                        if string.get("name") == string_name:
                            return string.text or "Unknown"
        return "Unknown"

    def rebuild(self):
        output_apk = self.work_dir / "modified.apk"
        subprocess.run(
            ["apktool", "b", str(self.decompiled_dir), "-o", str(output_apk)],
            check=True, capture_output=True, text=True,
        )

    def sign(self, package_id: str = None):
        apk_path = self.work_dir / "modified.apk"
        keystore = self.work_dir / "keystore.jks"

        if not keystore.exists():
            self._generate_keystore(keystore, package_id)

        subprocess.run(
            [
                "apksigner", "sign",
                "--ks", str(keystore),
                "--ks-key-alias", KEY_ALIAS,
                "--ks-pass", f"pass:{KEYSTORE_PASS}",
                "--v2-signing-enabled", "true",
                "--v3-signing-enabled", "true",
                str(apk_path),
            ],
            check=True, capture_output=True, text=True,
        )

    def _generate_keystore(self, keystore_path: Path, package_id: str = None):
        cn_name = package_id or "MobileMorpher"
        subprocess.run(
            [
                "keytool", "-genkeypair", "-v",
                "-keystore", str(keystore_path),
                "-alias", KEY_ALIAS,
                "-keyalg", "RSA",
                "-keysize", "2048",
                "-validity", "10000",
                "-storepass", KEYSTORE_PASS,
                "-keypass", KEYSTORE_PASS,
                "-dname", f"CN={cn_name}, OU=Development, O=MobileMorpher, L=Unknown, ST=Unknown, C=US",
            ],
            check=True, capture_output=True, text=True,
        )
