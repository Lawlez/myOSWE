#!/bin/bash

# flush the file system buffer.
sync

#Clear PageCache only.
echo "echo 1 > /proc/sys/vm/drop_caches"
