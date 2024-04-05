# syntax=docker/dockerfile:1

FROM ghcr.io/vipm-io/actions-runner-labview:main

ARG LABVIEW_VERSION 2024
ARG LABVIEW_BITNESS 64
ARG VIPC_TIMEOUT 600

COPY source/.vipc .vipc

RUN . start_display && \
    echo "Applying VIPC File..." && \
    dragon vipm apply-vipc --labview-version 2024 --labview-bitness 64 --timeout 600 .vipc && \
    rm .vipc
