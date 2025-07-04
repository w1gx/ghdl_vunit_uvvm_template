# GHDL VUnit + UVVM + OSVVM Template

This provides a fully working VHDL testbench environment with GHDL, UVVM, OSVVM, and VUnit pre-installed framework using:

- [VUnit](https://vunit.github.io/)
- [UVVM](https://uvvm.org/)
- [OSVVM](https://osvvm.org/)
- [GHDL](https://ghdl.github.io/ghdl/)
- [GTKWave](http://gtkwave.sourceforge.net/)

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

## Documentation

For additional information, refer to the following documentation links:

- UVVM: [UVVM documentation](https://uvvm.github.io/)
- OSVVM: [OSVVM documentation](https://github.com/OSVVM/Documentation)
- VUNIT: [VUnit documentation](https://vunit.github.io/)
- GTKWave: [GTKWave documenation](https://gtkwave.sourceforge.net/gtkwave.pdf)

## License

This project is licensed under the [MIT License](./LICENSE.TXT).

You are free to use, modify, and distribute this software in accordance with the terms of the MIT license. See the [LICENSE](./LICENSE) file for details.
