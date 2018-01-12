import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


# use this for testing
# https://github.com/asukakenji/performance-tuning/wiki/Too-many-open-files---Open-files-limit


def test_etc_security_limits_file(host):
    seclimits = host.file("/etc/security/limits.conf")
    assert seclimits.contains("* hard memlock unlimited")
    assert seclimits.contains("* soft memlock unlimited")
    assert seclimits.contains("* hard nofile 65536")
    assert seclimits.user == "root"
    assert seclimits.group == "root"
    assert seclimits.mode == 0o644


def test_etc_sysctl_file(host):
    seclimits = host.file("/etc/sysctl.conf")
    assert seclimits.contains("fs.file-max=65536")
    assert seclimits.user == "root"
    assert seclimits.group == "root"
    assert seclimits.mode == 0o644


@pytest.mark.parametrize('f',
                         ['fs.file-max'])
def test_systcl_file_max(host, f):

    cmd = 'sysctl -n {}'.format(f)
    out = host.command.check_output(cmd)

    assert '65536' == out
