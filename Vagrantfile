Vagrant.configure('2') do |config|
  config.vm.define 'db1' do |db1|
    db1.vm.box = 'hashicorp/precise64'
    db1.vm.network 'private_network', ip: '192.168.60.110'
    db1.vm.network 'forwarded_port', guest: 3306, host: 3306

    db1.vm.provision 'ansible' do |ansible|
      ansible.playbook = 'provisioning/development.yaml'
      ansible.inventory_path = 'provisioning/vagrant'
      ansible.limit = 'db'
    end
  end

  config.vm.define 'web1' do |web1|
    web1.vm.box = 'hashicorp/precise64'
    web1.vm.network 'private_network', ip: '192.168.60.100'
    web1.vm.network 'forwarded_port', guest: 8000, host: 8080

    web1.vm.provision 'ansible' do |ansible|
      ansible.playbook = 'provisioning/development.yaml'
      ansible.inventory_path = 'provisioning/vagrant'
      ansible.limit = 'web'
    end
  end

  config.vm.define 'worker1' do |worker1|
    worker1.vm.box = 'hashicorp/precise64'
    worker1.vm.network 'private_network', ip: '192.168.60.120'

    worker1.vm.provision 'ansible' do |ansible|
      ansible.playbook = 'provisioning/development.yaml'
      ansible.inventory_path = 'provisioning/vagrant'
      ansible.limit = 'workers'
    end
  end
end
