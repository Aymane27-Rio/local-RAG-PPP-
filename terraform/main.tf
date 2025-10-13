provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "rag_server" {
  ami           = "ami-08c40ec9ead489470" # Ubuntu 22.04 AMI
  instance_type = "t2.micro"

  tags = {
    Name = "LocalRAGServer"
  }
}
