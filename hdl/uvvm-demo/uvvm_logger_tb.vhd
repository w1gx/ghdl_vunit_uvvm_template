library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- VUnit
library vunit_lib;
context vunit_lib.vunit_context;

-- UVVM
library uvvm_util;
use uvvm_util.types_pkg.all;
use uvvm_util.methods_pkg.all;

entity uvvm_logger_tb is
  generic (runner_cfg : string);
end entity;

architecture sim of uvvm_logger_tb is

  signal clk100M : std_logic;
  signal clk100M_60 : std_logic;
  signal clk100M_ena  : boolean := true;

  signal clk50M : std_logic;
  signal clk50M_ena : boolean := true;

  begin


--    uvvm_util.methods_pkg.clock_generator(clk100M, clk100M_ena, 10 ns, "100 MHz with 60% duty cycle", 60);
    clock_generator(clk100M_60, clk100M_ena, 10 ns, "100 MHz with 60% duty cycle", 60);
    clock_generator(clk100M, clk100M_ena, 10 ns, "100 MHz");
    clock_generator(clk50M, clk50M_ena, 20 ns, "50 MHz");


  process
    variable test_val1 : integer := 42;
    variable test_val2 : integer := 42;
  begin
    -- Start VUnit runner
    test_runner_setup(runner, runner_cfg);

    -- UVVM Log Message
    uvvm_util.methods_pkg.log("Starting UVVM testbench");

    wait for 100 ns;

    -- UVVM Alert
    alert(WARNING, "Test Warning");
    alert(NOTE, "Test Note");

    wait for 100 ns;
    -- Example check
    check_equal(test_val1, test_val2, "Comparing test values");

    uvvm_util.methods_pkg.log("UVVM testbench complete");

    -- Done
    test_runner_cleanup(runner);
    wait;
  end process;

end architecture;
