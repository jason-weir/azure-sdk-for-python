import time
import pytest
from azure.mgmt.resource import ResourceManagementClient
from devtools_testutils import AzureMgmtRecordedTestCase, recorded_by_proxy, set_custom_default_matcher
from azure.mgmt.netapp.models import Volume, VolumePatch, ReplicationObject, VolumePropertiesDataProtection, AuthorizeRequest, PoolChangeRequest
from test_pool import create_pool, delete_pool
from test_account import delete_account
from setup import *
import azure.mgmt.netapp.models

GIGABYTE = 1024 * 1024 * 1024
SUBSID = '69a75bda-882e-44d5-8431-63421204132a'


def create_volume_body(volume_name, location, rg=TEST_RG, vnet=VNET):
    default_protocol_type = ["NFSv3"]

    volume_body = Volume(
        location=location,
        usage_threshold=100 * GIGABYTE,
        protocol_types=default_protocol_type,
        creation_token=volume_name,
        service_level=SERVICE_LEVEL,
        subnet_id="/subscriptions/" + SUBSID + "/resourceGroups/" + rg + "/providers/Microsoft.Network/virtualNetworks/"
                  + vnet + "/subnets/default"
    )

    return volume_body


def create_volume(client, rg=TEST_RG, account_name=TEST_ACC_1, pool_name=TEST_POOL_1, volume_name=TEST_VOL_1,
                  location=LOCATION, vnet=VNET, volume_only=False, live=False):
    if not volume_only:
        create_pool(
            client,
            rg,
            account_name,
            pool_name,
            location,
            False)
        if live:
            time.sleep(10)

    volume_body = create_volume_body(volume_name, location, rg, vnet)
    volume = client.volumes.begin_create_or_update(
        rg,
        account_name,
        pool_name,
        volume_name,
        volume_body
    ).result()

    return volume


def create_dp_volume(client, source_volume, rg=TEST_REPL_REMOTE_RG, account_name=TEST_ACC_2, pool_name=TEST_POOL_2,
                     volume_name=TEST_VOL_2, location=REMOTE_LOCATION, volume_only=False, live=False):
    if not volume_only:
        create_pool(
            client,
            rg,
            account_name,
            pool_name,
            location,
            False)
        if live:
            time.sleep(10)

    # data protection and replication object
    replication = ReplicationObject(
        endpoint_type="dst",
        remote_volume_resource_id=source_volume.id,
        replication_schedule="_10minutely"
    )

    data_protection = VolumePropertiesDataProtection(
        replication=replication
    )

    default_protocol_type = ["NFSv3"]

    volume_body = Volume(
        location=location,
        usage_threshold=100 * GIGABYTE,
        protocol_types=default_protocol_type,
        creation_token=volume_name,
        subnet_id="/subscriptions/" + SUBSID + "/resourceGroups/" + rg + "/providers/Microsoft.Network/virtualNetworks/"
                  + REMOTE_VNET + "/subnets/default",
        volume_type="DataProtection",
        data_protection=data_protection
    )

    destination_volume = client.volumes.begin_create_or_update(
        rg,
        account_name,
        pool_name,
        volume_name,
        volume_body
    ).result()

    return destination_volume


def get_volume(client, rg, account_name, pool_name, volume_name):
    volume = client.volumes.get(rg, account_name, pool_name, volume_name)
    return volume


def wait_for_no_volume(client, rg, account_name, pool_name, volume_name, live=False):
    # a workaround for the async nature of certain ARM processes
    co = 0
    while co < 10:
        co += 1
        if live:
            time.sleep(200)
        try:
            get_volume(client, rg, account_name, pool_name, volume_name)
        except:
            # not found is an exception case (status code 200 expected)
            # but is what we are waiting for
            break


def wait_for_volume(client, rg, account_name, pool_name, volume_name, live=False):
    # a work around for the async nature of certain ARM processes
    co = 0
    while co < 10:
        co += 1
        if live:
            time.sleep(10)
        try:
            get_volume(client, rg, account_name, pool_name, volume_name)
            break
        except:
            # not found is an exception case (status code 200 expected)
            # but is what we are waiting for
            pass


def delete_volume(client, rg, account_name, pool_name, volume_name, live=False):
    client.volumes.begin_delete(rg, account_name, pool_name, volume_name).wait()
    wait_for_no_volume(client, rg, account_name, pool_name, volume_name, live)


def wait_for_replication_status(client, target_state, live=False):
    # python isn't good at do-while loops but loop until we get the target state
    while True:
        replication_status = client.volumes.replication_status(TEST_REPL_REMOTE_RG, TEST_ACC_2, TEST_POOL_2, TEST_VOL_2)
        if replication_status.mirror_state == target_state:
            break
        if live:
            time.sleep(1)


def wait_for_succeeded(client, live=False):
    # python isn't good at do-while loops but loop until we get volumes in succeeded state
    while True:
        source_volume = client.volumes.get(TEST_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1)
        dp_volume = client.volumes.get(TEST_REPL_REMOTE_RG, TEST_ACC_2, TEST_POOL_2, TEST_VOL_2)
        if (source_volume.provisioning_state == "Succeeded") and (dp_volume.provisioning_state == "Succeeded"):
            break
        if live:
            time.sleep(1)


class TestNetAppVolume(AzureMgmtRecordedTestCase):

    def setup_method(self, method):
        self.client = self.create_mgmt_client(azure.mgmt.netapp.NetAppManagementClient)

    # Before tests are run live a resource group needs to be created along with vnet and subnet
    # Note that when tests are run in live mode it is best to run one test at a time.
    @recorded_by_proxy
    def test_create_delete_list_volume(self):
        # this can be reverted to set_bodiless_matcher() after tests are re-recorded and don't contain these headers
        set_custom_default_matcher(
            compare_bodies=False, excluded_headers="Authorization,Content-Length,x-ms-client-request-id,x-ms-request-id"
        )
        volume = create_volume(
            self.client,
            TEST_RG,
            TEST_ACC_1,
            TEST_POOL_1,
            TEST_VOL_1,
            live=self.is_live
        )
        assert volume.name == TEST_ACC_1 + '/' + TEST_POOL_1 + '/' + TEST_VOL_1
        # check default export policy and protocol
        assert volume.export_policy.rules[0].nfsv3
        assert not volume.export_policy.rules[0].nfsv41
        assert "0.0.0.0/0" == volume.export_policy.rules[0].allowed_clients
        assert volume.protocol_types[0] == "NFSv3"

        volume_list = self.client.volumes.list(TEST_RG, TEST_ACC_1, TEST_POOL_1)
        assert len(list(volume_list)) == 1

        delete_volume(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, live=self.is_live)
        volume_list = self.client.volumes.list(TEST_RG, TEST_ACC_1, TEST_POOL_1)
        assert len(list(volume_list)) == 0

        wait_for_no_volume(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, live=self.is_live)
        delete_pool(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_1, live=self.is_live)
        delete_account(self.client, TEST_RG, TEST_ACC_1, live=self.is_live)

    @recorded_by_proxy
    def test_list_volumes(self):
        # this can be reverted to set_bodiless_matcher() after tests are re-recorded and don't contain these headers
        set_custom_default_matcher(
            compare_bodies=False, excluded_headers="Authorization,Content-Length,x-ms-client-request-id,x-ms-request-id"
        )
        create_volume(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, LOCATION, live=self.is_live)
        create_volume(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_2, LOCATION, volume_only=True, live=self.is_live)
        volumes = [TEST_VOL_1, TEST_VOL_2]

        volume_list = self.client.volumes.list(TEST_RG, TEST_ACC_1, TEST_POOL_1)
        assert len(list(volume_list)) == 2
        idx = 0
        for volume in volume_list:
            assert volume.name == volumes[idx]
            idx += 1

        delete_volume(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, live=self.is_live)
        delete_volume(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_2, live=self.is_live)
        delete_pool(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_1, live=self.is_live)
        delete_account(self.client, TEST_RG, TEST_ACC_1, live=self.is_live)

    @recorded_by_proxy
    def test_volume_replication(self):
        # this can be reverted to set_bodiless_matcher() after tests are re-recorded and don't contain these headers
        set_custom_default_matcher(
            compare_bodies=False, excluded_headers="Authorization,Content-Length,x-ms-client-request-id,x-ms-request-id"
        )
        source_volume = create_volume(
            self.client,
            TEST_RG,
            TEST_ACC_1,
            TEST_POOL_1,
            TEST_VOL_1,
            vnet=VNET,
            live=self.is_live)
        dp_volume = create_dp_volume(
            self.client,
            source_volume,
            TEST_REPL_REMOTE_RG,
            TEST_ACC_2,
            TEST_POOL_2,
            TEST_VOL_2,
            live=self.is_live)

        if self.is_live:
            time.sleep(30)

        # sync replication
        body = AuthorizeRequest(remote_volume_resource_id=dp_volume.id)
        self.client.volumes.begin_authorize_replication(TEST_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, body)
        wait_for_succeeded(self.client, self.is_live)
        if self.is_live:
            time.sleep(30)
        wait_for_replication_status(self.client, "Mirrored", self.is_live)

        # break replication
        self.client.volumes.begin_break_replication(TEST_REPL_REMOTE_RG, TEST_ACC_2, TEST_POOL_2, TEST_VOL_2)
        wait_for_replication_status(self.client, "Broken", self.is_live)
        if self.is_live:
            time.sleep(30)
        wait_for_succeeded(self.client, self.is_live)

        # resync
        self.client.volumes.begin_resync_replication(TEST_REPL_REMOTE_RG, TEST_ACC_2, TEST_POOL_2, TEST_VOL_2)
        wait_for_replication_status(self.client, "Mirrored", self.is_live)
        if self.is_live:
            time.sleep(30)

        # break again
        self.client.volumes.begin_break_replication(TEST_REPL_REMOTE_RG, TEST_ACC_2, TEST_POOL_2, TEST_VOL_2)
        wait_for_replication_status(self.client, "Broken", self.is_live)
        if self.is_live:
            time.sleep(30)

        # delete the data protection object
        #  - initiate delete replication on destination, this then releases on source, both resulting in object deletion
        self.client.volumes.begin_delete_replication(TEST_REPL_REMOTE_RG, TEST_ACC_2, TEST_POOL_2, TEST_VOL_2)

        replication_found = True  # because it was previously present
        while replication_found:
            try:
                self.client.volumes.replication_status(TEST_REPL_REMOTE_RG, TEST_ACC_2, TEST_POOL_2, TEST_VOL_2)
            except:
                # an exception means the replication was not found
                # i.e. it has been deleted
                # ok without checking it could have been for another reason
                # but then the delete below will fail
                replication_found = False

            if self.is_live:
                time.sleep(1)

        # seems the volumes are not always in a terminal state here so check again
        # and ensure the replication objects are removed
        # python isn't good at do-while loops but loop until we get volumes in succeeded state
        while True:
            source_volume = self.client.volumes.get(TEST_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1)
            dp_volume = self.client.volumes.get(TEST_REPL_REMOTE_RG, TEST_ACC_2, TEST_POOL_2, TEST_VOL_2)
            if (source_volume.provisioning_state == "Succeeded") and (dp_volume.provisioning_state == "Succeeded") and \
                    (source_volume.data_protection.replication is None) and \
                    (dp_volume.data_protection.replication is None):
                break
            if self.is_live:
                time.sleep(1)

        # now proceed with the delete of the volumes and tidy up resources

        # delete destination volume
        delete_volume(self.client, TEST_REPL_REMOTE_RG, TEST_ACC_2, TEST_POOL_2, TEST_VOL_2, live=self.is_live)
        delete_pool(self.client, TEST_REPL_REMOTE_RG, TEST_ACC_2, TEST_POOL_2, live=self.is_live)
        delete_account(self.client, TEST_REPL_REMOTE_RG, TEST_ACC_2, live=self.is_live)

        # delete source volume
        delete_volume(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, live=self.is_live)
        delete_pool(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_1, live=self.is_live)
        delete_account(self.client, TEST_RG, TEST_ACC_1, live=self.is_live)

    @recorded_by_proxy
    def test_get_volume_by_name(self):
        # this can be reverted to set_bodiless_matcher() after tests are re-recorded and don't contain these headers
        set_custom_default_matcher(
            compare_bodies=False, excluded_headers="Authorization,Content-Length,x-ms-client-request-id,x-ms-request-id"
        )
        create_volume(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, LOCATION, live=self.is_live)

        volume = self.client.volumes.get(TEST_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1)
        assert volume.name == TEST_ACC_1 + '/' + TEST_POOL_1 + '/' + TEST_VOL_1

        delete_volume(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, live=self.is_live)
        delete_pool(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_1, live=self.is_live)
        delete_account(self.client, TEST_RG, TEST_ACC_1, live=self.is_live)

    @recorded_by_proxy
    def test_update_volume(self):
        # this can be reverted to set_bodiless_matcher() after tests are re-recorded and don't contain these headers
        set_custom_default_matcher(
            compare_bodies=False, excluded_headers="Authorization,Content-Length,x-ms-client-request-id,x-ms-request-id"
        )
        volume = create_volume(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, live=self.is_live)
        assert "Premium" == volume.service_level
        assert 100 * GIGABYTE == volume.usage_threshold

        volume_body = Volume(
            usage_threshold=200 * GIGABYTE,
            creation_token=TEST_VOL_1,
            service_level="Premium",  # cannot differ from pool
            location=LOCATION,
            subnet_id="/subscriptions/" + SUBSID + "/resourceGroups/" + TEST_RG +
                      "/providers/Microsoft.Network/virtualNetworks/" + VNET + "/subnets/default"
        )

        volume = self.client.volumes.begin_create_or_update(
            TEST_RG,
            TEST_ACC_1,
            TEST_POOL_1,
            TEST_VOL_1,
            volume_body
        ).result()
        assert "Premium" == volume.service_level  # unchanged
        assert 200 * GIGABYTE == volume.usage_threshold

        delete_volume(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, live=self.is_live)
        delete_pool(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_1, live=self.is_live)
        delete_account(self.client, TEST_RG, TEST_ACC_1, live=self.is_live)

    @recorded_by_proxy
    def test_patch_volume(self):
        # this can be reverted to set_bodiless_matcher() after tests are re-recorded and don't contain these headers
        set_custom_default_matcher(
            compare_bodies=False, excluded_headers="Authorization,Content-Length,x-ms-client-request-id,x-ms-request-id"
        )
        volume = create_volume(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, live=self.is_live)
        assert "Premium" == volume.service_level
        assert 100 * GIGABYTE == volume.usage_threshold

        volume_patch = VolumePatch(usage_threshold=200 * GIGABYTE)
        volume = self.client.volumes.begin_update(TEST_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, volume_patch).result()
        assert "Premium" == volume.service_level
        assert 200 * GIGABYTE == volume.usage_threshold

        delete_volume(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, live=self.is_live)
        delete_pool(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_1, live=self.is_live)
        delete_account(self.client, TEST_RG, TEST_ACC_1, live=self.is_live)

    @recorded_by_proxy
    def test_pool_change(self):
        # this can be reverted to set_bodiless_matcher() after tests are re-recorded and don't contain these headers
        set_custom_default_matcher(
            compare_bodies=False, excluded_headers="Authorization,Content-Length,x-ms-client-request-id,x-ms-request-id"
        )
        create_volume(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, live=self.is_live)
        pool2 = create_pool(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_2, LOCATION, True)
        if self.is_live:
            time.sleep(10)

        body = PoolChangeRequest(new_pool_resource_id=pool2.id)
        self.client.volumes.begin_pool_change(TEST_RG, TEST_ACC_1, TEST_POOL_1, TEST_VOL_1, body).wait()
        volume = self.client.volumes.get(TEST_RG, TEST_ACC_1, TEST_POOL_2, TEST_VOL_1)
        assert volume.name == TEST_ACC_1 + "/" + TEST_POOL_2 + "/" + TEST_VOL_1

        volume_list = self.client.volumes.list(TEST_RG, TEST_ACC_1, TEST_POOL_1)
        assert len(list(volume_list)) == 0

        delete_volume(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_2, TEST_VOL_1, live=self.is_live)
        delete_pool(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_1, live=self.is_live)
        delete_pool(self.client, TEST_RG, TEST_ACC_1, TEST_POOL_2, live=self.is_live)
        delete_account(self.client, TEST_RG, TEST_ACC_1, live=self.is_live)
