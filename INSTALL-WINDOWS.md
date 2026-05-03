# Installation Windows

## Méthode 1 : Script automatique
1. Télécharger `install.bat` depuis [Releases](https://github.com/HiTechTN/Mobile-Morpher/releases)
2. Clic-droit → "Exécuter en tant qu'administrateur"
3. Suivre les instructions

## Méthode 2 : Manuelle
1. Installer [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Télécharger `mobile-morpher-v1.0.0-windows.zip` depuis [Releases](https://github.com/HiTechTN/Mobile-Morpher/releases)
3. Extraire le ZIP
4. Ouvrir PowerShell dans le dossier et exécuter :
```powershell
docker compose up -d
```
5. Accéder à http://localhost:9001

## Méthode 3 : Avec WSL2 (Recommandé)
```bash
# Dans Ubuntu WSL2
curl -fsSL https://github.com/HiTechTN/Mobile-Morpher/releases/download/v1.0.0/install.sh | bash
```
