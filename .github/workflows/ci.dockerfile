# syntax=docker/dockerfile:1

FROM ghcr.io/vipm-io/actions-runner-labview:main

ARG LABVIEW_VERSION 2024
ARG LABVIEW_BITNESS 64
ARG VIPC_TIMEOUT 600
ARG SOURCE_VIPC source/.vipc
ARG DEV_VIPC **/dev.vipc

# note that files after the first COPY are optional, which is nice (since might not have a dev.vipc)
# also note that dockerfile doesn't do whitespace characters, which is why we have a * in the COPY command
COPY "${SOURCE_VIPC}" "${DEV_VIPC}" ./

RUN if [ -f $(basename ${DEV_VIPC}) ] || [ -f $(basename ${SOURCE_VIPC}) ]; then \
        . start_display && \
        echo "Refreshing Package List..." && \
        dragon refresh --vipm && \
        if [ -f $(basename ${DEV_VIPC}) ]; then \
            echo "Applying VIPC (Dev Deps)..." && \
            dragon vipm apply-vipc --labview-version ${LABVIEW_VERSION} --labview-bitness ${LABVIEW_BITNESS} --timeout ${VIPC_TIMEOUT} $(basename ${DEV_VIPC}) && \
            rm $(basename ${DEV_VIPC}); \
        fi && \
        if [ -f $(basename ${SOURCE_VIPC}) ]; then \
            echo "Applying VIPC (Library Deps)..." && \
            dragon vipm apply-vipc --labview-version ${LABVIEW_VERSION} --labview-bitness ${LABVIEW_BITNESS} --timeout ${VIPC_TIMEOUT} $(basename ${SOURCE_VIPC}) && \
            rm $(basename ${SOURCE_VIPC}); \
        fi; \
    fi

