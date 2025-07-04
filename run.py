# -------------------------------------------------------------------------------------------------
# VUnit run.py script for integrating UVVM and OSVVM libraries
# Author: Martin Mauersberg (W1GX)
# Last updated: July 2025
#
# This script configures and runs VUnit simulations with GHDL, supporting advanced verification
# using UVVM and OSVVM modules. Customize the configuration section as needed for your project.
# -------------------------------------------------------------------------------------------------

import os
from vunit import VUnit
from pathlib import Path

# -----------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------ CONFIGURATION BLOCK --------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

use_osvvm = True  # Enable OSVVM
use_uvvm = True  # Enable UVVM
print_debug_messages = False  # debug messages for compilation

# Path to UVVM
uvvm_path = Path(os.environ.get("UVVM_HOME", "/opt/uvvm"))

# Path to HDL source files
HDL_PATH = "hdl"

# Add only the needed UVVM libraries (customize as needed)
uvvm_libraries = [
    "uvvm_util",                      # Core UVVM utilities (mandatory) - logging, checks, synchronization, etc.
    "uvvm_vvc_framework",             # VVC (Verification Component) infrastructure - enables structured VVC communication
    "bitvis_vip_scoreboard",          # Generic scoreboard - for data comparison and functional coverage
    # ---------- Protocol component model (often used with the VIP) ----------
    "bitvis_uart",                    # Synthesizable UART model (DUT-side) - for testing UART receivers/transmitters
    # ---------- Protocol-specific Verification IPs (VIPs) -----------
    "bitvis_vip_uart",                # UART VIP - for stimulating and monitoring UART interfaces
    "bitvis_vip_sbi",                 # Simple Bus Interface VIP - for interacting with simple memory-mapped buses
    "bitvis_vip_gpio",                # GPIO VIP - for verifying general-purpose digital I/O
    "bitvis_vip_i2c",                 # I2C protocol VIP - master/slave transactions
    #"bitvis_vip_axilite",             # AXI4-Lite VIP - for register access verification
    #"bitvis_vip_axi",                 # AXI4 VIP - full AXI protocol including burst transactions
    #"bitvis_vip_axistream",           # AXI-Stream VIP - for streaming data interfaces
    #"bitvis_vip_clock_generator",     # VIP for generating clocks with configurable frequency and jitter
    #"bitvis_vip_error_injection",     # Injects protocol-level or timing errors to test robustness
    #"bitvis_vip_ethernet",            # Ethernet MAC-level protocol VIP
    #"bitvis_vip_gmii",                # VIP for GMII (Gigabit Media Independent Interface)
    #"bitvis_vip_spi",                 # SPI protocol VIP - master/slave simulation
    #"bitvis_vip_avalon_mm",           # Avalon-MM (Memory-Mapped) VIP for Altera/Intel FPGAs
    #"bitvis_vip_avalon_st",           # Avalon-ST (Streaming) VIP
    #"bitvis_vip_wishbone",            # Wishbone protocol VIP
    #"bitvis_vip_hvvc_to_vvc_bridge",  # Bridge between hierarchical VVC and flat VVC (advanced usage)
    #"bitvis_vip_spec_cov",            # Specification coverage VIP - maps functional coverage to spec requirements
    #"bitvis_irqc",                    # Interrupt Request Controller component model/VIP
    #"bitvis_vip_rgmii",               # VIP for RGMII (Reduced Gigabit Media Independent Interface)
]

# -----------------------------------------------------------------------------------------------------------------------------------
#                                           DO NOT TOUCH ANYTHING BELOW THIS LINE !!!
# -----------------------------------------------------------------------------------------------------------------------------------

# Force GHDL as the simulator
os.environ["VUNIT_SIMULATOR"] = "ghdl"


# Define VUnit object
vu = VUnit.from_argv(compile_builtins=False)
vu.add_vhdl_builtins()
vu.add_com()

vu.set_compile_option(
    "ghdl.a_flags", ["-frelaxed", "-frelaxed-rules", "-Wno-hide"], allow_empty=True
)

# ------------------------------------------------ OSVVM ----------------------------------------------------------------------------
if use_osvvm:
    vu.add_osvvm()

# ------------------------------------------------ UVVM -----------------------------------------------------------------------------
# UVVM
if use_uvvm:

    # Track libraries already created
    added_uvvm_libraries = {}

    # Helper to determine library name from a relative path
    def get_library_name_from_path(
        path_str: str, current_lib: str, uvvm_libraries: list[str]
    ) -> str:
        # Special case: if this file is part of current lib's src_target_dependent
        if "src_target_dependent" in str(path_str):
            return current_lib

        # Normalize the path
        parts = Path(path_str).parts

        # Look for known library name in reverse
        for i in range(len(parts) - 1, -1, -1):
            part = parts[i]
            if part in uvvm_libraries:
                return part

        # Fallback: "../src" or single "../" paths belong to current lib
        if "../src" in path_str or path_str.startswith("../"):
            return current_lib

        raise ValueError(f"Failed to determine library for: {path_str}")

    # Main processing loop
    for lib_name in uvvm_libraries:
        script_dir = uvvm_path / lib_name / "script"
        compile_order_file = script_dir / "compile_order.txt"

        if not compile_order_file.exists():
            if print_debug_messages:
                print(f"Missing compile_order.txt for {lib_name}")
            continue

        if print_debug_messages:
            print(f"Processing {lib_name}")

        for line in compile_order_file.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # skip empty lines and comments

            source_path = (script_dir / line).resolve()

            if "../src" in line or "src_target_dependent" in line:
                # Source file belongs to current lib
                target_lib = lib_name
            else:
                # Source file belongs to another lib (resolve its name)
                target_lib = get_library_name_from_path(line, lib_name, uvvm_libraries)

            if print_debug_messages:
                print(f"We have target lib {target_lib} in line {line}")

            if target_lib not in added_uvvm_libraries:
                lib = vu.add_library(target_lib)
                added_uvvm_libraries[target_lib] = lib
            else:
                lib = added_uvvm_libraries[target_lib]

            # Add the file to the correct library
            lib.set_compile_option(
                "ghdl.a_flags",
                ["-frelaxed", "-frelaxed-rules", "-Wno-shared", "-Wno-hide"],
                allow_empty=True,
            )
            lib.add_source_files(str(source_path), vhdl_standard="2008")
            lib.set_compile_option(
                "ghdl.a_flags",
                ["-frelaxed", "-frelaxed-rules", "-Wno-shared", "-Wno-hide"],
                allow_empty=True,
            )

# --------------------------------------- DESIGN AND TEST BENCH ---------------------------------------------------------------------
lib_main = vu.add_library("main")
lib_main.add_source_files(f"{HDL_PATH}/**/*.vhd", vhdl_standard="2008")
lib_main.set_compile_option(
    "ghdl.a_flags", ["-frelaxed", "-Wno-hide", "-Wno-shared"], allow_empty=True
)
main_files = list(Path(HDL_PATH).rglob("*.vhd"))
if not main_files:
    print(f"Warning: No HDL files found under '{HDL_PATH}/'")

# Set up GTKWave for each test bench
gtkwave_tabs = []
for tb in lib_main.get_test_benches():

    tb_entity_name = tb._test_bench.design_unit.name  # Entity name
    if print_debug_messages:
        print("Setting up GTKWave for ", tb_entity_name)

    tb_folder = os.path.join(
        os.path.dirname(tb._test_bench.design_unit.file_name), "sim"
    )
    os.makedirs(tb_folder, exist_ok=True)

    wave_file = os.path.join(tb_folder, "wave.ghw")
    gtkw_file = os.path.join(tb_folder, "wave.gtkw")

    if print_debug_messages:
        print(f"Configuring waveform output for testbench: {tb.name}")
        print(f"  → waveform file: {wave_file}")
        print(f"  → GTKWave config: {gtkw_file}")
        print(
            f"  → GTKWave command: gtkwave {wave_file} {gtkw_file}"
            if os.path.exists(gtkw_file)
            else f"  → GTKWave command: gtkwave {wave_file}"
        )

    # Set simulation flags
    tb.set_sim_option("ghdl.elab_flags", ["--std=08", "-frelaxed"])
    tb.set_sim_option("ghdl.sim_flags", [f"--wave={wave_file}"])

    # Create minimal GTKWave layout if missing
    if not os.path.exists(gtkw_file):
        print(f"  → Creating minimal GTKWave layout with clock signal")
        with open(gtkw_file, "w") as f:
            f.write("[dumpfile] wave.ghw\n")
            f.write("[timescale] 1 ns\n")
            f.write("[opt] 0\n")
            f.write("[sst_expanded] 0\n")
            f.write("[sst_width] 200\n")
            f.write("[sst_vpaned_height] 300\n")
            f.write("[treeopen] /\n")
            f.write("[sst_signal] clk\n")

    gtkwave_tabs.append(f"gtkwave {wave_file} {gtkw_file}  # {tb.name}")

# Create batch script for GTKWave sessions
session_file = "gtkwave_sessions.sh"
if print_debug_messages:
    print(f"\nGenerating tabbed GTKWave session: {session_file}")
with open(session_file, "w") as f:
    f.write("# GTKWave commands for all test benches\n")
    for entry in gtkwave_tabs:
        f.write(entry + "\n")

# Run all tests
vu.main()
