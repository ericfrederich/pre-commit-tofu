# pre-commit-tofu

A repository providing [pre-commit](https://pre-commit.com/) hooks for OpenTofu/Terraform

### Hooks available

#### `tofu-fmt`
Run `tofu fmt` against .tf and .tfvars files
  - Falls back to `terraform fmt` if `tofu` command is not available.
  - Specify command order with `args: ['--commands', 'foo,bar']` (default=tofu,terraform).
