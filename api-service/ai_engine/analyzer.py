from pathlib import Path
import re
from typing import List, Dict


class AIAnalyzer:
    def __init__(self, work_dir: Path):
        self.work_dir = work_dir
        self.decompiled_dir = work_dir / "decompiled"

    def analyze(self) -> List[Dict]:
        suggestions = []
        suggestions.extend(self._analyze_ads())
        suggestions.extend(self._analyze_tracking())
        suggestions.extend(self._analyze_performance())
        suggestions.extend(self._analyze_permissions())
        return suggestions

    def _analyze_ads(self) -> List[Dict]:
        suggestions = []
        smali_dir = self.decompiled_dir / "smali"
        if not smali_dir.exists():
            return suggestions

        ad_patterns = [
            r'com/google/ads',
            r'com/facebook/ads',
            r'com/admob',
            r'Lcom/google/android/gms/ads',
        ]

        for smali_file in smali_dir.rglob("*.smali"):
            try:
                content = smali_file.read_text(encoding="utf-8")
            except Exception:
                continue
            for pattern in ad_patterns:
                if re.search(pattern, content):
                    suggestions.append({
                        "type": "ads",
                        "message": f"Publicité détectée dans {smali_file.name}",
                        "file": str(smali_file.relative_to(self.decompiled_dir)),
                        "action": "remove_ads",
                    })
                    break

        return suggestions

    def _analyze_tracking(self) -> List[Dict]:
        suggestions = []
        smali_dir = self.decompiled_dir / "smali"
        if not smali_dir.exists():
            return suggestions

        tracking_patterns = [
            r'Lcom/google/firebase/analytics',
            r'Lcom/facebook/appevents',
            r'Lcom/flurry/sdk',
            r'\.getDeviceId\(\)',
            r'\.getImei\(\)',
        ]

        for smali_file in smali_dir.rglob("*.smali"):
            try:
                content = smali_file.read_text(encoding="utf-8")
            except Exception:
                continue
            for pattern in tracking_patterns:
                if re.search(pattern, content):
                    suggestions.append({
                        "type": "tracking",
                        "message": f"Tracking détecté dans {smali_file.name}",
                        "file": str(smali_file.relative_to(self.decompiled_dir)),
                        "action": "remove_tracking",
                    })
                    break

        return suggestions

    def _analyze_performance(self) -> List[Dict]:
        suggestions = []
        manifest_path = self.decompiled_dir / "AndroidManifest.xml"
        if manifest_path.exists():
            try:
                content = manifest_path.read_text(encoding="utf-8")
                if 'android:hardwareAccelerated="false"' in content:
                    suggestions.append({
                        "type": "performance",
                        "message": "Accélération matérielle désactivée",
                        "file": "AndroidManifest.xml",
                        "action": "enable_hardware_accel",
                    })
            except Exception:
                pass
        return suggestions

    def _analyze_permissions(self) -> List[Dict]:
        suggestions = []
        manifest_path = self.decompiled_dir / "AndroidManifest.xml"
        if manifest_path.exists():
            try:
                content = manifest_path.read_text(encoding="utf-8")
            except Exception:
                return suggestions
            intrusive_permissions = [
                "READ_PHONE_STATE",
                "READ_CONTACTS",
                "ACCESS_FINE_LOCATION",
                "CAMERA",
            ]
            for perm in intrusive_permissions:
                if f"android.permission.{perm}" in content:
                    suggestions.append({
                        "type": "permission",
                        "message": f"Permission intrusive détectée: {perm}",
                        "file": "AndroidManifest.xml",
                        "action": "review_permission",
                    })
        return suggestions
