# Setting up daily backup script on Ubuntu

## Setting up configuration file
The backup script uses `json` configuration file to get the list of files/folders to be backed up. The config file looks like below.

```json
{
    "archive_type": "bz2",
    "archive_prefix": "username_ubuntu_backup",
    "archive_destination": "/home/username/backups/",
    "items": [
        "/home/username/Documents",
        "/home/username/Desktop",
        "/home/username/Pictures"
    ]
}
```

* `archive_type` - Provides the type of backup archive file to be created. Supported formats are `tar.bz2`, `tar.gz`, `tar`. `zip` is NOT SUPPORTED.
* `archive_prefix` - Prefix given to the backup archive file.
* `archive_destination` - Destination where the backup archive should be placed.
* `items` - List of files/folders to be included in the backup.

## Using `crontab` to backup periodically
`cron` is a daemon on Linux to run scheduled commands. This is available and running by default on Ubuntu. We need to add an entry for the backup generator script so that it is run as per a given schedule.
`crontab` is the tool which manages the list of commands executed by `cron`. You can add a new configuration by executing the following command.

```bash
crontab -e # This will open the configuration in an editor (vim/nano)
```

Once the configuration file is ready for edit, add the following lines. Save and exit.

```
0 10 * * * /home/username/home-made-backup/hmb.py --config /home/username/home-made-backup/sample/config.json
0 16 * * * /home/username/home-made-backup/hmb.py --config /home/username/home-made-backup/sample/config.json
```

`crontab` configuration is in the following format.

```bash
#
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
#
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').#
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
#
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
#
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
#
# For more information see the manual pages of crontab(5) and cron(8)
#
# m h  dom mon dow   command
```

Test that the configuration is saved and available for `cron` to pickup.

```bash
crontab -l # Should show the entries added previously
```

If everything is OK, you should find a backup archive created in the configured folder. User OneDrive to save it on the cloud.
