resource "aws_db_instance" "default" {
  allocated_storage    = 10
  db_name              = "mysqldb"
  identifier           = "week3-rds"
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t3.micro"
  username             = "jagadeesh"
  password             = "Jagadeesh219"
  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot  = true
  publicly_accessible  = true
  vpc_security_group_ids = [aws_security_group.allow_mql.id]
}

resource "aws_security_group" "allow_mql" {
  name        = "week3-rds-sg"
  description = "Allow mql inbound traffic and all outbound traffic"
  vpc_id      = "vpc-09d7d48442f764b5d"

  tags = {
    Name = "week3-rds-sg"
  }
}

resource "aws_vpc_security_group_ingress_rule" "allow_mysql" {
  security_group_id = aws_security_group.allow_mql.id
  cidr_ipv4         = "103.6.157.200/32"
  from_port         = 3306
  ip_protocol       = "tcp"
  to_port           = 3306
}

resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv4" {
  security_group_id = aws_security_group.allow_mql.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1" # semantically equivalent to all ports
}