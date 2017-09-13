# jrsd (Jackson's Rogue System Detection)

jrsd is a network device monitoring and alerting utility designed to run on a RHEL/CentOS host. It's built for an extremely specific use case of providing rogue system detection on a small, static network. This is accomplished by providing a complete whitelist of MAC addresses that will be used on the network, and periodically ARP scanning to ensure all network devices are within the whitelist.

## Install
* [Click here](https://github.com/vesche/jrsd/archive/master.zip) to download this repo.
* Unzip the contents and transfer to your RHEL/CentOS host.
* Run `sudo ./install.sh`

## Configuration
The config file for jrsd is located at `/etc/jrsd.conf`, it will need to be updated before jrsd is started.

* `ip_space` is the subnet you wish to continually scan for rogue systems.
* `interval` is the time in seconds to wait before another scan is conducted.
* Underneath `[whitelist]` place all whitelisted MAC addresses on seperate lines. MAC addresses must be in the form of `11-11-11-11-11-11` seperated using `-` marks only!

```ini
[settings]
ip_space = 10.0.0.0/24
interval = 60

[whitelist]
# my laptop
11-22-33-44-55-66

# my router
aa-bb-cc-dd-ee-ff
```

## Usage
jrsd is managed using systemd:

* To start jrsd run: `sudo systemctl start jrsd`
* To set jrsd to start on boot run: `sudo systemctl enable jrsd`

If jrsd is tripped it will display a message to all logged in users, and also create a log in `/var/log/jrsd.log`.