# syntax=docker/dockerfile:1

ARG LABVIEW_VERSION=2024
FROM ghcr.io/vipm-io/actions-runner-labview-${LABVIEW_VERSION}-linux:dev

ARG LABVIEW_BITNESS=64
ARG VIPC_TIMEOUT=600
ARG SOURCE_VIPC=source/.vipc*
ARG DEV_VIPC=dev.vipc*
ARG GITHUB_REPOSITORY

USER labview
ENV USER=labview
ENV GITHUB_REPOSITORY=${GITHUB_REPOSITORY}

# note that files after the first COPY are optional, which is nice (since might not have a dev.vipc)
# also note that dockerfile doesn't do whitespace characters, which is why we have a * in the COPY command
COPY ${SOURCE_VIPC} ./source.vipc
COPY ${DEV_VIPC} ./dev.vipc

# the script below will apply VIPC files, if they are found.
RUN if [ -f dev.vipc ] || [ -f source.vipc ]; then \
        init_labview && \
        echo "Refreshing Package List..." && \
        dragon refresh --vipm && \
        if [ -f dev.vipc ]; then \
            echo "Applying VIPC (Dev Deps)..." && \
            dragon vipm apply-vipc --labview-version ${LABVIEW_VERSION} --labview-bitness ${LABVIEW_BITNESS} --timeout ${VIPC_TIMEOUT} dev.vipc && \
            rm dev.vipc; \
        fi && \
        if [ -f source.vipc ]; then \
            echo "Applying VIPC (Library Deps)..." && \
            dragon vipm apply-vipc --labview-version ${LABVIEW_VERSION} --labview-bitness ${LABVIEW_BITNESS} --timeout ${VIPC_TIMEOUT} source.vipc && \
            rm source.vipc; \
        fi; \
    fi
