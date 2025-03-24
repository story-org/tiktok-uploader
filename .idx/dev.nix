# To learn more about how to use Nix to configure your environment
# see: https://developers.google.com/idx/guides/customize-idx-env
{ pkgs, ... }:
{
  channel = "stable-24.05";
  packages = [
    pkgs.python312
    pkgs.python312Packages.pip
    pkgs.nodejs
    pkgs.docker
  ];
  services.docker.enable = true;
  idx = {
    extensions = [];
    previews = {
      enable = true;
      previews = {
        web = {
          command = [ "python" "api/app.py"];
          manager = "web";
          env = {
            PORT = "$PORT";
          };
        };
      };
    };
  };
}
