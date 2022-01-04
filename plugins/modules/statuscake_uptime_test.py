from ansible.module_utils.basic import AnsibleModule

from ansible_collections.caktus.tech_support.plugins.module_utils.statuscake import (
    UptimeTest,
)


def main():
    argument_spec = {
        "api_key": {"required": True, "type": "str", "no_log": True},
        "state": {"required": True, "type": "str", "choices": ["present", "absent"]},
        "name": {"required": True, "type": "str"},
        "test_type": {
            "required": True,
            "type": "str",
            "choices": ["DNS", "HEAD", "HTTP", "PING", "SSH", "TCP"],
        },
        "website_url": {"required": True, "type": "str"},
        "check_rate": {
            "required": True,
            "type": "int",
            "choices": [0, 30, 60, 300, 900, 1800, 3600, 86400],
        },
        "basic_user": {"required": False, "type": "str"},
        "basic_pass": {"required": False, "type": "str", "no_log": True},
        "confirmation": {"required": False, "type": "int"},
        "contact_groups_csv": {"required": False, "type": "str"},
        "custom_header": {"required": False, "type": "str"},
        "do_not_find": {"required": False, "type": "bool"},
        "dns_ip_csv": {"required": False, "type": "str"},
        "dns_server": {"required": False, "type": "str"},
        "enable_ssl_alert": {"required": False, "type": "bool"},
        "final_endpoint": {"required": False, "type": "str"},
        "find_string": {"required": False, "type": "str"},
        "follow_redirects": {"required": False, "type": "str"},
        "host": {"required": False, "type": "str"},
        "include_header": {"required": False, "type": "bool"},
        "paused": {"required": False, "type": "bool"},
        "port": {"required": False, "type": "int"},
        "post_body": {"required": False, "type": "str"},
        "post_raw": {"required": False, "type": "str"},
        "regions": {"required": False, "type": "list"},
        "status_codes_csv": {"required": False, "type": "str"},
        "tags_csv": {"required": False, "type": "str"},
        "timeout": {"required": False, "type": "int"},
        "trigger_rate": {"required": False, "type": "int"},
        "use_jar": {"required": False, "type": "str"},
        "user_agent": {"required": False, "type": "str"},
    }
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    api_key = module.params["api_key"]
    name = module.params["name"]
    state = module.params["state"]
    test = UptimeTest(
        api_key=api_key,
        name=name,
        test_type=module.params["test_type"],
        website_url=module.params["website_url"],
        check_rate=module.params["check_rate"],
        basic_user=module.params["basic_user"],
        basic_pass=module.params["basic_pass"],
        confirmation=module.params["confirmation"],
        contact_groups_csv=module.params["contact_groups_csv"],
        custom_header=module.params["custom_header"],
        do_not_find=module.params["do_not_find"],
        dns_ip_csv=module.params["dns_ip_csv"],
        dns_server=module.params["dns_server"],
        enable_ssl_alert=module.params["enable_ssl_alert"],
        final_endpoint=module.params["final_endpoint"],
        find_string=module.params["find_string"],
        follow_redirects=module.params["follow_redirects"],
        host=module.params["host"],
        include_header=module.params["include_header"],
        paused=module.params["paused"],
        port=module.params["port"],
        post_body=module.params["post_body"],
        post_raw=module.params["post_raw"],
        regions=module.params["regions"],
        status_codes_csv=module.params["status_codes_csv"],
        tags_csv=module.params["tags_csv"],
        trigger_rate=module.params["trigger_rate"],
        use_jar=module.params["use_jar"],
        user_agent=module.params["user_agent"],
    )

    fetch_data = test.fetch()
    status_cake_id = fetch_data["id"] if fetch_data else None
    if state == "present":
        if status_cake_id:
            # pre_update = test.get(status_cake_id)
            test.update(status_cake_id)
            # post_update = test.get(status_cake_id)
            module.exit_json(
                changed=False,
                msg="Test Updated: %s, ID: %s" % (name, status_cake_id),
            )
        else:
            test.create()
            module.exit_json(
                changed=True,
                msg="Test Created: %s, ID: %s" % (name, test.response.content),
            )
    elif state == "absent" and status_cake_id:
        test.delete(status_cake_id)
        module.exit_json(
            changed=True,
            msg="Test Deleted: %s, ID: %s" % (name, test.response.content),
        )


if __name__ == "__main__":
    main()
