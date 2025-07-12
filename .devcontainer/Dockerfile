FROM w1gx/ghdl-env:v0.5

ENV VUNIT_SIMULATOR=ghdl

RUN \
    # Disable UVVM's initial banner/info printout
    sed -i 's/\(constant C_SHOW_UVVM_UTILITY_LIBRARY_INFO\s*:\s*boolean := \)true;/\1false;/' \
        /opt/uvvm/uvvm_util/src/adaptations_pkg.vhd && \
    \
    # Disable UVVM's release/version info printout
    sed -i 's/\(constant C_SHOW_UVVM_UTILITY_LIBRARY_RELEASE_INFO\s*:\s*boolean := \)true;/\1false;/' \
        /opt/uvvm/uvvm_util/src/adaptations_pkg.vhd && \
    \
    # Suppress log warning about time truncation
    sed -i 's/\(constant C_LOG_TIME_TRUNC_WARNING\s*:\s*boolean := \)true;/\1false;/' \
        /opt/uvvm/uvvm_util/src/adaptations_pkg.vhd && \
    \
    # Downgrade unwanted activity alert from ERROR to NOTE
    sed -i 's/\(constant C_UNWANTED_ACTIVITY_SEVERITY\s*:\s*t_alert_level := \)ERROR;/\1NOTE;/' \
        /opt/uvvm/uvvm_util/src/adaptations_pkg.vhd
        
