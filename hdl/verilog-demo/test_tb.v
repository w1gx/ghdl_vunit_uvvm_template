module main;
  reg a, b;
  wire y;

  test uut (.a(a), .b(b), .y(y));

  initial begin
    $dumpfile("test_tb_wave.vcd");
    $dumpvars(0, main);

    $display("a b | y");
    a = 0; b = 0; #1 $display("%b %b | %b", a, b, y);
    a = 0; b = 1; #1 $display("%b %b | %b", a, b, y);
    a = 1; b = 0; #1 $display("%b %b | %b", a, b, y);
    a = 1; b = 1; #1 $display("%b %b | %b", a, b, y);
    $finish;
  end
endmodule

