terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.60.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region     = "ap-northeast-1"
  access_key = var.access_key
  secret_key = var.secret
}

resource "aws_lightsail_instance" "small" {
  name              = "teflo"
  availability_zone = "ap-northeast-1a"
  blueprint_id      = "centos_7_2009_01"
  bundle_id         = "nano_2_0"
  key_pair_name     = "automation"
  tags = {
    foo = "bar"
  }

}

output "ip_addr_teflo" {
  value     = aws_lightsail_instance.small.public_ip_address
}
