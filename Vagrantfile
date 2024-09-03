# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  (1..3).each do |i|
    config.vm.define "sftp_#{i}" do |sftp|
      sftp.vm.box = "ubuntu/bionic64"
      sftp.vm.hostname = "sftp-#{i}"
      sftp.vm.network "private_network", ip: "192.168.56.20#{i}"

      sftp.vm.provider "virtualbox" do |vb|
        vb.name = "sftp-#{i}"
        vb.memory = "1024"
        vb.cpus = 2
      end
     
    end
  end
end
