#!/bin/bash

[ -f /etc/rdma/mlx4.conf ] || exit 1
# any non-empty, non-commented lines?
grep -q '^[^#].\+$' /etc/rdma/mlx4.conf || exit 1

exit 0
