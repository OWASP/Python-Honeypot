import unittest

from core.get_modules import (load_all_modules,
                              virtual_machine_name_to_container_name,
                              virtual_machine_names_to_container_names)
from core.load import honeypot_configuration_builder


class TestCoreGetModules(unittest.TestCase):

    def test_virtual_machine_container_names(self):
        modules_list = load_all_modules()
        config = honeypot_configuration_builder(modules_list)
        container_names = virtual_machine_names_to_container_names(config)
        # list of all modules available
        all_modules = [
            'ohp_ftpserver_weak_password',
            'ohp_ftpserver_strong_password',
            'ohp_icsserver_veeder_root_guardian_ast',
            'ohp_sshserver_weak_password',
            'ohp_sshserver_strong_password',
            'ohp_smtpserver_strong_password',
            'ohp_httpserver_basic_auth_strong_password',
            'ohp_httpserver_basic_auth_weak_password'
        ]
        self.assertCountEqual(container_names, all_modules)

    def test_load_all_modules(self):
        """
        checking total number of modules
        """
        modules_list = load_all_modules()
        self.assertEqual(len(modules_list), 8)

    def test_vm_to_container_name(self):
        vm_name = "ohp_sshserver"
        module_name = "ssh/weak_password"
        container_name = virtual_machine_name_to_container_name(vm_name, module_name)
        self.assertEqual(container_name, "ohp_sshserver_weak_password")
