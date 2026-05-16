from pathlib import Path
import re
from typing import List, Dict


class Applier:
    def __init__(self, decompiled_dir: Path):
        self.decompiled_dir = decompiled_dir

    def apply(self, suggestions: List[Dict]) -> Dict[str, int]:
        counts = {
            "ads_removed": 0,
            "tracking_removed": 0,
            "permissions_removed": 0,
            "hardware_accel_fixed": 0,
            "errors": [],
        }

        for s in suggestions:
            action = s.get("action")
            try:
                if action == "remove_ads":
                    counts["ads_removed"] += self._remove_ad_sdk(s)
                elif action == "remove_tracking":
                    counts["tracking_removed"] += self._remove_tracking_sdk(s)
                elif action == "enable_hardware_accel":
                    counts["hardware_accel_fixed"] += self._enable_hardware_accel()
                elif action == "review_permission":
                    perm_name = self._extract_permission_name(s)
                    if self._remove_permission(perm_name):
                        counts["permissions_removed"] += 1
            except Exception as e:
                counts["errors"].append(f"{action}: {e}")

        return counts

    def _remove_ad_sdk(self, suggestion: Dict) -> int:
        file_path = self.decompiled_dir / suggestion.get("file", "")
        if not file_path.exists():
            return 0

        content = file_path.read_text(encoding="utf-8")
        neutralized = self._neutralize_smali_class(content)
        if neutralized != content:
            file_path.write_text(neutralized, encoding="utf-8")

        return 1

    def _remove_tracking_sdk(self, suggestion: Dict) -> int:
        file_path = self.decompiled_dir / suggestion.get("file", "")
        if not file_path.exists():
            return 0

        content = file_path.read_text(encoding="utf-8")
        neutralized = self._neutralize_smali_class(content)
        if neutralized != content:
            file_path.write_text(neutralized, encoding="utf-8")

        return 1

    def _neutralize_smali_class(self, content: str) -> str:
        lines = content.splitlines()
        result = []
        in_method = False
        brace_depth = 0

        for line in lines:
            stripped = line.strip()

            if stripped.startswith(".method "):
                in_method = True
                brace_depth = 0
                result.append(line)
                if "abstract" not in stripped and "native" not in stripped:
                    result.append(self._indent(line) + "return-void")
                continue

            if in_method:
                if "}" in stripped:
                    brace_depth -= stripped.count("}")
                    if brace_depth <= 0:
                        in_method = False
                        result.append(line)
                    continue
                if "{" in stripped:
                    brace_depth += stripped.count("{")

            result.append(line)

        return "\n".join(result)

    def _indent(self, line: str) -> str:
        return re.match(r"^\s*", line).group()

    def _enable_hardware_accel(self) -> int:
        manifest_path = self.decompiled_dir / "AndroidManifest.xml"
        if not manifest_path.exists():
            return 0

        content = manifest_path.read_text(encoding="utf-8")
        if 'android:hardwareAccelerated="false"' in content:
            content = content.replace(
                'android:hardwareAccelerated="false"',
                'android:hardwareAccelerated="true"',
            )
            manifest_path.write_text(content, encoding="utf-8")
            return 1
        elif 'android:hardwareAccelerated="true"' in content:
            return 0

        content = content.replace(
            "<application",
            '<application android:hardwareAccelerated="true"',
        )
        manifest_path.write_text(content, encoding="utf-8")
        return 1

    def _extract_permission_name(self, suggestion: Dict) -> str:
        msg = suggestion.get("message", "")
        match = re.search(r"android\.permission\.(\w+)", msg)
        return match.group(0) if match else ""

    def _remove_permission(self, permission: str) -> bool:
        if not permission:
            return False

        manifest_path = self.decompiled_dir / "AndroidManifest.xml"
        if not manifest_path.exists():
            return False

        content = manifest_path.read_text(encoding="utf-8")
        pattern = re.compile(
            r'\s*<uses-permission[^>]*' + re.escape(permission) + r'[^>]*/>\s*',
        )
        new_content = pattern.sub("\n", content)
        if new_content != content:
            manifest_path.write_text(new_content, encoding="utf-8")
            return True
        return False


def apply_suggestions(decompiled_dir: str, suggestions: List[Dict]) -> Dict[str, int]:
    applier = Applier(Path(decompiled_dir))
    return applier.apply(suggestions)
