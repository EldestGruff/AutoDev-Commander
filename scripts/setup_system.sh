#!/bin/bash

set -euo pipefail

# Configuration
USER_ID=$(id -u)
GROUP_ID=$(id -g)
ZFS_POOL="eniac"
BASE_DATASET="${ZFS_POOL}/autodev"
MOUNT_BASE="/eniac"

# Logging
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*"
}

error_exit() {
    log "ERROR: $*" >&2
    exit 1
}

# Check for root privileges
if [ "$EUID" -ne 0 ]; then
    error_exit "Please run as root"
fi

# Install required packages
log "Installing required packages..."
apt-get update
apt-get install -y \
    zfsutils-linux \
    nvidia-container-toolkit \
    curl \
    jq

# Configure NVIDIA Container Toolkit
log "Configuring NVIDIA Container Toolkit..."
nvidia-ctk runtime configure --runtime=docker
systemctl restart docker

# Create ZFS datasets
log "Creating ZFS datasets..."
datasets=(
    "models/ollama"
    "qdrant_live/storage"
    "qdrant_live/snapshots"
    "redis"
    "n8n"
    "artifacts"
)

for dataset in "${datasets[@]}"; do
    zfs create -p "${BASE_DATASET}/${dataset}"
done

# Set ZFS properties
log "Configuring ZFS properties..."
zfs set compression=lz4 "${BASE_DATASET}"
zfs set atime=off "${BASE_DATASET}"
echo "options zfs zfs_arc_max=34359738368" > /etc/modprobe.d/zfs.conf

# Create systemd service
log "Creating systemd service..."
cat > /etc/systemd/system/autodev.service << EOL
[Unit]
Description=AutoDev Commander
After=docker.service zfs.target
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/${SUDO_USER}/AutoDev-Commander
ExecStart=/usr/bin/docker compose -f docker/compose/base.yml -f docker/compose/dev.yml up -d
ExecStop=/usr/bin/docker compose -f docker/compose/base.yml -f docker/compose/dev.yml down

[Install]
WantedBy=multi-user.target
EOL

# Set permissions
log "Setting permissions..."
chown -R "${USER_ID}:${GROUP_ID}" "${MOUNT_BASE}/autodev"
chmod -R 755 "${MOUNT_BASE}/autodev"

# Enable and start service
log "Enabling and starting service..."
systemctl daemon-reload
systemctl enable autodev
systemctl start autodev

log "Setup complete!"
