# syntax=docker/dockerfile:1

FROM ghcr.io/vipm-io/actions-runner-labview:main

ARG LABVIEW_VERSION 2024
ARG LABVIEW_BITNESS 64
ARG VIPC_TIMEOUT 600

COPY source/*.vipc ./

RUN echo "Starting Display..." && \
    . start_display && \
    echo "Applying VIPC File..." && \
    dragon vipc-apply --labview-version ${LABVIEW_VERSION} --labview-bitness ${LABVIEW_BITNESS} --timeout ${VIPC_TIMEOUT} *.vipc && \
    rm *.vipc
