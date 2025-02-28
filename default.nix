{ pkgs ? import <nixpkgs> { } }:

let
  venv-packages = ps: with ps; [
    numpy
  ];
in

pkgs.mkShell
{
  nativeBuildInputs = with pkgs; [
  ];

  shellHook = ''
    poetry update
    alias pdoc="poetry run pdoc"
    alias pytest="poetry run pytest"
  '';

  packages = with pkgs; [
    poetry
    (python3.withPackages venv-packages)
  ];
}