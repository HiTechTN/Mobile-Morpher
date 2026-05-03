import os
import re
import shutil
from pathlib import Path
from typing import Dict

class AppRefactor:
    def __init__(self, work_dir: str, old_package: str, new_package: str,
                 old_app_name: str, new_app_name: str):
        self.work_dir = Path(work_dir)
        self.old_package = old_package
        self.new_package = new_package
        self.old_app_name = old_app_name
        self.new_app_name = new_app_name
        
        self.old_package_path = old_package.replace('.', '/')
        self.new_package_path = new_package.replace('.', '/')
        
    def refactor_all(self) -> Dict[str, int]:
        results = {
            'manifest_updated': 0,
            'smali_updated': 0,
            'resources_updated': 0,
            'directories_renamed': 0,
            'errors': []
        }
        
        try:
            results['manifest_updated'] = self._update_manifest()
            results['smali_updated'] = self._update_smali_files()
            results['resources_updated'] = self._update_resources()
            results['directories_renamed'] = self._rename_package_directories()
        except Exception as e:
            results['errors'].append(str(e))
            
        return results
    
    def _update_manifest(self) -> int:
        manifest_path = self.work_dir / 'AndroidManifest.xml'
        if not manifest_path.exists():
            return 0
            
        content = manifest_path.read_text(encoding='utf-8')
        
        content = content.replace(self.old_package, self.new_package)
        
        content = re.sub(
            r'android:authorities="[^"]*' + re.escape(self.old_package),
            lambda m: m.group(0).replace(self.old_package, self.new_package),
            content
        )
        
        manifest_path.write_text(content, encoding='utf-8')
        return 1
    
    def _update_smali_files(self) -> int:
        smali_dir = self.work_dir / 'smali'
        if not smali_dir.exists():
            return 0
            
        count = 0
        for smali_file in smali_dir.rglob('*.smali'):
            content = smali_file.read_text(encoding='utf-8')
            
            if self.old_package in content:
                content = content.replace(self.old_package, self.new_package)
                smali_file.write_text(content, encoding='utf-8')
                count += 1
                
        return count
    
    def _update_resources(self) -> int:
        count = 0
        res_dir = self.work_dir / 'res'
        if not res_dir.exists():
            return 0
            
        strings_files = list(res_dir.rglob('strings.xml'))
        for strings_file in strings_files:
            content = strings_file.read_text(encoding='utf-8')
            
            if self.old_app_name in content:
                content = content.replace(self.old_app_name, self.new_app_name)
                strings_file.write_text(content, encoding='utf-8')
                count += 1
                
        return count
    
    def _rename_package_directories(self) -> int:
        base_dirs = ['smali', 'smali_classes2', 'smali_classes3']
        count = 0
        
        for base_dir_name in base_dirs:
            base_dir = self.work_dir / base_dir_name
            if not base_dir.exists():
                continue
                
            old_path = base_dir / self.old_package_path
            new_path = base_dir / self.new_package_path
            
            if old_path.exists() and old_path != new_path:
                new_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(old_path), str(new_path))
                count += 1
                
        return count


def refactor_apk(work_dir: str, old_package: str, new_package: str,
                 old_app_name: str, new_app_name: str) -> Dict:
    refactor = AppRefactor(work_dir, old_package, new_package, 
                          old_app_name, new_app_name)
    return refactor.refactor_all()


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 6:
        print("Usage: python refactor.py <work_dir> <old_package> <new_package> <old_app_name> <new_app_name>")
        sys.exit(1)
    
    results = refactor_apk(sys.argv[1], sys.argv[2], sys.argv[3], 
                          sys.argv[4], sys.argv[5])
    print(results)
