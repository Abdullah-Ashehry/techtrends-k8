# set up the default terminal
ENV["TERM"]="linux"

# set minimum version for Vagrant
Vagrant.require_version ">= 2.2.10"
Vagrant.configure("2") do |config|
  config.vm.provision "shell",
    inline: "sudo su - && zypper update && zypper install -y apparmor-parser"
  
    #config.vm.box = "opensuse/Leap-15.2.x86_64"
    #config.vm.box_version = "15.2.31.632"
    
    # Set the image for the vagrant box
    config.vm.box = "bento/ubuntu-20.04-arm64"
    # Set the image version
    config.vm.box_version = "202404.23.0"

  # Forward the ports from the guest VM to the local host machine
  # Forward more ports, as needed
  config.vm.network "forwarded_port", guest: 8080, host: 4444
  config.vm.network "forwarded_port", guest: 6111, host: 6111
  config.vm.network "forwarded_port", guest: 6112, host: 6112

  # Set the static IP for the vagrant box
  config.vm.network "private_network", ip: "192.168.50.4"
  
  # Set the boot timeout
  config.vm.boot_timeout = 600

  # Configure the parameters for Parallels provider
  config.vm.provider "parallels" do |vb|
    vb.memory = "4096"
    vb.cpus = 4
    #vb.customize ["modifyvm", :id, "--ioapic", "on"]
  end
end
