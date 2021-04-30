#!/bin/bash
mkdir -p ~/.local/bin/
cp teflo_terraform_plugin/terraform_cli/terraform ~/.local/bin/
export PATH=$PATH:~/.local/bin/