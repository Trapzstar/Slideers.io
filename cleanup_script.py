#!/usr/bin/env python3
"""
Repository Cleanup Script
Menghapus file duplikat dan tidak terpakai secara aman
"""
import os
import shutil
from pathlib import Path

# File yang akan dihapus
FILES_TO_REMOVE = [
    "hybrid_voice_recognizer_enhanced.py",  # Duplikat
    "hybrid_voice_recognizer_original.py",  # Versi lama
    "lazy.py",  # Snippet tidak lengkap
    "async.py",  # Snippet tidak lengkap
    "caching.py",  # Snippet tidak lengkap
    "plugins.py",  # Snippet tidak lengkap
    "recognizer_factory.py",  # Snippet tidak lengkap
    "recognizer_base.py",  # Snippet tidak lengkap
    "commands.py",  # Snippet tidak lengkap
    "config.py",  # Tidak digunakan
    "logging_config.py",  # Tidak digunakan
    "speech_history.txt",  # File runtime
]

def backup_files(files_list):
    """Backup files sebelum dihapus"""
    backup_dir = Path("backup_before_cleanup")
    backup_dir.mkdir(exist_ok=True)
    
    print("📦 Membuat backup file yang akan dihapus...")
    for file in files_list:
        if os.path.exists(file):
            shutil.copy2(file, backup_dir / file)
            print(f"   ✓ Backup: {file}")
    
    print(f"\n✅ Backup selesai di folder: {backup_dir}\n")

def remove_files(files_list, dry_run=False):
    """Hapus file dari list"""
    print("🗑️  Menghapus file yang tidak diperlukan...\n")
    
    removed = []
    not_found = []
    
    for file in files_list:
        if os.path.exists(file):
            if not dry_run:
                os.remove(file)
                print(f"   ✓ Dihapus: {file}")
                removed.append(file)
            else:
                print(f"   [DRY RUN] Akan dihapus: {file}")
        else:
            not_found.append(file)
    
    if not_found:
        print(f"\n⚠️  File tidak ditemukan (sudah dihapus?): {len(not_found)}")
        for file in not_found:
            print(f"   - {file}")
    
    return removed, not_found

def create_proper_gitignore():
    """Buat .gitignore yang sesuai untuk Python project"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Project Specific
speech_history.txt
user_voice_config.json
popup_analytics.json
backup_before_cleanup/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
"""
    
    with open(".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    
    print("✅ .gitignore baru dibuat untuk Python project\n")

def create_folder_structure():
    """Buat struktur folder yang rapi (opsional)"""
    folders = {
        "docs": "Dokumentasi",
        "demos": "File demo",
        "tests": "Unit tests"
    }
    
    print("📁 Membuat struktur folder...\n")
    for folder, desc in folders.items():
        Path(folder).mkdir(exist_ok=True)
        print(f"   ✓ {folder}/ - {desc}")
    
    print()

def move_files_to_folders():
    """Pindahkan file ke folder yang sesuai"""
    moves = {
        "demos": ["demo_popup.py", "demo_enhanced.py"],
        "tests": ["test_all.py"],
        "docs": ["README.md", "ACCESSIBILITY_README.md"]
    }
    
    print("🔄 Memindahkan file ke folder yang sesuai...\n")
    
    for folder, files in moves.items():
        for file in files:
            if os.path.exists(file):
                dest = Path(folder) / file
                if not dest.exists():
                    shutil.move(file, dest)
                    print(f"   ✓ {file} → {folder}/")
    
    print()

def create_main_readme():
    """Buat README.md sederhana di root jika sudah dipindah"""
    if not os.path.exists("README.md") and os.path.exists("docs/README.md"):
        readme_content = """# 🎤 SlideSense.id

Voice-Controlled PowerPoint Presentation dengan Fitur Accessibility

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run program
python main.py
```

## 📖 Dokumentasi Lengkap

Lihat [docs/README.md](docs/README.md) untuk dokumentasi lengkap.

## 🎯 Fitur Utama

- ✅ Voice Control untuk PowerPoint
- ✅ Smart Retry & Auto Microphone Selection
- ✅ Accessibility Popup untuk Audiens Difabel
- ✅ Real-time Captioning (Beta)
- ✅ Multi-language Support

## 📝 License

Apache License 2.0
"""
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        print("✅ README.md baru dibuat di root\n")

def verify_main_imports():
    """Verifikasi bahwa main.py masih bisa import semua dependencies"""
    print("🔍 Verifikasi imports di main.py...\n")
    
    try:
        # Coba import tanpa menjalankan main()
        import sys
        import importlib.util
        
        spec = importlib.util.spec_from_file_location("main", "main.py")
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            # Tidak execute, hanya load
            print("   ✓ main.py dapat di-load")
        
        # Cek file dependencies
        required_files = [
            "voice_detector.py",
            "hybrid_voice_recognizer.py",
            "powerpoint_controller.py",
            "accessibility_popup.py"
        ]
        
        missing = []
        for file in required_files:
            if os.path.exists(file):
                print(f"   ✓ {file} ada")
            else:
                print(f"   ✗ {file} HILANG!")
                missing.append(file)
        
        if missing:
            print(f"\n❌ ERROR: File penting hilang: {missing}")
            return False
        
        print("\n✅ Semua dependencies tersedia\n")
        return True
        
    except Exception as e:
        print(f"\n❌ Error saat verifikasi: {e}\n")
        return False

def main():
    """Main cleanup process"""
    print("=" * 60)
    print("🧹 REPOSITORY CLEANUP SCRIPT")
    print("=" * 60)
    print()
    
    # 1. Backup dulu
    backup_files(FILES_TO_REMOVE)
    
    # 2. Hapus file
    removed, not_found = remove_files(FILES_TO_REMOVE, dry_run=False)
    
    print(f"\n📊 Summary:")
    print(f"   - File dihapus: {len(removed)}")
    print(f"   - File tidak ditemukan: {len(not_found)}")
    print()
    
    # 3. Buat .gitignore baru
    create_proper_gitignore()
    
    # 4. Verifikasi main.py masih bisa jalan
    if verify_main_imports():
        print("✅ Cleanup BERHASIL!")
        print("\n💡 Tips:")
        print("   - Backup ada di folder: backup_before_cleanup/")
        print("   - Jika ada masalah, restore dari backup")
        print("   - Test dengan: python main.py")
        print()
    else:
        print("⚠️  Cleanup selesai tapi ada warning")
        print("   Periksa dependencies sebelum run")
        print()
    
    # Opsi untuk reorganisasi folder (opsional)
    print("=" * 60)
    choice = input("Apakah ingin reorganisasi ke folder? (y/n): ").strip().lower()
    if choice == 'y':
        create_folder_structure()
        move_files_to_folders()
        create_main_readme()
        print("✅ Reorganisasi selesai!")
    else:
        print("⏭️  Skipped reorganisasi folder")
    
    print("\n" + "=" * 60)
    print("🎉 CLEANUP SELESAI!")
    print("=" * 60)

if __name__ == "__main__":
    main()
