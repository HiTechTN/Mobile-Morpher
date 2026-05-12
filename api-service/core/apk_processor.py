import subprocess
import os
from pathlib import Path
import xml.etree.ElementTree as ET

class APKProcessor:
    def __init__(self, work_dir: str):
        self.work_dir = Path(work_dir)
        self.apk_path = self.work_dir / "original.apk"
        self.decompiled_dir = self.work_dir / "decompiled"
        
    def decompile(self):
        cmd = [
            "apktool",
            "d",
            "-f",
            str(self.apk_path),
            "-o",
            str(self.decompiled_dir)
        ]
        subprocess.run(cmd, check=True)
        
    def get_package_name(self) -> str:
        manifest_path = self.decompiled_dir / "AndroidManifest.xml"
        if not manifest_path.exists():
            raise FileNotFoundError("AndroidManifest.xml not found")
            
        tree = ET.parse(manifest_path)
        root = tree.getroot()
        package = root.get("package")
        
        if not package:
            raise ValueError("Package name not found in manifest")
        return package
    
    def get_app_name(self) -> str:
        manifest_path = self.decompiled_dir / "AndroidManifest.xml"
        tree = ET.parse(manifest_path)
        root = tree.getroot()
        
        app = root.find("application")
        if app is not None:
            label = app.get("{http://schemas.android.com/apk/res/android}label")
            if label and label.startswith("@string/"):
                string_name = label.split("/")[1]
                strings_path = self.decompiled_dir / "res" / "values" / "strings.xml"
                if strings_path.exists():
                    strings_tree = ET.parse(strings_path)
                    for string in strings_tree.findall("string"):
                        if string.get("name") == string_name:
                            return string.text
        return "Unknown"
    
    def rebuild(self):
        output_apk = self.work_dir / "modified.apk"
        cmd = [
            "apktool",
            "b",
            str(self.decompiled_dir),
            "-o",
            str(output_apk)
        ]
        subprocess.run(cmd, check=True)
        
    def sign(self, package_id: str = None):
        apk_path = self.work_dir / "modified.apk"
        keystore = self.work_dir / "keystore.jks"
        
        if not keystore.exists():
            self._generate_keystore(keystore, package_id)
        
        # Sign with both v2 and v3 for better compatibility
        cmd = [
            "apksigner",
            "sign",
            "--ks", str(keystore),
            "--ks-key-alias", "mobile-morpher",
            "--ks-pass", "pass:changeit",
            "--v2-signing-enabled", "true",
            "--v3-signing-enabled", "true",
            str(apk_path)
        ]
        subprocess.run(cmd, check=True)
    
    def _generate_keystore(self, keystore_path: Path, package_id: str = None):
        # Use package ID in the certificate for better identification
        cn_name = package_id.split('.')[-1] if package_id else "MobileMorpher"
        cmd = [
            "keytool",
            "-genkeypair",
            "-v",
            "-keystore", str(keystore_path),
            "-alias", "mobile-morpher",
            "-keyalg", "RSA",
            "-keysize", "4096",  # Use stronger key
            "-validity", "10000",
            "-storepass", "changeit",
            "-keypass", "changeit",
            "-dname", f"CN={cn_name}, OU=Development, O=MobileMorpher, L=Unknown, ST=Unknown, C=US",
            "-ext", "SAN=dns:{cn_name}"
        ]
        subprocess.run(cmd, check=True)
