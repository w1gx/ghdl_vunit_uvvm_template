library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library vunit_lib;
context vunit_lib.vunit_context;
context vunit_lib.com_context;

-- OSVVM
library osvvm;
use osvvm.AlertLogPkg.all;

entity osvvm_logger_tb is
  generic (runner_cfg : string);
end entity;

architecture tb of osvvm_logger_tb is
begin

  main : process
  begin
    -- Setup test runner
    set_stop_level(failure);
    test_runner_setup(runner, runner_cfg);

    wait for 100 ns;

    info("This is an OSVVM test");

    -- OSVVM logging using named parameters to disambiguate overloads
    osvvm.AlertLogPkg.log("This is an OSVVM INFO", INFO);

    wait for 100 ns;

    -- Show alert summary
    ReportAlerts;

    -- Cleanup
    test_runner_cleanup(runner);
    wait;
  end process;

end architecture;
