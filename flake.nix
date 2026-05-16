{
  description = "Mobile-Morpher development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }: let
    system = "x86_64-linux";
    pkgs = import nixpkgs {
      inherit system;
      config = {
        allowUnfree = true;
        android_sdk.accept_license = true;
      };
    };

    android = pkgs.androidenv.composeAndroidPackages {
      platformVersions = [ "34" ];
      buildToolsVersions = [ "34.0.0" ];
      includeEmulator = false;
      includeExtras = [];
    };

  in {
    devShells.${system}.default = pkgs.mkShell {
      name = "mobile-morpher";
      buildInputs = with pkgs; [
        jdk
        apktool
        android.androidsdk
        (python3.withPackages (p: with p; [ fastapi uvicorn python-multipart pydantic httpx ]))
      ];

      shellHook = ''
        export ANDROID_SDK_ROOT="${android.androidsdk}/libexec/android-sdk"
        export PATH="$ANDROID_SDK_ROOT/build-tools/34.0.0:$PATH"
        echo "Mobile-Morpher environment ready"
        echo "Java: $(java -version 2>&1 | head -1)"
        echo "Apktool: $(apktool --version 2>&1)"
        echo "apksigner: $(which apksigner 2>/dev/null || echo 'checking...')"
        which apksigner 2>/dev/null || apksigner --version 2>/dev/null
      '';
    };
  };
}
