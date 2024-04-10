# syntax=docker/dockerfile:1

FROM ghcr.io/vipm-io/actions-runner-labview:main

ARG LABVIEW_VERSION 2024
ARG LABVIEW_BITNESS 64
ARG VIPC_TIMEOUT 600

# note that files after the first COPY are optional, which is nice (since might not have a dev.vipc)
COPY "source/.vipc" "build support/dev.vipc?" ./

RUN . start_display && \
    echo "Refreshing Package List..." && \
    dragon refresh --vipm && \
    echo "Applying VIPC (Dev Deps) File..." && \
    dragon vipm apply-vipc --labview-version 2024 --labview-bitness 64 --timeout 600 dev.vipc && \
    rm dev.vipc && \
    echo "Applying VIPC File (Library Deps)..." && \
    dragon vipm apply-vipc --labview-version 2024 --labview-bitness 64 --timeout 600 .vipc && \
    rm .vipc
