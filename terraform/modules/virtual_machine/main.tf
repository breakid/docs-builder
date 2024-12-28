/**
 * # virtual_machine
 *
 * An example Terraform module copied from [GitHub - spotlessthoughful/mkdocs-terraform](https://github.com/spotlessthoughful/mkdocs-terraform/tree/f5cc78bbd978d1b3a48ff1579e9e9b2003bb4ccd/modules).
 */
resource "aws_instance" "example" {
  ami           = var.ami
  instance_type = var.instance_type

  subnet_id = var.subnet_id

  key_name = var.key_name

  vpc_security_group_ids = [var.security_group_id]

  tags = {
    Name = var.instance_name
  }

  user_data = file("user_data.sh")

  ebs_block_device {
    device_name           = var.device_name
    volume_type           = var.volume_type
    volume_size           = var.volume_size
    delete_on_termination = var.delete_on_termination
  }
}
