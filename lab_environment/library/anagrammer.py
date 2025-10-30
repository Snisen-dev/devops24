#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

def run_module():
    # Define module arguments
    module_args = dict(
        message=dict(type='str', required=True)
    )

    # Create the Ansible module object
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    message = module.params['message']
    reversed_message = message[::-1]

    # Special failure condition
    if message == "fail me":
        module.fail_json(
            msg="You requested this to fail",
            changed=True,
            original_message=message,
            reversed_message=reversed_message
        )

    # Determine if the message has changed (is not the same reversed)
    changed = message != reversed_message

    # Return results
    result = dict(
        changed=changed,
        original_message=message,
        reversed_message=reversed_message
    )

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
