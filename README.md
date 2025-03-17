# Blender Generate Thumbnail From Texture

This project automatically generates thumbnails from 3D assets using Blender's Python API. All files in the `assets/` folder will be rendered into thumbnails and saved to the `output/` folder.

## 🛠️ Requirements

- **Blender 4.3 or newer**
- **Make** (for running Makefile commands)
- **Git Bash or WSL** (for Windows users, to use Bash/Make)

---

### 🔄 Update Blender

1. Visit [https://www.blender.org/download/](https://www.blender.org/download/)
2. Download the **latest version** for your OS.
3. Install it (or extract if using portable `.zip` version).
4. Verify version:
   ```bash
   blender --version
   ```

### 🛠️ Install Make (Windows)

#### Option 1: Using Chocolatey

1. Open PowerShell as Administrator
2. Run: `` choco install make``

#### Option 2: Using MSYS2

1. Install MSYS2: [https://www.msys2.org/](https://www.msys2.org/)
2. Run: ``pacman -S make ``

## 🚀 Usage

1. Clone the repo and navigate to the project:
2. Place your textures inside the `assets/` folder.
3. Run the script: `` make run``
4. Thumbnails will be generated and saved in the `output/` folder.
