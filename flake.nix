{
  nixConfig = {
    bash-prompt-prefix = "(ff-dev) ";
  };
  
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }: flake-utils.lib.eachSystem [ "x86_64-linux" ] (system: 
    let 
      pkgs = import nixpkgs {
        inherit system;
        config.allowUnfree = true;
      };
    in 
    {
      packages = rec {
        spization = pkgs.python3Packages.callPackage ./spization.nix { };

        default = spization;
      };

      devShells.default = pkgs.mkShell {
        inputsFrom = [
          self.packages.${system}.spization 
        ];

        buildInputs = (with pkgs; [
          python3
        ]);
      };
    }
  );
}
# vim: set tabstop=2 shiftwidth=2 expandtab:
