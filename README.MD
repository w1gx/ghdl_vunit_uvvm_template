# GHDL VUnit + UVVM + OSVVM Template

This provides a fully working VHDL testbench environment with GHDL, UVVM, OSVVM, and VUnit pre-installed framework using:

- [VUnit](https://vunit.github.io/)
- [UVVM](https://uvvm.org/)
- [OSVVM](https://osvvm.org/)
- [GHDL](https://ghdl.github.io/ghdl/)
- [GTKWave](http://gtkwave.sourceforge.net/)
- [VHDL LS](https://github.com/VHDL-LS/rust_hdl_vscode)

---

## Motivation

### Why VUnit with UVVM and OSVVM?

VUnit is a powerful Python-based test automation framework for VHDL and SystemVerilog. It excels at managing testbenches, dependencies, and simulation workflows in a modern and scalable way - but it doesn’t natively integrate higher-level verification frameworks.

UVVM and OSVVM are advanced VHDL verification libraries that provide:

- **UVVM**
  - Structured test architecture with reusable Verification Components (VVCs)
  - Logging, scoreboarding, and error injection
  - Rich protocol VIP support (UART, SPI, AXI, etc.)

- **OSVVM**
  - Intelligent constrained random test generation
  - Coverage-driven verification and functional coverage tracking
  - Transaction-level modeling

Combining VUnit with UVVM or OSVVM provides the best of both worlds:

- Automation with test control, logging, filtering, and batch runs (VUnit)
- Powerful verification features like protocol VIPs, coverage, and scoreboards (UVVM/OSVVM)
- Modern simulation workflows with GTKWave integration and parallel test execution

### Challenges with GHDL Integration

While GHDL is a fast and open-source VHDL simulator, integrating it with UVVM or OSVVM can be tricky:

- UVVM libraries must be compiled in strict order based on `compile_order.txt` scripts
- GHDL is picky about library boundaries, hierarchy, and redefinitions
- Most examples assume ModelSim or Riviera-Pro, making GHDL workflows less documented
- One misclassified file or incorrect compile option can break the whole testbench

### This Project Solves That

This `run.py` script provides a ready-to-run VUnit test framework that:

- Automatically compiles UVVM and OSVVM in the correct order
- Integrates designs and testbenches from a single `hdl/` folder
- Adds waveform generation and GTKWave session handling
- Works reliably with GHDL out of the box
- Allows easy configuration of which libraries to include

This framework serves as a starting point for any VHDL project requiring structured, automated verification.

---

## Quick Start

This project includes a fully configured **DevContainer for VSCode**, built on the Docker image `w1gx/ghdl-env:v0.3`, which includes GHDL, UVVM, and Python with VUnit.  

This project setup can be used in two ways:

### Option A: Using VSCode with DevContainers

1. Prerequisites: **Docker** and **Visual Studio Code** installation
2. The **"Dev Containers"** extension must be installed in VSCode
3. Open the project folder in VSCode
4. When prompted, select **"Reopen in Container"**

The devcontainer can be configured by editing the [devcontainer.json](./.devcontainer/devcontainer.json) file.

<div style="background-color: #fff9c4; border-left: 6px solid #ffeb3b; color: #000; padding: 16px; margin: 2em 0;">
  <strong>Note:</strong> The first time a container starts takes very long, as the docker image will have to be downloaded and run. Subsequent runs are much faster.
</div>  

### Option B: Manual Setup

```sh
# Clone this repository and enter the directory
git clone <your_repo_url>
cd <project_folder>

# Set UVVM path if not installed in /opt/uvvm
export UVVM_HOME=/path/to/UVVM

# Install Python dependencies
pip install -r requirements.txt
```

<div style="background-color: #ffebee; border-left: 6px solid #f44336; color: #000; padding: 16px; margin: 2em 0;">
  <strong>Warning:</strong> The manual setup requires that the UVVM and OSVVM libraries are already installed in the environment. Be sure to set the environment variables <code>UVVM_HOME</code> and <code>OSVVM_HOME</code> correctly.
</div>

## Compiling the Project and Running Simulations

The project can be compiled by running the `run.py` script:

```sh
python3 run.py
```

Verbose output can be forced with

```sh
python3 run.py -v
```

For more command-line options, please refer to the [VUnit Documentation](https://vunit.github.io/cli.html)

<div style="background-color: #fff9c4; border-left: 6px solid #ffeb3b; color: #000; padding: 16px; margin: 2em 0;">
<strong>Note:</strong> VUnit sets the compile order itself, and doesn't always adhere to the order in which the files were added. Especially with more complex inter-dependencies, this sometimes results in an error.<br>
The remedy is typically to just restart the compilation process with <code>python run.py</code>, but sometimes a restart needs to be forced by deleting the <strong>vunit_out</strong> folder.
<br>
I will try to resolve this issue in the next version, but for now I can live with it.
<br><br>
The initial compile run can take somewhat long, as it has to compile all the VUnit, OSVVM and UVVM files. Subsequent runs just only compile the modified HDL files and are much faster.
</div>

## Configuring the VUnit environment

The [run.py](./run.py) script contains a configuration block, which needs to be adjusted to the project needs (enable UVVM, OSVVM, load UVVM libraries, etc)

```python
# -----------------------------------------------------------------------------------------------------------------------------------
#                                                    CONFIGURATION BLOCK 
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
    #"bitvis_vip_sbi",                 # Simple Bus Interface VIP - for interacting with simple memory-mapped buses
    #"bitvis_vip_gpio",                # GPIO VIP - for verifying general-purpose digital I/O
    #"bitvis_vip_i2c",                 # I2C protocol VIP - master/slave transactions
    #"bitvis_vip_axilite",             # AXI4-Lite VIP - for register access verification
    #"bitvis_vip_axi",                 # AXI4 VIP - full AXI protocol including burst transactions
    #"bitvis_vip_axistream",           # AXI-Stream VIP - for streaming data interfaces
    "bitvis_vip_clock_generator",     # VIP for generating clocks with configurable frequency and jitter
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
```

<div style="background-color: #fff9c4; border-left: 6px solid #ffeb3b; color: #000; padding: 16px; margin: 2em 0;">
<strong>Note:</strong> The <a href=./run.py>run.py</a> script works with both GHDL and Questa/Modelsim, and it determines which one to use by the environment <code>VUNIT_SIMULATOR</code>. Valid settings for this are <i>ghdl</i>, <i>modelsim</i>, or <i>questa</i>.
</div>

## Launching Waveform Viewers (GTKWave)

```sh
./gtkwave_sessions.sh
```

## Folder Structure

```txt
.
├── run.py                  # VUnit + UVVM + OSVVM integration script
├── requirements.txt        # Python dependency list (VUnit)
├── hdl/                    # Design and testbench source files
│   └── <module name>       # HDL Module
│          └── sim/         # Generated wave files and waveform configurations
├── gtkwave_sessions.sh     # Auto-generated waveform viewer script
└── README.md               # This file
```

<div style="background-color: #fff9c4; border-left: 6px solid #ffeb3b; color: #000; padding: 16px; margin: 2em 0;">
<strong>Note:</strong> Each HDL module requires a <strong>sim</strong> folder, where the generated wave files and waveform configurations are stored.
</div>

## Configuring the Dev Container

The [devcontainer](./.devcontainer) folder  contains two files:

- a [Dockerfile](./.devcontainer/Dockerfile), which configures the Docker environment
- a [devcontainer.json](./.devcontainer/devcontainer.json) file, which configures the vscode environment

### Dockerfile

Within the [Dockerfile](./.devcontainer/Dockerfile), it is easy to reconfigure files such the `adaptations_pkg.vhd` of UVVM. With simple sed expressions, these files can be reconfigured as so:

```docker
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
```

### devcontainer.json

The [devcontainer.json](./.devcontainer/devcontainer.json) file contains the vscode modules that are loaded on startup of the container along with
settings for these modules as well as mounts to the host filesystem.

To allow access to the .ssh folder of the home directory (which is needed for GIT), I configured the following in there:

```json
"mounts": [
        {
            "source": "/dev/bus/usb",
            "target": "/dev/bus/usb", 
            "type": "bind"
        },
        "source=${localEnv:HOME}${localEnv:USERPROFILE}/.ssh,target=/home/ubuntu/.ssh,consistency=cached,type=bind"
    ],
```

## VHDL LS

VHDL LS provides a VHDL language server, which in turn enables syntax-checking, references, hovering for more info, and all the good things
that improve productivity. It is available as an extension in VSCode and works out of the box.

The only thing that needs to be configured are the libraries that it has access to. This configuration takes place in the file [vhdl_ls.toml](./vhdl_ls.toml). The UVMM libraries are straight-forward (usually in /opt/uvvm), but VUnit and the included OSVVM files are a bit more tricky, as they depend on how VUnit was installed.
The solution to this is that the run.py script creates a file 'vhdl_ls_vunit.toml', which contains the libraries and locations of the project for both VUnit and OSVVM. These two sections from this file can then be copied into `vhdl_ls.toml`

## Documentation

For additional information, refer to the following documentation links:

- UVVM: [UVVM documentation](https://uvvm.github.io/)
- OSVVM: [OSVVM documentation](https://github.com/OSVVM/Documentation)
- VUNIT: [VUnit documentation](https://vunit.github.io/)
- GTKWave: [GTKWave documenation](https://gtkwave.sourceforge.net/gtkwave.pdf)

## License

This project is licensed under the [MIT License](./LICENSE.TXT).

You are free to use, modify, and distribute this software in accordance with the terms of the MIT license. See the [LICENSE](./LICENSE) file for details.
